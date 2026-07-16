<!-- /software/scripsit/scripsit-provenance.md — what is Lindley's, what is mine -->

# SCRIPSIT/SP and WP/CMD — provenance

*Narrative account: [`scripsit-sp-article-en.md`](./scripsit-sp-article-en.md) (EN) · [`scripsit-sp-artikel.md`](./scripsit-sp-artikel.md) (DE). Index: [`README.md`](./README.md).*

Established from: the object code printed in the magazine listing; `WP.ASM` + `WP.CMD` (an EDTASM
transcription of that listing and its assembly); `wpand.scr` (a second EDTASM
transcription); `wp.cmd` / `wp7.cmd` (further builds of Lindley's program),
`WP/CMD` (esnd-04), `SCRIPSIT/CMD`, `SCRIPSIT/SP`, and Lindley, *"Inside Scripsit — Part II"*,
80 Micro, October 1982, p. 276ff.

## 1. What the files are

**Authorship is settled and is not what any of this is about.** Craig A. Lindley wrote the patch
program; the article carries his byline and every copy carries his banner. The open questions
below are narrower: *which* copy is which build, and which of them can serve as a reference. A
banner travels with every copy and so cannot answer either — `SCRIPSIT/SP` carries
`COPYRIGHT 1979 BY RADIO SHACK` at 5214H, and that does not make it Radio Shack's file.

| file | identification | evidence |
|---|---|---|
| `WP.ASM` (16163 B) + `WP.CMD` (1372 B) | **An EDTASM transcription of Lindley's published Listing One, and its assembly.** Who keyed it in is **not established**. **Not Lindley's own source** — the printed listing carries comments on every equate (`;*DISK I/O BUFFER` and the rest of that block) and `WP.ASM` has none of them. A listing is generated *from* a source, so the source had them; a file missing them is a copy. What it does establish: its code **matches the printed object bytes at 41 of 42 sample points** (the one miss is my reading of the scan), and it assembles to `WP.CMD` with zero differing bytes. It also carries the Model III insertion points, which no other copy has. |
| `wp.cmd` (1392 B) | **Lindley's program — a third build of it.** Authorship is not in question here or anywhere below: he wrote it, the article says so, and every copy carries his name. What is unresolved is only *which build this is*: it differs from `WP.ASM`'s output in 43 bytes (the sign-on message, uppercase where `WP.ASM` has it mixed case) and calls 4476H for `LOUT` where the printed equate block and both transcriptions say 4467H — so it is not a clean build of the published listing. Line Printer IV build. | banner at 7F62: `*** SCRIPSIT PATCH PROGRAM *** BY  CRAIG A. LINDLEY`; targets `SCRIPSIT/LC` + `SCRIPSIT/UC`; underline codes at 7AA8/7AA9 = `0E`/`0F`, matching the article's *"0FH to turn underlining on and 0EH to turn it off"* |
| `wp7.cmd` (1536 B) | same program, **retargeted to an ESC-sequence printer** | 7AA8/7AA9 = `59`/`58` (`'Y'`/`'X'`); `UNDRLN` reworked to busy-wait on bit 7 of 37E8H and emit `1BH` before the code — i.e. `ESC X` / `ESC Y`. Not pursued further; I had a **Seikosha** printer around 1984 *(recollection, not established from the bytes)* |
| `wpand.scr` | **A TRS-80 EDTASM source file** containing Lindley's Listing One, carrying one of my edits. Origin uncertain — see below | file format is EDTASM, not text: header `D3 'WP    '`, then 820 records of five high-bit digits + text + `0D`, terminated `1A`. The only high-bit bytes in the file are `B0`–`B9` and that `D3`. Its `DEFS`/`DEFB` layout predicts `wp.cmd`'s load-record gaps exactly (7AA5–7AA6 = `DIRPTR DEFS 2`, 7AAA–7AAB = `VDVR DEFS 2`, both absent) |
| `WP/CMD` (883 B) | **my derivative** of Lindley's program | see §3 |

`wpand.scr` retains the original EDTASM line numbers — 820 lines, 100 to 8290 — and the
article's own text references resolve exactly against it: *"lines 550 and 560"* are `UNDOFF`
and `UNDON`; *"Lines 610-810 of Listing 1 show these new command lookup tables"* runs from
`CMDTB1 DEFB 4` to `DEFW KILL`. It is the complete listing in machine-readable form.

### Origin of `wpand.scr`

My recollection is that this came off the internet and that my own source is lost. The bytes
complicate that:

- It is an **EDTASM source file**, not a text transcription. Someone keyed it in on a TRS-80 or
  an emulator. A scan-to-text pass does not produce a `D3` header and high-bit line numbers.
- It is **not the source of my WP/CMD**. It targets `SCRIPSIT/LC` + `SCRIPSIT/UC`, carries
  Lindley's banner, and contains `UNDRLN`/7A9E and `RETURN`/6595 — none of which my WP/CMD
  has. It is Lindley's program, not the stripped-down derivative.
- But **line 5020 carries an edit only I am known to have made** (see the table below), and that
  edit is corroborated by my binary and my manual.

Best reading: `wpand.scr` is an **intermediate stage** — Lindley's listing keyed in and given its
first printer-oriented edits, before the strip-down that produced WP/CMD. The lost source would
be the later, stripped version. This is inference, not proof; an unrelated transcriber
independently choosing `CP 0FFH` is possible but would be a sharp coincidence.

*Superseded: an earlier pass argued I had hand-retyped this, on the grounds that OCR does not
produce errors like `QUERY DISH`, `DCB FOB`, `SMD LINE`. That reasoning was wrong — K→H, R→B and
C→S are ordinary OCR confusions. The typos establish nothing about who made the file.*

### Verified by assembly

The assembler used here (purpose-written, EDTASM subset) was checked first against the
`WP.ASM`/`WP.CMD` pair: **zero differing bytes** — 1336 bytes, identical address coverage,
`START` = 7B49H, `TXTBUF` = 8342H, `TSTBYT` = 7C21H. Every relative displacement, operand order
and prefix byte agrees.

**The referee is the magazine, not any of these files.** 80 Micro printed an assembler listing —
address, object bytes, line number, source — so the printed bytes decide. Against 42 sample
points read off those pages:

| | matches printed object bytes |
|---|---|
| `WP.ASM` | **41 / 42** |
| `wpand.scr` | 38 / 42 |

`wpand.scr` misses at 7AA8, 7AA9 and 8131 — the three edits below, and nothing else. The point
both miss (8162) is my reading of the scan, not a real difference: `MSG5+31` resolves identically
in both.

**What that does and does not establish.** Two pages of the listing are available, covering the
header, the equates, the storage area, both dispatch tables, and roughly lines 4880–5910. Against
those pages the following are checked **directly against print**:

| claim | printed evidence |
|---|---|
| 7AA8 / 7AA9 = `0E` / `0F` | `UNDOFF DEFB 14` / `UNDON DEFB 15` |
| 8131 = `FE20` | `CP 20H ;NUM LESS THAN 32 ?` |
| `LOUT` = 4467H | the equate block |
| printer range 1–31 | Table 1, and the `CP 20H` above |

Everything else — line 5670, the case of `MSG1` at 7F62H, and the roughly 95% of the listing not
on those two pages — is **not** verified against print. Where a claim rests on `WP.ASM` alone, it
rests on one transcription against another, and is marked.

`wpand.scr` was then assembled the same way (0 errors, 820 lines) and diffed against `wp.cmd`:

- **1336 bytes emitted; 1336 bytes in `wp.cmd`. Identical address coverage — no byte present in
  one and absent from the other. Five bytes differ.**
- Symbols land exactly where the binary requires: `START` = 7B49 = `wp.cmd`'s `ENTRY` record;
  `TXTBUF` = 8342 = the value its installer stores into the thirteen sites; `TSTBYT` = 7C21 =
  one past its last loaded byte (7C20).

The transcription is faithful. The five bytes are three edits:

| line | `wpand.scr` | `wp.cmd` | reading |
|---|---|---|---|
| 550 / 560 | `DEFB 45` ×2 | `0E` / `0F` | **unfinished or abandoned.** 45 = 2DH = `'-'` for both on *and* off — cannot work as written. The article instructs the reader to change exactly these two lines for their printer; I had a Seikosha around 1984. |
| 5020 | `CP 0FFH` | `CP 20H` | **deliberate, and mine.** See below. |
| 5670 | `JR Z,NODRV` | `JR Z,NODRV` | **a branch inversion relative to `WP.ASM`**, which has `JR NZ,NODRV`. ⚠ **Not on either printed page available**, so which form the magazine carried is unknown — this rests on one copy against another. `wp.cmd` shares the inverted form, so it is not unique to `wpand.scr`. In the `QUERY` drive check. Untested. |
| 6130 + 6850 | `CALL LOUT` → 4467H | → 4476H | **not an error in `wpand.scr`.** `WP.ASM` reads `LOUT EQU 4467H` too, and the magazine printed `4467  LOUT  EQU  4467H` in the equate block. Two transcriptions and the printed listing agree; `wp.cmd` is the only file carrying 4476H. See §5.8. |

**Line 5020 is mine, established against the printed listing.** The published Listing 1 reads:

```
8131  FE20    05020    CP    20H     ;NUM LESS THAN 32 ?
```

`FE 20` at 8131 — the operand lands on 8132, exactly the byte where `wpand.scr` and `wp.cmd`
disagree. Lindley shipped 0–31 in print *and* in binary, consistent with his Table 1
(*"decimal printer control codes from 1-31"*). `wpand.scr` reads `CP 0FFH`, my `WP/CMD`
at 80C7 reads `CP 0FFH`, and SCRIPSIT.TXT documents *"BREAK X=nnnn (n= 1-255)"*. Print, two
binaries and the manual all agree on the direction of the change.

This is the one substantive functional extension I made to Lindley's Layer B. Everything else I
did to WP/CMD was subtraction.

## 2. The source resolves the whole structure

Lindley's own labels confirm, independently, the reading derived from the binary — including
the reversed address indexing of the 58F0 dispatcher:

```
CMDTB1  DEFB 4          CMDTB2  DEFB 4
        DEFB 2                  DEFB 'K'
        DEFB 8                  DEFB 'N'   ;RESTART SCRIPSIT
        DEFB 1FH                DEFB 'X'   ;EXECUTE PRINTER INIT
        DEFB 7                  DEFB 'Q'   ;QUERY DISH
        DEFW RSKP               DEFW QUERY
        DEFW FSKP               DEFW PRTINT
        DEFW 6E56H              DEFW 5200H
        DEFW CURDWN             DEFW KILL
```

`K`→`KILL`, `N`→`5200H`, `X`→`PRTINT`, `Q`→`QUERY` only line up under `C = N-1-i`. Confirmed.

The article also explains two oddities the binary could only show mechanically:

> *"I solved the first problem by overlaying the tab-key code byte in the main command lookup
> table (79AAH) with a 14H for the @, T key code."*

That is `LD A,14H / LD (79AA),A` — freeing code `1F` for `@`,right-arrow. And:

> *"…the keyboard driver routine located at 6061H didn't provide a unique key code for the @,
> left-arrow combination. I patched the keyboard driver (at address 6156H) with the Keymod
> routine… This patch causes the @, left-arrow key combination to return a 7H code (the same
> as the @, G key combination)."*

`KEYMOD` in the source is byte-for-byte my 8002.

## 3. My WP/CMD = Lindley's installer minus four items

Every hook I kept is at **Lindley's address**:

| Lindley | kept? | mine |
|---|---|---|
| 13 × `LD (nnnn),HL` ← `TXTBUF` | ✅ | same 13 sites, `81A1` vs Lindley's `8342` |
| `C3` → 6155 + `KEYMOD` → 6156 | ✅ | → 8002 |
| `C3` → **7A9E** + `UNDRLN` → **7A9F** | ❌ **dropped** | — |
| `C3` → 5FAF + `UNDERL` → 5FB0 | ✅ | → 808A |
| `C3` → 73A2 + `LPWAIT` → 73A3 | ✅ | → 805D |
| `C3` → 5E16 + `NEWOLD` → 5E17 | ✅ | → 8076 |
| `LKUP1` → 52F8 | ✅ | → 8046 |
| `LKUP2` → 6466 | ✅ | → 8052 |
| `RETURN` → **6595** | ❌ **dropped** | — |
| `UPWSRL` → 79D9, `DWSRL` → 79D7, `CURUP` → 79BF | ✅ | → 7FBB / 7F9C / 7FAD |
| `LD A,14H / LD (79AA),A` | ✅ | identical |
| `LDIR MSG1 (51 B) → 57F7` | ❌ **dropped** | banner moved into SCRIPSIT/SP statically |

Only ~2% of overlapping bytes are identical between `wp.cmd` and `WP/CMD`. I reassembled from
source and relaid the code out; I did not copy the binary. *(Which source is not
established — see §1.)*

### Why 7A9E had to go

`UNDRLN` is Lindley's **printer** underline routine, hooked at 7A9E. SCRIPSIT/SP extends the
7A00 load record from 126 to 165 bytes — **7A00–7AA4 — which covers 7A9E**. My own
umlaut/printer patch occupies Lindley's hook slot. The collision is structural, not a choice.

I kept the **screen** half (`UNDERL` at 5FAF: `CP 40H → LD (HL),5FH`), so the underscore marker
still displays — but nothing acts on it at print time, and SCRIPSIT.TXT documents no underlining
at all. `UNDERL` is confirmed working at runtime: `SHIFT`-0 produces a glyph distinct from the
`@p` hatched square. Whether dropping the printer half was deliberate is a question about intent
in 1988 — not something the bytes settle, and not something a test can.

### Other reductions

- `QUERY`: Lindley reads the GAT, counts free granules, reads 8 directory sectors and prints
  `FREE GRANS - DIRECTORY - DRIVE X - FILENAME - DATE`. My 80D8 does `DIR 0`/`DIR 1`/`DIR 2`.
- `SCRIPSIT/LC` + `SCRIPSIT/UC` → `SCRIPSIT/CMD` + `SCRIPSIT/SP`.
- `TXTBUF` 8342 → 81A1 (my program is 490 bytes smaller).

## 4. What is actually mine

**SCRIPSIT/SP — Layer A — owes nothing to Lindley.** Lindley's patch is a `/CMD` RAM patcher;
he never modifies the Scripsit file. My static file patch, the umlaut table at FFCF/FFE0,
the `@p` + two-hex-digit printer escape with the `RLD` assembler, the FFE2→FFF1 printer
translate table, the relocation of Scripsit's marker glyphs off 5B/5C/5D, and the `DI` at 52C0
are all his.

The two layers were built to fit each other: 7AA7 begins three bytes after SP ends at 7AA4,
and WP's 8002 falls through to 615D — which in SP is `JP FFAC`.

**Assessment: this is a port-and-extend, not a borrowed idea.** The reference in Club-80
Sonderinfo 27.5 is appropriate and the derivation should be stated plainly in the repo.
My original contribution is the German-language layer, which is substantial and separate.

## 5. Corrections made during this analysis

1. **`1F` and `07` were swapped.** `1F` = `@`right-arrow → `FSKP` → **start of next word**.
   `07` = `@G` / `@`left-arrow → `RSKP` → **end of previous word**. My 7FCC calls `CURRHT`
   (5518) and 7FE7 calls `CURLFT` (54FB), confirming Lindley's labels.
2. **Key `02` is `CURDWN`**, cursor down 13 lines (`@B`), not window scroll. The scroll routines
   are `UPWSRL`/`DWSRL` on keys `1B`/`1C`.
3. **The 7BD7 reentry flag is Lindley's design, not mine.** The source reads `TSTBYT EQU $`
   — the flag falls one past the last byte by construction. The 52C0/52DD warm-reentry sequence
   is Lindley's too. An earlier pass credited both to me. Wrong. The `DI` *at* 52C0 inside
   SCRIPSIT/SP remains mine.
4. **DOS vectors** — from Lindley's equates, not guesswork: `402DH` OPSYS reentry, `441CH`
   PARSE filespec, `4428H` CLOSE (not @CLS), `4430H` LOAD, `4436H` read sector, `4467H` LOUT.
5. **Open item #5 resolved.** The 5FAF hook is Lindley's `UNDERL`: Table 1 item 9, *"<shift>0 —
   Placing the underscore character in the text causes underlining."*
6. **Open item #6 resolved** by (4) above.

8. **Withdrawn — the `LOUT` transposition.** An earlier pass called `wpand.scr`'s
   `LOUT EQU 4467H` a retyping slip against `wp.cmd`'s 4476H, and said it would have broken
   `QUERY`. That was backwards. The magazine's own equate block prints 4467H, `WP.ASM` reads
   4467H, and both assemble to `67` at 8203 and 828D. **`wp.cmd` is the outlier**, and what
   4476H is remains unexplained. Nothing was ever broken.

10. **Overstated:** an earlier pass called `WP.ASM`/`WP.CMD` "Lindley's source and its binary"
    and "the reference pair". Neither is established. `WP.ASM` is an EDTASM file someone keyed
    in — it lacks the equate comments the magazine printed, so it is a copy, not the original.
    `WP.CMD` is simply what it assembles to. The printed listing is the reference; these files
    are measured against it like any other.

9. **`wpand.scr` is not an independent transcription.** Against `WP.ASM` it differs in 150
   lines, of which all but six are comments — the section prose stripped to bare `;`, and
   explanatory comments *added* to the equates that Lindley never wrote. The six code lines are
   550, 560, 2730/2740 (the sign-on message), 5020 and 5670. It also **corrects** Lindley's own
   typos (`LOOPUP`→`LOOKUP`, `ADDTION`→`ADDITION`) while **introducing** others
   (`WRITTEN`→`WRITEN`, `AREA`→`AERA`, `FOR`→`FOB`). OCR does not correct spelling, and it does
   not annotate. Someone retyped this while reading it closely. Who, is still not established.

7. **Withdrawn:** an earlier pass claimed `wpand.scr` carries `DEFW 5200H` where the magazine
   shows `5209H`. That `5209H` came from OCR of the scan — the same pass that produced `5661`
   for `566E`, `3608` for `3680`, and `HSKP` for `RSKP`. `wp.cmd` has `00 52` = 5200H,
   and assembling `wpand.scr` reproduces it. The listing reads 5200H; the OCR was wrong. The
   real source-stage edits are lines 550/560, 5020, and the `LOUT` equate — see §1.

## 6. Still open

7CB6→7CB9 at 5DCC; 603A/6056 `05`→`04`; 7A20/7A22 `3C`,`42`→`7F`. None appear anywhere
in Lindley — they are mine, in SCRIPSIT/SP.

Three of the four are Scripsit internals, so the two things that would close them:

1. **An EDTASM source for the SP patch**, if one survives. `SCRIPSIT/TXT` came off `esnd-05.dmk`,
   so that disk held Scripsit material; it has not been searched for a source.
2. **Lindley Part I**, if it carries a Scripsit memory map. Part II's prose does not.
