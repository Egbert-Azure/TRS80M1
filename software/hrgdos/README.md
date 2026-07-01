<!-- /software/hrgdos/README.md — umlaut keyboard driver (KBDHRG) for NewDos80, paired with the patched HRG super-driver (HRGDOS) -->
<!-- (c) E. Schroeer -->
# KBDHRG — Umlaut-fähiger Tastaturtreiber für NewDos80
# KBDHRG — Umlaut-capable keyboard driver for NewDos80

**Autor / Author:** Egbert Schroeer
**Original © / Original copyright:** 1989 Egbert Schröer *(Schreibweise der Quelle / spelling as in the source)*
**Version:** 1.1 — October 1989
**Ziel / Target:** TRS-80 Model I · NEWDOS/80 v2.0 · RB-Electronic HRG-1B
**Lizenz / License:** GPLv3 — siehe LICENSE im Repository-Wurzelverzeichnis / see the LICENSE file at the repository root

---

## Was ist das? (DE)

`KBDHRG` ist ein 128 Byte großer Tastaturtreiber für den TRS-80 Model I, der
zusammen mit dem gepatchten HRG-Supertreiber von RB-Electronic die direkte
Eingabe der deutschen Umlaute (ä ö ü ß / Ä Ö Ü) ermöglicht — jederzeit und
ohne erneutes Definieren des G-Zeichensatzes.

Funktionsweise: Der Treiber klinkt sich in den Tastaturvektor bei `4016H`
ein und schaltet über `JP 0EB36H` auf die HRG-Karte (High Resolution
Graphics) um. Wird `ß` gefolgt von einem Vokal getippt, wandelt der Treiber
die Kombination in den entsprechenden Umlaut um; folgt kein Vokal, wird `ß`
ausgegeben. `<SHIFT>` erzeugt die Großbuchstaben-Umlaute.

`KBDHRG` gehört zu einem Paar:
- **`KBDHRG/CMD`** — dieser Tastaturtreiber (128 Byte, Ladeadresse `DA84H`).
- **`HRGDOS/CMD`** — der HRG-Supertreiber `HRG/CMD` von RB-Electronic,
  von Egbert Schröer gepatcht und umbenannt. Der Patch ergänzt u. a. den
  Rücksprung ins DOS ohne die Tastenkombination 1,2,3 (`#PRINT(2)`-Pfad).

## What is this? (EN)

`KBDHRG` is a 128-byte keyboard driver for the TRS-80 Model I that, together
with the patched RB-Electronic HRG super-driver, enables direct entry of the
German umlauts (ä ö ü ß / Ä Ö Ü) — at any time, without redefining the G
character set.

How it works: the driver hooks the keyboard vector at `4016H` and switches to
the HRG (High Resolution Graphics) card via `JP 0EB36H`. Typing `ß` followed
by a vowel converts the pair into the matching umlaut; if no vowel follows,
`ß` is emitted. `<SHIFT>` produces the upper-case umlauts.

`KBDHRG` is one of a pair:
- **`KBDHRG/CMD`** — this keyboard driver (128 bytes, load address `DA84H`).
- **`HRGDOS/CMD`** — RB-Electronic's `HRG/CMD` super-driver, patched by
  Egbert Schröer and renamed. The patch adds, among other things, return to
  DOS without the 1,2,3 key combination (the `#PRINT(2)` path).

---

## Aufbau / Build

Der Quelltext ist für einen Z80-Assembler mit Standard-Mnemonik geschrieben
(getestet gegen `pasmo`-Syntax). Ladeadresse und HIMEM werden per `ORG` /
`DEFW` im Quelltext gesetzt. /

The source uses standard Z80 mnemonics (tested against `pasmo` syntax). Load
address and HIMEM are set via `ORG` / `DEFW` in the source.

```sh
pasmo kbdhrg.z80 kbdhrg.cmd
```

**Wichtig / Important:** Der Entry Point `DA84H` ist auf den HRG-Supertreiber
V1.1 abgestimmt. Wird der Treiber ohne HRG oder an anderer Stelle benutzt,
müssen `ORG` und der `JP 0EB36H` angepasst werden. /
The entry point `DA84H` is tuned to HRG super-driver V1.1. To use the driver
without the HRG or at a different address, adjust the `ORG` and the
`JP 0EB36H`.

Ein Detail, das beim Assemblieren auffällt: `DRIVER: CALL 0000H` ist ein
**absichtlicher Platzhalter**. Der Aufruf-Operand wird zur Ladezeit von
`LD (DRIVER+1),HL` mit dem originalen Tastatur-Vektor aus `4016H`
überschrieben (Selbstmodifikation). Im gedruckten Artikel steht dafür
`CALL $-$`. /
One detail worth noting: `DRIVER: CALL 0000H` is a **deliberate placeholder**.
Its operand is overwritten at load time by `LD (DRIVER+1),HL` with the
original keyboard vector from `4016H` (self-modifying code). The printed
article writes this as `CALL $-$`.

---

## Dateien / Files

| Datei / File | Beschreibung / Description |
|---|---|
| [`kbdhrg.z80`](./kbdhrg.z80) | Binär-verifizierter Z80-Quelltext / binary-verified Z80 source |
| `KBDHRG/CMD` | Original-Binär (auf Diskette) / original binary (on disk) |
| `HRGDOS/CMD` | gepatchter RB-Electronic HRG-Supertreiber / patched HRG super-driver |

Eine DMK-Diskette mit dem Z80-Quelltext ist geplant. /
A DMK disk image carrying the Z80 source is planned.

---

## Herkunft & Verifikation / Provenance & verification

Der Treiber wurde 1989 von Egbert Schröer geschrieben und im Januar 1990 in
Club-80, Heft 29 (S. 12–17) veröffentlicht. Der vollständige Artikeltext (deutsch und
englisch) steht weiter unten. /

The driver was written by Egbert Schröer in 1989 and published in January
1990 in Club-80, Heft 29 (pp. 12–17). The full article (German and English) appears
below.

**Fundort des Binärs / where the binary was found:** `KBDHRG/CMD` liegt auf
den Disketten **esnd-01** und **NEWDOS80**. Beide zeigen identische
Verzeichnislisten (gleiche 45 Dateien, gleiche Reihenfolge, gleiche
Geometrie) und sind mit hoher Wahrscheinlichkeit dieselbe Diskette, zweimal
abgebildet. /
`KBDHRG/CMD` is present on disks **esnd-01** and **NEWDOS80**. Both show
identical directory listings (same 45 files, same order, same geometry) and
are very likely the same disk imaged twice.

**Verifikation / verification:** [`kbdhrg.z80`](./kbdhrg.z80) wurde Byte für
Byte aus `KBDHRG.CMD` dekodiert (Ladeblock 128 Byte, `DA84H`–`DB03H`,
Transfer-Adresse `DA84H`, AKKU-Zelle `DB04H`) und gegen Listing 1 des
Artikels abgeglichen. **Der assemblierte Bytestrom stimmt vollständig
überein — keine Abweichungen.** Nur der Bytestrom ist prüfbar; Label-Namen,
Kommentare und Direktiven stammen aus dem gedruckten Quelltext. /
[`kbdhrg.z80`](./kbdhrg.z80) was decoded byte-for-byte from `KBDHRG.CMD` and
cross-checked against Listing 1 of the article. **The assembled byte stream
matches completely — no discrepancies.** Only the byte stream is verifiable;
label names, comments and directives come from the printed source.

---

## Der Artikel — Club-80, Heft 29 (1990), deutsche Originalfassung

> Quelle: Club-80, Heft 29, Januar 1990, S. 12–17. Transkribiert aus dem Original-Scan.

### Modifikation des HRG Treibers von RB-Elektronik
#### Umlaute mit NewDos/80 Vers. 2.0; neuer Tastaturtreiber

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

---

## The article — Club-80, Heft 29 (1990), English translation

> Source: Club-80, Heft 29, January 1990, pp. 12–17. Translated from the original German.
> Translation provided for accessibility; the German text above is authoritative.

### Modifying the RB-Elektronik HRG driver
#### Umlauts with NewDos/80 v2.0; a new keyboard driver

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

## Listings 2 & 3 (HRG-Supertreiber / HRG super-driver)

Listing 1 (der Tastaturtreiber) liegt binär-verifiziert als
[`kbdhrg.z80`](./kbdhrg.z80) vor. Die folgenden Listings 2 und 3 dokumentieren
den HRG-Supertreiber und die Patches; sie stammen aus dem gedruckten Artikel
und sind **noch nicht** gegen `HRGDOS/CMD` abgeglichen. Einige Hex-Operanden
im Scan sind unsicher. /

Listing 1 (the keyboard driver) is provided binary-verified as
[`kbdhrg.z80`](./kbdhrg.z80). Listings 2 and 3 below document the HRG
super-driver and the patches; they come from the printed article and are
**not yet** verified against `HRGDOS/CMD`. Some hex operands in the scan are
uncertain.

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