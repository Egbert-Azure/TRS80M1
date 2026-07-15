;-----------------------------------------------------------------------
; scripsit-sp-patch.asm
; SCRIPSIT/SP - Umlaut- und Druckererweiterung fuer SCRIPSIT/CMD
; Egbert Schroeer, 1988  (Vers.1.02)
;
; RECONSTRUCTED 2026 by disassembly of SCRIPSIT/CMD vs SCRIPSIT/SP.
; Source files were supplied directly; both were later verified
; byte-identical to the copies on esnd-04.dmk. esnd-05.dmk has never
; been examined. This is NOT the original source; it is a byte-faithful
; reconstruction. Labels and comments are modern additions.
;-----------------------------------------------------------------------

PRPORT  EQU     37E8H           ; parallel printer, read=status write=data
HIGH$   EQU     4049H           ; DOS top-of-memory pointer

; --- original Scripsit entry points reused by the patch ---
KBD41   EQU     6161H           ; CP 80H / AND 9FH  (control-code fold)
KBDCHK  EQU     6167H           ; CP 41H ... SHIFT-lock / XOR 20H
KBDOUT  EQU     6179H           ; LD D,A  (character accepted, no case flip)
PRNEXT  EQU     5F74H           ; printer path, after the character went out
PRLF    EQU     7183H           ; INC DE / LD A,0AH / JP 5F44
PRNOTM  EQU     7189H           ; 8Dh-marker not matched

;=======================================================================
; RESIDENT DRIVER  FF6C-FFFF   (protected via HIGH$ = FF6BH)
;=======================================================================
        ORG     0FF6CH
;-----------------------------------------------------------------------
; PRCHR - send character in A to the printer
;   - 7FH ("hashed block", @ p) starts a 2-digit hex escape: the next
;     two characters are assembled into one byte and sent instead
;   - all other characters run through the XLAT table
;-----------------------------------------------------------------------
PRCHR   PUSH    HL
        PUSH    BC
        PUSH    AF
        LD      HL,HEXCNT
        LD      A,(HL)
        AND     A
        JR      NZ,PRHEX        ; hex digits pending
        POP     AF
        PUSH    AF
        CP      7FH
        JR      Z,PRESC         ; start escape, swallow the 7FH
        LD      HL,XLFROM
        LD      BC,15
        CPIR
        JR      NZ,PROUT        ; not in table: pass through
        LD      BC,14
        ADD     HL,BC           ; -> matching entry in XLTO
        LD      A,(HL)
PROUT   LD      (PRPORT),A
PRDONE  POP     AF
        POP     BC
        POP     HL
        RET
PRESC   LD      (HL),2          ; expect two hex digits
        JR      PRDONE
PRHEX   POP     AF
        PUSH    AF
        CP      3AH             ; '0'-'9' ?
        JR      C,PRHEX1
        SUB     7               ; 'A'-'F'
PRHEX1  SUB     30H
        INC     HL              ; -> HEXVAL
        RLD                     ; shift nibble in
        LD      A,(HL)
        DEC     HL
        DEC     (HL)            ; one digit less
        JR      NZ,PRDONE       ; first of two: nothing sent yet
        JR      PROUT           ; second: send assembled byte

HEXCNT  DEFB    0               ; FFAA - digits still expected
HEXVAL  DEFB    0               ; FFAB - assembled byte

;-----------------------------------------------------------------------
; UMLKBD - replaces  CP 41H / JR C,KBDCHK  at 615DH
;   @A @O @U -> Ae Oe Ue      @a @o @u -> ae oe ue
;   @:       -> ss            @P @p    -> 7FH (hashed block)
; Umlauts are handed to KBDCHK so that Scripsit's own SHIFT-lock
; XOR 20H produces the lower/upper case pair (5B/7B, 5C/7C, 5D/7D).
; 7EH and 7FH must bypass it, so they go straight to KBDOUT.
;-----------------------------------------------------------------------
UMLKBD  LD      HL,UMLKEY
        LD      BC,11H
        CPIR
        JR      NZ,UMLNO
        LD      BC,10H
        ADD     HL,BC           ; -> matching entry in UMLCHR
        LD      A,(HL)
        CP      7EH
        JP      C,KBDCHK        ; 5B 5C 5D 7B 7C 7D : allow case flip
        JP      KBDOUT          ; 7E 7F             : no case flip
UMLNO   CP      41H             ; original 615DH semantics
        JP      C,KBDCHK
        JP      KBD41

;-----------------------------------------------------------------------
; PRSTAT - vectored printer status read (replaces LD A,(37E8H) inline)
;-----------------------------------------------------------------------
PRSTAT  LD      A,(PRPORT)
        RET

UMLKEY  DEFM    'PpAOUaou:'     ; FFCF
        DEFB    0,0,0,0,0,0,0
UMLCHR  DEFB    7FH,7FH         ; FFE0  P p
XLFROM  DEFB    5BH,5CH,5DH     ; FFE2  Ae Oe Ue      <- also printer
        DEFB    7BH,7CH,7DH     ;       ae oe ue         XLAT source
        DEFB    7EH             ;       ss
        DEFB    0,0,0,0,0,0,0,0
XLTO    DEFB    5BH,5CH,5DH     ; FFF1  printer XLAT target
        DEFB    7BH,7CH,7DH     ;       (identity in this build -
        DEFB    7EH             ;        patch here per printer)
        DEFB    0,0,0,0,0,0,0,0

;=======================================================================
; EXTENSION IN THE RESIDENT IMAGE  7A7D-7AA4
; (the last load record was lengthened from 80H to A7H to hold this;
;  the old XFER record was overwritten and re-emitted at the end)
;=======================================================================
        ORG     7A7DH
;-----------------------------------------------------------------------
; MRK8C - replaces  CP 8DH / JR NZ  at 717FH
; accept the re-assigned marker code 8CH wherever 8DH was accepted
;-----------------------------------------------------------------------
MRK8C   CP      8CH
        JP      Z,PRLF
        CP      8DH
        JP      NZ,PRNOTM
        JP      PRLF

;-----------------------------------------------------------------------
; PSUPP - replaces  JR NZ,5F74 / LD (37E8H),A  at 5F6FH
; entered with Z from  BIT 4,(IY+34H)  and the character in A.
; Z  = printing enabled -> print it
; NZ = >P=N suppression -> print a BLANK instead of dropping the
;      character, so column/line counting stays correct; CR and LF
;      are still passed through unchanged.
;-----------------------------------------------------------------------
PSUPP   JR      Z,PSPRT
        CP      0DH
        JR      Z,PSPRT
        CP      0AH
        JR      Z,PSPRT
        EX      AF,AF'
        LD      A,20H
        CALL    PRCHR
        EX      AF,AF'
        JP      PRNEXT
PSPRT   CALL    PRCHR
        JP      PRNEXT

;=======================================================================
; IN-PLACE PATCHES  (byte list, apply to SCRIPSIT/CMD)
;=======================================================================
;  4049H  6B FF                 ; HIGH$ = FF6BH, protect the driver
;
;  5242H  3E 0A CD 6C FF        ; was 3E 0D 32 E8 37  (LF, via PRCHR)
;  52C0H  F3                    ; was 00             (DI)
;  5800H  'Modification Copyright 1988 by Egbert Schr'
;         DEFB 7CH              ; oe
;         'er Vers.1.02'        ; 55 bytes, terminator 13H at 5837 kept
;  5D47H  CD 6E 7A              ; was 3A B9 7C  (CALL the dead RS stub)
;  5DCCH  C4 EF 5D 79 32 B9 7C  ; was 32 B6 7C C4 EF 5D 00
;  5F63H  CD CB FF              ; was 3A E8 37  (PRSTAT)
;  5F6FH  00 00 C3 8A 7A        ; was 20 03 32 E8 37  (JP PSUPP)
;  615DH  C3 AC FF 00           ; was FE 41 38 06  (JP UMLKBD)
;  663FH  CD CB FF              ; was 3A E8 37
;  6650H  CD CB FF              ; was 3A E8 37
;  665EH  CD 6C FF              ; was 32 E8 37
;  6722H  CD 6C FF              ; was 32 E8 37
;  717FH  C3 7D 7A              ; was FE 8D 20      (JP MRK8C)
;  7970H  97                    ; was 5C  marker glyph for 8CH
;  7972H  A6                    ; was 5B  marker glyph for 8BH
;  7974H  AD                    ; was 5D  default marker glyph
;  7A20H  7F                    ; was 3C  default BM   (verify)
;  7A22H  7F                    ; was 42  default PL   (verify)
;
; NOT patches - runtime state captured when SP was written out:
;  6038H 04 / 6056H 04  (ring-buffer displacements, were 05)
;  7973H 8D             (search sentinel, was 8C)
;=======================================================================
        END
