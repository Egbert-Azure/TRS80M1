# Disk esnd-20a — NEWDOS/80 +10 v2.5 (repaired esnd-20)

**Operating system:** NEWDOS/80 +10, Version 2.5, 31.12.85 (same release branch as esnd-08/esnd-09)
**Geometry:** 40-track, double density
**System:** SYS0–SYS29 present (full NEWDOS/80 system complement)
**Status:** Repaired/good copy of the previously damaged esnd-20. The `ACCEL3/CMD` file
that was missing on esnd-20 (preventing `H/JCL` from running) is present here.

## Graphics driver
`HRG/CMD` — high-resolution graphics driver for the **RB-Elektronik (Rolf Best, Eitorf)
HRG1-B** card. NOT Schmidtke. Resolution 384 × 192. Loaded from DOS via `DO H` or from
BASIC via `POKE16561,254:POKE16562,251:CLEAR50:CMD"HRG"`.

## Notable files

| File | Type | Purpose |
|------|------|---------|
| `H/JCL` | JCL chain | Two-stage loader: (1) BASIC@64510 + `CMD"HRG"`; (2) `LOAD ACCEL3/CMD`, BASIC@58878, `SYSTEM /59872`, `CMD"HRGACC"`. `HRGACC` = ACCEL3-compatible HRG build. |
| `GREDIT/JCL` | JCL chain | Runs `ACCRUN/CMD` then `GREDIT/ACC` — a compiled high-res graphics editor. |
| `ACCEL3/CMD` | Compiler/runtime | Southern Software ACCEL3 BASIC compiler + `ACCRUN` runtime. |
| `ZEDIT/BAS` | Compiled BASIC | **Z-EDIT V2.0** character-set (font) editor, (C) U.Themann & B.Wedell 1984, compiled with ACCEL3. Edits 6×12 char matrices; 4 font types (std / dbl-wide / dbl-high / dbl-high+wide); block copy/merge/invert/XOR; load/save char sets to disk. |
| `DEMOHRG/BAS` | BASIC | **HRG-Demoprogramm** (C)1983 Ulrich Mueller. Interactive manual + live demo for HRG1-B and HRG/CMD. Source of the four documentation screenshots below. |

## Screenshot documentation (DEMOHRG/BAS output)

### Screen 1 — Software / loading & basic graphics commands
**Deutsch (original):**
> Software:
> Das Programm HRG/CMD erweitert den BASIC-Interpreter um verschiedene Grafikbefehle.
> Es wird wie folgt geladen:
> Aus dem DOS:      DO H
> Von BASIC aus:    POKE16561,254:POKE16562,251:CLEAR50:CMD"HRG"
> Vorsicht: HRG/CMD ist unvertraeglich mit Programmen, die in den Bereich
> FC00H – FFFFH laden oder den NAME-Befehl benutzen.
>
> Grafikbefehle:
> OUT 1,0    schaltet Grafikseite ein.
> OUT 0,0    schaltet Grafikseite aus.
> NAME CLS   loescht den Grafikbildschirm.
> NAME ON    setzt alle Punkte auf dem Bildschirm.
> NAME NOT   invertiert den Grafikbildschirm.

**English (translation):**
> Software:
> The program HRG/CMD extends the BASIC interpreter with various graphics commands.
> It is loaded as follows:
> From DOS:        DO H
> From BASIC:      POKE16561,254:POKE16562,251:CLEAR50:CMD"HRG"
> Caution: HRG/CMD is incompatible with programs that load into the range
> FC00H – FFFFH or that use the NAME command.
>
> Graphics commands:
> OUT 1,0    turns the graphics page on.
> OUT 0,0    turns the graphics page off.
> NAME CLS   clears the graphics screen.
> NAME ON    sets all points on the screen.
> NAME NOT   inverts the graphics screen.

### Screen 2 — Point & line commands
**Deutsch (original):**
> Im Folgenden bezeichnet x,y eine Bildschirmposition. Dabei zaehlt x von links
> nach rechts (0 – 383) und y von unten nach oben (0 – 191).
> NAME SET x,y     setzt Punkt an Position x,y.
> NAME RESET x,y   setzt Punkt zurueck.
> NAME POINT x,y   invertiert Punkt.
> FN POINT (x,y)   fragt Punkt ab (-1 = hell, 0 = dunkel).
> NAME SET TO x,y          zieht Linie vom zuletzt gesetzten Punkt nach Position x,y.
> NAME SET x1,y1 TO x2,y2  zieht Linie von Position x1,y1 nach Position x2,y2.
> Analog sind die beiden vorhergehenden Befehle fuer Ruecksetzen (RESET) und
> Invertieren (POINT) einer Linie definiert.
> Es koennen auch mehrere Linien in einem Befehl gezogen werden,
> z. B. durch NAME SET x1,y1 TO x2,y2 TO x3,y3 usw.

**English (translation):**
> In the following, x,y denotes a screen position. x counts from left to right
> (0 – 383) and y from bottom to top (0 – 191).
> NAME SET x,y     sets a point at position x,y.
> NAME RESET x,y   resets the point.
> NAME POINT x,y   inverts the point.
> FN POINT (x,y)   queries the point (-1 = lit, 0 = dark).
> NAME SET TO x,y          draws a line from the last set point to position x,y.
> NAME SET x1,y1 TO x2,y2  draws a line from position x1,y1 to position x2,y2.
> The two preceding commands are defined analogously for resetting (RESET) and
> inverting (POINT) a line.
> Several lines can also be drawn in a single command,
> e.g. NAME SET x1,y1 TO x2,y2 TO x3,y3 etc.

### Screen 3 — Hardcopy, disk I/O, shape definition
**Deutsch (original):**
> NAME LPRINT       Hardcopy des Grafikbildschirms auf MX-82 oder kompatiblem Drucker.
> NAME LOAD "file"  Grafikseite von Disk laden.
> NAME SAVE "file"  Grafikseite auf Disk schreiben.
> NAME @ p,s$       zeichnet Shape s$ an Position p.
>
> Shape-Definition: Ein Shape wird in einem String abgespeichert.
> Die einzelnen Bytes des Strings haben folgende Bedeutung:
> Bits 0 – 5:  Bit-Image von 6 nebeneinanderliegenden Punkten.
> Bits 6 – 7:  Richtung, in der das Bit-Image relativ zum vorherigen liegt
>              (bei Byte 0: unbenutzt). Der Wert dieser beiden Bits:
>              0 – nach links
>              1 – nach rechts
>              2 – nach unten
>              3 – nach oben

**English (translation):**
> NAME LPRINT       Hardcopy of the graphics screen to an MX-82 or compatible printer.
> NAME LOAD "file"  Load graphics page from disk.
> NAME SAVE "file"  Write graphics page to disk.
> NAME @ p,s$       draws shape s$ at position p.
>
> Shape definition: A shape is stored in a string.
> The individual bytes of the string mean the following:
> Bits 0 – 5:  Bit-image of 6 adjacent points.
> Bits 6 – 7:  Direction in which the bit-image lies relative to the previous one
>              (for byte 0: unused). The value of these two bits:
>              0 – to the left
>              1 – to the right
>              2 – downward
>              3 – upward

### Screen 4 — NAME@ port detail & SPOOL/CMD
**Deutsch (original):**
> Die Position p im NAME@-Befehl wird direkt in die Ports 2 (LSB) und 3 (MSB)
> geschrieben. Folglich bezeichnen die Bits 0 – 9 die 'PRINT@'-Position und die
> Bits 10 – 13 die vertikale Zeile innerhalb dieser Bildschirmposition.
>
> Programm SPOOL/CMD:
> Das Spoolerprogramm benutzt die 12k Bildwiederholspeicher als Ringpuffer.
> Es erlaubt gleichzeitiges Drucken und Ausfuehren eines anderen Programms.
> Selbstverstaendlich darf dabei die HRG-Grafik nicht benutzt werden.

**English (translation):**
> The position p in the NAME@ command is written directly to ports 2 (LSB) and
> 3 (MSB). Consequently bits 0 – 9 denote the 'PRINT@' position and bits 10 – 13
> the vertical row within that screen position.
>
> Program SPOOL/CMD:
> The spooler program uses the 12k display refresh memory as a ring buffer.
> It allows simultaneous printing and execution of another program.
> Naturally, HRG graphics may not be used while doing so.
