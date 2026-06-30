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
- **[Disk inventory](Disk_Inventory.md)** — curated companion: provenance, German
  annotations, damaged-disk and duplicate notes.
- **[Annotated walkthrough](diskimages.md)** — narrative, screenshot-by-screenshot tour.

## DOS editions
Modified NEWDOS/80 and G-DOS builds, each verified from its own SYS overlays.

- **[NEWDOS/80 variants](NewDos/dos-versions/README.md)** — index of per-edition
  documents (Weikamp 02.03.87, and others as verified).
- *(G-DOS editions — planned)*

## Software & subsystems
Individual programs and drivers, documented where they span disks or warrant detail.

- *(HRG-1B / HRG/CMD graphics driver — planned; source disks incl. esnd-20a)*
- *(ACCEL3 toolchain & editors — planned)*

## Original work
Software written or ported by the collection's author.

- **[Educational expert system](../TRS80%20_Expertsystem/EXPERTSYSTEM_REFERENCE.md)** —
  rule-based backward-chaining inference engine, ported and extended for the Model I
  (1989–1990).

## Notable disks
Disks whose individual story is worth a page beyond the inventory row — repairs,
reconstructions, unusual payloads.

- *(esnd-20a — repaired esnd-20; HRG/CMD + ACCEL3 payload — planned)*

## Tooling
- **[trsextract](NewDos/trsextract.md)** — native Python 3 directory lister and
  byte-exact file extractor for NEWDOS/80 and G-DOS images.
- **SDLTRS-Wrapper** — macOS launcher, in its own repo:
  <https://github.com/Egbert-Azure/SDLTRS-Wrapper>

---

## How these fit together

- **Inventory** answers *"what disks do I have?"* — every `esnd-NN`, once.
- **Subjects** (DOS editions / Software / Original work / Notable disks) answer
  *"what is worth understanding?"* Each links *down* to the inventory rows it came from.
- **Tooling** is how the disks are read and run.

When a new disk arrives it appears in the catalog automatically. It earns a page in one
of the subject sections above only if it introduces a new edition, a program worth
documenting, or a notable disk-level story.
