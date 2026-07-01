<!-- /software/hrgdos/README.md — umlaut keyboard driver (KBDHRG) for NewDos80, paired with the patched HRG super-driver (HRGDOS) -->
<!-- (c) E. Schroeer -->
# KBDHRG — Umlaut-capable keyboard driver for NewDos80

**Author:** Egbert Schroeer
**Original copyright:** © 1989 Egbert Schröer (spelling as in the source)
**Version:** 1.1 — October 1989
**Target:** TRS-80 Model I · NEWDOS/80 v2.0 · RB-Electronic HRG-1B
**License:** GPLv3 — see the LICENSE file at the repository root

---

## What is this?

`KBDHRG` is a 128-byte keyboard driver for the TRS-80 Model I running
NEWDOS/80. It lets you type the German umlauts (ä ö ü ß / Ä Ö Ü) directly, at
any time, without redefining the G character set.

It works by hooking the DOS keyboard vector at `4016H`. Type `ß` followed by a
vowel and the driver converts the pair into the matching umlaut; if no vowel
follows, `ß` is emitted. `<SHIFT>` produces the upper-case umlauts. The driver
can be relocated in memory and used on its own; on the disks here it is tuned
(entry point `DA84H`, `JP 0EB36H`) to hand off to HRGDOS on load.

`KBDHRG` is one of a pair:

- **`KBDHRG/CMD`** — this keyboard driver (128 bytes, load address `DA84H`).
- **`HRGDOS/CMD`** — RB-Electronic's `HRG/CMD` high-resolution-graphics
  super-driver, patched by Egbert Schröer and renamed. The patch adds, among
  other things, return to DOS without the 1,2,3 key combination (via the
  `#PRINT(2)` path).

The two work hand in hand, but the OS is NEWDOS/80 and that is what the
keyboard driver is for.

---

## Files

| File | Description |
|---|---|
| [`kbdhrg.z80`](./kbdhrg.z80) | Binary-verified Z80 source |
| `KBDHRG/CMD` | Original binary (on disk) |
| `HRGDOS/CMD` | Patched RB-Electronic HRG super-driver |

A DMK disk image carrying the Z80 source is planned.

---

## Provenance & verification

The driver was written by Egbert Schröer in 1989 and published in January 1990
in Club-80, Heft 29 (pp. 12–17). The full article appears below in the German
original, followed by an English translation.

**Where the binary was found:** `KBDHRG/CMD` is present on disks **esnd-01**
and **NEWDOS80**. Both show identical directory listings (same 45 files, same
order, same geometry) and are very likely the same disk imaged twice.

**Verification:** [`kbdhrg.z80`](./kbdhrg.z80) was decoded byte-for-byte from
`KBDHRG.CMD` (128-byte load block, `DA84H`–`DB03H`) and cross-checked against
Listing 1 of the article. The assembled byte stream matches completely, with
no discrepancies. Only the byte stream is verifiable; the label names,
comments, and directives in the source come from the printed listing.

---

## The article — Club-80, Heft 29 (1990)

### German original

> Quelle: Club-80, Heft 29, Januar 1990, S. 12–17. Transkribiert aus dem Original-Scan.

#### Modifikation des HRG Treibers von RB-Elektronik
##### Umlaute mit NewDos/80 Vers. 2.0; neuer Tastaturtreiber

Der hier beschriebene Patch des Supertreibers ermöglicht die Eingabe von
Umlauten, die Rückkehr vom BASIC zum DOS ohne die Tastenkombination 1,2,3.
Außerdem erübrigt sich eine neue Definition des G-Zeichensatzes zur
Darstellung von Umlauten durch Einlesen des Zeichensatzes. Die Umlaute sind
jederzeit aktiv. Nachteil ist das stete Geflimmer der HRG, aber hier kann
eventuell ein Hardware-Fachmann helfen?

Grundidee dieses Patches war eigentlich nur ein neuer Tastaturtreiber, der
es mir ermöglichen sollte, jederzeit Umlaute ohne große Mühe einzugeben. Die
Bedingung dazu war, daß dies mit der gleichen Tastenkombination geschehen
sollte wie bei dem von mir durchgeführten SCRIPSIT-Patch (siehe SONDERINFO
27.5). Außerdem sollte die eigentliche Funktion der Tasten nicht verändert
werden. Als dieser Tastaturtreiber fertiggestellt war, stürzte ich mich auf
den HRG-Supertreiber V1.1 von RB-Elektronik. Es ist nämlich nicht
einzusehen, daß man nach dem Laden des Treibers und Basic nun auch noch den
G-Zeichensatz beispielsweise mit Umlauten neu definieren muß. Zusätzlich
störte mich schon immer, daß man über DEBUG (Tasten 1,2,3) in das DOS
zurückkehren mußte.

Hilfsmittel für die nun folgende kriminalistische Kleinarbeit war das
Monitorprogramm TASMON.

Doch zunächst zum neuen Tastaturtreiber, der ganze 124 Bytes belegt. Min.
25 Bytes könnte man einsparen, indem man Teile des Tastaturtreibers in eine
freigewordene Stelle des HRG Supertreibers installiert. Ich hielt dies nicht
für sinnvoll, möchte aber auf die Möglichkeit hinweisen.

Die Abfrage der Tasten erfolgt direkt über die Abfrage der entsprechenden
Tastaturzeile. Der Entry Point DA84H ist auf den HRG Supertreiber
abgestimmt. Der Tastaturtreiber kann aber auch im Speicher frei verschoben
und ohne HRG benutzt werden. `JP EB36H` wird später erläutert.

Nun zum HRG-Treiber. Um die Umlaute stets präsent zu haben, wurden diese
einmalig in den G-Zeichensatz eingelesen und anschließend das Programm von
EB00H bis EB79H mit Entry Point EB00H auf Diskette gebannt.

Die Darstellung der Umlaute sollte mit der Option `#PRINT(2)` erfolgen, die
den normalen Bildschirminhalt auf die HRG umleitet und dabei den definierten
G-Zeichensatz benutzt. Anschließend sollte ein Rücksprung in das DOS
erfolgen.

Nachdem der Tastaturtreiber geladen wurde, wird ein Sprung von diesem nach
EB36H ausgeführt und dort die HRG eingeschaltet. Dann wird der normale
Bildschirmtreiber vollwertig ersetzt. Alle Ausgaben erfolgen mittels
G-Zeichensatz durch die HRG.

Anstatt die Message ab EB44H auszugeben, kann man den freigewordenen
Speicherplatz, wie ich eingangs erwähnte, anders nutzen oder Teile des
Tastaturtreibers dort unterbringen.

Das Tastaturtreiberprogramm wird als KBDHRG/CMD abgespeichert, HRG/CMD habe
ich in HRGDOS/CMD umbenannt.

Für Anregungen, Verbesserungen, Kritik und weitere Möglichkeiten wäre ich
dankbar.

**(c) 1989 Egbert Schröer**

### English translation

> Source: Club-80, Heft 29, January 1990, pp. 12–17. Translated from the German original above, which is authoritative.

#### Modifying the RB-Elektronik HRG driver
##### Umlauts with NewDos/80 v2.0; a new keyboard driver

The super-driver patch described here enables entering umlauts and returning
from BASIC to DOS without the 1,2,3 key combination. It also removes the need
to redefine the G character set for displaying umlauts by reloading the
character set. The umlauts are active at all times. The drawback is the
constant flicker of the HRG — but perhaps a hardware expert could help with
that?

The original idea behind this patch was really just a new keyboard driver
that would let me enter umlauts at any time without much effort. The
condition was that it should work with the same key combination as the
SCRIPSIT patch I had done earlier (see SONDERINFO 27.5). The actual function
of the keys was not to be changed. Once this keyboard driver was finished, I
threw myself at RB-Elektronik's HRG super-driver V1.1. After all, there's no
reason why, after loading the driver and BASIC, one should then have to
redefine the G character set — with umlauts, for example — all over again.
On top of that, it had always bothered me that one had to return to DOS via
DEBUG (keys 1,2,3).

My tool for the detective work that followed was the monitor program TASMON.

But first, the new keyboard driver, which occupies a full 124 bytes. One
could save at least 25 bytes by placing parts of the keyboard driver in a
freed-up spot in the HRG super-driver. I did not consider this worthwhile,
but I wanted to point out the possibility.

The keys are read directly by polling the corresponding keyboard row. The
entry point DA84H is tuned to the HRG super-driver. However, the keyboard
driver can also be relocated freely in memory and used without the HRG.
`JP EB36H` is explained later.

Now to the HRG driver. To keep the umlauts always present, they were loaded
once into the G character set, after which the program from EB00H to EB79H,
with entry point EB00H, was committed to disk.

The umlauts should be displayed using the `#PRINT(2)` option, which redirects
the normal screen content to the HRG using the defined G character set. A
return to DOS should follow.

After the keyboard driver has been loaded, it jumps to EB36H, where the HRG
is switched on. The normal screen driver is then fully replaced. All output
is rendered through the HRG using the G character set.

Instead of printing the message at EB44H, one can use the freed-up memory
otherwise, as mentioned at the start, or place parts of the keyboard driver
there.

The keyboard driver program is saved as KBDHRG/CMD; I renamed HRG/CMD to
HRGDOS/CMD.

I would be grateful for suggestions, improvements, criticism, and further
possibilities.

**(c) 1989 Egbert Schröer**

---

## Listings 2 & 3 (HRG super-driver)

> **Editor's note — what TASMON was.** The article mentions TASMON as the tool
> for its "detective work." TASMON was a machine-language monitor/debugger for
> the TRS-80: it disassembled binaries, displayed and edited memory, and
> single-stepped code. It is what made this patch possible — the RB-Electronic
> super-driver shipped only as a binary, so it had to be disassembled and read
> before it could be modified. That process produced Listing 2 (the
> disassembled super-driver) and Listing 3 (the located patch points).

Listing 1 (the keyboard driver) is provided binary-verified as
[`kbdhrg.z80`](./kbdhrg.z80). Listings 2 and 3 below document the HRG
super-driver and the patches applied to it. They are transcribed from the
printed article and are **not yet** verified against `HRGDOS/CMD`; some hex
operands in the scan are uncertain.

### Listing 2: HRG-Supertreiber V1.1 (from print — unverified)

```
EB00H   LD      HL,EB79H
        LD      (4004H),HL
        LD      HL,0DAFFH
        LD      (EB74H),HL
        LD      HL,0AAFFH
        LD      (EB76H),HL
        LD      HL,(401EH)
        LD      (0F6B7H),HL
        LD      A,(4012H)
        CP      0FBH
        JP      Z,EB32H
        LD      HL,(EB74H)
        LD      (4049H),HL      ; setzt HIMEM
        LD      HL,EB51H        ; HL auf Text ab EB51H
        CALL    4467H           ; Ausgabe Text RB-EL HRG usw.
        LD      HL,EB4BH        ; HL auf Text ab EB4BH = BASIC
        JP      4419H           ; DOS Call -> BASIC
EB32H:  LD      HL,(EB51H)
        CALL    28A7H
        LD      HL,(EB74H)
        LD      (40B1H),HL
        LD      DE,0FFCEH
        ADD     HL,DE
        LD      (40A0H),HL
        CALL    1B4DH
        JP      1A19H
EB4BH:  DEFM    'BASIC'
        DEFB    0DH
EB51H:  DEFM    'RB-EL HRG SUPER-TREIBER V1.1'
        DEFB    0DH
;   ... Dispatch-Tabelle #SET / #RESET / #POINT / #OPEN / #CLOSE / #LINE /
;   ... #CLS / #CLEAR / #GET / #NAME / #PUT / #PRINT(2) usw.
;   ... einige Zieladressen im Scan unsicher.
```

### Listing 3: Patches im HRG-Treiberprogramm (from print — unverified)

```
EB00H   LD      HL,EB79H
        LD      (4004H),HL
        LD      HL,0DAFFH
        LD      (EB74H),HL
        LD      HL,0AAFFH
        LD      (EB76H),HL
        LD      HL,(401EH)
        LD      (0F6B7H),HL
        LD      HL,(EB74H)
        LD      (4049H),HL
        CALL    01C9H           ; CLS-Befehl
        CALL    04FCH           ; Umschalten auf 32 cpl
        LD      HL,3C04H        ; Cursor nach 3C04H
        LD      (4020H),HL
        LD      HL,EB44H        ; HL auf Text ab EB44H
        CALL    4467H           ; Text ausgeben
        LD      HL,EB3DH        ; HL auf DOS Command ab EB3DH
        JP      4419H           ; DOS Command ausführen = KBDHRG
EB36H:  LD      A,0CH
        OUT     (01H),A         ; HRG einschalten
        JP      0F6E5H          ; HRG löschen und #PRINT(2)
EB3DH:  DEFM    'KBDHRG'
        DEFB    0DH
EB44H:  DEFM    'HRG-DOS Version 1.6'
        DEFB    0AH
        DEFB    0AH
        DEFM    ' (c) by E.Schröer '89'
        DEFB    0DH

F6F2H   JP      1DEH            ; original: Steuerung Programmausführung
;       wird ersetzt durch / replaced by:
F6F2H   JP      402DH           ; Rücksprung zum DOS / return to DOS
```