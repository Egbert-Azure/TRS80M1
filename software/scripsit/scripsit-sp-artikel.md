<!-- /software/scripsit/scripsit-sp-artikel.md — Neufassung, 2026. Nicht der Originaltext von 1988. -->

# SCRIPSIT/SP — eine deutsche Scripsit-Modifikation

**Was von Craig Lindley stammt, was nicht, und warum**

*Englische Fassung: [`scripsit-sp-article-en.md`](./scripsit-sp-article-en.md) · Belege: [`scripsit-provenance.md`](./scripsit-provenance.md) · Index: [`README.md`](./README.md).*

> **Vorbemerkung zur Fassung.** Der Originalartikel (Club-80, SONDERINFO 27.5, 1988) ist
> verschollen. Dies ist **keine Rekonstruktion jenes Textes**, sondern eine Neufassung von 2026.
> Der Rückblick in Abschnitt 1 stammt aus meiner Erinnerung und ist als solche zu lesen. Alle
> technischen Angaben dagegen sind aus den Binärdateien abgeleitet — `SCRIPSIT/CMD`,
> `SCRIPSIT/SP`, `WP/CMD` (aus `esnd-04.dmk`), `wp.cmd` (Lindleys Fassung) — und nicht aus dem
> Gedächtnis. Wo etwas unsicher ist, steht es dabei.

---

## 1. Wie es dazu kam

1988. Vor mir ein Stapel alter 80-Micro-Hefte — für mich die einzige Zeitschrift, die wirklich
etwas taugte.

Das waren die Jahre, in denen man Programme aus der Zeitschrift abtippte. Ein mühsames
Geschäft: Zeile für Zeile, Hexzahl für Hexzahl, und ein einziger Zahlendreher kostete einen
Abend. Aber man lernte dabei etwas, das man beim bloßen Benutzen nie lernt — man ging durch
fremden Code hindurch, statt an ihm vorbei.

Gerade fertig geworden war ich mit zwei Sachen: NEWDOS zu einem HRG-DOS erweitert, und einen
deutschen Tastaturtreiber geschrieben. Umlaute gab es unter NEWDOS nämlich nicht. Nicht
schlecht gelöst, nicht umständlich zu erreichen — schlicht nicht vorhanden.

Bei Scripsit 1.0 (Radio Shack, 1979) war es dasselbe, nur ärgerlicher, weil es ja ein
Textsystem ist. Die Codes 5BH, 5CH, 5DH, 7BH, 7CH, 7DH und 7EH, die im deutschen
7-Bit-Zeichensatz Ä Ö Ü ä ö ü ß tragen, belegt Scripsit selbst — teils als Bildschirm-Marken,
teils gar nicht. Und dem Drucker ein beliebiges Steuerbyte zu schicken war überhaupt nicht
vorgesehen.

Craig A. Lindleys Artikelserie *"Inside Scripsit"* in 80 Micro nahm ich als Ausgangspunkt.
Nicht als Vorlage zum Abtippen und Gutsein-lassen, sondern als Einstieg: er zeigte, wo man in
Scripsit hineinkommt. Darauf ließ sich aufbauen — neue Funktionen, ein deutscher Umlauttreiber,
insgesamt eine Auffrischung. Das Verzeichnis lesen zu können, ohne Scripsit zu verlassen, war
so eine Sache, die man einmal gehabt hat und danach nicht mehr missen will.

Was daraus wurde, besteht aus **zwei Schichten**, die getrennt voneinander funktionieren:

| | | |
|---|---|---|
| **Schicht A** | `SCRIPSIT/SP` | statischer Patch **in der Programmdatei**. Umlaute, Druckersteuerung. Läuft auch ohne WP. |
| **Schicht B** | `WP/CMD` | Lader, der Scripsit **im RAM** patcht. Neue BREAK-Kommandos, Cursor-Funktionen. |

Schicht B geht auf eine fremde Arbeit zurück. Schicht A nicht.

Das gilt auch für die Verzeichnisanzeige aus dem Rückblick oben: sie stammt von Lindley
(`QUERY`), nicht von mir. Ich habe sie übernommen und vereinfacht. Neu ist sie nur gegenüber
Scripsit — nicht gegenüber der Vorlage.

---

## 2. Die Herkunft: Craig A. Lindley

Craig A. Lindley beschrieb in *"Inside Scripsit"* (80 Micro, Teil II: Oktober 1982) ein
Patch-Programm, das Scripsit nach dem Laden im Speicher verändert. `WP/CMD` ist eine
**Portierung dieses Programms**, keine Anregung daraus. Das gehört offen gesagt.

Inzwischen liegt eine zweite Abschrift seines Listings vor, womit die offene Frage geklärt ist:
sie stimmt mit dem in der Zeitschrift abgedruckten Objektcode überein. Der Abdruck ist damit die
Referenz, und was ich abgetippt habe, ist daran messbar.

Der Nachweis ist einfach: jeder Einhängepunkt, den `WP/CMD` benutzt, liegt auf Lindleys
Adresse. Die Installationsroutine ist seine, Zeile für Zeile:

| Lindley | in `WP/CMD` |
|---|---|
| 13 × Textpuffer-Basis setzen | ✅ dieselben 13 Stellen |
| `C3` → 6155 + Tastatur-Fix → 6156 | ✅ |
| `C3` → 7A9E + Unterstreichung → 7A9F | ❌ **entfallen** |
| `C3` → 5FAF + Bildschirm-Marke → 5FB0 | ✅ |
| `C3` → 73A2 + Druckerpause → 73A3 | ✅ |
| `C3` → 5E16 + Datei-Meldung → 5E17 | ✅ |
| Tabellen-Erweiterung → 52F8 / 6466 | ✅ |
| `RETURN` → 6595 | ❌ **entfallen** |
| Rollroutinen → 79D9 / 79D7 / 79BF | ✅ |
| `14H` → 79AA (Tabulator umlegen) | ✅ |
| Kennzeile ins RAM kopieren → 57F7 | ❌ **entfallen** |

Von Lindley stammt auch der eigentliche Kunstgriff: die Erkenntnis, dass Scripsits eigene
Tabellensuche bei **58F0H** wiederverwendbar ist, und dass die beiden *"unbekanntes
Kommando"*-Ausgänge bei 52F7H und 6466H sich in drei Bytes auf eigene Tabellen umbiegen lassen.
Die Erweiterung kann das Original nicht beschädigen, weil sie im Fehlerfall auf denselben
Fehlerausgang zurückfällt. Das ist sein Entwurf.

Ebenso von ihm: der Wiedereinsprung. Das Kennbyte liegt **ein Byte hinter dem letzten geladenen
Byte** und überlebt deshalb das Nachladen des Patches. In seiner Quelle steht dafür schlicht
`TSTBYT EQU $`.

### Was hinzukam

Genau eine Erweiterung, und die ist belegt. Lindley begrenzt `BREAK X=` auf Codes 1–31:

```
8131  FE20    CP    20H     ;NUM LESS THAN 32 ?
```

In `WP/CMD` steht an der entsprechenden Stelle (80C7H) `CP 0FFH`. Damit sind Codes 1–255
möglich — so, wie es die Bedienungsanleitung SCRIPSIT/SP beschreibt. Für einen Drucker, der
mehr als die reinen ASCII-Steuercodes braucht, ist das der Unterschied zwischen brauchbar und
unbrauchbar.

Alles Übrige, was an Schicht B geändert wurde, war **Weglassen**: die Verzeichnisanzeige wurde
von Lindleys ausführlicher Form (freie Granulen, Datum, acht Verzeichnissektoren) auf `DIR 0`
bis `DIR 2` eingedampft, und der Textpuffer beginnt entsprechend früher — bei 81A1H statt
8342H.

---

## 3. Schicht A: SCRIPSIT/SP

Hier gibt es keine Vorlage. Lindley fasst die Programmdatei nie an; sein Patch lebt
ausschließlich im RAM. `SCRIPSIT/SP` ist dagegen eine **veränderte Programmdatei**.

### Das Bauprinzip

Jeder Eingriff im Programmkörper ist ein **längentreuer Austausch**:

```
32 E8 37    LD (37E8H),A   →   CD 6C FF    CALL 0FF6CH
3A E8 37    LD A,(37E8H)   →   CD CB FF    CALL 0FFCBH
```

Drei Bytes gegen drei Bytes. Keine Adresse in Scripsit verschiebt sich. Vierzehn Stellen, alle
nach demselben Muster. Der gesamte neue Code liegt in den obersten 148 Bytes des Speichers
(FF6CH–FFFFH) plus 39 Bytes bei 7A7DH.

### Umlaute

Die Übersetzung hängt bei 615DH ein — dort, wo Scripsit die mit @ gedrückte Taste in einen
Steuercode umsetzt. Tabelle bei FFCFH, Ergebnis 16 Bytes weiter bei FFE0H:

| Taste | Code | Zeichen |
|---|---|---|
| `@A` `@O` `@U` | 5B 5C 5D | Ä Ö Ü |
| `@a` `@o` `@u` | 7B 7C 7D | ä ö ü |
| `@:` | 7E | ß |
| `@p` | 7F | schraffiertes Quadrat |

```
FFAC  LD HL,0FFCFH / LD BC,17 / CPIR
      JR NZ,FFC3
      LD BC,16 / ADD HL,BC / LD A,(HL)
      CP 7EH / JP C,6167H      ; Umlaute: Groß/Klein-Umschaltung
      JP 6179H                 ; ß und 7FH umgehen sie
FFC3  CP 41H / JP C,6167H      ; Originalcode, unverändert
      JP 6161H
```

Der Vergleich mit 7EH ist nötig, weil 6167H ein `XOR 20H` ausführt. Ä/ä sollen davon erfasst
werden, ß und das Quadrat nicht.

**Der weniger offensichtliche Teil:** 5BH, 5CH und 5DH waren nicht frei. Scripsit zeigte damit
eigene Marken an. Die Übersetzungstabelle bei 7966H musste geändert werden — die Marken
erscheinen jetzt als Grafikblöcke 97H, A6H und ADH. Ohne diesen Schritt kollidieren Marken und
Umlaute auf dem Bildschirm.

### Druckersteuerung: @p und zwei Hexziffern

Das eigentliche Stück Arbeit. `@p` erzeugt 7FH; die beiden folgenden Zeichen werden als
Hexziffern gelesen und als **ein** Byte an den Drucker gegeben:

```
FF6C  PUSH HL / PUSH BC / PUSH AF
      LD HL,0FFAAH        ; FFAA = Zähler, FFAB = Sammelbyte
      LD A,(HL) / AND A / JR NZ,FF96
      POP AF / PUSH AF
      CP 7FH / JR Z,FF92
      LD HL,0FFE2H / LD BC,15 / CPIR    ; Drucker-Übersetzung
      JR NZ,FF8B
      LD BC,14 / ADD HL,BC / LD A,(HL)
FF8B  LD (37E8H),A                      ; einziger direkter Portzugriff
      POP AF / POP BC / POP HL / RET
FF92  LD (HL),2 / JR FF8E               ; @p: zwei Ziffern erwarten
FF96  POP AF / PUSH AF
      CP 3AH / JR C,FF9E / SUB 7        ; ASCII-Hex → Nibble
FF9E  SUB 30H
      INC HL / RLD / LD A,(HL) / DEC HL ; Nibble einschieben
      DEC (HL) / JR NZ,FF8E
      JR FF8B                           ; zweite Ziffer: Byte ausgeben
```

`RLD` schiebt ein Nibble aus A in `(HL)` und das alte obere Nibble zurück nach A. Zweimal
angewandt setzt es zwei Hexziffern zu einem Byte zusammen — ohne Schiebeschleife, ohne
Zwischenregister. Der Befehl ist genau dafür gemacht und wird selten so gebraucht.

Der Preis steht in der Anleitung: aus drei Bildschirmzeichen wird ein Druckerbyte, die
Zeichenzählung kann daher durcheinandergeraten.

### Drucker-Übersetzungstabelle

FFE2H (Quelle) → FFF1H (Ziel), 15 Einträge, ab Werk **identisch abgebildet**. Wer einen Drucker
mit deutschem Zeichensatz hat, lässt sie in Ruhe. Wer keinen hat, trägt bei FFF1H ein, was sein
Gerät versteht. Das ist die vorgesehene Stellschraube.

### Woher der Speicher kommt

Scripsit bemisst seinen Textpuffer beim Kaltstart selbst: `LD HL,(4049)` bei 5260 liefert die
Obergrenze, bei 5276 steht die Untergrenze fest verdrahtet auf 7F62H.

4049H ist der Speicherobergrenzen-Zeiger. Der Ladesatz von `SCRIPSIT/SP` trägt dort **FF6BH**
ein — ein Byte unter dem Treiber bei FF6CH. Scripsit legt seinen Puffer daraufhin bis FF6B an und
rührt nichts darüber an. Dafür wird nichts gepatcht; es nutzt Scripsits eigenen Startcode.

**Das ist der Unterschied zu Lindley, und zwar der ganze.** Er lädt sein Programm nach
7F62H–8342H, also *in* den Puffer, und muss deshalb anschließend dreizehn Zeiger umschreiben, um
die Untergrenze hochzuschieben — das kostet rund 960 Bytes Dokumentplatz. Sein Artikel sagt das
auch.

Schicht A verschiebt stattdessen die Obergrenze. Das kostet nichts. Dasselbe Problem, vom anderen
Ende her — und genau deshalb zählt die Drei-Bytes-gegen-drei-Bytes-Regel: sie erreicht Code bei
FF6CH, ohne ein einziges Byte von Scripsit zu verschieben.

### FFCB und das `DI` bei 52C0

`FFCBH` ist nur `LD A,(37E8H) / RET` — ein Durchreicher. Sein Zweck ist, dass **jeder**
Druckerzugriff über einen Einhängepunkt läuft. *(Wirkung sicher, Absicht erschlossen.)*

Bei 52C0H, dem Kopf der Hauptschleife, steht statt `NOP` ein `DI`. Damit bleiben die Interrupts
in der Editorschleife gesperrt — der Treiber liegt bei FF6CH–FFFFH, ganz oben im Speicher.
*(Wirkung sicher, Begründung erschlossen.)*

---

## 4. Was von wem stammt

Die Bedienungsanleitung SCRIPSIT/SP führt alles zusammen auf, ohne die Herkunft zu trennen. Das
sei hier nachgeholt.

| Funktion | Schicht | Herkunft |
|---|---|---|
| Umlaute `@a @o @u @A @O @U`, `@:` = ß | A | **neu** |
| `@p` + zwei Hexziffern → ein Druckerbyte | A | **neu** |
| Drucker-Übersetzungstabelle FFE2→FFF1 | A | **neu** |
| Marken von 5B/5C/5D auf Grafikblöcke verlegt | A | **neu** |
| Druckunterdrückung gibt Leerzeichen statt nichts | A | **neu** |
| `BREAK X=nnnn`, Codes **1–255** | B | Lindley, **erweitert** (er: 1–31) |
| `BREAK Qn` Verzeichnis | B | Lindley, vereinfacht |
| `KILL` / `K dateiname` | B | Lindley |
| `BREAK N` / `New` | B | Lindley |
| `SHIFT P` Druckerpause | B | Lindley |
| `@h` Cursor Home | B | Lindley |
| `@→` / `@←` Wortsprung | B | Lindley |
| `@` Auf-/Abpfeil: Fenster 13 Zeilen | B | Lindley |
| `@f` / `@b`: Cursor 13 Zeilen | B | Lindley |
| Wiedereinsprung `WP SP*` | B | Lindley |
| `NEW FILE!` / `FILE UPDATED!` | B | Lindley |
| Silbentrennung, `BREAK H`, hot zone | — | **Scripsit selbst** |
| `@d` `@s` `@e`, Blöcke, Marken | — | **Scripsit selbst** |
| Druckformat `>PL >LM >RM >J` usw. | — | **Scripsit selbst** |

Die letzten drei Zeilen sind wichtig. Die Silbentrennung ist nicht Teil der Modifikation — die
Zeichenketten `HOT`, `ZONE` und `HYPHEN` stehen bei 6AA3H, 6AA7H und 6AB5H im **unveränderten**
Radio-Shack-Programm.

---

## 5. Wie die Schichten zusammenpassen

Beide wurden gegeneinander gebaut:

- `SCRIPSIT/SP` endet bei 7AA4H. `WP/CMD` beginnt bei 7AA7H.
- `WP/CMD` hängt bei 6155H ein und fällt auf 615DH durch — dort steht in `SCRIPSIT/SP` der
  Sprung zum Umlaut-Übersetzer.

Die Kette lautet also: `6155 → 8002 (Sondertasten) → 615D → FFAC (Umlaute) → 6167`. Keine
Schicht kennt das Innere der anderen. `SCRIPSIT/SP` läuft auch allein — unter jedem Namen, `WP`
wird dafür nicht gebraucht.

---

## 6. Eine Baustelle

Lindleys Unterstreichung hängt bei **7A9EH** ein. `SCRIPSIT/SP` verlängert den 7A00H-Block von
126 auf 165 Bytes — also bis 7AA4H, und damit **über 7A9EH hinweg**. Der Platz war weg. Die
Druckerhälfte der Unterstreichung entfiel deshalb.

Die Bildschirmhälfte blieb: bei 5FAFH wird 40H weiterhin als 5FH dargestellt — im Betrieb
bestätigt, `SHIFT`-0 erzeugt ein anderes Zeichen als das schraffierte Quadrat von `@p`. Die Marke
ist also sichtbar, bewirkt beim Drucken aber nichts mehr. Die Bedienungsanleitung erwähnt
Unterstreichung folgerichtig gar nicht. Ob das eine bewusste Streichung oder ein übersehener Rest
war, ist eine Frage nach meiner Absicht von 1988. Die Bytes beantworten sie nicht, und ein Test
auch nicht.

---

## 7. Die drei sonderbaren Änderungen

Ermittelt, indem verfolgt wurde, wofür die Adressen innerhalb von Scripsit verwendet werden.

**5DCCH — ein Fehler in Radio Shacks Scripsit.** Im Originalprogramm wird 7CB6H bei 5DCC
geschrieben und nirgends gelesen; 7CB9H wird bei 5D47 und 7A6E gelesen und nirgends geschrieben.
1979 hat jemand die falsche Adresse getippt, und der Leser griff ab, was gerade dort stand. Das
Schreiben nach 7CB9H verbindet beide. Die Umstellung ergibt sich daraus: das Original verlässt
sich darauf, dass `OR A` die Flags für `CALL NZ` setzt, speichert also zuerst; der Patch ruft
zuerst, lädt `LD A,C` neu (5DEF überschreibt A) und speichert dann — bezahlt mit dem `NOP` bei
5DD2.

**7A20H / 7A22H — die Seitenvorgaben.** Der 20-Byte-Block bei 7A15H wird beim Start nach 7C64H
kopiert. 7C6FH ist `BM` (Unterer Rand, 60), 7C71H ist `PL` (Seitenlänge, 66) — bestätigt durch die
Anweisungsroutinen bei 766EH und 7798H. Beide auf 127 gesetzt. 66 Zeilen sind US-Letter bei 6 lpi;
A4 braucht etwa 72, und die Anleitung beginnt mit `PL=72 BM=66`. Höhere Vorgaben verhindern, dass
ein Text ohne Angabe am amerikanischen Seitenende umbricht. *(Zuordnung sicher, Begründung
erschlossen.)*

**603AH / 6056H — ohne Wirkung.** Das sind selbstmodifizierende Displacement-Bytes: die
Ringindizes eines 32-Byte-Tastaturpuffers bei 7E11H. Der Kaltstart nullt beide bei 5254/5257,
bevor der Puffer benutzt wird — die Änderung erreicht die Laufzeit nie.

## 8. Nachweis

Alle Aussagen sind gegen die Binärdateien geprüft. Ergänzend:

- Die Abschrift, mit der ich gearbeitet habe (`wpand.scr`, EDTASM-Format), wurde mit einem eigens geschriebenen Assembler
  übersetzt: **1336 Bytes, identische Adressabdeckung mit `wp.cmd`, fünf abweichende Bytes.**
  `START` = 7B49H, `TXTBUF` = 8342H, `TSTBYT` = 7C21H — jeweils genau das, was die Binärdatei
  verlangt.
- Von den fünf Bytes betrifft eines Zeile 5020 (`CP 20H` → `CP 0FFH`), zwei die
  Unterstreichungscodes in den Zeilen 550/560 — beides meine Änderungen. Die restlichen zwei
  betreffen das `LOUT`-Ziel, wo `wpand.scr` mit Lindleys eigener Quelle übereinstimmt (4467H);
  nur die Archivfassung seines Binärprogramms trägt 4476H.
- Das vollständige Listing 1 liegt vor. Gegen Objektcode-Stichpunkte über das ganze Listing
  stimmt `WP.ASM` an **68 von 68**, `wpand.scr` an **65 von 68** — die drei Abweichungen sind genau
  meine Änderungen, sonst nichts. Eine Zeile (5670) liegt in einem Abschnitt, der sich auf dem Scan
  nicht sicher lesen ließ, und bleibt ungeprüft. Listing 2 ist der Modell-III-Patch und für ein
  Modell-I-Programm ohne Belang.
- `WP/CMD` wurde aus `esnd-04.dmk` neu ausgelesen, nachdem eine frühere Extraktion 883 Bytes
  `E5`-Füllung geliefert hatte. Die Plattengeometrie: `Sektor = 36 + Lump·10 + Granule·5`,
  Lump = 10 Sektoren, Granule = 5, GPL = 2, Zylinder 0 ausgenommen, Verzeichnis auf Spur 6.

**Fazit.** Schicht B ist eine Portierung fremder Arbeit mit einer Erweiterung. Der Verweis auf
Lindley gehört dorthin und ist keine Höflichkeit, sondern eine Feststellung. Schicht A ist
eigenständig — und sie ist der Teil, der Scripsit überhaupt erst deutsch macht.

*Egbert Schroeer*
