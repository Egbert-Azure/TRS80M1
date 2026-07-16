<!-- /software/scripsit/scripsit-sp-patch-analysis.md — binary-derived reconstruction of the SCRIPSIT/SP patch -->

# SCRIPSIT/SP — reconstruction from binary evidence

*Narrative account: [`scripsit-sp-article-en.md`](./scripsit-sp-article-en.md) (EN) · [`scripsit-sp-artikel.md`](./scripsit-sp-artikel.md) (DE). Index: [`README.md`](./README.md).*

Derived by structural diff of `SCRIPSIT/CMD` (10752 B) vs `SCRIPSIT/SP` (10920 B).
All statements below are grounded in bytes, not in the article text.

## 1. File-level structure

Both files are ordinary TRSDOS/NEWDOS `/CMD` load-module files.

| | SCRIPSIT/CMD | SCRIPSIT/SP |
|---|---|---|
| load records | 5200–79FF (40 × 256 B), 7A00 × 126 B | identical, but 7A00 record grown to **165 B** (7A00–7AA4) |
| entry record | `02 02 00 52` at file 2922h | moved to 2AA6h |
| trailing bytes | 2926h–29FFh = **stale sector residue** (218 B, duplicate of 2826h–28FFh) | residue kept, but a **dummy record `06 B5`** at 2949h skips it up to the 2A00h sector boundary |
| appended records | — | `01 04 49 40` → **(4049h) = FF6Bh**<br>`01 1A 6C FF` → code FF6Ch–FF83h<br>`01 80 82 FF` → code+tables FF82h–FFFFh |

**Design consequence:** the whole patch lives at **FF6Ch–FFFFh** (top 148 bytes of RAM) plus
39 bytes appended at **7A7Dh**. Nothing in the body is relocated, and everything is in the file's
own load records — so **everything documented in this file works with `SCRIPSIT/SP` started on
its own**: umlauts, the `@p` printer escape, the translation table, the relocated marker glyphs.
`WP/CMD` is not needed for any of that.

**What is not there without `WP/CMD`** is the whole of Layer B — `BREAK Q` (directory), `KILL`,
`BREAK N`, `BREAK X=`, `SHIFT P` (printer pause), the cursor and window functions, the
`NEW FILE!` / `FILE UPDATED!` messages, and reentry via `WP SP*`. Those are patched into RAM at
load time and vanish with the loader. See `wp-cmd-analysis.md`.

Both halves confirmed at runtime: started directly, `@A` gives Ä and `BREAK` `Q0` gives an
illegal-command error; started as `WP SCRIPSIT`, `Q0` gives the directory.

## 2. The governing trick

Every in-body patch is an **exact-length in-place substitution**:

- `32 E8 37`  `LD (37E8H),A`  → `CD 6C FF`  `CALL 0FF6CH`   (printer data out)
- `3A E8 37`  `LD A,(37E8H)`  → `CD CB FF`  `CALL 0FFCBH`   (printer status in)

3 bytes for 3 bytes. No address in Scripsit moves. That is the entire engineering premise.

## 3. Patch sites (address = live Z80 address, not file offset)

| Addr | Original | Patched | Purpose |
|---|---|---|---|
| 5243 | `0D` `32 E8 37` | `0A` `CD 6C FF` | printer out hook (+ `DEC C`→`LD A,(BC)`) |
| 52C0 | `NOP` | `DI` | ⚠ unexplained — see §6 |
| 5800 | 51 blanks in sign-on line | `Modification Copyright 1988 by I Schr|er Vers.1.02` (`7C` = ö) | banner |
| 5D47 | `LD A,(7CB9H)` | `CALL 7A6EH` | uses existing subroutine at 7A6E (unchanged) |
| 5DCC | `LD (7CB6H),A` / `CALL NZ,5DEFH` / `NOP` | `CALL NZ,5DEFH` / `LD A,C` / `LD (7CB9H),A` | re-order + variable moved 7CB6→7CB9 |
| 5F63 | `LD A,(37E8H)` | `CALL 0FFCBH` | printer status |
| 5F6F | `JR NZ,5F74H` / `LD (37E8H),A` | `NOP NOP` / `JP 7A8AH` | print-suppress filter → §5 |
| 603A, 6056 | `05` | `04` | data constants (paired, difference preserved) |
| 615D | `CP 41H` / `JR C,6167H` | `JP 0FFACH` / `NOP` | **@-key (Control) translation hook** |
| 663F, 6650 | `LD A,(37E8H)` | `CALL 0FFCBH` | printer status |
| 665E, 6722 | `LD (37E8H),A` | `CALL 0FF6CH` | printer out |
| 7970/7972/7974 | `5C`, `5B`, `5D` | `97`, `A6`, `AD` | **screen marker glyphs moved off 5B/5C/5D** |
| 7A20, 7A22 | `3C`, `42` | `7F`, `7F` | defaults block LDIR'd to 7C64 by 708B |
| 717F | `CP 8DH` / `JR NZ,7189H` | `JP 7A7DH` | accept **8CH as well as 8DH** as terminator |

## 4. FF6CH — printer output driver (the `@p` engine)

```
FF6C  PUSH HL / PUSH BC / PUSH AF
      LD HL,0FFAAH        ; FFAA = pending-nibble counter, FFAB = byte accumulator
      LD A,(HL) / AND A / JR NZ,FF96   ; escape in progress?
      POP AF / PUSH AF
      CP 7FH / JR Z,FF92               ; the "hashed block" from @p
      LD HL,0FFE2H / LD BC,15 / CPIR   ; printer translate table (source)
      JR NZ,FF8B
      LD BC,14 / ADD HL,BC / LD A,(HL) ; -> destination table at FFF1
FF8B  LD (37E8H),A                     ; the ONLY surviving direct port write
      POP AF / POP BC / POP HL / RET
FF92  LD (HL),2 / JR FF8E              ; @p seen: expect 2 hex digits, emit nothing
FF96  POP AF / PUSH AF
      CP 3AH / JR C,FF9E / SUB 7       ; ASCII hex digit -> nibble
FF9E  SUB 30H
      INC HL / RLD / LD A,(HL) / DEC HL ; shift nibble into (FFAB)
      DEC (HL) / JR NZ,FF8E            ; still one digit to go: emit nothing
      JR FF8B                          ; second digit: emit assembled raw byte
```

`RLD` to assemble two ASCII hex nibbles into one byte is the neat bit. This is exactly
what SCRIPSIT.TXT describes: *"kommt … in Verbindung mit den folgenden beiden Bytes nur
ein Byte an den Drucker"* — and also exactly why the doc warns the character count can
drift (three screen chars → one printer byte).

**FFCBH** is `LD A,(37E8H) / RET` — a pure pass-through stub. Its only purpose is to make
every printer port access a hook point (e.g. for a serial printer). *Confidence: medium
on intent, high on behaviour.*

## 5. 7A8AH — print-suppression filter

```
7A8A  JR Z,7A9E        ; Z from BIT 4,(IY+34H) at 5F6B -> normal print
      CP 0DH / JR Z,7A9E
      CP 0AH / JR Z,7A9E   ; CR/LF always pass
      EX AF,AF' / LD A,20H / CALL 0FF6CH / EX AF,AF'  ; else emit a SPACE
      JP 5F74H
7A9E  CALL 0FF6CH / JP 5F74H
```

Original behaviour: suppressed characters emitted **nothing**. Patched: emits a **blank**,
so horizontal position is preserved. *Confidence: high on mechanism, medium on which
Scripsit feature bit 4 of (IY+34H) corresponds to.*

## 6. FFACH — the @-key umlaut translator

Key table at **FFCFH** (17 bytes, searched with `CPIR`), result table 16 bytes later at **FFE0H**:

| key | → code | glyph |
|---|---|---|
| `P` 50 / `p` 70 | 7F | hashed block |
| `A` 41 | 5B | Ä |
| `O` 4F | 5C | Ö |
| `U` 55 | 5D | Ü |
| `a` 61 | 7B | ä |
| `o` 6F | 7C | ö |
| `u` 75 | 7D | ü |
| `:` 3A | 7E | ß |

```
FFAC  LD HL,0FFCFH / LD BC,17 / CPIR
      JR NZ,FFC3
      LD BC,16 / ADD HL,BC / LD A,(HL)
      CP 7EH / JP C,6167H      ; umlauts -> case-fold path
      JP 6179H                 ; ß and 7FH bypass case folding
FFC3  CP 41H / JP C,6167H      ; original code, verbatim
      JP 6161H
```

Confirmed at runtime: F5(=@)+a/o/u → umlauts, F5+`:` → ß, F5+p → hashed block.
The `CP 7EH` split exists because 6167H applies `XOR 20H` case folding, which must not
touch ß or 7FH.

**Consequence you had to deal with:** 5B/5C/5D were already used by Scripsit as *screen
marker glyphs*. That is why the screen translate table at 7966H was edited — its outputs
5C/5B/5D became the graphics blocks 97/A6/AD. Without that, your markers and your Ä/Ö/Ü
would collide.

## 7. Printer translation table — the user knob

FFE2H (source, 15 B): `5B 5C 5D 7B 7C 7D 7E 00 …`  (Ä Ö Ü ä ö ü ß)
FFF1H (dest, 15 B):   `5B 5C 5D 7B 7C 7D 7E 00 …`  — **identity by default**

So as shipped it assumes a printer that already carries the German set; FFF1H+ is the
table the reader is meant to patch for their own printer.

## 8. KBDGER/CMD is a separate, unrelated artefact

`KBDGER/CMD` = `(4049H) ← FFEFH` + 126 bytes at F000H + entry F000H. Its 126-byte block
shares **zero** bytes with SCRIPSIT/SP's FF82H block. Different code. Do not conflate them
in the documentation.

Both happen to touch **4049H**, but that is the only thing they share, and what SCRIPSIT/SP does
with it is established in §9. Whatever KBDGER does with the same address is a question about
KBDGER.

## 9. 4049H — how the driver gets its memory

Scripsit sizes its own text buffer at cold start:

```
5260  LD HL,(4049)      ; ceiling
5263  NOP x 7           ; a deliberate gap in Radio Shack's code, right here
526A  LD (7C5D),HL      ; end-of-buffer pointers
526D  LD (7C2D),HL
5270  LD (7C55),HL
5276  LD HL,7F62        ; floor - hard-coded
5279  LD (7C43),HL / (7C53),HL / (7C57),HL / (7C2B),HL
```

**4049H is the top-of-memory pointer and Scripsit reads it to find its ceiling.** SCRIPSIT/SP's
load record writes **FF6BH** there — one byte below the FF6CH driver. Scripsit sizes its buffer
to end at FF6B and never touches what sits above. The reservation is made using Scripsit's own
startup code; nothing is patched to achieve it.

**This is the architectural difference from Lindley.** 7F62H is hard-coded at 5276 as the buffer
*floor*. Lindley loads his program at 7F62H–8342H — inside the buffer — and must therefore
rewrite thirteen pointer sites afterwards to move the floor up to 8342H. That costs the user
~960 bytes of document space, and his article says so.

Layer A moves the **ceiling** instead. It costs **zero** text buffer. Same problem, opposite end.
It is also why the 3-byte-for-3-byte substitution matters: it reaches code at FF6CH without
moving a single byte of Scripsit.

## 10. What the remaining changes turned out to be

Traced by following what each address is used for inside Scripsit. No new material was needed.

### 5DCCH — a bug in Radio Shack's Scripsit, fixed

Every absolute reference into 7CB0–7CC0 in **stock** `SCRIPSIT/CMD`:

```
7CB6 : written at 5DCC - read NOWHERE
7CB9 : read at 5D47 and 7A6E - written NOWHERE
```

One variable written and never consulted, another consulted and never written: an off-by-three
slip in a hand-assembled 1979 program. The reader at 5D47 was picking up whatever happened to
sit at 7CB9.

The patch writes 7CB9 instead of 7CB6, connecting the writer to its two readers. The reordering
follows from that: the original relies on `OR A` at 5DCB setting flags for `CALL NZ,5DEF`, so it
stores first. The patch calls first, then reloads `LD A,C` (5DEF clobbers A) and stores — same
flags, correct target, paid for with the `NOP` at 5DD2.

The companion change at 5D47 (`LD A,(7CB9)` → `CALL 7A6E`) routes the read through stock
Scripsit's 7A6E, which reads 7CB9 *and* applies a `DEC B` correction. Both changes are one repair.

### 603AH / 6056H — no runtime effect

These are **self-modifying displacement bytes**. 6038 is `LD (IY+5),A` with IY=7E11, and the `05`
*is* that displacement; 603B reads it back as data, increments, masks `AND 1F`, writes it back.
6056 is the same trick on `LD A,(IY+5)` at 6054. Write index, read index, 32-byte circular
type-ahead buffer, compared at 6046 to test for empty.

But cold start at 523F does `XOR A` and zeroes both (5254, 5257) before the buffer is used.
**The file's value is overwritten on every start, so 05→04 changes nothing at runtime.**

### 7A20H / 7A22H — the page defaults

The 20-byte block at 7A15H is LDIR'd to 7C64H at 708BH. It decodes against the manual:

| | value | |
|---|---|---|
| 7C65 | 12 | `LM` — Linker Rand (12 voreingestellt) |
| 7C66 | 72 | `RM` — Rechter Rand (72) |
| 7C67 | 1 | `LS` — Zeilenabstand (1) |
| 7C6E | 6 | `TM` — Oberer Rand (6) |
| 7C6F | 60 → **127** | `BM` — Unterer Rand (60) |
| 7C71 | 66 → **127** | `PL` — Seitenlänge (66) |

Confirmed by the directive handlers: `766E LD HL,7C6F` is `>BM=`, `7798 LD HL,7C71` is `>PL=`.
The `Y`/`N` bytes at 7C68–7C6C are the `C`/`FR`/`J` flags.

66 lines is US Letter at 6 lpi; A4 needs about 72. SCRIPSIT.TXT opens with `PL=72 BM=66` and tells
the reader to set the same. *Inference:* raising both defaults to 127 pushes the page-break logic
out of the way so an unmarked document does not break at the American boundary. The
identification is certain; the reason is not.

## 11. Still open

Nothing in the byte-level account. What remains are questions about intent in 1988 — why 127
rather than 72/66, and whether dropping the printer half of the underlining was deliberate.
Neither is answerable from the bytes or by testing.
