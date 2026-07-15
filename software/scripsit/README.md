<!-- /software/scripsit/README.md — subject index: Scripsit and the SCRIPSIT/SP modification -->

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

| file | subject |
|---|---|
| `scripsit-sp-patch-analysis.md` | **Layer A.** Every change between `SCRIPSIT/CMD` and `SCRIPSIT/SP`, derived by structural diff. The FFACH umlaut translator, the FF6CH printer driver and its `RLD` escape, the FFE2→FFF1 translate table, the marker-glyph relocation. |
| `scripsit-sp-patch.asm` | Reconstructed assembly source for Layer A. **Not the original source** — a byte-faithful reconstruction; labels and comments are modern. |
| `wp-cmd-analysis.md` | **Layer B.** Load map, entry at 7B19H, the six hooks, the thirteen text-buffer stores, both dispatch tables, and the NEWDOS/80 geometry used to recover the file. |
| `scripsit-provenance.md` | **What is Lindley's and what is mine.** Hook-by-hook comparison, the `CP 20H` → `CP 0FFH` extension, and a list of corrections to the two analyses above. |
| `edtasm-z80.py` | Two-pass Z80 assembler for the EDTASM subset. Written to verify `wpand.scr` against Lindley's binary; reusable for any EDTASM source in the archive. |

**Reading order:** provenance first — it corrects several claims in the two analyses and is
dated later. Then Layer A, then Layer B.

## Provenance of the artefacts

- `SCRIPSIT/CMD`, `SCRIPSIT/SP` — supplied directly; both verified **byte-identical** to the
  copies on `esnd-04.dmk`.
- `WP/CMD` — re-extracted from `esnd-04.dmk` (track 10 / side 1 / sectors 13–16). An earlier
  extraction returned 883 bytes of `E5` fill; the disk was never at fault. See
  `wp-cmd-analysis.md` §8.
- `wp.cmd`, `wp7.cmd` — Lindley's binaries, third-party.
- `wpand.scr` — an EDTASM source file carrying Lindley's Listing One. Origin unresolved.
- The 1988 Club-80 article (SONDERINFO 27.5) is **lost**. A 2026 article covering the same
  ground exists but belongs with the other Club-80 material, not here.

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

- `diskimages/` — `esnd-04.dmk`, the canonical source for `WP/CMD`.
- `KBDGER/CMD` — my German keyboard driver, unrelated code. Its 126-byte
  F000H block shares **zero** bytes with SCRIPSIT/SP's FF82H block. Do not group the two.
