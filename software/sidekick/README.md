<!-- /software/sidekick/README.md — SideKick multi-computer banker disk -->
<!-- (c) E. Schroeer -->
# Disk SIDEKICK — NEWDOS/80 V2.0 (Apparat) with SideKick multi-computer banker

**Operating system:** NEWDOS/80 V2.0 — appears to be original Apparat Inc. stock
**Geometry:** 80-track, single-sided, single density (JV1, 204,800 bytes)
**Directory:** Track 17, 23 file entries, 56 free granules (per `DIR` under SDLTRS)
**Status:** Good. The on-disk SideKick assembler source is complete and clean.

**Files here:** [`SIDEKICK.JV1`](SIDEKICK.JV1) (disk image) ·
[`SIDEKICK.SRC`](SIDEKICK.Z80) (Z80 source, reference copy extracted from the disk)

*Sources: the `SIDEKICK/SRC` Z80 source; Gerald Schröder's original article and
listing in Club80 Nr. 17 (1986), pp. 8–15; Helmut Bernhardt's banker hardware
in BHV-03 (1986), pp. 5–10; the disk directory under SDLTRS; and the JV1 byte
image. Statements about authorship and mechanism are read from these primary
sources, not inferred.*

> **Note on extraction:** early trsextract runs returned zero-filled copies of
> `CHAINTST/JCL` and `NWD80V2/XLF` on this disk — the disk carries both live
> (attr `0x10`) and superseded (attr `0x00`) directory slots for those names,
> and the dead slots were being read. This is a trsextract directory-liveness
> issue, tracked separately; the disk itself is intact.

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

The geometry that shapes SideKick:

- The 64K address space splits into two 32K halves. The **upper half
  (8000h–FFFFh) is fixed and always visible — the Common area.** Interrupt
  routines, the stack, and anything that must always be reachable live here.
- The **lower half (0000h–7FFFh) is banked** — several parallel 32K blocks,
  selected by writing a bank number to the latch port.
- RESET forces bank 0, so initialization always starts from a known state.
- Bank 1 would overlap the Common block, so the logic redirects it to the
  highest bank; the top bank (7 at 256K, 15 at 512K, 31 at 1024K) is therefore
  unusable.

This is why SideKick can only **swap the lower halves** of the computers
physically, while the **upper halves are merely bank-switched** — the Common
must stay put.

---

## 3. How to use it

1. The banker hardware must be installed (256K + Bernhardt's banker in 1986;
   the Alpha Technology SuperMem in the 2024 version).
2. Run `SIDEKICK/CMD` once from DOS Ready. It installs itself into the
   **GDOS/NEWDOS SYS0 interrupt routine**, copies the computer halves into the
   banks, and returns to DOS Ready.
3. Switch between the four computers by holding **SHIFT + Down-Arrow + a digit**
   together:
   - SHIFT + Down-Arrow + **0** → computer 0
   - SHIFT + Down-Arrow + **1** → computer 1
   - SHIFT + Down-Arrow + **2** → computer 2
   - SHIFT + Down-Arrow + **3** → computer 3

   Each computer can run its own program.

In the 2024 version the active computer's number is shown in the top-right
corner of the screen (`LD (3c3fh),A`).

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
| [`SIDEKICK/SRC`](SIDEKICK.SRC) | Z80 source | Multi-computer banker, commented (German); 11,146 bytes. Header credits Sopp / Bernhardt / G. Schröder 1986 / Günther 2024. |
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

## Sources

- Gerald Schröder, *Wie Phönix aus der Asche — Vier Computer in einem
  Schrotthaufen*, Club80 Nr. 17 (1986), pp. 8–15.
- Helmut Bernhardt, *256K RAM für Z80-Systeme*, BHV-03 (1986), pp. 5–10
  (correction: BHV 1987-2 p. 16 / 1987-3 p. 7).