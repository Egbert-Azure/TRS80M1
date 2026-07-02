<!-- /software/sidekick/README.md — SideKick multi-computer banker disk -->
<!-- (c) E. Schroeer -->
# Disk SIDEKICK — NEWDOS/80 V2.0 (Apparat) with SideKick multi-computer banker

**Operating system:** NEWDOS/80 V2.0 — appears to be original Apparat Inc. stock
**Geometry:** 80-track, single-sided, single density (JV1, 204,800 bytes)
**Directory:** Track 17, 23 file entries, 56 free granules (per `DIR` under SDLTRS)
**Status:** Good. The on-disk SideKick assembler source is complete and clean.

**Files here:** [`SIDEKICK.JV1`](SIDEKICK.JV1) (disk image) ·
[`SIDEKICK.Z80`](SIDEKICK.Z80) (Z80 source, reference copy extracted from the disk)

*Sources: the `SIDEKICK/Z80` Z80 source; Gerald Schröder's original article and
listing in Club80 Nr. 17 (1986), pp. 8–15; Helmut Bernhardt's banker hardware
in BHV-03 (1986), pp. 5–10; the disk directory under SDLTRS; and the JV1 byte
image. Statements about authorship and mechanism are read from these primary
sources, not inferred.*

---

## 1. What SideKick is

`SIDEKICK/Z80` is the complete, commented Z80 source of a resident utility that
keeps **four independent "computers"** — four complete machine states — in
bank-switched memory at once, and lets you hotkey between them. Only the active
computer runs; the others are frozen. It is a fast manual context switch
between whole machine states, not multitasking.

Schröder titled the 1986 article *"Wie Phönix aus der Asche — Vier Computer in
einem Schrotthaufen"* ("Four computers in one scrap heap"): the point was to
get IIIs-style multi-machine capability out of a plain TRS-80 Model I plus a
cheap memory banker.

**Authorship chain:**

| Contribution | Person | Date |
|--------------|--------|------|
| Idea | Arnulf Sopp | — |
| Banker hardware (256K bank-switch board) | Helmut Bernhardt | 1986 |
| Original SideKick implementation | Gerald Schröder | Dec. 1986 |
| Adaptation for Alpha Technology **SuperMem** + on-screen computer display | Jens Günther | Nov. 2024 |

---

## 2. The banker hardware (Bernhardt, 1986)

SideKick depends on a memory banker, not on any standard bus card. Bernhardt's
design replaces the machine's 4164/4116 RAMs with pin-compatible 41256 chips
plus a small banking logic, giving 256K (optionally 512K/1024K).

The geometry that shapes SideKick. On a BASIC-in-ROM machine like the TRS-80
the split is dictated by what *can* be banked:

- The **lower region (0000h–3FFFh)** is ROM (0000h–2FFFh) plus memory-mapped
  I/O and video RAM (3000h–3FFFh). None of it is bankable — there is no RAM
  there to swap — so it is always visible. This is the true Common area:
  interrupt routines reachable through ROM/SYS0, and the fixed I/O and screen.
- Bernhardt's banker therefore switches the **upper 32K (8000h–FFFFh)**. As the
  Club-80 hardware note puts it, "Banking der oberen 32K ist nur dann sinnvoll,
  wenn es sich um einen BASIC-im-ROM-Computer … handelt," and it is done by
  inverting A15 (e.g. a 74LS04) so the latch selects among parallel 32K blocks
  in the high half.
- RESET forces bank 0, so initialization always starts from a known state.
- Bank 1 would overlap the block that must stay put, so the logic redirects it
  to the highest bank; the top bank (7 at 256K, 15 at 512K, 31 at 1024K) is
  therefore unusable.

So the earlier description here — "upper half fixed, lower half banked" — was
backwards, and the correction is due to Jens Günther (corroborated by the
Club-80 *256K RAM für Z80-Systeme* note). On the TRS-80 it is the **upper 32K
that is bank-switched** and the **low ROM/I/O/video region that is common**.

What the SuperMem source actually does. The on-disk `SIDEKICK/Z80` is the 2024
SuperMem port, which has no A15-inversion hardware and banks in software via
`OUT (043h),A`. Read from the bytes rather than the hardware note, two routines
matter:

- **`copy`** (initial fill) block-copies **3000h–7FFFh into the high bank
  window B000h–FFFFh** (`LD DE,8000h+3000h` / `LD H,30h` / `LDIR` →
  "(3000-7FFF)=>(B000-FFFF)"); its comment "kopiert oberen und unteren Teil in
  Banks" confirms it stages both halves.
- **`tausch`** (the live switch) does **not** bulk-swap a 32K half. It relocates
  the swap code to 7E00h and rotates only the **512-byte window 7E00h–7FFFh**
  between bank 0, the target bank, and bank 1 through a buffer at A000h. The
  bulk movement is already done by `copy`; `tausch` performs the small, careful
  exchange of processor-visible state at switch time.

(Verified against `SIDEKICK.SRC`, 11,146 bytes, `copy` and `tausch` routines
read in full.)

---

## 3. How to use it

1. The banker hardware must be installed (256K + Bernhardt's banker in 1986;
   the Alpha Technology SuperMem in the 2024 version).
2. Run `SIDEKICK/CMD` once from DOS Ready. It installs itself into the
   **GDOS/NEWDOS SYS0 interrupt routine**, copies the computer halves into the
   banks, and returns to DOS Ready.
3. Switch between the four computers by holding the switch key (the routine
   scans the TRS-80 Down-Arrow matrix position) and briefly tapping a digit
   0–3. The host key depends on your keyboard:

   - **PC / SDLTRS:** **End** + digit
   - **macOS / SDLTRS:** **Fn + Right-Arrow** + digit (Fn + Right-Arrow sends
     End on a Mac) — confirmed working

   So:
   - switch key + **0** → computer 0
   - switch key + **1** → computer 1
   - switch key + **2** → computer 2
   - switch key + **3** → computer 3

   Each computer can run its own program.

In the 2024 version the active computer's number is shown in the top-right
corner of the screen (`LD (3c3fh),A`) — e.g. a **1** while computer 1 is
active, a **3** while computer 3 is active.

Switching verified under SDLTRS on macOS (Fn + Right-Arrow + digit). Two of the
four computers, each holding its own independent machine state:

![Computer 3 active — DISK BASIC READY, "3" shown top-right](images/sidekick-computer-3-diskbasic.png)
*Computer 3: NEWDOS/80 DISK BASIC at `READY`, computer number `3` top-right.*

![Computer 1 active — NEWDOS DOS prompt with its own directory, "1" shown top-right](images/sidekick-computer-1-newdos.png)
*Computer 1: NEWDOS/80 `DOS` prompt, a separate disk (`DOS0387`/`KBDGER`
directory) with its own state, computer number `1` top-right.*

### Running SideKick under SDLTRS

The switch combination is a held multi-key press scanned directly from the
TRS-80 keyboard matrix, so on an emulator the host mapping and timing matter.
Notes from Jens Günther for SDLTRS:

- **Hold the switch key, then tap the digit.** The key differs by platform:
  - **PC:** **End**
  - **macOS:** **Fn + Right-Arrow** (sends End) — tested and working
  Hold it down and press **0–3** briefly. The active computer's number then
  appears top-right (e.g. pressing switch-key + 1 shows a **1**).
- **If the digit prints on screen instead of switching**, the keystroke is
  being stretched/repeated. Reduce the **Keystretch Value** (via **Alt-O**),
  e.g. to **100**.
- **Set SuperMem to 256 KB before starting SIDEKICK.** In **Emulator Settings**
  (**Alt-E**), enable/size **SuperMem** to **256 KB**; without it the banking
  cannot work.

**Two rules for any program running inside a computer (stated by Schröder):**

- It must **leave interrupts enabled.** SideKick lives in the interrupt
  routine, so a program that does a permanent `DI` blocks switching.
- It must **not leave special hardware engaged across a switch.** Graphics
  cards specifically: a program may use the HRG card, but must switch it
  **off before hotkeying away**, because the destination computer knows nothing
  about it.

**Expected behaviour:** the screen briefly shows garbage during a switch,
because computer 0 is selected as an intermediate step before the target
computer comes online. This is normal, not a fault. To avoid spurious effects
(e.g. printer output), the I/O region 3700h–37FFh is deliberately not saved.

---

## 4. NEWDOS/80 and G-DOS vs. LDOS

SideKick's four-computer mechanism is specific to **NEWDOS/80 and G-DOS**,
because it hooks their **SYS0 interrupt routine**. Under **LDOS 5.3.1** that
path is not available; there the banker is used differently — as a single
RAM-disk on **drive :4** — rather than as four parallel computers. So:

- **NEWDOS/80 or G-DOS** → SideKick, four switchable computers via SYS0.
- **LDOS 5.3.1** → one bank exposed as drive :4 (RAM disk), not SideKick.

---

## 5. 1986 original vs. 2024 SuperMem version

| | 1986 (Bernhardt banker) | 2024 (SuperMem) |
|--|--|--|
| Bank-select port | **0ECh** | **43h** |
| Code origin (`ORG`) | **3300h** | **5300h** |
| Computer-number display | — | top-right (`3c3fh`) |
| Adapter | — | Jens Günther |

---

## 6. Notable files

| File | Type | Contents |
|------|------|----------|
| [`SIDEKICK/Z80`](SIDEKICK.Z80) | Z80 source | Multi-computer banker, commented (German); 11,146 bytes. Header credits Sopp / Bernhardt / G. Schröder 1986 / Günther 2024. Extracted host copy: `SIDEKICK.Z80`. |
| `SIDEKICK/CMD` | Program | Assembled SideKick. |
| `EDTASM/CMD` | Assembler | Editor/assembler. |
| `ZEUS/CMD`, `ZEUS/TXT` | Assembler + docs | ZEUS assembler with German on-disk help. |
| `DISASSEM/CMD` | Tool | Disassembler. |
| `SUPERZAP/CMD` | Tool | Sector/file editor. |
| `DIRCHECK/CMD` | Tool | Directory check. |
| `LMOFFSET/CMD` | Tool | Loads/relocates machine-code files. |
| `ASPOOL/MAS` | Print spooler | Background printing. |
| `CHAINTST/JCL` | JCL/test | Chain-loader test (binary load block followed by English operating notes; not related to SideKick). |
| `CHAINBLD/BAS` | BASIC | Builds chain files. |

---

## Provenance

*I obtained the banker from Helmut Bernhardt and fitted it to my TRS-80 Model I —
that was quite a journey to get working. In the end I didn't use it much: I
later had a Genie IIIs, which already carried bank-switched 256K of its own.*

---

## Sources

- [Gerald Schröder, *Wie Phönix aus der Asche — Vier Computer in einem
  Schrotthaufen*, Club80 Nr. 17 (1986), pp. 8–15](https://oldcomputers-ddns.org/public/pub/rechner/eaca/common/user-clubs/club-80/hardwarespezial%28html%29/1986-club80-17%20wie%20phoenix%20aus%20der%20asche.htm)
- [Helmut Bernhardt, *256K RAM für Z80-Systeme*, BHV-03 (1986), pp. 5–10
  (correction: BHV 1987-2 p. 16 / 1987-3 p. 7)](https://oldcomputers-ddns.org/public/pub/rechner/eaca/common/user-clubs/club-80/hardwarespezial%28html%29/1986-bhv-03%20256k%20fuer%20z80-systeme/256k%20ram%20fuer%20z80-systeme.htm)