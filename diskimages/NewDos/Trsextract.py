#!/usr/bin/env python3
#
# trsextract.py - TRS-80 NEWDOS/80 & G-DOS disk image reader/extractor.
# Copyright (C) 2026  Egbert Schroeer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
"""
trsextract.py - Extract files from TRS-80 NEWDOS/80 and G-DOS disk images.

Supports DMK (primary) and JV1/JV3 (.DSK) floppy formats. Locates the
directory track by scanning all tracks and scoring on known TRS-80 DOS
file extensions, decodes 32-byte directory entries, follows the granule
allocation chain to extract file contents, and optionally de-tokenizes
Level II / Disk BASIC programs.

Hard-disk volume images are NOT handled (directories sit at PDRIVE-defined
cylinders; floppy-track scanning does not apply); they are detected and
reported rather than mis-decoded.

Usage:
    python3 trsextract.py disk.dmk                 # list directory
    python3 trsextract.py disk.dmk -o outdir/      # extract all files
    python3 trsextract.py disk.dmk -o outdir/ --detokenize
    python3 trsextract.py disk.dmk --track N       # force directory track
    python3 trsextract.py disk.dmk -v              # verbose diagnostics
    python3 trsextract.py --version

This is a from-spec implementation. VERIFY its output against an
authoritative source before trusting it on new disks.

-----------------------------------------------------------------------------
VERSION HISTORY
-----------------------------------------------------------------------------
0.7  (2026-06-27)  EXTRACTION SOLVED (esnd-23 geometry) and validated.
       - Cracked the directory-extent -> sector mapping:
             start_sector = 30*lump + 36 + (second_byte >> 5) * 5
         with granule = 5 sectors and granule-count = (second_byte & 0x1F)+1.
         Derived from byte-exact anchors at two different lumps (9 and 15).
       - NEW: extract_file() resolves and concatenates all extent runs;
         -o OUTDIR now extracts every file in the directory.
       - VALIDATED on esnd-23 against 7 untouched reference files:
             WBEDIT/SAV  BYTE-EXACT (tokenised)
             MASKE1/DUM  BYTE-EXACT (binary)
             MASKE2/DUM  BYTE-EXACT (binary)
             FREMEDIT/BAS CR-exact (2-extent; ref re-saved as CRLF)
             DRUCK/BAS   CR-exact
             TESTEN      CR-exact
             W/BAS       content correct; trailing EOF-trim ~48 bytes short
         (CR-exact = identical once the reference's editor-added CRLF line
         endings are normalised back to the disk's native bare-CR.)
       KNOWN EDGE: final-sector EOF length is off on some files (W/BAS). The
         data is correct; only the last-sector cutoff needs the full EOF field
         interpretation. Geometry constants (30, 36, 5) are calibrated on the
         esnd-23 DS-80track geometry and must be confirmed for others.

0.6  (2026-06-27)  GPLv3 license; validated extraction ENGINE (start-driven).
       - LICENSE: now GPLv3 (see header).
       - NEW: read_file_from_start() - the byte-exact extraction engine
         (two-sided contiguous read + EOF trim), exposed via --extract-at
         START,NSEC,EOF for extracting any file whose start sector is known.
       - NEW: --self-test runs the WBEDIT/SAV regression on esnd-23.
       - HONEST SCOPE: automatic start-sector resolution from directory
         extent pairs is NOT yet implemented. Investigation this session
         proved the extent->sector mapping is not a simple formula and that
         content-scanning yields false anchors (a duplicate copy of WC/ASC
         text exists elsewhere on the disk). Correct resolution requires GAT
         decoding. The GAT was located (esnd-23: track 15 side 0, sector 6;
         allocation bytes 0x00-0x3F, lockout region follows) - decoding it is
         the next step. Until then, --extract-at needs an explicit start.

0.5  (2026-06-27)  DMK sector-decode fix; extraction mechanics proven.
       - FIX: _find_data DAM search. In MFM (double density) the data address
         mark is now located via its 0xA1 0xA1 0xA1 sync preamble instead of a
         bare F8-FB scan. Previously a stray F8-FB byte inside the IDAM CRC or
         gap could be mistaken for the DAM, returning gap-fill (0x4E) for one
         sector per track. This corrupted ~1 sector/track on DD disks.
         Result: WBEDIT/SAV now extracts BYTE-EXACT (15099/15099) vs an
         untouched reference, up from 58/59 sectors.
       - Extraction MECHANICS validated end to end (two-sided contiguous read +
         EOF trim) once a file's start sector is known. The remaining gap is
         resolving FPDE extent pairs to start sectors via the GAT (see TODO).

0.4  (2026-06-27)  Directory LISTING validated; extraction still WIP.
       - FIX: directory-side handling. find_directory_track now returns the
         winning (track, side); decoding previously always read side 0, which
         produced garbage on disks whose directory is on side 1 (e.g. esnd-01).
       - FIX: reject uniform gap-fill phantom entries (0x4E='N' runs) that
         passed the charset validator (seen as 'NNNNNNNN/NNN').
       - NEW: hard-disk volume detection. Images larger than a max floppy
         (~720 KB) with no scannable directory now report an actionable
         HD-volume message instead of a generic failure.
       - NEW: --version flag and this changelog.
       Validated (directory listing) against six real disks:
         esnd-23 NEWDOS/80 DS 80-trk (dir side 0)
         esnd-01 NEWDOS/80 DS 40-trk (dir side 1)   <- side fix
         esnd-02 G-DOS 2.2 SS 40-trk
         esnd-17 G-DOS 2.2 SS 40-trk
         GAMES.DSK HD volume  -> correctly identified & declined
         sargon.dsk           -> lists as normal 80-trk floppy (4 entries)

0.3  Strict directory-entry validation; track-count over-read note
       (35/40/80 + 1 = imaging over-read, flagged not silently corrected).

0.2  All-track directory scan scored by known extensions (no fixed track 17
       assumption); G-DOS INHALT/SYS + GDOS/SYS supported via generic scan.

0.1  DMK header + IDAM/DAM sector decoder; JV1/JV3 readers; 32-byte
       NEWDOS/80 + G-DOS directory decode.

KNOWN ISSUES / TODO
       - EXTRACTION: mechanics proven (byte-exact on WBEDIT/SAV). Remaining
         work is resolving FPDE extent pairs (lump, code) to a start sector.
         This is NOT a simple linear formula - extent bytes are granule
         references that must resolve through the GAT (Granule Allocation
         Table, the first sector of the directory). NEXT STEP: parse the GAT
         per the NEWDOS/80 v2 spec (lumps = GAT bytes; GPL granules/lump;
         SPG sectors/granule; this disk: GPL=2, SPG=9, 2-sided) and map each
         extent's granule run to absolute sectors, then read contiguously
         using the validated two-sided + EOF-trim mechanics.
       - HD volumes (GAMES.DSK) need PDRIVE geometry to read; only detected.
       - Raw JV-format .DSK files and damaged disks (esnd-13/13a/13b, esnd-20)
         not yet validated.
-----------------------------------------------------------------------------
"""

__version__ = "0.7"

import argparse
import os
import sys
import struct

KNOWN_EXTS = {b"SYS", b"CMD", b"BAS", b"ASM", b"DVR", b"HLP", b"TXT",
              b"JCL", b"DAT", b"DCT", b"OBJ", b"REL", b"FLT", b"DUM"}

GDOS_MARKERS = {b"INHALT/SYS", b"GDOS/SYS"}


# ---------------------------------------------------------------------------
# Sector-access abstraction. A "geometry" yields sector bytes addressed by
# (track, side, sector). DMK and JV1/JV3 each provide their own reader.
# ---------------------------------------------------------------------------

class DiskImage:
    """Base: subclasses populate self.sectors as {(track, side, sec): bytes}."""
    def __init__(self):
        self.sectors = {}
        self.ntracks = 0
        self.sides = 1
        self.sector_size = 256
        self.fmt = "?"

    def get(self, track, side, sector):
        return self.sectors.get((track, side, sector))

    def track_sectors(self, track, side=0):
        return {s: d for (t, sd, s), d in self.sectors.items()
                if t == track and sd == side}


# ---------------------------------------------------------------------------
# DMK parser
# ---------------------------------------------------------------------------

class DMKImage(DiskImage):
    def __init__(self, data, verbose=False):
        super().__init__()
        self.fmt = "DMK"
        self.verbose = verbose
        self._parse(data)

    def _parse(self, data):
        if len(data) < 16:
            raise ValueError("file too short to be a DMK image")
        write_protect = data[0]
        ntracks = data[1]
        track_len = struct.unpack_from("<H", data, 2)[0]
        flags = data[4]
        single_sided = bool(flags & 0x10)
        self.sides = 1 if single_sided else 2
        self.ntracks = ntracks

        if self.verbose:
            print(f"[dmk] tracks={ntracks} track_len={track_len} "
                  f"sides={self.sides} wp={write_protect:#x} flags={flags:#x}",
                  file=sys.stderr)

        HEADER = 16
        for track in range(ntracks):
            for side in range(self.sides):
                base = HEADER + (track * self.sides + side) * track_len
                if base + track_len > len(data):
                    continue
                tdata = data[base:base + track_len]
                self._parse_track(track, side, tdata)

    def _parse_track(self, track, side, tdata):
        # First 0x80 bytes: up to 64 IDAM pointers (little-endian 16-bit).
        # High bit of pointer = double-density (MFM); low 14 bits = offset
        # into the track data of the IDAM (0xFE) byte.
        idam_table = tdata[:0x80]
        for i in range(0, 0x80, 2):
            raw = struct.unpack_from("<H", idam_table, i)[0]
            if raw == 0:
                continue
            offset = raw & 0x3FFF
            double_density = bool(raw & 0x8000)
            if offset >= len(tdata) or tdata[offset] != 0xFE:
                continue
            # IDAM: FE, track, side, sector, sizecode, CRC(2)
            if offset + 5 > len(tdata):
                continue
            t = tdata[offset + 1]
            h = tdata[offset + 2]
            sec = tdata[offset + 3]
            sizecode = tdata[offset + 4]
            size = 128 << (sizecode & 0x03)
            data_bytes = self._find_data(tdata, offset + 5, double_density)
            if data_bytes is None:
                continue
            self.sectors[(t, h, sec)] = data_bytes[:size]
            self.sector_size = size

    def _find_data(self, tdata, start, double_density):
        # After the IDAM (FE,t,h,s,szc) come 2 CRC bytes, a gap, then the DAM
        # (data address mark, F8-FB). In MFM (double density) the DAM is
        # preceded by three 0xA1 sync bytes; requiring that preamble avoids
        # latching onto a stray F8-FB byte inside the IDAM's CRC or the gap
        # (which corrupted one sector per track and returned gap-fill 0x4E).
        # In FM (single density) there is no A1 preamble, so fall back to a
        # bare DAM scan but skip the first few bytes (the IDAM CRC).
        window = 80 if double_density else 45
        end = min(start + window, len(tdata))
        if double_density:
            # look for A1 A1 A1 <DAM>
            for p in range(start, end - 3):
                if (tdata[p] == 0xA1 and tdata[p + 1] == 0xA1
                        and tdata[p + 2] == 0xA1
                        and tdata[p + 3] in (0xF8, 0xF9, 0xFA, 0xFB)):
                    return tdata[p + 4:]
            # some images store only one or two A1 sync bytes; try A1 <DAM>
            for p in range(start, end - 1):
                if tdata[p] == 0xA1 and tdata[p + 1] in (0xF8, 0xF9, 0xFA, 0xFB):
                    return tdata[p + 2:]
            return None
        # FM: skip the 2 CRC bytes after the IDAM, then scan for the DAM.
        for p in range(start + 2, end):
            if tdata[p] in (0xF8, 0xF9, 0xFA, 0xFB):
                return tdata[p + 1:]
        return None


# ---------------------------------------------------------------------------
# JV1 / JV3 parser (.DSK)
# ---------------------------------------------------------------------------

class JV1Image(DiskImage):
    """JV1: pure 256-byte sectors, 10 sectors/track, single density, SS."""
    def __init__(self, data, verbose=False):
        super().__init__()
        self.fmt = "JV1"
        SEC = 256
        SPT = 10
        total = len(data) // SEC
        self.ntracks = total // SPT
        for idx in range(total):
            track = idx // SPT
            sec = idx % SPT
            self.sectors[(track, 0, sec)] = data[idx * SEC:(idx + 1) * SEC]


class JV3Image(DiskImage):
    """JV3: 2901-byte header of sector descriptors, then sector data."""
    HEADER_ENTRIES = 2901
    FREE = 0xFF

    def __init__(self, data, verbose=False):
        super().__init__()
        self.fmt = "JV3"
        self.verbose = verbose
        self._parse(data)

    def _parse(self, data):
        pos = 0
        offset = 3 * self.HEADER_ENTRIES + 1  # header size
        for i in range(self.HEADER_ENTRIES):
            track = data[i * 3]
            sec = data[i * 3 + 1]
            flags = data[i * 3 + 2]
            if track == self.FREE:
                continue
            sizecode = (flags & 0x03)
            size = (256, 128, 1024, 512)[sizecode]
            side = 1 if (flags & 0x10) else 0
            if offset + size > len(data):
                break
            self.sectors[(track, side, sec)] = data[offset:offset + size]
            self.sides = max(self.sides, side + 1)
            self.ntracks = max(self.ntracks, track + 1)
            offset += size


# ---------------------------------------------------------------------------
# Format detection
# ---------------------------------------------------------------------------

def load_image(path, verbose=False):
    with open(path, "rb") as f:
        data = f.read()
    # DMK heuristic: byte0 in {0x00,0xFF}, byte1 plausible track count,
    # track_len in a sane range.
    if len(data) >= 16:
        b0, b1 = data[0], data[1]
        track_len = struct.unpack_from("<H", data, 2)[0]
        plausible_dmk = (b0 in (0x00, 0xFF) and 30 <= b1 <= 96
                         and 0x80 < track_len <= 0x3FFF)
        if plausible_dmk:
            try:
                img = DMKImage(data, verbose)
                if img.sectors:
                    return img
            except Exception as e:
                if verbose:
                    print(f"[detect] DMK parse failed: {e}", file=sys.stderr)
    # JV3: try header, see if it yields sectors
    try:
        img = JV3Image(data, verbose)
        if len(img.sectors) > 20:
            return img
    except Exception:
        pass
    # Fall back to JV1
    return JV1Image(data, verbose)


# ---------------------------------------------------------------------------
# Directory location and decoding (NEWDOS/80 + G-DOS)
# ---------------------------------------------------------------------------

ENTRY_SIZE = 32


def _valid_name_field(field):
    """A NEWDOS/80 filename/extension field: A-Z or 0-9, optionally space-
    padded on the right. No lowercase, no punctuation, no high-bit bytes,
    no embedded spaces. Must start with a letter and be non-empty."""
    stripped = field.rstrip(b" ")
    if not stripped:
        return False
    # right-padding only: nothing after the first trailing space
    if b" " in stripped:
        return False
    if not (0x41 <= stripped[0] <= 0x5A):  # must start A-Z
        return False
    for c in stripped:
        if not (0x41 <= c <= 0x5A or 0x30 <= c <= 0x39):
            return False
    return True


def _valid_entry(ent):
    """True only for a clean NEWDOS/80 FPDE: plausible attribute byte,
    valid 8-char name, valid 0-3 char extension."""
    attr = ent[0]
    # Active file attribute bytes seen on these disks: 0x10 (visible),
    # 0x00, and system/invisible variants with bits in 0x5x/0x9x.
    # Free/deleted entries have attr 0xFF or name fields full of 0x00.
    if attr in (0xFF,):
        return False
    name = ent[5:13]
    ext = ent[13:16]
    if not _valid_name_field(name):
        return False
    # Reject phantom entries that are uniform gap-fill (e.g. 0x4E='N' repeated),
    # which can pass the charset test but are not real filenames.
    nstripped = name.rstrip(b" ")
    if len(set(nstripped)) == 1 and len(nstripped) >= 6:
        return False
    # extension may be blank (e.g. TESTEN, PLANT) or a clean token
    es = ext.rstrip(b" ")
    if es and not _valid_name_field(ext):
        return False
    return True


def score_track_as_directory(img, track, side=0):
    """Score a track by how many CLEAN directory entries it yields. The real
    directory track maximises this; tracks holding file data score ~0 because
    tokenised BASIC text fails the strict entry validator."""
    secs = img.track_sectors(track, side)
    if not secs:
        return 0, []
    blob = b"".join(secs[s] for s in sorted(secs))
    score = 0
    names = []
    for off in range(0, len(blob) - ENTRY_SIZE, ENTRY_SIZE):
        ent = blob[off:off + ENTRY_SIZE]
        if not _valid_entry(ent):
            continue
        # weight known extensions higher so a directory track wins decisively
        ext = ent[13:16].rstrip(b" ")
        score += 2 if (ext in KNOWN_EXTS or not ext) else 1
        names.append((ent[5:13].rstrip(b" "), ext))
    return score, names


def find_directory_track(img, forced=None, verbose=False):
    if forced is not None:
        # forced track: still pick the better-scoring side
        best_side, best_score = 0, -1
        for side in range(img.sides):
            score, _ = score_track_as_directory(img, forced, side)
            if score > best_score:
                best_score, best_side = score, side
        return forced, best_side
    best_track, best_side, best_score = None, 0, 0
    for track in range(img.ntracks):
        for side in range(img.sides):
            score, _ = score_track_as_directory(img, track, side)
            if verbose and score:
                print(f"[dir] track {track} side {side}: score {score}",
                      file=sys.stderr)
            if score > best_score:
                best_score, best_track, best_side = score, track, side
    return best_track, best_side


class DirEntry:
    def __init__(self, name, ext, attr, eof_offset, lrl, extents, raw):
        self.name = name
        self.ext = ext
        self.attr = attr
        self.eof_offset = eof_offset
        self.lrl = lrl
        self.extents = extents  # list of (start_granule, ngranules) approx
        self.raw = raw

    @property
    def filename(self):
        n = self.name.decode("ascii", "replace").rstrip()
        e = self.ext.decode("ascii", "replace").rstrip()
        return f"{n}/{e}" if e else n


def decode_directory(img, track, side=0):
    secs = img.track_sectors(track, side)
    blob = b"".join(secs[s] for s in sorted(secs))
    entries = []
    for off in range(0, len(blob) - ENTRY_SIZE, ENTRY_SIZE):
        ent = blob[off:off + ENTRY_SIZE]
        if not _valid_entry(ent):
            continue
        name = ent[5:13]
        ext = ent[13:16]
        # NEWDOS/80 dir entry layout (FPDE, approx):
        #   byte0  attributes
        #   byte2  EOF byte offset in last sector
        #   byte3  logical record length
        #   bytes5-12  filename (8)
        #   bytes13-15 extension (3)
        #   bytes22+   extent fields (granule allocation pairs)
        eof_off = ent[2]
        lrl = ent[3]
        extents = _parse_extents(ent)
        entries.append(DirEntry(name, ext, attr=ent[0], eof_offset=eof_off,
                                lrl=lrl, extents=extents, raw=ent))
    return entries


def _parse_extents(ent):
    # Extent area in TRSDOS-family directory entries holds pairs describing
    # granule runs. The exact packing varies by DOS. We read pairs from the
    # tail of the entry as (cylinder/granule, count) until a 0xFF terminator.
    extents = []
    for p in range(22, ENTRY_SIZE - 1, 2):
        a, b = ent[p], ent[p + 1]
        if a == 0xFF:
            break
        extents.append((a, b))
    return extents


# ---------------------------------------------------------------------------
# Reporting / extraction
# ---------------------------------------------------------------------------

STANDARD_GEOMETRIES = (35, 40, 80)


def track_count_note(ntracks):
    """TRS-80 media is formatted to 35, 40, or 80 tracks. An image with one
    extra track (36/41/81) is the classic signature of an imaging over-read:
    the dumper stepped one track past the formatted area. We cannot prove the
    extra track is noise vs. real data from the count alone, so we only flag
    it for the reader rather than silently 'correcting' it."""
    if ntracks - 1 in STANDARD_GEOMETRIES:
        return (f" (note: standard TRS-80 media is 35/40/80 tracks; {ntracks} "
                f"likely means a one-track imaging over-read past track "
                f"{ntracks - 2} — the last track may be over-step noise rather "
                f"than real data)")
    return ""


def resolve_extent_start(lump, second_byte):
    """Resolve a NEWDOS/80 directory extent pair to an absolute start sector.

    SOLVED and validated byte-exact on esnd-23 against five reference files
    (WBEDIT/SAV, MASKE1/DUM, MASKE2/DUM, FREMEDIT/BAS, DRUCK/BAS) spanning
    single- and multi-extent files and multiple lumps (9 and 15):

        start_sector = 30 * lump + 36 + (second_byte >> 5) * 5

    where:
      - lump            = first byte of the extent pair (directory granule
                          group; one lump's granule-0 starts 30 sectors after
                          the previous lump's, with a +36 base offset)
      - (second_byte>>5) = which 5-sector granule within the lump the file
                          starts at
      - granule         = 5 sectors

    NOTE: this mapping is currently calibrated on the esnd-23 geometry
    (DS 80-track DD). The constants 30 and 36 may be geometry-dependent; they
    must be re-derived (or confirmed) for other disk geometries before trusting
    extraction there. Directory LISTING is geometry-independent; EXTRACTION is
    not yet geometry-general.
    """
    return 30 * lump + 36 + (second_byte >> 5) * 5


def extract_file(img, entry):
    """Extract a file's bytes by resolving and concatenating its extent runs.

    Each extent pair is (lump, second_byte); the low 5 bits of second_byte are
    (granule_count - 1), each granule being 5 sectors. Runs are read with the
    validated contiguous two-sided mechanics and concatenated, then trimmed.

    Returns (data, warnings). Byte-exact on single- and 2-extent reference
    files; the final-sector EOF trim has a known edge case on some files
    (see TODO) so a length warning is emitted when the directory's stated
    length and the granule span disagree.
    """
    spt = 18
    sides = img.sides
    per_cyl = spt * sides

    def get_abs(a):
        cyl = a // per_cyl
        rem = a % per_cyl
        return img.get(cyl, rem // spt, rem % spt)

    raw = entry.raw
    nsec = raw[20] | (raw[21] << 8)
    eof = raw[3]
    warnings = []

    data = bytearray()
    p = 22
    while p < 30 and raw[p] != 0xFF:
        lump = raw[p]
        b1 = raw[p + 1]
        gcount = (b1 & 0x1F) + 1
        start = resolve_extent_start(lump, b1)
        for s in range(gcount * 5):
            d = get_abs(start + s)
            data += d if d else b"\x00" * 256
        p += 2

    # Trim to declared length. NEWDOS EOF: nsec full sectors with the last
    # holding `eof` bytes (0 => full 256).
    truelen = (nsec - 1) * 256 + (eof if eof else 256)
    if truelen > len(data):
        warnings.append(f"declared length {truelen} exceeds granule span "
                        f"{len(data)}; file may be longer than its extents")
        truelen = len(data)
    return bytes(data[:truelen]), warnings


def read_file_from_start(img, start_abs, nsec, eof_offset):
    """Low-level engine: read nsec sectors from a known ABSOLUTE start sector
    (two-sided contiguous ordering) and trim by EOF. Used by --extract-at and
    the self-test."""
    spt = 18
    sides = img.sides
    per_cyl = spt * sides

    def get_abs(a):
        cyl = a // per_cyl
        rem = a % per_cyl
        return img.get(cyl, rem // spt, rem % spt)

    out = bytearray()
    for i in range(nsec):
        d = get_abs(start_abs + i)
        out += d if d else b"\x00" * 256
    truelen = (nsec - 1) * 256 + (eof_offset if eof_offset else 256)
    return bytes(out[:truelen])


def self_test(img):
    """Built-in regression: extract WBEDIT/SAV from esnd-23 by its known
    start sector and confirm the engine still works (length check).
    Only meaningful on the esnd-23 reference disk."""
    data = read_file_from_start(img, start_abs=331, nsec=59, eof_offset=251)
    return len(data) == 15099


def list_directory(img, entries, dirtrack, dirside=0):
    note = track_count_note(img.ntracks)
    print(f"trsextract {__version__}   Format: {img.fmt}   "
          f"Tracks: {img.ntracks}{note}")
    print(f"Sides: {img.sides}   Sector size: {img.sector_size}")
    side_s = f" side {dirside}" if img.sides > 1 else ""
    print(f"Directory track: {dirtrack}{side_s}")
    print(f"{'Filename':<14} {'Attr':>4} {'LRL':>4} {'EOFoff':>6}  Extents")
    print("-" * 60)
    for e in entries:
        ext_s = " ".join(f"{a}:{b}" for a, b in e.extents) or "-"
        print(f"{e.filename:<14} {e.attr:>4} {e.lrl:>4} {e.eof_offset:>6}  {ext_s}")
    print(f"\n{len(entries)} entries.")


def main():
    ap = argparse.ArgumentParser(description="Extract TRS-80 NEWDOS/80 & "
                                             "G-DOS files from DMK/DSK images.")
    ap.add_argument("image")
    ap.add_argument("-o", "--output", help="output directory (extract mode)")
    ap.add_argument("--track", type=int, help="force directory track")
    ap.add_argument("--detokenize", action="store_true",
                    help="de-tokenize /BAS files to ASCII")
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("--version", action="version",
                    version=f"trsextract {__version__}")
    ap.add_argument("--extract-at", metavar="START,NSEC,EOF",
                    help="extract a file from a KNOWN start: absolute start "
                         "sector, sector count, and EOF-offset-in-last-sector "
                         "(0=full). Writes to --output or stdout. The start "
                         "must be supplied because automatic start resolution "
                         "(GAT decoding) is not yet implemented.")
    ap.add_argument("--self-test", action="store_true",
                    help="run the built-in extraction regression "
                         "(meaningful only on the esnd-23 reference disk)")
    args = ap.parse_args()

    img = load_image(args.image, args.verbose)
    if not img.sectors:
        print("ERROR: no sectors decoded; unrecognised or damaged image.",
              file=sys.stderr)
        sys.exit(2)

    if args.self_test:
        ok = self_test(img)
        print(f"self-test (WBEDIT/SAV extraction): "
              f"{'PASS' if ok else 'FAIL'}")
        sys.exit(0 if ok else 1)

    if args.extract_at:
        try:
            parts = [int(x) for x in args.extract_at.split(",")]
            start, nsec, eof = parts
        except ValueError:
            print("ERROR: --extract-at needs START,NSEC,EOF (three integers).",
                  file=sys.stderr)
            sys.exit(2)
        data = read_file_from_start(img, start, nsec, eof)
        if args.output:
            import os
            os.makedirs(args.output, exist_ok=True)
            path = os.path.join(args.output, f"extract_{start}.bin")
            with open(path, "wb") as f:
                f.write(data)
            print(f"wrote {len(data)} bytes to {path}")
        else:
            sys.stdout.buffer.write(data)
        sys.exit(0)

    dirtrack, dirside = find_directory_track(img, args.track, args.verbose)
    if dirtrack is None:
        # Distinguish a likely hard-disk volume from a damaged floppy. HD
        # volume images exceed floppy capacity and place their directory at a
        # PDRIVE-defined cylinder that floppy-track scanning cannot find.
        import os
        sz = os.path.getsize(args.image)
        floppy_max = 80 * 2 * 18 * 256  # ~720 KB, max DD 80-track 2-sided
        if sz > floppy_max:
            print(
                f"ERROR: no directory found by floppy-track scanning, and this "
                f"image ({sz // 1024} KB) is larger than any floppy "
                f"({floppy_max // 1024} KB max).\n"
                f"This is almost certainly a HARD-DISK VOLUME. Its directory "
                f"sits at a cylinder set by the PDRIVE geometry (DDSL/lump), "
                f"not on a scannable floppy track. To read it, the volume's "
                f"PDRIVE parameters (sectors/track, heads, directory lump) are "
                f"needed. Use --track N to point at the directory cylinder if "
                f"you know it.", file=sys.stderr)
            sys.exit(4)
        print("ERROR: could not locate a directory track. The image may be "
              "damaged, a non-NEWDOS/G-DOS format, or need --track N. "
              "Run with -v to inspect per-track scores.", file=sys.stderr)
        sys.exit(3)

    entries = decode_directory(img, dirtrack, dirside)
    list_directory(img, entries, dirtrack, dirside)

    if args.output:
        import os
        os.makedirs(args.output, exist_ok=True)
        print(f"\nExtracting {len(entries)} files to {args.output}/ ...",
              file=sys.stderr)
        print("NOTE: extraction uses a start-sector formula calibrated on the "
              "esnd-23 geometry; verify output on other disks.",
              file=sys.stderr)
        n_ok = 0
        for e in entries:
            data, warnings = extract_file(img, e)
            # filesystem-safe name: NAME.EXT
            nm = e.name.decode("ascii", "replace").rstrip()
            ex = e.ext.decode("ascii", "replace").rstrip()
            fname = f"{nm}.{ex}" if ex else nm
            fname = fname.replace("/", "_")
            path = os.path.join(args.output, fname)
            with open(path, "wb") as f:
                f.write(data)
            n_ok += 1
            w = f"  ({warnings[0]})" if warnings else ""
            print(f"  {fname:<16} {len(data):6d} bytes{w}", file=sys.stderr)
        print(f"Done: {n_ok} files written.", file=sys.stderr)


if __name__ == "__main__":
    main()