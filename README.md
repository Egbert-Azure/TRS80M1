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
  and G-DOS directories, identifying the OS via boot-sector signatures, and
  extracting files byte-for-byte. See **[trsextract](diskimages/NewDos/trsextract.md)**,
  a native, dependency-free directory lister and file extractor.
- **Emulator** — a compiled macOS build of SDLTRS, plus a configuration file
  to run the disks under emulation.

## Disk images

[Disk images (DMK) — NEWDOS](diskimages/NewDos/diskimages.md)

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

## Running on macOS (SDLTRS)

The disks run under **SDLTRS**, a TRS-80 Model I/III/4/4P emulator derived
from Tim Mann's xtrs. A compiled macOS build is included in this repository,
so there is no need to build it yourself. ROM images are not bundled with the
emulator and must be supplied separately.

A configuration file (`.t8c`) sets the machine type, attached disk images,
and ROM path. **This file is a starting point — edit it to match your own
paths and the disks you want mounted before running.**

### Launch with Automator

An Automator application wraps the launch so the emulator can be started by
double-clicking instead of from the command line:

1. Create a new **Application** in Automator.
2. Add a **Run Shell Script** action.
3. Point it at the SDLTRS binary and the config file, for example:

   ```bash
   /path/to/sdltrs -conf /path/to/your.t8c
   ```

4. Save as an application and double-click to run.

**Note:** SDLTRS 1.1 and newer number disk drives from 0 (earlier versions
started at 1). Older config files and `-disk` / `-hard` options need
adjusting for this change.

## Expert system

A German rule-based expert system, originally written by Dr. H.-J. Soll
(1987) and ported to the TRS-80 Model I in 1989. The reference document
covers its structure, the BASIC modules that make it up, and notes from the
extraction and porting work.

[Expert system reference](EXPERTSYSTEM_REFERENCE.md)

## Author

Egbert Schröer