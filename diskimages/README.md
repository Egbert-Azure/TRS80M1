<!-- /diskimages/README.md — documentation index: routes to inventory, DOS editions, software, original work -->
<!-- (c) E. Schroeer -->
# TRS-80 Model I — Disk Images & Documentation

This folder holds the disk images and everything written about them. It is the front
door for two different questions:

- **"What disks exist?"** → the inventory (every `esnd-NN`, listed once).
- **"What is worth understanding?"** → the subjects (DOS editions, programs, original
  work), each of which may span several disks or share one.

A disk is not a subject. A disk lands in the inventory automatically; it only earns a
subject page if it introduces something worth documenting — a new edition, a program, or
a notable disk-level story. Subject pages cite the `esnd-NN` inventory id they come from
rather than re-listing the disk.

---

## Inventory — what disks exist

- **[Disk catalog](Disk_Catalog.md)** — auto-generated index of every disk image
  (geometry, file counts, distinctive files). Machine truth; do not hand-edit.
- **[Annotated walkthrough](diskimages.md)** — narrative, screenshot-by-screenshot tour.

## DOS editions
Modified NEWDOS/80 and G-DOS builds, each verified from its own SYS overlays.

- **[NEWDOS/80 variants](NewDos/dos-versions/README.md)** — index of per-edition
  documents: Weikamp 02.03.87 and [HS-DOS](NewDos/dos-versions/esnd-20a.md)
  (NEWDOS/80 +10 v2.5, 31.12.85, via the repaired esnd-20a).
- **[G-DOS editions](GDos/README.md)** — the German NEWDOS lineage (TCS); first
  documented edition: [H-DOS 2.3c](GDos/hdos.md), Arnulf Sopp's 1984
  zap-modification of G-DOS 2.1b (The HACKTORY), disk imaged by Fritz Chwolka.

## Software & subsystems
Individual programs and drivers, documented where they span disks or warrant detail.

- **[SideKick](../software/sidekick/README.md)** — four-computer memory banker
  (Gerald Schröder / Helmut Bernhardt 1986; SuperMem port by Jens Günther 2024).
- *(ACCEL3 toolchain & editors — planned)*

## Original work
Software written or ported by the collection's author.

- **[Educational expert system](../software/expertsystem/README.md)** —
  rule-based backward-chaining inference engine, ported and extended for the Model I
  (1989–1990); disk esnd-23.
- **[HRGDOS / KBDHRG](../software/hrgdos/README.md)** — umlaut-capable keyboard
  driver for the HRG-1B (1989), paired with the patched RB Electronic HRG
  super-driver; Z80 source binary-verified against Club-80 Heft 29, Listing 1.

## Tooling
- **[trsextract](NewDos/trsextract.md)** — native Python 3 directory lister and
  byte-exact file extractor for NEWDOS/80 and G-DOS images.
- **SDLTRS-Wrapper** — macOS launcher, in its own repo:
  <https://github.com/Egbert-Azure/SDLTRS-Wrapper>

---

## How these fit together

- **Inventory** answers *"what disks do I have?"* — every `esnd-NN`, once.
- **Subjects** (DOS editions / Software / Original work) answer
  *"what is worth understanding?"* Each links *down* to the inventory rows it came from.
- **Tooling** is how the disks are read and run.

When a new disk arrives it appears in the catalog automatically. It earns a page in one
of the subject sections above only if it introduces a new edition, a program worth
documenting, or a notable disk-level story.