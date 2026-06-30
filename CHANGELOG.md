<!-- /CHANGELOG.md — running log of notable repository changes -->
<!-- (c) E. Schroeer -->
# Changelog

Notable changes to this repository. This is an archival/documentation project, so
entries are dated rather than versioned. Newest first.

The format loosely follows [Keep a Changelog](https://keepachangelog.com/).
Categories: **Added**, **Changed**, **Fixed**, **Removed**, **Documented**.

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

- `TRS80_Expertsystem/` — structure and content of the ported German rule-based
  expert system documented in `EXPERTSYSTEM_REFERENCE.md`.
- `newdos80-weikamp-020387.md` — NEWDOS/80 Weikamp (DL9YAP) build documented from
  its SYS overlays.
- `diskimages/Disk_Catalog.md` — auto-generated disk catalog established.
- `trsextract` — native Python directory lister and byte-exact extractor for
  NEWDOS/80 and G-DOS images; documentation at `diskimages/NewDos/trsextract.md`.
- Initial repository: disk images, ROM images, and emulator notes.
