<!-- /CHANGELOG.md — running log of notable repository changes -->
<!-- (c) E. Schroeer -->
# Changelog

Notable changes to this repository. This is an archival/documentation project, so
entries are dated rather than versioned. Newest first.

The format loosely follows [Keep a Changelog](https://keepachangelog.com/).
Categories: **Added**, **Changed**, **Fixed**, **Removed**, **Documented**.

## 2026-07-01

### Added
- New top-level `hardware/` section with an index (`hardware/README.md`) for the
  physical TRS-80 Model I build documentation, following the repository's
  subject-index convention.
- `hardware/model1-tuneup-1992.md` — digitized primary source: *TRS-80 Model I
  Tuneup .. Hardware* (Bernhardt / Schröer / Ruschinski, Club 80 INFO 38, Dez.
  1992). Full German transcription with English translation, covering the WD2793
  double-density board, the 256K address decoder + banker (incl. A15-inversion
  banking for NewDos vs CP/M), the 5.3 MHz speed-up, and the CP/M 3.0 boot-disk
  geometry. Includes the two hand-drawn schematics as scans
  (`hardware/images/abb-1-rom-patch.png`, `abb-2-refresh-mux.png`) with
  conservative netlist-style transcriptions marked as reading aids, and a dated
  2026 editorial note recording that the build was later completed and the
  WD2793 ran. Cross-linked from `software/sidekick/README.md`; section 6
  corroborates the HRG-1B → RB (Rolf Best) Electronic attribution. (Historical
  byline uses "Schröer" with umlaut; repo copyright line uses "Schroeer".)

### Fixed
- `software/sidekick/README.md` — corrected the banker memory-map description.
  The earlier text had it backwards ("upper half fixed, lower half banked"). On
  the TRS-80 the low ROM/I/O/video region (0000h–3FFFh) is the unbankable common
  area; Bernhardt's banker switches the **upper 32K (8000h–FFFFh)** via A15
  inversion. Correction from Jens Günther, corroborated by the Club-80 *256K RAM
  für Z80-Systeme* note.

### Changed
- Root `README.md` — added `hardware/` to the repository-layout tree and a
  **Hardware** quick-link in the Documentation section; attributed the 256K
  bank-switched memory to Helmut Bernhardt's banker (previously unattributed),
  now that the 1992 article establishes it.

### Documented
- `software/sidekick/README.md` — described what the SuperMem source actually
  does, read from `SIDEKICK.Z80`: `copy` stages 3000h–7FFFh into the high bank
  window B000h–FFFFh; the live switch `tausch` rotates only a 512-byte window
  (7E00h–7FFFh) between banks through a buffer at A000h, rather than bulk-swapping
  a 32K half.
- `software/sidekick/README.md` — SDLTRS operating notes (from Jens Günther):
  switch keys: real TRS-80 = **SHIFT + Down-Arrow** + digit (per the `schalt`
  matrix scan); on SDLTRS the Down-Arrow position maps to **End** (PC) or
  **Fn + Right-Arrow** (macOS) + digit. Also: reduce **Keystretch** (Alt-O,
  ~100) if a digit prints instead of switching, and set **SuperMem to 256 KB**
  (Alt-E) before starting SIDEKICK.
  Switching verified on macOS; added two SDLTRS screenshots showing the active
  computer number (`3c3fh`) top-right.

## 2026-06-30

### Added
- Repository-layout tree and a `Documentation` section to the root `README.md`.
- Documentation index at `diskimages/README.md`, organized by subject (inventory,
  DOS editions, software, original work, notable disks).
- Path-style purpose comments at the top of each `README.md` so every index states
  its own location and role.
- Expansion Interface, double-density floppy controller, and 256K bank-switched
  memory to the hardware list in the root `README.md`.

### Changed
- Moved the expert-system documentation and program files from the repository root
  into `software/expertsystem/` (`README.md`, `expertsystem_overview.png`,
  `recursion_stack_trace.png`, `TRS80_vs_Prolog.md`, plus the BASIC sources and
  compiled binaries: `wc.bas`/`WC/CMD`, `wbedit.bas`, `maskgen.bas`, `testen`, etc.);
  linked from the root `README.md`.
- `diskimages/NewDos/dos-versions/README.md` reduced to a NEWDOS/80 variants index
  (one row per documented edition), removing a duplicated copy of the top-level
  documentation index.
- Moved disk screenshots into `diskimages/images/` and updated all image references
  in `diskimages.md` accordingly.

### Removed
- `TRS80_prog_src/` (upstream Tim Mann xtrs sources and Windows build artifacts;
  not part of this collection's preservation scope).
- Duplicate root-level ROM copies and stray Windows tooling leftovers.

### Documented
- `esnd-20a` — repaired `esnd-20`: NEWDOS/80 +10 v2.5 (31.12.85) carrying the
  RB Electronic HRG-1B driver (`HRG/CMD`) and the ACCEL3 toolchain, with the
  `H/JCL` ACCEL3 chain and the Z-EDIT and GREDIT editors; DEMOHRG screen text
  transcribed (German original + English translation).

## Earlier

- Expert system — structure and content of the ported German rule-based expert
  system documented (now at `software/expertsystem/`).
- `newdos80-weikamp-020387.md` — NEWDOS/80 Weikamp (DL9YAP) build documented from
  its SYS overlays.
- `diskimages/Disk_Catalog.md` — auto-generated disk catalog established.
- `trsextract` — native Python directory lister and byte-exact extractor for
  NEWDOS/80 and G-DOS images; documentation at `diskimages/NewDos/trsextract.md`.
- Initial repository: disk images, ROM images, and emulator notes.