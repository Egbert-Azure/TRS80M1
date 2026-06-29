# TRS80M1

Software, disk images, and tooling for a **TRS-80 Model I** equipped with a
**RB Electronic (Rolf Best) HRG-1B** high-resolution graphics card.

My first "real" computer — this repository preserves its disks and the tools
used to read them.

## Hardware

The system as it ran:

- **TRS-80 Model I** with a double-density floppy controller upgrade
- **RB Electronic (Rolf Best) HRG-1B** high-resolution graphics card
  (RB Electronic GmbH, Eitorf)
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
- **NEWDOS/80 variants** — per-build documentation of the modified NEWDOS/80
  disks (Weikamp 02.03.87 and others), verified from their SYS overlays.
  See [NEWDOS/80 variants](diskimages/NewDos/dos-versions/README.md).
- **Expert system** — a German rule-based expert system (originally by
  Dr. H.-J. Soll, 1987) ported to the TRS-80 Model I in 1989. BASIC source
  included.
- **Tooling** — Python utilities for parsing DMK images, decoding NEWDOS/80
  and G-DOS directories, identifying the OS via boot-sector signatures, and
  extracting files byte-for-byte. See **[trsextract](diskimages/NewDos/trsextract.md)**,
  a native, dependency-free directory lister and file extractor.
- **Emulation** — run the disks under SDLTRS on macOS. See
  [Running on macOS](#running-on-macos-sdltrs) below; the maintained launcher
  now lives in its own repository.

## Disk images

[Disk images (DMK) — NEWDOS](diskimages/diskimages.md)

## Reading and extracting disks (trsextract)

**[trsextract](diskimages/NewDos/trsextract.md)** is a native Python 3 tool
(no emulator, no Windows, no external dependencies) that lists directories and
extracts files byte-exact from NEWDOS/80 and G-DOS disk images. It
auto-detects disk geometry (sides, density, granules-per-lump) and has been
validated against authoritative TRSTools extractions across single-sided
single-density G-DOS and double-sided double-density NEWDOS disks.

```
python3 trsextract.py DISK.dmk                 # list the directory
python3 trsextract.py DISK.dmk -o OUTDIR/      # extract all files
```

See the **[trsextract documentation](diskimages/NewDos/trsextract.md)** for
full usage, supported geometries, and notes.

## NEWDOS/80 variants

These disks descend from NEWDOS/80 V2.0 (Apparat Inc.) but were extended by
different authors. Each build is documented from its own SYS overlays —
author signatures, LIB command tables, embedded strings — with release notes
used as corroboration.

[NEWDOS/80 variants](diskimages/NewDos/dos-versions/README.md)

## Running on macOS (SDLTRS)

The disks run under **SDLTRS / SDL2TRS**, a TRS-80 Model I/III/4/4P emulator
derived from Tim Mann's xtrs, maintained by Jens Günther at
<https://gitlab.com/jengun/sdltrs>. In Model I mode it emulates the HRG-1B
graphics card, which is why these disks run correctly under it.

### Maintained launcher: SDLTRS-Wrapper

The recommended way to run the disks on macOS is the **SDLTRS-Wrapper**, a
native SwiftUI launcher in its own repository:

> **https://github.com/Egbert-Azure/SDLTRS-Wrapper**

It provides a real macOS window with drag-and-drop floppy and hard-disk slots,
machine presets (including the TCS Genie IIIs), ROM and `.t8c` config
selection, and a helper that builds the current **`sdl2` branch** of SDLTRS
from source (hardware rendering, resizable window; binary named `sdl2trs`).

> **Note:** the older pre-compiled SDLTRS binary and Automator launcher
> previously kept in this repository are **no longer updated**. Use the
> SDLTRS-Wrapper repository above for the current build and launcher.

ROM images are not bundled and must be supplied separately. A `.t8c`
configuration file sets the machine type, attached disk images, and ROM path;
treat any included one as a starting point and edit it to match your own paths.

> **Drive numbering:** SDLTRS 1.1 and newer number disk drives from 0 (earlier
> versions started at 1). Older config files and `-disk` / `-hard` options
> need adjusting for this change.

## Expert system

A German rule-based expert system, originally written by Dr. H.-J. Soll
(1987) and ported to the TRS-80 Model I in 1989. The reference document
covers its structure, the BASIC modules that make it up, and notes from the
extraction and porting work.

[Expert system reference](EXPERTSYSTEM_REFERENCE.md)

## Author

Egbert Schröer