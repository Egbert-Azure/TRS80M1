## 2026-07-05

### Documented
- `software/dta/README.md` — **Runtime reconstruction (2026)**: the DTA
  evaluation pipeline runs again in sdltrs. Original DTA/CMD, restored
  FORMFILE (byte-identical to the independently preserved copy) and resident
  HRG/DUM; clearly-labeled modern additions: zmac rebuild of AUSWERT/CMD
  (runtime-validated), synthetic INHALT and PEAK measurement files. Work
  disk `dta-work3.dsk`; PDRIVE TC=40,SPT=10,TSR=0,GPL=2,DDSL=17,DDGA=2.
  Screenshots: menu, curve, Peakfläche result.
- INHALT record format decoded from the AUSWERT parser: 0DH-terminated
  filename list, 03H filler skipped, `:d` suffix terminated at the colon
  for the FCB, EOF rewind via 443FH (down-arrow cycles the list).
- Measurement-file format: 8-bit ΔT samples in the first half of the file,
  sample count = size/2 (runtime-confirmed); second half unknown (AUFNAHME
  would tell).
- Peakfläche: full Flaechenberechnung executed (boundary cursors, chord
  baseline, piecewise cubic fit, signed result, printer option). Strong
  boundary sensitivity documented (3.19 / 0.90 / −1.67 on identical data) —
  authentic to manual-baseline DTA practice. Coordinate space of the
  absolute value still open; linearity test prepared on dta-work3.dsk.
- HRG clear: source clears before every plot (GRAPH: CLS + HRGCLS →
  0FBCFH, verified in the dump as a 48×256 = 12,288-write RAM wipe); in
  the 2026 environment the routine executes without visible effect, plots
  overlay. 1984 hardware behaviour undeterminable from surviving material.

### Changed
- System-overview table: three-way status made explicit — AUFNAHME/CMD
  original lost (outputs synthesized, program NOT reconstructed);
  AUSWERT/CMD original binary lost, source-rebuild runtime-validated;
  PLOT/CMD lost, nothing reconstructed.
- TEST/ASS, WECKER/ASS, TESTTEXT/CMD, BASIC/CMD explicitly marked as
  unrelated disk residents, not DTA material. WECKER/ASS content is
  unrecoverable (granules reallocated to HRG/DUM; only the name survives).
- Open items: INHALT/AUSWERT items superseded by the reconstruction; new
  item: Peakfläche linearity test (pending).