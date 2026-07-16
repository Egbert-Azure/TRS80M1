<!-- /software/scripsit/scripsit-sp-article-en.md — English version of scripsit-sp-artikel.md -->
<!-- (c) E. Schroeer -->

# SCRIPSIT/SP — a German Scripsit modification

**What came from Craig Lindley, what did not, and why**

*German version: [`scripsit-sp-artikel.md`](./scripsit-sp-artikel.md)*

*Evidence: [`scripsit-provenance.md`](./scripsit-provenance.md) · Index: [`README.md`](./README.md).*

> **Note on this version.** The original article (Club-80, SONDERINFO 27.5, 1988) is lost. This
> is **not a reconstruction of that text** but a 2026 rewrite. The recollection in section 1 is
> memory and should be read as such. Everything technical is derived from the binaries —
> `SCRIPSIT/CMD`, `SCRIPSIT/SP`, `WP/CMD` (from `esnd-04.dmk`), `wp.cmd` (Lindley's build) — not
> from memory. Where something is uncertain, it says so.

---

## 1. How it came about

1988. In front of me, a stack of old 80 Micro issues — to my mind the only magazine that was
actually any good.

Those were the years when you typed programs in from the magazine. A tedious business: line by
line, hex number by hex number, and one transposed digit cost you an evening. But you learned
something you never learn from just using software — you went *through* someone else's code
instead of past it.

I had just finished two things: extending NEWDOS into an HRG-DOS, and writing a German keyboard
driver. NEWDOS had no umlauts. Not badly solved, not awkward to reach — simply absent.

Scripsit 1.0 (Radio Shack, 1979) was the same, only more irritating, because it is a word
processor. The codes 5BH, 5CH, 5DH, 7BH, 7CH, 7DH and 7EH — which carry Ä Ö Ü ä ö ü ß in the
German 7-bit set — Scripsit uses for itself, partly as on-screen markers, partly not at all.
And sending an arbitrary control byte to the printer was not provided for at all.

I took Craig A. Lindley's series *"Inside Scripsit"* in 80 Micro as a starting point. Not as
something to type in and be done with, but as a way in: he showed where you can get inside
Scripsit. That gave me something to build on — new functions, a German umlaut driver, a
facelift overall. Being able to read the directory without leaving Scripsit was one of those
things you have once and then never want to be without again.

What came of it consists of **two layers**, which work independently of one another:

| layer | file | what it is |
|---|---|---|
| **A** | `SCRIPSIT/SP` | a static patch **in the program file**. Umlauts, printer control. Runs on its own. |
| **B** | `WP/CMD` | a loader that patches Scripsit **in RAM**. New BREAK commands, cursor functions. |

Layer B goes back to someone else's work. Layer A does not.

That applies to the directory display in the recollection above as well: it is Lindley's
(`QUERY`), not mine. I took it and simplified it. It is new only relative to Scripsit — not
relative to the source I worked from.

---

## 2. The origin: Craig A. Lindley

Lindley described, in *"Inside Scripsit"* (80 Micro, Part II: October 1982), a patch program
that alters Scripsit in memory after loading. `WP/CMD` is a **port of that program**, not an
idea taken from it. That should be said plainly.

A second transcription of his listing has since turned up, which settles what was open: it
matches the object code printed in the magazine. So the printed listing is the reference, and
what I typed in is measurable against it.

The proof is simple: every hook `WP/CMD` uses sits at Lindley's address. The installer is his,
line for line:

| Lindley | in `WP/CMD` |
|---|---|
| 13 × set text-buffer base | ✅ the same 13 sites |
| `C3` → 6155 + keyboard fix → 6156 | ✅ |
| `C3` → 7A9E + underline → 7A9F | ❌ **dropped** |
| `C3` → 5FAF + screen marker → 5FB0 | ✅ |
| `C3` → 73A2 + printer pause → 73A3 | ✅ |
| `C3` → 5E16 + file message → 5E17 | ✅ |
| table extension → 52F8 / 6466 | ✅ |
| `RETURN` → 6595 | ❌ **dropped** |
| scroll routines → 79D9 / 79D7 / 79BF | ✅ |
| `14H` → 79AA (move the tab key) | ✅ |
| copy sign-on line into RAM → 57F7 | ❌ **dropped** |

The actual stroke of design is his too: the insight that Scripsit's own table search at
**58F0H** is reusable, and that the two *"unknown command"* exits at 52F7H and 6466H can be
bent onto your own tables in three bytes. The extension cannot damage the original, because on
a miss it falls back to the same error exit.

His as well: the reentry. The flag byte sits **one byte past the last loaded byte** and
therefore survives reloading the patch. His source says simply `TSTBYT EQU $`.

### What I added

Exactly one extension, and it is documented. Lindley caps `BREAK X=` at codes 1–31:

```
8131  FE20    CP    20H     ;NUM LESS THAN 32 ?
```

In `WP/CMD`, the corresponding place (80C7H) reads `CP 0FFH`. Codes 1–255 are possible — as the
SCRIPSIT/SP manual describes. For a printer that needs more than the plain ASCII control codes,
that is the difference between usable and useless.

Everything else I did to layer B was **subtraction**: the directory display went from Lindley's
detailed form (free granules, date, eight directory sectors) down to `DIR 0` … `DIR 2`, and the
text buffer starts correspondingly earlier — at 81A1H instead of 8342H.

---

## 3. Layer A: SCRIPSIT/SP

There is no model for this. Lindley never touches the program file; his patch lives entirely in
RAM. `SCRIPSIT/SP` is a **modified program file**.

### The construction principle

Every change in the program body is a **length-preserving substitution**:

```
32 E8 37    LD (37E8H),A   →   CD 6C FF    CALL 0FF6CH
3A E8 37    LD A,(37E8H)   →   CD CB FF    CALL 0FFCBH
```

Three bytes for three bytes. No address in Scripsit moves. Fourteen sites, all on the same
pattern. All the new code lives in the top 148 bytes of memory (FF6CH–FFFFH) plus 39 bytes at
7A7DH.

### Umlauts

The translation hooks in at 615DH — where Scripsit turns a key pressed with @ into a control
code. Table at FFCFH, result 16 bytes further on at FFE0H:

| key | code | character |
|---|---|---|
| `@A` `@O` `@U` | 5B 5C 5D | Ä Ö Ü |
| `@a` `@o` `@u` | 7B 7C 7D | ä ö ü |
| `@:` | 7E | ß |
| `@p` | 7F | hatched block |

```
FFAC  LD HL,0FFCFH / LD BC,17 / CPIR
      JR NZ,FFC3
      LD BC,16 / ADD HL,BC / LD A,(HL)
      CP 7EH / JP C,6167H      ; umlauts: case folding
      JP 6179H                 ; ß and 7FH bypass it
FFC3  CP 41H / JP C,6167H      ; original code, unchanged
      JP 6161H
```

The comparison against 7EH is necessary because 6167H performs an `XOR 20H`. Ä/ä should be
caught by it; ß and the block should not.

**The less obvious part:** 5BH, 5CH and 5DH were not free. Scripsit used them to display its own
markers. The translation table at 7966H had to be changed — the markers now appear as graphics
blocks 97H, A6H and ADH. Without that step, markers and umlauts collide on screen.

### Printer control: @p and two hex digits

The real piece of work. `@p` generates 7FH; the two characters that follow are read as hex
digits and handed to the printer as **one** byte:

```
FF6C  PUSH HL / PUSH BC / PUSH AF
      LD HL,0FFAAH        ; FFAA = counter, FFAB = accumulating byte
      LD A,(HL) / AND A / JR NZ,FF96
      POP AF / PUSH AF
      CP 7FH / JR Z,FF92
      LD HL,0FFE2H / LD BC,15 / CPIR    ; printer translation
      JR NZ,FF8B
      LD BC,14 / ADD HL,BC / LD A,(HL)
FF8B  LD (37E8H),A                      ; the only direct port access
      POP AF / POP BC / POP HL / RET
FF92  LD (HL),2 / JR FF8E               ; @p: expect two digits
FF96  POP AF / PUSH AF
      CP 3AH / JR C,FF9E / SUB 7        ; ASCII hex → nibble
FF9E  SUB 30H
      INC HL / RLD / LD A,(HL) / DEC HL ; shift the nibble in
      DEC (HL) / JR NZ,FF8E
      JR FF8B                           ; second digit: emit the byte
```

`RLD` shifts one nibble out of A into `(HL)` and the old high nibble of `(HL)` back into A.
Applied twice, it assembles two hex digits into one byte — no shift loop, no scratch register.
The instruction exists for exactly this and is rarely used for it.

The price is in the manual: three screen characters become one printer byte, so the character
count can get out of step.

### Printer translation table

FFE2H (source) → FFF1H (destination), 15 entries, **identity-mapped as shipped**. Anyone with a
printer that already carries the German set leaves it alone. Anyone who hasn't enters at FFF1H
whatever their device understands. That is the intended adjustment point.

### Where the memory came from

Scripsit sizes its own text buffer at cold start: `LD HL,(4049)` at 5260 gives it a ceiling,
and 5276 hard-codes the floor at 7F62H.

4049H is the top-of-memory pointer. `SCRIPSIT/SP`'s load record writes **FF6BH** there — one byte
below the driver at FF6CH. Scripsit then sizes its buffer to end at FF6B and never touches what
is above it. Nothing is patched to achieve this; it uses Scripsit's own startup code.

**That is the difference from Lindley, and it is the whole of it.** He loads his program at
7F62H–8342H, which is *inside* the buffer, so he must rewrite thirteen pointers afterwards to
push the floor up — and it costs the user around 960 bytes of document space. His article says so.

Layer A moves the ceiling instead. It costs nothing. Same problem, opposite end — and it is why
the three-bytes-for-three-bytes rule matters: it reaches code at FF6CH without moving a byte of
Scripsit.

### FFCB and the `DI` at 52C0

`FFCBH` is only `LD A,(37E8H) / RET` — a pass-through. Its purpose is that **every** printer
access goes through a hook. *(Effect certain, intent inferred.)*

At 52C0H, the head of the main loop, there is a `DI` instead of a `NOP`. Interrupts therefore
stay disabled inside the editor loop — the driver sits at FF6CH–FFFFH, right at the top of
memory. *(Effect certain, reasoning inferred.)*

---

## 4. What came from whom

The SCRIPSIT/SP manual lists everything together without separating origins. Let that be made
good here.

| function | layer | origin |
|---|---|---|
| umlauts `@a @o @u @A @O @U`, `@:` = ß | A | **new** |
| `@p` + two hex digits → one printer byte | A | **new** |
| printer translation table FFE2→FFF1 | A | **new** |
| markers moved off 5B/5C/5D onto graphics blocks | A | **new** |
| print suppression emits a blank instead of nothing | A | **new** |
| `BREAK X=nnnn`, codes **1–255** | B | Lindley, **extended** (his: 1–31) |
| `BREAK Qn` directory | B | Lindley, simplified |
| `KILL` / `K filename` | B | Lindley |
| `BREAK N` / `New` | B | Lindley |
| `SHIFT P` printer pause | B | Lindley |
| `@h` cursor home | B | Lindley |
| `@→` / `@←` word skip | B | Lindley |
| `@` up/down arrow: window 13 lines | B | Lindley |
| `@f` / `@b`: cursor 13 lines | B | Lindley |
| reentry `WP SP*` | B | Lindley |
| `NEW FILE!` / `FILE UPDATED!` | B | Lindley |
| hyphenation, `BREAK H`, hot zone | — | **Scripsit itself** |
| `@d` `@s` `@e`, blocks, markers | — | **Scripsit itself** |
| print format `>PL >LM >RM >J` etc. | — | **Scripsit itself** |

The last three rows matter. The hyphenation is not part of the modification — the strings
`HOT`, `ZONE` and `HYPHEN` sit at 6AA3H, 6AA7H and 6AB5H in the **unmodified** Radio Shack
program.

---

## 5. How the layers fit together

Both were built against each other:

- `SCRIPSIT/SP` ends at 7AA4H. `WP/CMD` begins at 7AA7H.
- `WP/CMD` hooks in at 6155H and falls through to 615DH — where `SCRIPSIT/SP` has the jump to
  the umlaut translator.

So the chain reads: `6155 → 8002 (special keys) → 615D → FFAC (umlauts) → 6167`. Neither layer
knows the other's internals. `SCRIPSIT/SP` also runs on its own — under any filename; `WP` is
not needed for it.

---

## 6. One loose end

Lindley's underlining hooks in at **7A9EH**. `SCRIPSIT/SP` extends the 7A00H block from 126 to
165 bytes — to 7AA4H, and therefore **across 7A9EH**. The space was gone. The printer half of
the underlining was dropped as a result.

The screen half stayed: at 5FAFH, 40H is still displayed as 5FH — confirmed at runtime, where
`SHIFT`-0 produces a glyph distinct from the `@p` hatched square. So the marker is visible but no
longer does anything when printing, and the manual, consistently, does not mention underlining at
all. Whether that was a deliberate cut or an overlooked remnant is a question about what I
intended in 1988. The bytes cannot answer it and neither can a test.

---

## 7. The three odd changes

Traced by following what each address is used for inside Scripsit.

**5DCCH — a bug in Radio Shack's Scripsit.** In the stock file, 7CB6H is written at 5DCC and read
nowhere; 7CB9H is read at 5D47 and 7A6E and written nowhere. Somebody typed the wrong address in
1979, and the reader picked up whatever happened to be there. Writing 7CB9H connects them. The
reordering follows: the original leans on `OR A` setting the flags for `CALL NZ`, so it stores
first; the patch calls first, reloads `LD A,C` because 5DEF clobbers A, then stores — paid for
with the `NOP` at 5DD2.

**7A20H / 7A22H — the page defaults.** The 20-byte block at 7A15H is copied to 7C64H at startup.
7C6FH is `BM` (Unterer Rand, 60) and 7C71H is `PL` (Seitenlänge, 66) — confirmed by the directive
handlers at 766EH and 7798H. Both raised to 127. 66 lines is US Letter at 6 lpi; A4 wants about
72, and the manual opens with `PL=72 BM=66`. Raising the defaults keeps an unmarked document from
breaking at the American boundary. *(Identification certain; the reasoning inferred.)*

**603AH / 6056H — no effect.** These are self-modifying displacement bytes: the ring indices of a
32-byte type-ahead buffer at 7E11H. Cold start zeroes both at 5254/5257 before the buffer is
touched, so the change never reaches runtime.

## 8. Evidence

All statements are checked against the binaries. In addition:

- The transcription I worked from (`wpand.scr`, EDTASM format) was assembled with a purpose-written assembler:
  **1336 bytes, address coverage identical to `wp.cmd`, five differing bytes.** `START` = 7B49H,
  `TXTBUF` = 8342H, `TSTBYT` = 7C21H — in each case exactly what the binary requires.
- Of those five bytes, one is line 5020 (`CP 20H` → `CP 0FFH`) and two are the underline codes in
  lines 550/560 — both my changes. The remaining two are the `LOUT` target, where `wpand.scr`
  agrees with the magazine's printed equate block (4467H) and only one archive build carries 4476H.
- The full Listing 1 is available. Against object-byte points read across all of it, `WP.ASM`
  matches at **68 of 68** and `wpand.scr` at **65 of 68** — the three misses being exactly my
  changes and nothing else. One line (5670) falls in a stretch that could not be read off the
  scan with confidence and remains unverified. Listing 2 is the Model III patch and has no
  bearing on a Model I program.
- `WP/CMD` was re-extracted from `esnd-04.dmk` after an earlier extraction returned 883 bytes
  of `E5` fill. The disk geometry: `sector = 36 + lump·10 + granule·5`, lump = 10 sectors,
  granule = 5, GPL = 2, cylinder 0 excluded, directory on track 6.

**Conclusion.** Layer B is a port of someone else's work with one extension. The reference to
Lindley belongs there, and it is not a courtesy but a statement of fact. Layer A stands on its
own — and it is the part that makes Scripsit German in the first place.

*Egbert Schroeer*
