<!-- /README.md — repository root: overview, layout, how to read and run the disks -->
<!-- (c) E. Schroeer -->
# TRS80M1

Software, disk images, and tooling for a **TRS-80 Model I** equipped with a
**RB Electronic (Rolf Best) HRG-1B** high-resolution graphics card.

My first "real" computer — this repository preserves its disks and the tools
used to read them.

## Repository layout

```
TRS80M1/
├── README.md                      this file
├── LICENSE                        GPL-3.0
├── CHANGELOG.md                   notable repository changes, newest first
├── diskimages/                    disk images and their documentation
│   ├── README.md                  documentation index — start here
│   ├── Disk_Catalog.md            auto-generated catalog of all disk images
│   ├── diskimages.md              annotated walkthrough with screenshots
│   ├── images/                    screenshots for diskimages.md
│   ├── GDos/
│   │   ├── README.md              G-DOS editions index
│   │   ├── hdos.md                H-DOS 2.3c (Arnulf Sopp / The HACKTORY, 1984)
│   │   └── DMK/                   disk image and boot screenshot
│   │       ├── HDOS23c.dmk
│   │       └── hdos23c-boot.png
│   └── NewDos/
│       ├── trsextract.md          trsextract tool documentation
│       └── dos-versions/          per-build NEWDOS/80 edition docs
│           ├── README.md          variants index
│           ├── esnd-20a.md        HS-DOS (NEWDOS/80 +10 v2.5, 31.12.85)
│           ├── newdos80-weikamp-020387.md
│           └── DMK/               disk images and boot screenshots
│               ├── esnd-20a.dmk
│               ├── weikamp.dmk
│               └── weikamp-boot.png
├── software/                      programs and original work
│   ├── README.md                  software documentation index
│   ├── dta/                       DTA-Programmsystem (Schmidtke Diplomarbeit, 1984)
│   │   ├── README.md              forensic reconstruction + algorithm
│   │   └── DTA/ASS, AUSWERT/ASS … EDTASM sources, disassemblies, HRG/DUM
│   ├── expertsystem/              rule-based expert system (1989 port)
│   │   ├── README.md              reference + theory
│   │   ├── TRS80_vs_Prolog.md     inference model vs. Prolog
│   │   └── wc.bas, wbedit.bas …   BASIC sources and compiled binaries
│   ├── hrgdos/                    umlaut keyboard driver + HRGDOS (1989)
│   │   ├── README.md              software doc + Club-80 Heft 29 article (DE/EN)
│   │   └── kbdhrg.z80             binary-verified Z80 source
│   ├── scripsit/                  SCRIPSIT/SP — German Scripsit modification (1988)
│   │   ├── README.md              subject index
│   │   ├── SCRIPSIT.TXT                the 1988 manual (original Scripsit document)
│   │   ├── scripsit-sp-anleitung.md    manual, transcribed (DE)
│   │   ├── scripsit-sp-manual-en.md    manual, translated (EN)
│   │   ├── scripsit-sp-artikel.md      article (DE)
│   │   ├── scripsit-sp-article-en.md   article (EN)
│   │   ├── scripsit-provenance.md      what is Lindley's, what is mine
│   │   ├── scripsit-sp-patch-analysis.md   Layer A: the file patch
│   │   └── wp-cmd-analysis.md          Layer B: the RAM patcher
│   └── sidekick/                  four-computer banker (Schröder 1986)
│       ├── README.md              disk doc, usage, hardware model
│       ├── SIDEKICK.JV1           80-track NEWDOS/80 disk image
│       └── SIDEKICK.Z80           Z80 source (reference copy)
├── hardware/                      physical machine: build notes and boards
│   ├── README.md                  hardware documentation index
│   └── model1-tuneup-1992.md      DD controller, 256K banker, speed-up (Club 80, 1992)
└── rom/                           ROM images for the emulator
    ├── LEVEL2.ROM
    └── MODEL1.ROM
```

> The maintained macOS launcher lives in its own repository:
> **[SDLTRS-Wrapper](https://github.com/Egbert-Azure/SDLTRS-Wrapper)**.

## Hardware

The system as it ran:

- **TRS-80 Model I** with the **Expansion Interface**
- **Double-density floppy controller** upgrade
- **256K bank-switched memory** expansion (Helmut Bernhardt's banker)
- **RB Electronic (Rolf Best) HRG-1B** high-resolution graphics card
  (RB Electronic GmbH, Eitorf)
- **Four floppy drives** — two 80-track, two 40-track
- **NEWDOS/80 v2.0** (Apparat Inc.), heavily modified, including a custom
  SYS-extension scheme
- **G-DOS**, likewise modified, on some disks

The physical build — the double-density controller, the 256K banker, and the
5.3 MHz speed-up — is documented in the **[hardware section](hardware/README.md)**,
including a digitized 1992 Club 80 build article.

## Documentation

Start at the **[disk images & documentation index](diskimages/README.md)** —
the curated front door, organized by subject (DOS editions, software, original
work) and pointing to the disk inventory.

Quick links:

- **[Disk catalog](diskimages/Disk_Catalog.md)** — auto-generated index of every
  disk image (geometry, file counts, distinctive files).
- **[Annotated walkthrough](diskimages/diskimages.md)** — screenshot-by-screenshot
  tour of the disks.
- **[NEWDOS/80 variants](diskimages/NewDos/dos-versions/README.md)** — per-build
  documentation of modified NEWDOS/80 disks (Weikamp 02.03.87; HS-DOS —
  NEWDOS/80 +10 v2.5, 31.12.85, via the repaired esnd-20a), verified from
  their SYS overlays.
- **[G-DOS editions](diskimages/GDos/README.md)** — the German NEWDOS lineage
  (TCS Trommeschläger Computer GmbH); first documented edition:
  **H-DOS 2.3c**, Arnulf Sopp's 1984 zap-modification of G-DOS 2.1b
  (The HACKTORY), disk imaged by Fritz Chwolka.
- **[Software](software/README.md)** — the author's programs, German ports, and
  reverse-engineered subsystems: the DTA-Programmsystem (1984 Diplomarbeit
  reconstruction), the rule-based expert system (1989 port), HRGDOS/KBDHRG for
  the HRG-1B (1989), and Schröder's four-computer SideKick banker (1986).
- **[Hardware](hardware/README.md)** — the physical Model I build: double-density
  controller, 256K bank-switch board, and 5.3 MHz speed-up, with a digitized
  1992 Club 80 build article (German + English) and the RB-Elektronik / HRG-1B
  attribution.
- **[Changelog](CHANGELOG.md)** — notable repository changes, newest first.

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

## Author

Egbert Schroeer