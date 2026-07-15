<!-- /software/scripsit/scripsit-sp-anleitung.md — readable transcription of SCRIPSIT/TXT -->
<!-- (c) E. Schroeer -->

# SCRIPSIT/SP — Bedienungsanleitung (1988)

*Transcription of [`SCRIPSIT.TXT`](./SCRIPSIT.TXT) · Article: [`scripsit-sp-artikel.md`](./scripsit-sp-artikel.md) (DE) · [`scripsit-sp-article-en.md`](./scripsit-sp-article-en.md) (EN) · Index: [`README.md`](./README.md)*

> **This is a derived file.** The canonical artefact is `SCRIPSIT.TXT`, the original Scripsit
> document, byte-exact. This transcription only makes it readable: the TRS-80 German 7-bit codes
> are mapped to UTF-8 (`5B 5C 5D 7B 7C 7D 7E` → `Ä Ö Ü ä ö ü ß`), Scripsit's paragraph marks
> (`8D`, `8E`) become line breaks, page-end marks (`8C`) are shown as `[SEITENENDE]`, and the
> trailing `E5` sector fill is stripped. Nothing else is changed — spelling, spacing and the
> `>`-format directives are as written in 1988.
>
> **The `«@p → …»` tokens are not annotations.** They are the document's own printer escapes,
> in the source. See the note at the foot of this file.

---

```text
>* Anleitung zum Arbeiten mit SCRIPSIT/SP              
>* Bei diesem Text ist W=66 einzustellen
>VC=Y PL=72 LM=8 RM=74 TM=1 BM=66 LS=1 PF=2 C=N FR=N J=N PN=1 WS=Y P=N
«97»«C8»«D3»«BE»C=N J=N FR=N LM=8 RM=76             
«@p → ESC x1»Seite «97»«D0»«BE»##«9B»          Anleitung zum Arbeiten mit Scripsit/SP
«9B»
>P=Y C=N
«@p → ESC x1»
«@p → ESC 4»
«@p → ESC W1»
Bedienungsanleitung
   für
SCRIPSIT/SP

einer Scripsit Modifikation
mit neuen Kommandos
und Umlauterweiterung
«@p → ESC W0»

<c>  by Egbert Schröer, Oktober 1988
«@p → ESC 5»
>C=N

[SEITENENDE]
Kommandos während der Texteingabe am Bildschirm
-----------------------------------------------
Pfeiltasten              Cursor bewegen
SHIFT Rechtspfeil        Cursor zum Zeilenende
SHIFT Linkspfeil         Cursor zum Zeilenanfang
SHIFT Aufpfeil           Cursor zum Textanfang
SHIFT Abpfeil            Cursor zum Textende

Arbeiten mit der 'Control'-Taste = @ (Klammeraffe)
--------------------------------------------------
Window (Fenster)-Kdo     @ w, CLEAR hebt auf
Bildsch.-Anf anspringen  @ Hochpfeil
Tab-Marke    anspringen  @ t
Zeichen      löschen     @ d
Wort         löschen     @ d, @ z
Satz         löschen     @ d, @ x
Blanks       löschen     @ d, @ f
Abschnitt    löschen     @ d, @ c, y/n
Block        löschen     Cursor auf Blockstart-Marke: @ d, d
Blockmarken  löschen     Cursor auf Blockstart-Marke: @ d, u
Bis Textende löschen     @ d, Abpfeil

Wiederholkommando        @ r, Zahl eingeben, dann Kommando

Wort        austauschen  Cursor auf 2. Wort   : @ e, @ z
Abschnitt   austauschen  Cursor auf 2. Abschn.: @ e, @ c
Block       austauschen  Cursor auf 2. Block  : @ e, @ q

Zeichen     einfügen     Cursor an Stelle     : @ s, Zeichen
Zeile       einfügen     Cursor an Stelle     : @ s, @ x
                         dann Text, dann CLEAR
Block       einfügen     Cursor an Stelle     : @ s, @ q
                         dann Kennbuchstabe des Blocks

Cursor Home (links oben) @ h
Cursor zum Anfang des
nächsten Wortes          @ Rechtspfeil
       zum Ende des
letzten Wortes           @ Linkspfeil
Window Scroll 13 Zeilen
rückw. zum Textanfang    @ Aufpfeil
              13 Zeilen
vorw.  zum Textanfang    @ Abpfeil
Cursor 13 Zeilen rückw.  @ f
                 vorw.   @ b

Wie Sie festgestellt haben werden, gibt es hier ein System
d  =  Zeichen für löschen     (delete)
s  =  Zeichen für einfügen    (insert)
e  =  Zeichen für austauschen (exchange)

z  =  Zeichen für Wort
x  =  Zeichen für Satz oder Zeile
c  =  Zeichen für Abschnitt
q  =  Zeichen für Block

[SEITENENDE]
Textbegrenzungs-Marke    ENTER
Abschnittende-Marke      @ c (- erscheint)
Seitenende-Marke         @ v («@p → \xed» erscheint)

CLEAR-Taste unterbricht alle Funktionen.

Arbeiten mit der Kommando-Ebene
-------------------------------
In die Kommando-Ebene kommt man mit der BREAK-Taste.

?W   = Bildbreite am Monitor anzeigen
?L   = Länge des Textes anzeigen in Anzahl Buchstaben
?M   = restlichen Speicherplatz anzeigen in Buchstaben
?C   = Zeilen-Nummer anzeigen, in der der Cursor steht
?N   = Text-Speicher-Name anzeigen
P    = drucken (print)
P,P  = drucken mit Einzelblättern
P,I  = drucken ohne Format mit allen unsichtbaren Zeilen
S    = S XXXXXX/xxx:1 (speichern) oder nur S wenn Current File
S,A  = wie oben, nur in ASCII
L    = L XXXXXX/xxx:1 (laden)     oder nur L wenn Current File
L,C  = L,C XXXXXX/xxx  laden und an vorhandenen Text anfügen      T    = T=1,5,10 (Tab auf 1,5,10 setzen)
TAB  = alle Tabulatoren löschen
TS   = Tabulator setzen,  wo vorher der Cursor stand
TC   = Tabulator löschen, wo vorher der Cursor stand

Silbentrennung
--------------
Silbentrennung geschieht außschließlich in einem 'Block' mit reserviertem Block-Namen '-'. Nach Abgrenzung dieses Blocks startet  BREAK H Enter den Silbentrennungsvorgang.
'Hot zone' meint die Mindest-Anzahl ungenutzter Spalten, die in der Zeile existieren müssen, um zur potentiellen Nutzung durch einen Teil des ersten Wortes der nächsten Spalte angeboten zu werden. Nach deren Spezifikation wird jegliche alte Silbentrennung rückgängign gemacht.
CLEAR       (weitere) Silbentrennung abbrechen.
ENTER       (hier) verweigern.
-           an der Cursor Position trennen.
^
>* obiges Zeichen setzt Druckersteuerung außer Kraft
Definieren von Blöcken
----------------------
Blockstart-Marke allgemein   @ q, dann Buchst. außer H,F,P
Blockstart-Marke Kopf        @ q, h
Blockstart-Marke Fuß         @ q, f
Blockstart-Marke Silben-Tr.  @ q, -
Blockstart-Marke Seiten-Nr.  @ q, P#####
Blockende-Marke              @ q, @ Abpfeil
Kopier-Marke                 Cursor auf 1. Stelle: BREAK C
                             Cursor auf le Stelle: BREAK C
                             nur dazwischen wird gedruckt

[SEITENENDE]
^
Druckformatanweisungen
----------------------
PL = Seitenlänge   (66 voreingestellt) auf 72 einstellen
LM = Linker Rand   (12 voreingestellt) auf  8 einstellen
RM = Rechter Rand  (72 voreingestellt)
TM = Oberer Rand   ( 6 voreingestellt)
BM = Unterer Rand  (60 voreingestellt) auf 66 einstellen
LS = Zeilenabstand ( 1 voreingestellt)
PF = Zeilenabstand zwischen Abschnitten ( 1 voreingestellt)

C  = Zentrierung horizontal (C=Y)
FR = Rechtsbündig (FR=Y)
J  = Justierung rechts- und linksbündig (J=Y)
VC = Zentrierung vertikal (zuerst angeben)
P  = Druckunterdrückung (P=N voreingestellt)
PN = Start mit Seiten-Nr. (PN=5)
H  = Ein-/Ausschalten des Kopfblockes (H=N/H=Y)
F  = Ein-/Ausschalten des Fußblockes  (F=N/F=Y)
WS = Randunterdrückung (Druck 1. Zeile eines Abschn. als letzte                           Zeile einer Seite wird unterdrückt)
>C=Y

Allgemeine Bemerkungen zu Druckformat-Anweisungen
-------------------------------------------------
>C=N

Eingabe am Anfang einer Zeile und ein '>' davor. Es sind mehrere Eingaben möglich, die durch ein Komma oder ein Blank voneinander getrennt werden müssen. Alle Eingaben müssen in Großbuchstaben erfolgen und bleiben so lange erhalten, bis sie geändert werden.
Druckformat-Anweisungen, die ein Seiten-Format beeinflussen, wie z.B. justiert (>J=Y) müssen immer am Anfang des Textes oder nach einer Seitenende-Marke erfolgen.

Folgendes ist noch zu beachten:
Zentrierung   (>C =Y) überschreibt nachfolgende Anweisungen
Rechtsbündig  (>FR=Y) überschreibt nachfolgende Anweisungen
Justierung    (>J =Y) überschreibt linksbündig
Linksbündig, wenn alle vorangehenden Anweisungen =N

>C=Y
Druckunterdrückung
------------------
>C=N
Man kann einige Zeilen beim Drucken übergehen, wenn man davor setzt: >P=N und am Ende setzt: >P=Y. Vor und nach jeder Anweisung muß eine Textbegrenzungsmarke stehen.

>C=Y
Zentrierung
-----------
Wie Sie sehen, kann mit der Anweisung '>C=Y' ein Text
in der Mitte zentriert werden. Dies wird mit '>C=N' wieder
gelöscht. Am Ende einer Zeile
kann eine Textbegrenzungsmarke stehen.

Drucken rechtsbündig
--------------------
>C=N FR=Y
Wie Sie sehen, kann mit der Anweisung '>FR=Y'
ein Text rechtbündig gedruckt werden und mit
'>FR=N' wieder gelöscht
werden.

[SEITENENDE]
>FR=N C=Y
Bemerkung zum Drucken justiert
------------------------------
>C=N J=Y
Es kann ein Text beidseitig bündig gedruckt werden, wenn man in der davorliegenden Zeile '>J=Y' angibt. Es sollte jedoch darauf geachtet werden, daß die Zeilen am Bildschirm einigermaßen voll sind, um nicht zu viele große Zwischenräume entstehen zu lassen.  Es sollte auch am Ende einer Zeile, die nicht annähernd voll ist, eine Textbegrenzungsmarke gesetzt werden.

>C=Y
Sonstiges
---------
>C=N J=Y
Die Umlaute: ÖöÜüÄä sowie ß können wie folgt erreicht werden: @ Buchstabe oder @ : für das ß, dann erscheint der Umlaut, bzw das ß.

SHIFT 0 ergibt @.

SHIFT @ = SHIFT-Verriegelung (nur Großschreibung)

Der bisher vorliegende Text wurde außerdem vertikal zentriert ge- druckt, was durch '>VC=Y' erfolgte.

[SEITENENDE]
>VC=N

Suchen eines Wortes
-------------------
'BREAK' drücken und dann F>xxxxxxx (Suchwort) eingeben. Die Suche beginnt ab der Stelle an der der Cursor stand, bevor 'BREAK' ge- drückt wurde. Der Cursor springt dann auf das 1. gefundene Wort. Bei einer erneuten Suche nach dem selben Wort genügt es, nur noch 'F' einzugeben. Das System merkt sich das Suchwort, bis es geän- dert wird.

Ersetzen eines Wortes
---------------------
Verfahren wie unter Suchen. Nur anstatt 'F' ein >xxxxxxx>zzzzzzz eingeben.

Löschen eines Wortes
--------------------
Verfahren wie unter Suchen. Nur anstatt 'F' ein D>xxxxxxxxxx ein- geben.

Wiederholung eines Kommandos
----------------------------
@ r und dann die Anzahl der Wiederholungen (ENTER = höchstmögli- che Anzahl: 255). Dann ein Kommando. Jedes Kommando kann wieder- holt werden.

[SEITENENDE]
>VC=Y
In die Modifikation wurden noch Druckersteuerungen eingebaut:
----------------------------------------------------------------
Durch BREAK X=nnnn (n= 1-255) kann der Drucker initialisiert werden

Die weitere Druckersteuerung ist sehr einfach aufgebaut, und kann unabhängig vom Druckertyp verwendet werden. Bei gleichzeitigem Drücken von @ und p wird der Code 7FH erzeugt, der auf dem Bildschirm als schraffiertes Quadrat erscheint. bei der Ausgabe auf den Drucker wird dieses aber nicht als solches weitergegeben, sondern in Verbindung mit den folgenden beiden Bytes nur ein Byte an den Drucker. Dieses Byte entspricht dem Wert des hinter dem @p in hexadezimaler Schreibweise notierten Bytes.
Da der modifizierte Druckertreiber bei dieser Zeichenkombination aus drei ein Zeichen macht, kommt unter Umständen die Zeichenzählung durcheinander.

Lesen des DIRECTORY's
---------------------
Durch BREAK Qn oder Q n, wobei n= Laufwerksnummer ist, kann das Directory gelesen werden.
Durch drücken von CLEAR gelangt man wieder in den Textmodus, durch drücken von BREAK in den Kommando Modus.
Im Kommando Modus bleibt das Directory auf dem Bildschirm erhalten.
Es kann so bequem eine Datei ausgesucht und geladen werden, ohne sich den Namen merken zu müssen.
Danach wird automatisch der Textmodus angesprungen.

Löschen eines Files
-------------------
KILL oder K filename löscht den Filenamen, wenn er gefunden wird.

Druckerpause
------------
SHIFT P unterbricht den Druck eines Dokumentes, CLEAR fährt fort.

Scripsit reinitialiseren
------------------------
BREAK N oder New reinitialisiert Scripsit/SP ähnlich dem Basic NEW-Befehl.

Reentry nach END
----------------
Nach Beendigung einer Scripsit Sitzung ist ein Reentry durch Eingabe von WP SP* möglich.
Eine Scripsit Patch Routine überprüft, ob ein Rücksprung möglich ist.
                                                              Reentry nach END
----------------
Nach Beendigung einer Scripsit Sitzung ist ein Reentry durch Eingabe
```

---

## The manual uses the feature it documents

`SCRIPSIT.TXT` contains **seventeen `7F` bytes** — the hatched block produced by `@p`. Each is
followed by two hex digits, which `SCRIPSIT/SP`'s printer driver at FF6CH assembles into one
byte via `RLD`. Folded back together they are six Epson sequences:

| in the document | bytes sent | effect |
|---|---|---|
| `@p1B @p78 @p31` | `1B 78 31` | `ESC x 1` — near-letter-quality on |
| `@p1B @p34` | `1B 34` | `ESC 4` — italic on |
| `@p1B @p57 @p31` | `1B 57 31` | `ESC W 1` — double width on |
| `@p1B @p57 @p30` | `1B 57 30` | `ESC W 0` — double width off |
| `@p1B @p35` | `1B 35` | `ESC 5` — italic off |

The title page is set in double-width italic NLQ, and it gets there through the `@p` escape
described in the *Druckersteuerung* section of the manual itself. The escape was not a
demonstration feature — it was in use the day the document was written.

This also shows what the `>* Bei diesem Text ist W=66 einzustellen` line at the top is guarding
against, and why the manual warns that the character count can drift: three screen characters
become one printer byte.

## Provenance

`SCRIPSIT/TXT` is **not on `esnd-04.dmk`**. That disk's directory holds 18 live entries —
`SCRIPSIT/CMD`, `SCRIPSIT/SP`, `WP/CMD`, `GROSS/TXT`, `FISCH/TXT`, `UEBERSIC/TXT`,
`CENTRAL/TXT` and others — and no manual. The copy here was supplied directly; which disk it
came from is **not established**. `esnd-05.dmk` is the obvious candidate and is unexamined.

10650 bytes as supplied, of which the last 154 are `E5` fill.
