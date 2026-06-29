# NEWDOS/80 variants

Documentation of the individual NEWDOS/80 V2.0 builds in this collection.

These disks all descend from **NEWDOS/80 V2.0 (Apparat Inc.)** but were modified
by different authors, who extended the LIB command set and the SYS-overlay
scheme in their own ways. Each document below is built primarily from the
**binary SYS overlays** of the disk in question (author signatures, command
tables, embedded strings), with the author's own release notes used as
corroboration rather than as the sole source.

## Documented builds

| Build | Author | Date | Source disk | Document |
|-------|--------|------|-------------|----------|
| NEWDOS/80 V2.0 + erw. LIB | Horst Weikamp (DL9YAP) | 02.03.87 | `NEWDOS80-80Track.DSK` / esnd-23 | [newdos80-weikamp-020387.md](newdos80-weikamp-020387.md) |

<!-- Add rows as further variants are verified, e.g.:
| NEWDOS/80 V2.0 Systemdiskette | H. Schuller | — | esnd-03 (image-3) | newdos80-schuller.md |
| NEWDOS/80 +10 Version 2.5 | (author tbd) | — | esnd-08 / esnd-09 | newdos80-25.md |
-->

## Method

For each build, authorship and feature claims are verified against the disk
itself before being recorded:

- **Author** is confirmed from in-binary signatures (e.g. `DL9YAP FEB. 1987`
  in SYS25, `DL9YAPDOS` installed by the SYS26 SYSGEN) rather than from prose
  alone.
- **Commands** are confirmed from the LIB name table (SYS15) and from the
  routines and strings present in the individual SYS overlays.
- **File presence** (e.g. whether a SYS29 exists) is taken from a directory
  parse of the disk image, not from the release notes.

Caveat: the SYS overlays are read at the string/structure level, not fully
disassembled. Command *presence* and embedded text are certain; exact internal
mechanics quoted from an author's notes are flagged as such where they are not
independently verified from the Z80 code.