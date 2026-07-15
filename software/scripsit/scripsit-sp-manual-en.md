<!-- /software/scripsit/scripsit-sp-manual-en.md — English translation of SCRIPSIT/TXT -->
<!-- (c) E. Schroeer -->

# SCRIPSIT/SP — User Manual (1988)

*English translation · German transcription: [`scripsit-sp-anleitung.md`](./scripsit-sp-anleitung.md) · Original: [`SCRIPSIT.TXT`](./SCRIPSIT.TXT) · Index: [`README.md`](./README.md)*

> **Twice derived.** The canonical artefact is `SCRIPSIT.TXT`, the original Scripsit document
> of October 1988. This is a translation of the transcription of that file. It follows the
> original closely, including its layout and its silences; where the German is ambiguous or
> plainly a slip of the pen, there is a note at the foot rather than a silent repair.

---

## Operating manual for SCRIPSIT/SP

**a Scripsit modification with new commands and umlaut extension**

© by Egbert Schröer, October 1988

*(Set for printing with `W=66`. The title page prints in double-width italic NLQ — see the note
on printer escapes at the foot of this file.)*

---

## Commands during text entry on screen

| Key | Action |
|---|---|
| Arrow keys | move the cursor |
| SHIFT right-arrow | cursor to end of line |
| SHIFT left-arrow | cursor to start of line |
| SHIFT up-arrow | cursor to start of text |
| SHIFT down-arrow | cursor to end of text |

## Working with the 'Control' key = @ (the at-sign)

| Function | Keys |
|---|---|
| Window command | `@ w`, CLEAR cancels |
| Jump to top of screen | `@` up-arrow |
| Jump to tab mark | `@ t` |
| Delete character | `@ d` |
| Delete word | `@ d`, `@ z` |
| Delete sentence | `@ d`, `@ x` |
| Delete blanks | `@ d`, `@ f` |
| Delete paragraph | `@ d`, `@ c`, y/n |
| Delete block | cursor on block-start mark: `@ d`, `d` |
| Delete block marks | cursor on block-start mark: `@ d`, `u` |
| Delete to end of text | `@ d`, down-arrow |
| **Repeat command** | `@ r`, enter a number, then a command |
| Exchange word | cursor on 2nd word: `@ e`, `@ z` |
| Exchange paragraph | cursor on 2nd paragraph: `@ e`, `@ c` |
| Exchange block | cursor on 2nd block: `@ e`, `@ q` |
| Insert character | cursor in place: `@ s`, character |
| Insert line | cursor in place: `@ s`, `@ x`, then text, then CLEAR |
| Insert block | cursor in place: `@ s`, `@ q`, then the block's letter |
| Cursor home (top left) | `@ h` |
| Cursor to start of next word | `@` right-arrow |
| Cursor to end of previous word | `@` left-arrow |
| Scroll window 13 lines back | `@` up-arrow |
| Scroll window 13 lines forward | `@` down-arrow |
| Cursor 13 lines back | `@ f` |
| Cursor 13 lines forward | `@ b` |

As you will have noticed, there is a system to this:

```
d  =  the letter for delete
s  =  the letter for insert
e  =  the letter for exchange

z  =  the letter for word
x  =  the letter for sentence or line
c  =  the letter for paragraph
q  =  the letter for block
```

| Mark | Keys |
|---|---|
| Text-boundary mark | ENTER |
| Paragraph-end mark | `@ c` (a `-` appears) |
| Page-end mark | `@ v` (a marker appears) |

The CLEAR key interrupts every function.

## Working at the command level

You reach the command level with the BREAK key.

| Command | Meaning |
|---|---|
| `?W` | show screen width |
| `?L` | show length of text in characters |
| `?M` | show remaining memory in characters |
| `?C` | show the line number the cursor is on |
| `?N` | show the text buffer name |
| `P` | print |
| `P,P` | print with single sheets |
| `P,I` | print unformatted, with all invisible lines |
| `S` | `S XXXXXX/xxx:1` (save), or just `S` for the current file |
| `S,A` | as above, but in ASCII |
| `L` | `L XXXXXX/xxx:1` (load), or just `L` for the current file |
| `L,C` | `L,C XXXXXX/xxx` — load and append to the existing text |
| `T` | `T=1,5,10` (set tabs at 1, 5, 10) |
| `TAB` | clear all tab stops |
| `TS` | set a tab where the cursor previously stood |
| `TC` | clear a tab where the cursor previously stood |

## Hyphenation

Hyphenation happens exclusively inside a 'block' with the reserved block name `-`. Once that
block has been delimited, `BREAK H` ENTER starts the hyphenation run.

'Hot zone' means the minimum number of unused columns that must exist in the line before it is
offered for potential use by part of the first word of the next line. Once it has been
specified, any previous hyphenation is undone.

| Key | Action |
|---|---|
| CLEAR | abort (further) hyphenation |
| ENTER | decline (here) |
| `-` | hyphenate at the cursor position |

## Defining blocks

| Mark | Keys |
|---|---|
| Block-start mark, general | `@ q`, then a letter other than H, F, P |
| Block-start mark, header | `@ q`, `h` |
| Block-start mark, footer | `@ q`, `f` |
| Block-start mark, hyphenation | `@ q`, `-` |
| Block-start mark, page number | `@ q`, `P#####` |
| Block-end mark | `@ q`, `@` down-arrow |
| Copy mark | cursor at first position: `BREAK C`; cursor at last position: `BREAK C`. Only what lies between is printed. |

## Print format directives

| | |
|---|---|
| `PL` | page length (default 66) — set to 72 |
| `LM` | left margin (default 12) — set to 8 |
| `RM` | right margin (default 72) |
| `TM` | top margin (default 6) |
| `BM` | bottom margin (default 60) — set to 66 |
| `LS` | line spacing (default 1) |
| `PF` | line spacing between paragraphs (default 1) |
| `C` | horizontal centring (`C=Y`) |
| `FR` | flush right (`FR=Y`) |
| `J` | justified, flush left and right (`J=Y`) |
| `VC` | vertical centring (specify this first) |
| `P` | print suppression (`P=N` is the default) |
| `PN` | start at page number (`PN=5`) |
| `H` | header block on/off (`H=N` / `H=Y`) |
| `F` | footer block on/off (`F=N` / `F=Y`) |
| `WS` | widow suppression (printing the first line of a paragraph as the last line of a page is suppressed) |

### General notes on print format directives

Enter them at the start of a line with a `>` in front. Several are possible on one line,
separated from each other by a comma or a blank. All entries must be in capitals, and they stay
in force until they are changed.

Directives that affect the page format — justification (`>J=Y`), for instance — must always
come at the start of the text or after a page-end mark.

Note also:

```
Centring    (>C =Y) overrides directives that follow
Flush right (>FR=Y) overrides directives that follow
Justified   (>J =Y) overrides flush left
Flush left  applies when all preceding directives are =N
```

### Print suppression

You can skip some lines when printing by putting `>P=N` before them and `>P=Y` at the end. A
text-boundary mark must stand before and after each directive.

### Centring

As you can see, text can be centred with the `>C=Y` directive. This is cancelled again with
`>C=N`. A text-boundary mark may stand at the end of a line.

### Printing flush right

As you can see, text can be printed flush right with the `>FR=Y` directive, and cancelled again
with `>FR=N`.

### A note on printing justified

Text can be printed flush on both sides by giving `>J=Y` on the line before. You should take
care that the lines on screen are reasonably full, so as not to produce too many large gaps.
A text-boundary mark should also be set at the end of any line that is not nearly full.

## Miscellaneous

The umlauts **Ä ä Ö ö Ü ü** and **ß** are reached as follows: `@` followed by the letter, or
`@ :` for the ß. The umlaut — or the ß — then appears.

`SHIFT 0` gives `@`.

`SHIFT @` = shift lock (capitals only).

The text so far was also printed vertically centred, which was done with `>VC=Y`.

## Searching for a word

Press `BREAK` and then enter `F>xxxxxxx` (the search word). The search begins from the position
the cursor stood at before `BREAK` was pressed. The cursor then jumps to the first word found.
To search again for the same word, entering `F` alone is enough — the system remembers the
search word until it is changed.

## Replacing a word

As for searching. Only instead of `F`, enter `>xxxxxxx>zzzzzzz`.

## Deleting a word

As for searching. Only instead of `F`, enter `D>xxxxxxxxxx`.

## Repeating a command

`@ r` and then the number of repetitions (ENTER = the highest possible number: 255). Then a
command. Every command can be repeated.

## Printer controls added by the modification

`BREAK X=nnnn` (n = 1–255) initialises the printer.

The rest of the printer control is very simply built, and can be used independently of the
printer type. Pressing `@` and `p` together generates the code 7FH, which appears on screen as
a hatched square. On output to the printer, however, this is not passed on as such: together
with the two bytes that follow it, only one byte goes to the printer. That byte corresponds to
the value written after the `@p` in hexadecimal notation.

Because the modified printer driver makes one character out of three at this combination, the
character count may under some circumstances get out of step.

## Reading the DIRECTORY

`BREAK Qn` or `Q n`, where n is the drive number, reads the directory.

Pressing CLEAR returns you to text mode; pressing BREAK takes you to command mode. In command
mode the directory stays on screen. A file can therefore be picked out and loaded conveniently,
without having to remember the name. Text mode is then entered automatically.

## Killing a file

`KILL` or `K filename` deletes the file name, if it is found.

## Printer pause

`SHIFT P` interrupts the printing of a document; CLEAR continues.

## Reinitialising Scripsit

`BREAK N` or `New` reinitialises Scripsit/SP, much like the BASIC NEW command.

## Reentry after END

After a Scripsit session has been ended, reentry is possible by entering `WP SP*`. A Scripsit
patch routine checks whether a return jump is possible.

---

## Notes on this translation

**Printer escapes.** `SCRIPSIT.TXT` contains seventeen 7FH bytes — the hatched square produced
by `@p` — each followed by two hex digits. Folded back together they are six Epson sequences:
`ESC x 1` (near-letter-quality on), `ESC 4` / `ESC 5` (italic on/off), `ESC W 1` / `ESC W 0`
(double width on/off). The manual is set using the escape it documents in the *Printer controls*
section above.

**The page-end marker.** The German reads *"`@ v` (ED erscheint)"*. In the file, the marker at
that point is itself a `@p` escape, not the literal letters `ED`. Rendered here as "a marker
appears".

**Slips in the original, left as they stand.** *außschließlich* (for *ausschließlich*),
*rückgängign* (*rückgängig*), *reinitialiseren* (*reinitialisieren*), *le Stelle* (*letzte
Stelle*), and in the hot-zone paragraph *der nächsten Spalte* where *Zeile* is meant — the
sense is the next **line**, not the next column. Translated for sense, noted here.

**The tail.** The document ends with the *Reentry after END* section repeated and then breaking
off mid-sentence, followed by 154 bytes of E5 sector fill. That is how the file is. Nothing has
been completed or tidied.

**Provenance.** `SCRIPSIT/TXT` is not on `esnd-04.dmk`. Which disk it came from is not
established.
