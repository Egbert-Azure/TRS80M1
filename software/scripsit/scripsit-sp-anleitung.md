<!-- /software/scripsit/scripsit-sp-anleitung.md — readable transcription of SCRIPSIT/TXT -->
<!-- (c) E. Schroeer -->

# SCRIPSIT/SP — Bedienungsanleitung (1988)

*Transkription von [`src/SCRIPSIT.TXT`](./src/SCRIPSIT.TXT) · English: [`scripsit-sp-manual-en.md`](./scripsit-sp-manual-en.md) · Artikel: [`scripsit-sp-artikel.md`](./scripsit-sp-artikel.md) (DE) · [`scripsit-sp-article-en.md`](./scripsit-sp-article-en.md) (EN) · Index: [`README.md`](./README.md)*

> **Abgeleitete Datei.** Der kanonische Bestand ist `src/SCRIPSIT.TXT`, das originale
> Scripsit-Dokument vom Oktober 1988, byte-genau. Diese Fassung macht es nur lesbar: die
> TRS-80-Umlautcodes (`5B 5C 5D 7B 7C 7D 7E`) sind nach UTF-8 abgebildet, Scripsits
> Absatzmarken zu Zeilenumbrüchen aufgelöst, die `E5`-Sektorfüllung entfernt. Die
> Spaltenausrichtung der Kommandolisten ist zu Tabellen geworden — auf 66 Spalten war sie
> genau das. **Der Wortlaut ist unverändert**, einschließlich der Tippfehler; siehe die
> Anmerkungen am Fuß.

---

## Bedienungsanleitung für SCRIPSIT/SP

**einer Scripsit Modifikation mit neuen Kommandos und Umlauterweiterung**

&copy; by Egbert Schröer, Oktober 1988

*(Bei diesem Text ist `W=66` einzustellen. Die Titelseite wird in doppelter Breite, kursiv und
NLQ gedruckt — siehe die Anmerkung zu den Druckersteuerzeichen am Fuß.)*

---

## Kommandos während der Texteingabe am Bildschirm

| Taste | Wirkung |
|---|---|
| Pfeiltasten | Cursor bewegen |
| SHIFT Rechtspfeil | Cursor zum Zeilenende |
| SHIFT Linkspfeil | Cursor zum Zeilenanfang |
| SHIFT Aufpfeil | Cursor zum Textanfang |
| SHIFT Abpfeil | Cursor zum Textende |

## Arbeiten mit der 'Control'-Taste = @ (Klammeraffe)

| Funktion | Tasten |
|---|---|
| Window (Fenster)-Kdo | `@ w`, CLEAR hebt auf |
| Bildsch.-Anf anspringen | `@` Hochpfeil |
| Tab-Marke anspringen | `@ t` |
| Zeichen löschen | `@ d` |
| Wort löschen | `@ d`, `@ z` |
| Satz löschen | `@ d`, `@ x` |
| Blanks löschen | `@ d`, `@ f` |
| Abschnitt löschen | `@ d`, `@ c`, y/n |
| Block löschen | Cursor auf Blockstart-Marke: `@ d`, `d` |
| Blockmarken löschen | Cursor auf Blockstart-Marke: `@ d`, `u` |
| Bis Textende löschen | `@ d`, Abpfeil |
| **Wiederholkommando** | `@ r`, Zahl eingeben, dann Kommando |
| Wort austauschen | Cursor auf 2. Wort: `@ e`, `@ z` |
| Abschnitt austauschen | Cursor auf 2. Abschn.: `@ e`, `@ c` |
| Block austauschen | Cursor auf 2. Block: `@ e`, `@ q` |
| Zeichen einfügen | Cursor an Stelle: `@ s`, Zeichen |
| Zeile einfügen | Cursor an Stelle: `@ s`, `@ x`, dann Text, dann CLEAR |
| Block einfügen | Cursor an Stelle: `@ s`, `@ q`, dann Kennbuchstabe des Blocks |
| Cursor Home (links oben) | `@ h` |
| Cursor zum Anfang des nächsten Wortes | `@` Rechtspfeil |
| Cursor zum Ende des letzten Wortes | `@` Linkspfeil |
| Window Scroll 13 Zeilen rückw. zum Textanfang | `@` Aufpfeil |
| Window Scroll 13 Zeilen vorw. | `@` Abpfeil |
| Cursor 13 Zeilen rückw. | `@ f` |
| Cursor 13 Zeilen vorw. | `@ b` |

Wie Sie festgestellt haben werden, gibt es hier ein System:

```
d  =  Zeichen für löschen     (delete)
s  =  Zeichen für einfügen    (insert)
e  =  Zeichen für austauschen (exchange)

z  =  Zeichen für Wort
x  =  Zeichen für Satz oder Zeile
c  =  Zeichen für Abschnitt
q  =  Zeichen für Block
```

| Marke | Tasten |
|---|---|
| Textbegrenzungs-Marke | ENTER |
| Abschnittende-Marke | `@ c` (`-` erscheint) |
| Seitenende-Marke | `@ v` (eine Marke erscheint) |

CLEAR-Taste unterbricht alle Funktionen.

## Arbeiten mit der Kommando-Ebene

In die Kommando-Ebene kommt man mit der BREAK-Taste.

| Kommando | Bedeutung |
|---|---|
| `?W` | Bildbreite am Monitor anzeigen |
| `?L` | Länge des Textes anzeigen in Anzahl Buchstaben |
| `?M` | restlichen Speicherplatz anzeigen in Buchstaben |
| `?C` | Zeilen-Nummer anzeigen, in der der Cursor steht |
| `?N` | Text-Speicher-Name anzeigen |
| `P` | drucken (print) |
| `P,P` | drucken mit Einzelblättern |
| `P,I` | drucken ohne Format mit allen unsichtbaren Zeilen |
| `S` | `S XXXXXX/xxx:1` (speichern) oder nur `S` wenn Current File |
| `S,A` | wie oben, nur in ASCII |
| `L` | `L XXXXXX/xxx:1` (laden) oder nur `L` wenn Current File |
| `L,C` | `L,C XXXXXX/xxx` — laden und an vorhandenen Text anfügen |
| `T` | `T=1,5,10` (Tab auf 1,5,10 setzen) |
| `TAB` | alle Tabulatoren löschen |
| `TS` | Tabulator setzen, wo vorher der Cursor stand |
| `TC` | Tabulator löschen, wo vorher der Cursor stand |

## Silbentrennung

Silbentrennung geschieht außschließlich in einem 'Block' mit reserviertem Block-Namen `-`. Nach
Abgrenzung dieses Blocks startet `BREAK H` ENTER den Silbentrennungsvorgang.

'Hot zone' meint die Mindest-Anzahl ungenutzter Spalten, die in der Zeile existieren müssen, um
zur potentiellen Nutzung durch einen Teil des ersten Wortes der nächsten Spalte angeboten zu
werden. Nach deren Spezifikation wird jegliche alte Silbentrennung rückgängign gemacht.

| Taste | Wirkung |
|---|---|
| CLEAR | (weitere) Silbentrennung abbrechen |
| ENTER | (hier) verweigern |
| `-` | an der Cursor Position trennen |

## Definieren von Blöcken

| Marke | Tasten |
|---|---|
| Blockstart-Marke allgemein | `@ q`, dann Buchst. außer H, F, P |
| Blockstart-Marke Kopf | `@ q`, `h` |
| Blockstart-Marke Fuß | `@ q`, `f` |
| Blockstart-Marke Silben-Tr. | `@ q`, `-` |
| Blockstart-Marke Seiten-Nr. | `@ q`, `P#####` |
| Blockende-Marke | `@ q`, `@` Abpfeil |
| Kopier-Marke | Cursor auf 1. Stelle: `BREAK C`; Cursor auf le[tzte] Stelle: `BREAK C`. Nur dazwischen wird gedruckt. |

## Druckformatanweisungen

| | |
|---|---|
| `PL` | Seitenlänge (66 voreingestellt) auf 72 einstellen |
| `LM` | Linker Rand (12 voreingestellt) auf 8 einstellen |
| `RM` | Rechter Rand (72 voreingestellt) |
| `TM` | Oberer Rand (6 voreingestellt) |
| `BM` | Unterer Rand (60 voreingestellt) auf 66 einstellen |
| `LS` | Zeilenabstand (1 voreingestellt) |
| `PF` | Zeilenabstand zwischen Abschnitten (1 voreingestellt) |
| `C` | Zentrierung horizontal (`C=Y`) |
| `FR` | Rechtsbündig (`FR=Y`) |
| `J` | Justierung rechts- und linksbündig (`J=Y`) |
| `VC` | Zentrierung vertikal (zuerst angeben) |
| `P` | Druckunterdrückung (`P=N` voreingestellt) |
| `PN` | Start mit Seiten-Nr. (`PN=5`) |
| `H` | Ein-/Ausschalten des Kopfblockes (`H=N` / `H=Y`) |
| `F` | Ein-/Ausschalten des Fußblockes (`F=N` / `F=Y`) |
| `WS` | Randunterdrückung (Druck 1. Zeile eines Abschn. als letzte Zeile einer Seite wird unterdrückt) |

### Allgemeine Bemerkungen zu Druckformat-Anweisungen

Eingabe am Anfang einer Zeile und ein `>` davor. Es sind mehrere Eingaben möglich, die durch ein
Komma oder ein Blank voneinander getrennt werden müssen. Alle Eingaben müssen in Großbuchstaben
erfolgen und bleiben so lange erhalten, bis sie geändert werden.

Druckformat-Anweisungen, die ein Seiten-Format beeinflussen, wie z.B. justiert (`>J=Y`), müssen
immer am Anfang des Textes oder nach einer Seitenende-Marke erfolgen.

Folgendes ist noch zu beachten:

```
Zentrierung   (>C =Y) überschreibt nachfolgende Anweisungen
Rechtsbündig  (>FR=Y) überschreibt nachfolgende Anweisungen
Justierung    (>J =Y) überschreibt linksbündig
Linksbündig, wenn alle vorangehenden Anweisungen =N
```

### Druckunterdrückung

Man kann einige Zeilen beim Drucken übergehen, wenn man davor setzt: `>P=N` und am Ende setzt:
`>P=Y`. Vor und nach jeder Anweisung muß eine Textbegrenzungsmarke stehen.

### Zentrierung

Wie Sie sehen, kann mit der Anweisung `>C=Y` ein Text in der Mitte zentriert werden. Dies wird
mit `>C=N` wieder gelöscht. Am Ende einer Zeile kann eine Textbegrenzungsmarke stehen.

### Drucken rechtsbündig

Wie Sie sehen, kann mit der Anweisung `>FR=Y` ein Text rechtbündig gedruckt werden und mit
`>FR=N` wieder gelöscht werden.

### Bemerkung zum Drucken justiert

Es kann ein Text beidseitig bündig gedruckt werden, wenn man in der davorliegenden Zeile `>J=Y`
angibt. Es sollte jedoch darauf geachtet werden, daß die Zeilen am Bildschirm einigermaßen voll
sind, um nicht zu viele große Zwischenräume entstehen zu lassen. Es sollte auch am Ende einer
Zeile, die nicht annähernd voll ist, eine Textbegrenzungsmarke gesetzt werden.

## Sonstiges

Die Umlaute **Ä ä Ö ö Ü ü** sowie **ß** können wie folgt erreicht werden: `@` Buchstabe oder
`@ :` für das ß, dann erscheint der Umlaut, bzw. das ß.

`SHIFT 0` ergibt `@`.

`SHIFT @` = SHIFT-Verriegelung (nur Großschreibung).

Der bisher vorliegende Text wurde außerdem vertikal zentriert gedruckt, was durch `>VC=Y`
erfolgte.

## Suchen eines Wortes

`BREAK` drücken und dann `F>xxxxxxx` (Suchwort) eingeben. Die Suche beginnt ab der Stelle, an
der der Cursor stand, bevor `BREAK` gedrückt wurde. Der Cursor springt dann auf das 1. gefundene
Wort. Bei einer erneuten Suche nach dem selben Wort genügt es, nur noch `F` einzugeben. Das
System merkt sich das Suchwort, bis es geändert wird.

## Ersetzen eines Wortes

Verfahren wie unter Suchen. Nur anstatt `F` ein `>xxxxxxx>zzzzzzz` eingeben.

## Löschen eines Wortes

Verfahren wie unter Suchen. Nur anstatt `F` ein `D>xxxxxxxxxx` eingeben.

## Wiederholung eines Kommandos

`@ r` und dann die Anzahl der Wiederholungen (ENTER = höchstmögliche Anzahl: 255). Dann ein
Kommando. Jedes Kommando kann wiederholt werden.

## In die Modifikation wurden noch Druckersteuerungen eingebaut

Durch `BREAK X=nnnn` (n = 1–255) kann der Drucker initialisiert werden.

Die weitere Druckersteuerung ist sehr einfach aufgebaut, und kann unabhängig vom Druckertyp
verwendet werden. Bei gleichzeitigem Drücken von `@` und `p` wird der Code 7FH erzeugt, der auf
dem Bildschirm als schraffiertes Quadrat erscheint. Bei der Ausgabe auf den Drucker wird dieses
aber nicht als solches weitergegeben, sondern in Verbindung mit den folgenden beiden Bytes nur
ein Byte an den Drucker. Dieses Byte entspricht dem Wert des hinter dem `@p` in hexadezimaler
Schreibweise notierten Bytes.

Da der modifizierte Druckertreiber bei dieser Zeichenkombination aus drei ein Zeichen macht,
kommt unter Umständen die Zeichenzählung durcheinander.

## Lesen des DIRECTORY's

Durch `BREAK Qn` oder `Q n`, wobei n = Laufwerksnummer ist, kann das Directory gelesen werden.

Durch Drücken von CLEAR gelangt man wieder in den Textmodus, durch Drücken von BREAK in den
Kommando-Modus. Im Kommando-Modus bleibt das Directory auf dem Bildschirm erhalten. Es kann so
bequem eine Datei ausgesucht und geladen werden, ohne sich den Namen merken zu müssen. Danach
wird automatisch der Textmodus angesprungen.

## Löschen eines Files

`KILL` oder `K filename` löscht den Filenamen, wenn er gefunden wird.

## Druckerpause

`SHIFT P` unterbricht den Druck eines Dokumentes, CLEAR fährt fort.

## Scripsit reinitialiseren

`BREAK N` oder `New` reinitialisiert Scripsit/SP ähnlich dem Basic NEW-Befehl.

## Reentry nach END

Nach Beendigung einer Scripsit Sitzung ist ein Reentry durch Eingabe von `WP SP*` möglich. Eine
Scripsit Patch Routine überprüft, ob ein Rücksprung möglich ist.

---

## Anmerkungen zu dieser Fassung

**Druckersteuerzeichen.** `src/SCRIPSIT.TXT` enthält **siebzehn 7FH-Bytes** — das schraffierte
Quadrat, das `@p` erzeugt. Auf jedes folgen zwei Hexziffern, die der Druckertreiber bei FF6CH
mittels `RLD` zu einem Byte zusammensetzt. Die Bytes stehen fest; sie als Epson-Befehle zu lesen,
ist eine **Deutung** — abgeglichen mit dem Epson-Befehlssatz, nicht am Drucker geprüft:

| im Dokument | gesendete Bytes | Wirkung |
|---|---|---|
| `@p1B @p78 @p31` | `1B 78 31` | `ESC x 1` — NLQ ein |
| `@p1B @p34` | `1B 34` | `ESC 4` — kursiv ein |
| `@p1B @p57 @p31` | `1B 57 31` | `ESC W 1` — Doppelbreite ein |
| `@p1B @p57 @p30` | `1B 57 30` | `ESC W 0` — Doppelbreite aus |
| `@p1B @p35` | `1B 35` | `ESC 5` — kursiv aus |

Die Titelseite ist in doppelbreiter NLQ-Kursive gesetzt, und sie kommt dorthin über genau die
`@p`-Sequenz, die der Abschnitt *Druckersteuerungen* weiter oben beschreibt. Das Verfahren war
keine Demonstration — es war an dem Tag im Einsatz, an dem das Dokument entstand.

Das erklärt auch, wogegen die Zeile `>* Bei diesem Text ist W=66 einzustellen` am Kopf sichert,
und warum die Anleitung vor der Zeichenzählung warnt: aus drei Bildschirmzeichen wird ein
Druckerbyte.

**Die Seitenende-Marke.** Der Text sagt *"`@ v` (ED erscheint)"*. In der Datei steht an dieser
Stelle selbst eine `@p`-Sequenz, nicht die Buchstaben `ED`. Hier als "eine Marke erscheint"
wiedergegeben.

**Tippfehler des Originals, unverändert übernommen.** *außschließlich*, *rückgängign*,
*reinitialiseren*, *le Stelle* (für *letzte Stelle*, hier in eckigen Klammern ergänzt) — und im
Hot-Zone-Absatz *der nächsten Spalte*, wo *Zeile* gemeint ist.

**Der Schluß.** Das Dokument endet damit, daß der Abschnitt *Reentry nach END* noch einmal
beginnt und mitten im Satz abbricht, gefolgt von 154 Bytes `E5`-Sektorfüllung. So ist die Datei.
Nichts davon wurde ergänzt oder geglättet.

**Herkunft.** Die Datei stammt von **`esnd-05.dmk`**. Auf `esnd-04.dmk` liegt sie nicht. Die
hier vorliegende Kopie wurde direkt geliefert und nicht aus dem Diskettenabbild neu ausgelesen.

10650 Bytes wie geliefert, davon die letzten 154 `E5`-Füllung.
