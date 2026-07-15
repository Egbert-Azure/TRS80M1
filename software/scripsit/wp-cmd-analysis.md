<!-- /software/scripsit/wp-cmd-analysis.md — binary-derived reconstruction of WP/CMD (Layer B) -->

# WP/CMD — reconstruction from binary evidence

*Narrative account: [`scripsit-sp-article-en.md`](./scripsit-sp-article-en.md) (EN) · [`scripsit-sp-artikel.md`](./scripsit-sp-artikel.md) (DE). Index: [`README.md`](./README.md).*

Recovered from `esnd-04.dmk`, physical track 10 / side 1 / sectors 13–16, 883 bytes.
Validates as an exact `/CMD`: eight load records, terminal `ENTRY` at file offset 0371h,
zero residue. Derived by disassembly; provenance noted per claim.

**Recovery note:** the previously extracted `WP/CMD` was 883 bytes of `E5` fill. The disk was
never at fault — see §7 for the extent geometry.

## 1. Load map

| record | address | len |
|---|---|---|
| 1 | 7AA7–7AD9 | 51 |
| 2 | 7AFA–7B79 | 128 |
| 3 | 7B7A–7BD6 | 93 |
| 4–8 | 7F62–81A0 | 575 |
| ENTRY | **7B19** | |

Two facts drop out of the map alone:

- **7AA7 begins three bytes after SCRIPSIT/SP ends at 7AA4.** The two files were allocated
  against each other.
- **7F62–81A0 is not free space** — it is Scripsit's text buffer. See §4.

## 2. Entry: 7B19 — which Scripsit to load

```
7B19  LD HL,431A        ; DOS command tail
      LD A,13 / CP (HL)
      JP Z,402D         ; no argument -> DOS error exit
      RST 10H           ; skip blanks, A = first non-blank
      PUSH HL
      CP 'S'
      JR NZ,7B2D
      LD DE,7ACE        ; "SCRIPSIT/SP"
      JR 7B30
7B2D  LD DE,7AC1        ; "SCRIPSIT/CMD"
7B30  CALL 4430
      JP NZ,402D
      CALL 4428
      DI
```

So `WP SP*` and `WP SCRIPSIT` both take the `S` branch and load **SCRIPSIT/SP**; any other
argument loads stock **SCRIPSIT/CMD**. WP patches whichever it loaded.

## 3. Reentry — and the answer to open item #1

```
7BAD  POP HL / INC HL / PUSH HL / POP IX
      LD A,'*' / CP (HL)
      JR NZ,7BBE        ; no '*' -> cold start
      LD A,(7BD7)
      CP 'Z'
      JR Z,7BC6         ; flag intact -> warm reentry
7BBE  LD A,'Z' / LD (7BD7),A
      JP 523F           ; COLD start
7BC6  DI
      LD SP,41FC
      LD HL,52C0 / PUSH HL
      LD A,8Bh
      LD (IX),' '       ; blank the '*' in the command tail
      JP 52DD           ; WARM reentry
```

**7BD7 is one byte past WP's last loaded byte (7BD6).** The `'Z'` flag therefore survives
reloading WP. That is the TXT's *"Scripsit Patch Routine überprüft, ob ein Rücksprung möglich
ist"* — the check is a byte deliberately parked outside every load record. *Confidence: high.*

**Open item #1 from the SCRIPSIT/SP analysis is resolved.** Scripsit's own main loop does
`LD SP,41FC / LD HL,52C0 / PUSH HL / … / 52DD` at 52CF–52DD; 52C0 is the loop head, reached
by `RET`. WP's warm path replicates that sequence byte for byte. SCRIPSIT/SP's `NOP`→`DI` at
52C0 therefore re-executes `DI` on **every pass of the editor main loop**. *Confidence: high
on what, medium on why — most likely protecting the FF6C–FFFF driver from interrupt use.*

## 4. The thirteen pointer stores are not hooks

```
7B3A  LD HL,81A1
      LD (5277),HL   LD (5416),HL   LD (5532),HL   LD (5993),HL
      LD (59CB),HL   LD (5DB6),HL   LD (6316),HL   LD (6352),HL
      LD (66DF),HL   LD (69B4),HL   LD (6E25),HL   LD (741A),HL
      LD (7428),HL
```

All thirteen sites hold **7F62** in both SCRIPSIT/CMD and SCRIPSIT/SP. 7F62 is Scripsit's
**start-of-text-buffer** constant. WP loads code at 7F62–81A0, so it relocates the buffer base
to **81A1 — exactly one byte past its own last loaded byte.** Nothing is hooked here; WP is
moving out of its own way. *Confidence: high.*

*(This corrects "fourteen hooks" in my earlier summary: thirteen buffer-base stores, and a
separate set of real hooks below.)*

## 5. The real hooks — six of them

WP reuses **Scripsit's own table dispatcher at 58F0**, whose format is:

```
58F0  PUSH BC / PUSH HL
      LD C,(HL) / LD B,0 / INC HL    ; C = count N, HL -> key list
      CPIR                            ; on match at key[i], C = N-1-i
      POP HL / LD A,C
      JR Z,58FF
      POP BC / XOR A / RET            ; not found: A=0, Z
58FF  LD C,(HL) / LD B,0 / INC HL
      ADD HL,BC                       ; -> address list
      RLCA / LD C,A / ADD HL,BC       ; index = (N-1-i)*2  <-- REVERSED
      POP BC / LD A,(HL) / INC HL / LD H,(HL) / LD L,A
      POP AF / JP (HL)                ; discards caller's return address
```

Table layout: `count, key[0..N-1], addr[0..N-1]` — **addresses indexed in reverse**. This is
the key to reading WP's tables correctly.

| site | original | patched | effect |
|---|---|---|---|
| 52F7 | `JP 6F76` (error) | `JP 8046` | **@-key table extension** |
| 6465 | `JP 6F77` (error) | `JP 8052` | **BREAK command extension** |
| 6155 | `CP 9Dh / JR NZ,615D / LD A,1Fh / JR 6179` | `JP 8002` | adds key 9Eh → code 07 |
| 5FAF | `INC (IY+6)` | `JP 808A` | screen: 40h displayed as 5Fh |
| 73A2 | `CALL 7177` | `JP 805D` | **SHIFT-P printer pause** |
| 5E16 | `JR NZ,5E2F` (+ `RET`) | `JP 8076` | **NEW FILE! / FILE UPDATED!** |

The two table extensions are the elegant part. 52F7 and 6465 were Scripsit's *"unknown key"*
error exits. WP repoints them at its own tables and falls through to the same error if still
unmatched — an extension that costs 3 bytes and cannot break the original:

```
8046  LD A,(7C3E) / LD HL,7AA7 / CALL 58F0 / JP 6F76   ; @-key
8052  LD A,(7C3A) / LD HL,7AB4 / CALL 58F0 / JP 6F76   ; BREAK
```

**The layering composes with SCRIPSIT/SP.** WP's 8002 ends `JP NZ,615D` — which in SP is
`JP FFAC`, the umlaut translator. Chain: `6155 → 8002 (9D/9E) → 615D → FFAC (umlauts) → 6167`.
Layer B chains into Layer A's hook without either knowing about the other's internals.

## 6. WP's two tables

### Table 1 — @-key, at 7AA7 (count 4)

| key | via | handler | function |
|---|---|---|---|
| 02h (`@b`) | | 7F8E | scroll 13 lines |
| 08h (`@h`) | | 6E56 | cursor home (Scripsit's own) |
| 1Fh | 9Dh via 8002 | 7FCC | cursor to end of previous word |
| 07h | 9Eh via 8002 | 7FE7 | cursor to start of next word |

WP also rewrites key `1F` → `14h` at 79AA in Scripsit's own 25-entry table at 7993, so the
code it now claims no longer collides.

Three further 13-line routines are installed by overwriting address slots in that same table:

```
LD HL,7FBB / LD (79D9),HL   ; key 1Bh : was 6E24
LD HL,7F9C / LD (79D7),HL   ; key 1Ch : was 6E5D
LD HL,7FAD / LD (79BF),HL   ; key 06h : was 5518
```

All four have the shape `LD A,13 / PUSH AF / CALL <scripsit move> / CALL 8153 / POP AF /
DEC A / JR NZ` — literally "do the move thirteen times". That is the TXT's *"Window Scroll
13 Zeilen"* and *"Cursor 13 Zeilen rückw. @ f / vorw. @ b"*.

### Table 2 — BREAK commands, at 7AB4 (count 4)

Reading through the reversed index:

| cmd | handler | evidence | TXT |
|---|---|---|---|
| `K` | 8014 | builds filespec, `CALL 442C` | `KILL` / `K filename` |
| `N` | 5200 | Scripsit cold entry | `BREAK N` / `New` reinitialise |
| `X` | 8098 | prints `PRINTER INITIALIZED` (7F62), parses number, `LD (37E8H),A` | `BREAK X=nnnn` |
| `Q` | 80D8 | selects `DIR 0`/`DIR 1`/`DIR 2` at 7AFA/7B00/7B06 | `BREAK Qn` directory |

The reversed indexing is why the naive reading (`K→80D8`) is wrong — all four only line up
with the TXT once 58F0's `C = N-1-i` is accounted for. *Confidence: high; three of four are
independently confirmed by their own string constants.*

## 7. Supporting routines

| addr | function |
|---|---|
| 8121 | clear screen (fill 3C00.. with 20h, `BIT 6,H` terminate) |
| 8132 | printer pause: fill 3F80–3FBF with 8Ch, `CALL 0060` ROM delay, `CALL 5FD2` |
| 8153 | `LD (7C43),DE / LD HL,(7C2B) / LD (HL),0` — cursor/state helper |
| 815D | `CALL 0033` — ROM display character |
| 8163 | decimal print, divisor table at 7B0C = `D8F0 FC18 FF9C FFF6 FFFF` (−10000…−1) |
| 8187 | advance cursor (4020) to next 64-column boundary |

## 8. Disk geometry — why the first extraction failed

```
linear_sector = 36 + lump*10 + granule*5
  addressing : cyl*36 + side*18 + sector    (cylinder 0 = SD boot, excluded)
  lump = 10 sectors, granule = 5 sectors, GPL = 2
  extent byte0 = lump
  extent byte1 = (granule << 5) | (count - 1)
  directory   : physical track 6, side 0, sectors 0–3 (32 entries)
```

Lumps straddle the side boundary — NEWDOS/80 is addressing the disk as one continuous
36-sector-per-cylinder stream. Validated on all 16 files: every `/CMD` parses to an exact
`ENTRY` record; `SCRIPSIT/CMD` and `SCRIPSIT/SP` come out byte-identical to the known-good
copies. Note `boot[2] = 11h` claims directory track 17; the directory is at track 6.

## 9. Open items

**Resolved since the SCRIPSIT/SP analysis:**
- ~~52C0 `NOP`→`DI`~~ — main-loop head, WP's warm-reentry landing (§3).
- ~~"fourteen hooks"~~ — thirteen buffer-base stores plus six real hooks (§4, §5).

**Still open:**
1. **7CB6 → 7CB9 variable move at 5DCC** (SCRIPSIT/SP). WP does not reference either address.
2. **603A / 6056 `05` → `04`** (SCRIPSIT/SP).
3. **7A20 / 7A22 `3C`,`42` → `7F`,`7F`** — in the 20-byte defaults block LDIR'd to 7C64.
4. **4049H.** SP writes FF6B, exactly one below its FF6C driver — consistent with 4049H being
   the DOS top-of-memory pointer, which would make the write a memory reservation. But KBDGER
   writes FFEF while loading at F000, which does not fit that reading. Unresolved.
5. **5FAF hook / 40h → 5Fh on screen.** Mechanism certain, purpose not. Plausibly a German
   character-generator artefact (DIN 66003 renders 40h as §), but unproven.
6. **DOS vector names** (4419, 441C, 442C, 4420, 4428, 4430) asserted from context only.
