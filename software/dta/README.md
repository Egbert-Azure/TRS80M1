<!-- /software/dta/README.md — DTA-Programmsystem (Gerd Schmidtke, FH Münster, 1984) -->
<!-- (c) E. Schroeer -->
# DTA-Programmsystem — Differential-Thermo-Analyse (1984)

A measurement, evaluation, and plotting system for **Differential Thermal Analysis
(Differentialthermoanalyse)** on the TRS-80 Model I, written in Z80 assembler.

**Author:** Gerd Schmidtke, Dipl.-Ing. thesis (Diplomarbeit), FH Münster, 1984
**Copyright strings (binary-verified):**
- `'<C> 1984  by Gerd Schmidtke, FH Muenster'` (DTA.ASS line 590)
- `'* * *   Differential - Thermo - Analyse   * * *'` (DTA.ASS line 610)

## Historical context

This source code and program are close to my heart, even though I didn't write
them. The memories run deep, because back in those days the TRS-80 M1
represented a first real capability to measure lab data, store it, and then
reuse it — to check, control, and optimize.

And there is more. Working as a chemist in industry, I built numerous
process-automation systems in my labs, work that later led to one of the first
client-server-based LIMS systems, to name just one example. Why am I telling
this here? At CWH (Chemische Werke Hüls — the line runs IG Farben → CWH →
Hüls AG → Degussa-Hüls → today's Evonik Industries), two TRS-80 M1 machines
measured waste-water quality 24/7 in one of the labs, the CWH Umweltlabor —
until the early 1990s. Around the clock, for more than a decade. Let that
sink in.

These machines ran NEWDOS/80 — a highly capable DOS whose open,
user-modifiable design suited unattended measurement duty in a way stock
TRSDOS did not. Seen with today's knowledge and technology, this is all the
more astonishing: a machine Tandy initially expected to sell in the low
thousands went on to sell roughly a quarter million units — and ended up doing
serious laboratory work. Bespoke lab software of this kind was almost never
preserved; this Diplomarbeit code is among the few surviving sources
documenting what was actually done with this unique computer in professional
measurement settings.

## Provenance

The TRS-80 was coupled to a DTA instrument for the thesis; the printed
Diplomarbeit is currently lost. The surviving sources below were rescued from
disk. Note: no relation to the HRG-1B manufacturer — the card is by
**RB (Rolf Best) Electronic GmbH, Eitorf**.

**Source disk:** [`esnd-40.dmk`](../../diskimages/NewDos/) — see the disk catalog
entry for the full file listing.

## What Differential Thermal Analysis is

A sample and an inert reference are heated on the same temperature program. The
instrument records the temperature difference **ΔT** between them. When the sample
undergoes a thermal transition — melting, crystallization, decomposition — it
absorbs or releases heat and ΔT deviates from zero, producing a peak in the
ΔT-vs-time curve. The **area of that peak, measured against a baseline, is
proportional to the enthalpy of the transition**. This is why the evaluation
module below is built entirely around baseline construction and peak-area
integration.

## System overview

`DTA/CMD` is the master menu. On start it loads the resident HRG graphics driver
(`HRG/DUM`), checks/initializes `FORMFILE` (the sample-header form), then offers:

| Menu item | Program | Status |
|-----------|---------|--------|
| 1 — Messwerterfassung | `AUFNAHME/CMD` | **missing** — not on esnd-40, not in catalog |
| 2 — Messwertauswertung | `AUSWERT/CMD` | binary missing; **full source survives** (`AUSWERT/ASS`) |
| 3 — Messkurven Plotten | `PLOT/CMD` | **missing** |
| 4 — Formfile neu initialisieren | (built into DTA/CMD) | present |
| 5 — Programmsystem verlassen | — | — |

Data files: `FORMFILE` (1024-byte header form), `INHALT` (data index, **missing**),
measurement files named by the user (`Dateiname : ......../...`).

Measurement values are stored as **single bytes** (verified: `LD A,(IX+0)` reads
per sample in `GRAPH2`/`SUMV1`) — i.e. 8-bit ΔT samples, implying an 8-bit ADC in
the missing acquisition module (inference; the converter itself is not in the
surviving code).

## The evaluation algorithm (AUSWERT/ASS, binary-verified)

The peak-area computation (`FLAECH` → `BASIS` → `FNTFL1`) works as follows:

1. **Display & scaling.** The curve is drawn on the HRG (384×192) via the driver
   line routine at FC04H. Autoscaling: `FAKT1 = YFAK/(max−min)`,
   `FAKT2 = XFAK/(x_max−x_min)`; screen Y = 128 − (y−min)·FAKT1 (`DEHN`,
   `MINMAX`, `GRAPH2`).
2. **Boundary selection.** The user moves an inverted 14-pixel cursor with the
   arrow keys to mark first the left, then the right peak boundary (`CURSER`),
   with interval validation ("Intervall zu klein").
3. **Baseline.** A straight line is drawn between the curve values at the two
   boundaries; `FLBAS` = the trapezoid area beneath it:
   Δx·(y₁ + (y₂−y₁)/2). X values are pre-scaled by 0.01 (`FAKT4`) to keep
   higher powers within floating-point range.
4. **Piecewise least-squares cubic fit.** The interval is split into chunks of
   8–150 samples (`BASUP0/2/3` adjusts the chunk count until this holds). Per
   chunk, the normal-equation sums Σxᵏ and Σy·xᵏ are accumulated in **double
   precision** (`SUMV1`/`SUM`/`XSUM`/`YSUM`) and the 4×4 system is solved by
   matrix inversion (`INVERT`, with `UP2` as 4×4 matrix multiply) — four
   coefficients, i.e. a cubic. (The source comment says "Ausgleichsparabeln";
   the matrix dimensions show it is actually a cubic fit.)
5. **Analytic integration.** `FNTFL` forms the antiderivative
   f₄x⁴/4 + f₃x³/3 + f₂x²/2 + f₁x — the stored constants `FAKT5..7` = 1/4, 1/3,
   1/2 are these divisors — evaluates it at both chunk ends (Horner scheme,
   `KUBFNT`), and accumulates the differences into `FLPEEK` (double precision).
6. **Result.** Peakfläche = `FLPEEK` − `FLBAS`, converted to ASCII and shown;
   optional printer output with "Drucker nicht bereit" handling, and refusal
   while the plot program is resident.

Fitting a smooth polynomial before integrating suppresses quantization/ADC noise
instead of integrating it — a sound numerical design given 8-bit samples, and
notably careful work for 1984 Z80 assembler. Floating point uses the Level II
ROM routines (single 4-byte / double 8-byte, type flag at 40AFH, WRA1 at 4121H);
only the matrix algebra is hand-rolled.

## Surviving files

| File | Type | Content (binary-verified) |
|------|------|---------------------------|
| `DTA/ASS` | EDTASM source | Master menu, `ORG 5200H`. FCBs for HRG/DUM, FORMFILE, INHALT, AUFNAHME/CMD, AUSWERT/CMD, PLOT/CMD. Full-screen form editor for FORMFILE (arrow keys, SHIFT-arrows = delete/insert char, CLEAR = save). Buffers: FE00H (Inhalt), FF00H (Messwerte), 7000H (Messwertspeicher). |
| `AUSWERT/ASS` | EDTASM source, 1779 lines, fully commented | Evaluation module, `ORG 5832H`. See algorithm above. |
| `HRG/DUM` | /CMD load file, 780 bytes | Memory dump of a resident HRG BASIC-extension driver, load range FB10H–FDFFH, entry 0000H (dump, no autostart). Embedded copyright: **`(C) 1983 Dieter Bolz`**. Drives **ports 00H–05H** — the RB Electronic HRG-1B port map. Intercepts BASIC tokens (82H, 83H, 84H, 9CH, A2H, A6H, A9H, B8H, C6H) via the 4004H vector. **Not** derived from HRG/CMD: byte comparison shows 746 of 752 overlapping bytes differ. |
| `HRGDUM/ASS` | Disassembly | Disassembly of HRG/DUM, label-free (addresses literal). **Byte-verified** against HRG/DUM on the opening instruction sequence at FB10H (exact match); full-length diff pending. |
| `DTAST/ASS` | Disassembly fragment | Truncated copy of the same disassembly (first ~34 lines). |
| `CODE/ASS` | Disassembly fragment | Middle section of the same disassembly; contains the comment `;LAUT LISTING: LD B,D` — the disassembly was cross-checked against a **printed listing**, presumably from the Diplomarbeit. |
| `FORMFILE` | Data, 1024 bytes | **Verbatim dump of the Model I video RAM (3C00H–3FFFH)** used as an editable screen mask — the `SAVE` routine in DTA/ASS writes the screen byte-by-byte (LRECL=1) into this file and reloads it on start. Begins `name` + blanks. |

Also on esnd-40 but not yet pulled into this folder: `TEST/ASS`, `WECKER/ASS`,
`TESTTEXT/CMD`.

## Technical notes

- DOS file I/O uses the NEWDOS/80 entry points 4420H (open/create), 4424H (open
  existing), 4428H (close), 4436H (read), 4467H (print string) — consistent with
  the NEWDOS/80 system on esnd-40. Disk I/O is bracketed by `STOP`/`START1`,
  which patch the interrupt vector at 4012H (RET/JP) to disable the heartbeat
  during transfers.
- **HRG/DUM vs HRG/CMD — byte-compared, unrelated.** `HRG/CMD` (9,253 bytes,
  DB00H–FF24H, entry EB00H) also occupies FB10H–FDFFH, but with completely
  different code there: **746 of 752 overlapping bytes differ**. Both drivers
  address ports 00H–05H (HRG-1B), but HRG/DUM is a third program — Dieter
  Bolz's compact 1983 BASIC-extension driver — not a variant of HRG/CMD.

## How the pieces connect

```
                RB Electronic HRG-1B  (I/O ports 00H-05H)
                     ▲                          ▲
                     │ drives                   │ drives
        HRG/CMD  (9.2K driver,        Dieter Bolz driver, (C) 1983
        DB00-FF24, entry EB00)        resident at FB10-FDFF
        separate lineage,                       │
        unrelated code                          │ memory dump (Schmidtke)
                                                ▼
                                            HRG/DUM  (752 bytes)
                                                │
                                                │ disassembled
                                                ▼
                                           HRGDUM/ASS ◄── cross-checked against
                                                │          printed listing
                                                │          (";LAUT LISTING" in
                                                │          CODE/ASS; DTAST/ASS
                                                │          is a fragment copy)
                                                │ yields internal entry points
                                                ▼
                                  AUSWERT/ASS:  LINE1 EQU 0FC04H,
                                  coordinate cells FD7BH-FD81H
                                  (direct calls, BASIC bypassed)
                                                │
                                                ▼
              DTA-Programmsystem (DTA/CMD menu → AUFNAHME* / AUSWERT / PLOT*)
                                                │
                          FORMFILE = video-RAM screen mask (3C00H dump)
                                                │ same technique, 1984
                                                ▼
                          maske1/dum, maske2/dum — expert system, 1991
                                        (* = binary lost)
```
- **Working method (binary-verified):** the resident Bolz driver was dumped
  from memory (`HRG/DUM`), disassembled (`HRGDUM/ASS`, cross-checked against a
  printed listing per the `;LAUT LISTING` comments in `CODE/ASS`), and its
  internal routines were then reused directly from assembler — `AUSWERT`
  declares `LINE1 EQU 0FC04H` and writes coordinates straight into the driver's
  cells at FD7BH–FD81H, bypassing the BASIC token interface entirely. Dump →
  disassemble → call internals: locating usable entry points in source-less
  binaries, the same pattern seen elsewhere in this archive.
- **Screen-mask technique:** `FORMFILE` is a pre-rendered full-screen form
  saved as a raw video-RAM dump and reloaded in one pass — conceptually
  identical to `maske1/dum`/`maske2/dum` in the
  [expert system](../expertsystem/) (1991), which draws forms once with
  `maskgen.bas` and reloads them via `CMD"load"`. The DTA system (1984) is the
  earlier of the two occurrences in this archive; here the mask is additionally
  editable in place via the built-in full-screen editor.

## Open items

- Locate `AUFNAHME/CMD` (or source) on remaining un-imaged disks — it contains
  the instrument/ADC interface and would document the hardware coupling.
- Locate `PLOT/CMD`, `AUSWERT/CMD`, `INHALT`.
- Identify **Dieter Bolz** and the published form of his 1983 driver. Lead: an
  HRG-1B cassette driver (`grl2.cas`, loaded via SYSTEM) is documented in a
  restoration thread on forum.classic-computing.de — obtain and byte-compare
  against HRG/DUM. Possible channels: Jens Günther, the Genie archive at
  oldcomputers.dyndns.org (hosts HRG-1B documentation), RB Electronic material.
- Identify the origin/author of `HRG/CMD` (the large 9.2K driver) — now known
  to be a separate lineage from HRG/DUM.
- Complete the full-length instruction diff of `HRGDUM/ASS` against `HRG/DUM`
  (opening sequence already verified).
- Diplomarbeit recovery: 1984 FH Diplomarbeiten were rarely library-cataloged;
  the responsible Fachbereich (Steinfurt) is the more promising contact than the
  Hochschulbibliothek.