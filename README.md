# TRS80M1

Software, disk images, and tooling for a **TRS-80 Model I** equipped with a
**Schmidtke Elektronik HRG1-B** high-resolution graphics card.

My first "real" computer — this repository preserves its disks and the tools
used to read them.

## Hardware

The system as it ran:

- **TRS-80 Model I** with a double-density floppy controller upgrade
- **Schmidtke Elektronik HRG1-B** high-resolution graphics card
- **Four floppy drives** — two 80-track, two 40-track
- **NEWDOS/80 v2.0** (Apparat Inc.), heavily modified, including a custom
  SYS-extension scheme
- **G-DOS**, likewise modified, on some disks

## Contents

- **Disk images** — archived floppies in DMK and DSK format, spanning
  NEWDOS/80 and G-DOS volumes (35-, 40-, and 80-track; FM single-density and
  MFM double-density), plus hard-disk volumes.
- **Disk inventory** — a catalog with per-disk volume labels, dates,
  geometries, density, OS identification, and file listings.
- **Expert system** — a German rule-based expert system (originally by
  Dr. H.-J. Soll, 1987) ported to the TRS-80 Model I in 1989. BASIC source
  included.
- **Tooling** — Python utilities for parsing DMK images, decoding NEWDOS/80
  directories, identifying the OS via boot-sector signatures, and extracting
  BASIC source.

## Disk images

[Disk images (DMK) — NEWDOS](diskimages/NewDos/diskimages.md)

## Expert system

A German rule-based expert system, originally written by Dr. H.-J. Soll
(1987) and ported to the TRS-80 Model I in 1989. The reference document
covers its structure, the BASIC modules that make it up, and notes from the
extraction and porting work.

[Expert system reference](EXPERTSYSTEM_REFERENCE.md)

## Author

Egbert Schröer