<!-- /software/README.md — software documentation index -->
<!-- (c) Egbert Schroeer, 2026 -->
# Software

Documentation of the software this collection preserves: the author's own
programs, the German-language ports and adaptations, and the reverse-engineered
subsystems recovered from the disk images — as distinct from the DOS editions
(documented under [`diskimages/`](../diskimages/README.md)) and the physical
machine (documented under [`hardware/`](../hardware/README.md)).

Each subsection is organized by subject, not by disk: a program or subsystem may
span several images, and its documentation lives in one place regardless of which
disk a given file was pulled from. Statements about code behavior, authorship, and
format are read from the actual bytes — sources, disassemblies, and byte images —
not inferred from surrounding prose.

## Subsystems

| Subsystem | Subject |
|-----------|---------|
| [`dta/`](dta/README.md) | **DTA-Programmsystem** — forensic reconstruction of Gerd Schmidtke's 1984 Diplomarbeit (FH Münster) Z80 assembler system for chromatographic peak evaluation. Surviving EDTASM sources decoded; the AUSWERT algorithm confirmed as piecewise least-squares cubic fitting with analytic integration; the pipeline brought back to execution under sdltrs. Includes the byte-level separation of the two HRG drivers (`HRG/DUM`, Dieter Bolz 1983, vs. `HRG/CMD`). |
| [`expertsystem/`](expertsystem/README.md) | **Expert system** — the author's 1989/1991 TRS-80 Model I (and Genie III) port of Hans-Jürgen Soll's rule-based BASIC expert-system shell: backward chaining, manual recursion stack, three-valued logic, constraint propagation, and an explainable-inference trace, with the engine/editor split and German-umlaut handling documented against the book's structure. |
| [`hrgdos/`](hrgdos/README.md) | **HRG-DOS** — the author's HRG super-driver work for the RB Electronic HRG-1B card, with the print listings of the driver patches (byline `(c) by E.Schröer '89`) transcribed. Listings 2/3 transcribed from print but not yet binary-verified against `HRGDOS/CMD`. |
| [`sidekick/`](sidekick/README.md) | **SideKick** — Gerald Schröder's 1986 multi-computer banker (four complete machine states held in bank-switched memory, hotkey-switched), with the complete commented `SIDEKICK/Z80` source, the banker-hardware dependency, and Jens Günther's 2024 SuperMem adaptation. Depends on Helmut Bernhardt's banker documented in [`hardware/`](../hardware/model1-tuneup-1992.md). |

## Related software notes elsewhere

- **NEWDOS/80 editions and builds** (Apparat stock, +10 v2.5, Weikamp/DL9YAP,
  G-DOS) are documented as DOS editions under
  [`diskimages/NewDos/`](../diskimages/NewDos/README.md), not here — they are
  operating systems rather than application software.
- **HRG driver lineage.** The two distinct HRG-1B drivers (`HRG/CMD`, 9.2K,
  separate lineage; and `HRG/DUM`, the 752-byte Bolz 1983 BASIC-extension driver)
  are byte-compared in [`dta/`](dta/README.md); the HRG-DOS super-driver is a
  third, later strand under [`hrgdos/`](hrgdos/README.md).
- The **`trsextract`** toolchain that produced the directory listings and
  byte-exact extractions these subsections rely on is documented at
  [`diskimages/NewDos/trsextract.md`](../diskimages/NewDos/trsextract.md).