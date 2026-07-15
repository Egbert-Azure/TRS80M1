<!-- /software/scripsit/README.md — subject index: Scripsit and the SCRIPSIT/SP modification -->
<!-- (c) E. Schroeer -->

# Scripsit / SCRIPSIT/SP

Radio Shack **Scripsit 1.0** (1979) and the German modification built on it in 1988.

Scripsit as shipped has no umlauts — the codes 5BH/5CH/5DH/7BH/7CH/7DH/7EH that carry
Ä Ö Ü ä ö ü ß in the German 7-bit set are either used by Scripsit itself or unreachable — and
no way to send an arbitrary control byte to the printer. The modification addresses both, in
**two independent layers**:

| layer | file | what it is |
|---|---|---|
| **A** | `SCRIPSIT/SP` | a static patch **in the program file**. Umlauts, `@p` printer escape. Runs standalone under any filename. |
| **B** | `WP/CMD` | a loader that patches Scripsit **in RAM**. New BREAK commands, cursor functions. |

**Layer B is a port of Craig A. Lindley's patch program** (*"Inside Scripsit — Part II"*,
80 Micro, October 1982), with one functional extension and three routines removed. **Layer A
owes nothing to Lindley** — he never touches the program file. The derivation is documented
rather than implied; see `scripsit-provenance.md`.

The two layers were built against each other: `SCRIPSIT/SP` ends at 7AA4H and `WP/CMD` begins
at 7AA7H; WP's 8002H hook falls through to 615DH, which in SP is the jump to the umlaut
translator.

## Index

### Primary artefact

| File | Description |
|---|---|
| [`SCRIPSIT.TXT`](./SCRIPSIT.TXT) | **The 1988 manual, byte-exact.** An original Scripsit document — TRS-80 German 7-bit encoding, Scripsit control codes, `E5` sector fill. Will not render on GitHub; that is what it is supposed to look like. The only surviving contemporaneous prose about the modification, and the source cited throughout the findings below. |
| [`scripsit-sp-anleitung.md`](./scripsit-sp-anleitung.md) | Readable transcription of the above. **Derived** — encoding mapped to UTF-8, control codes rendered, fill stripped; wording untouched. Includes the decode of the seventeen `@p` escapes the manual uses on itself. |

### Article

| File | Description |
|---|---|
| [`scripsit-sp-artikel.md`](./scripsit-sp-artikel.md) | **Article (DE)** — the account of the modification: what came from Lindley, what did not, and the feature list separated by origin. A 2026 rewrite; the 1988 original (SONDERINFO 27.5) is lost. |
| [`scripsit-sp-article-en.md`](./scripsit-sp-article-en.md) | **Article (EN)** — English version of the above. |

### Findings

| File | Description |
|---|---|
| [`scripsit-provenance.md`](./scripsit-provenance.md) | **What is Lindley's and what is mine.** Hook-by-hook comparison, the `CP 20H` → `CP 0FFH` extension, the assembly verification of `wpand.scr`, and a list of corrections to the two analyses below. |
| [`scripsit-sp-patch-analysis.md`](./scripsit-sp-patch-analysis.md) | **Layer A.** Every change between `SCRIPSIT/CMD` and `SCRIPSIT/SP`, derived by structural diff. The FFACH umlaut translator, the FF6CH printer driver and its `RLD` escape, the FFE2→FFF1 translate table, the marker-glyph relocation. |
| [`wp-cmd-analysis.md`](./wp-cmd-analysis.md) | **Layer B.** Load map, entry at 7B19H, the six hooks, the thirteen text-buffer stores, both dispatch tables, and the NEWDOS/80 geometry used to recover the file. |

**Reading order:** the article for the account; then provenance — it corrects several claims in
the two analyses and is dated later — then Layer A, then Layer B.

### Not in the repository

Two artefacts exist but are not committed here. Both would need a home decision first:

- `scripsit-sp-patch.asm` — reconstructed assembly source for Layer A. **Not the original
  source**; a byte-faithful reconstruction with modern labels, written before several later
  corrections and not re-audited against them.
- `edtasm-z80.py` — two-pass Z80 assembler for the EDTASM subset, written to verify `wpand.scr`
  against Lindley's binary. A tool, so arguably it belongs with `trsextract` rather than here.

## Provenance of the artefacts

- `SCRIPSIT/CMD`, `SCRIPSIT/SP` — supplied directly; both verified **byte-identical** to the
  copies on `esnd-04.dmk`.
- `WP/CMD` — re-extracted from `esnd-04.dmk` (track 10 / side 1 / sectors 13–16). An earlier
  extraction returned 883 bytes of `E5` fill; the disk was never at fault. See
  `wp-cmd-analysis.md` §8.
- `wp.cmd`, `wp7.cmd` — Lindley's binaries, third-party.
- `wpand.scr` — an EDTASM source file carrying Lindley's Listing One. Origin unresolved.
- `SCRIPSIT/TXT` — the 1988 manual. **Not on `esnd-04.dmk`**; supplied directly, source disk
  **not established**. `esnd-05.dmk` is the obvious candidate and is unexamined. Unlike the
  article, this document survived, and it is what fixes several findings: the `1-255` printer
  range, the absence of any underlining, and the character-count warning.
- The **1988 Club-80 article (SONDERINFO 27.5) is lost.** The article in this directory is a
  2026 rewrite, not a recovery of that text. Its opening section is recollection; everything
  technical is byte-derived.
- `wp.cmd` / `wp7.cmd` / `wpand.scr` are third-party or unresolved-origin material and are not
  committed here.

## Disk geometry (esnd-04)

Recorded here because it was derived in the course of this work and belongs with the evidence:

```
linear_sector = 36 + lump*10 + granule*5
  addressing : cyl*36 + side*18 + sector    (cylinder 0 = SD boot track, excluded)
  lump = 10 sectors, granule = 5 sectors, GPL = 2
  extent byte0 = lump ; byte1 = (granule << 5) | (count - 1)
  directory   : physical track 6, side 0, sectors 0–3 (32 entries)
```

Lumps straddle the side boundary — NEWDOS/80 addresses the disk as one continuous
36-sector-per-cylinder stream. Validated against all 16 files on the disk. Note `boot[2] = 11H`
claims directory track 17; the directory is on track 6.

## Open items

Four changes in `SCRIPSIT/SP` remain unexplained. None appears anywhere in Lindley — all are
Layer A:

1. **5DCCH** — variable moves 7CB6H → 7CB9H, with the instruction order changed.
2. **603AH / 6056H** — both `05` → `04`; the difference between them is preserved.
3. **7A20H / 7A22H** — `3C`,`42` → `7F`,`7F`, inside the 20-byte defaults block copied to 7C64H.
4. **4049H** — SP writes FF6BH, one below its FF6CH driver, consistent with a top-of-memory
   pointer. `KBDGER/CMD` writes FFEFH while loading at F000H, which is not consistent with that.

Also unresolved: Lindley's printer underline (`UNDRLN`) was dropped because SCRIPSIT/SP's
extended 7A00H block covers its 7A9EH hook — but I kept the screen half at 5FAFH, so the
underscore marker still displays with nothing acting on it at print time. **Testable in sdltrs
in two minutes**; not yet tested.

Would close items 1–3: an EDTASM source for the SP patch (`esnd-05.dmk` is unexamined), or
Lindley Part I if it carries a Scripsit memory map.

## Related

- [`diskimages/`](../../diskimages/README.md) — `esnd-04.dmk`, the canonical source for `WP/CMD`.
- [`hrgdos/`](../hrgdos/README.md) — the NEWDOS/80 side of the same problem: `KBDHRG`, my umlaut
  keyboard driver, and the patched HRG super-driver. Same motivation, different host.
- `KBDGER/CMD` — a **separate** German keyboard driver (140 bytes, loads at F000H, hooks 4049H).
  Not the same file as `KBDHRG/CMD` (128 bytes, DA84H, hooks 4016H) documented under `hrgdos/`,
  and its 126-byte F000H block shares **zero** bytes with SCRIPSIT/SP's FF82H block. Do not
  group the three.
