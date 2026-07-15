import re, pickle, sys

R8  = {'B':0,'C':1,'D':2,'E':3,'H':4,'L':5,'(HL)':6,'A':7}
RP1 = {'BC':0,'DE':1,'HL':2,'SP':3}          # for ADD HL / INC rr / PUSH uses RP2
RP2 = {'BC':0,'DE':1,'HL':2,'AF':3}
CC  = {'NZ':0,'Z':1,'NC':2,'C':3,'PO':4,'PE':5,'P':6,'M':7}
ALU = {'ADD':0,'ADC':1,'SUB':2,'SBC':3,'AND':4,'XOR':5,'OR':6,'CP':7}
ROT = {'RLC':0,'RRC':1,'RL':2,'RR':3,'SLA':4,'SRA':5,'SLL':6,'SRL':7}
NOARG = {'NOP':[0x00],'HALT':[0x76],'DI':[0xF3],'EI':[0xFB],'EXX':[0xD9],
         'RLCA':[0x07],'RRCA':[0x0F],'RLA':[0x17],'RRA':[0x1F],
         'DAA':[0x27],'CPL':[0x2F],'SCF':[0x37],'CCF':[0x3F],
         'NEG':[0xED,0x44],'RETN':[0xED,0x45],'RETI':[0xED,0x4D],
         'RRD':[0xED,0x67],'RLD':[0xED,0x6F],
         'LDI':[0xED,0xA0],'CPI':[0xED,0xA1],'INI':[0xED,0xA2],'OUTI':[0xED,0xA3],
         'LDD':[0xED,0xA8],'CPD':[0xED,0xA9],'IND':[0xED,0xAA],'OUTD':[0xED,0xAB],
         'LDIR':[0xED,0xB0],'CPIR':[0xED,0xB1],'INIR':[0xED,0xB2],'OTIR':[0xED,0xB3],
         'LDDR':[0xED,0xB8],'CPDR':[0xED,0xB9],'INDR':[0xED,0xBA],'OTDR':[0xED,0xBB]}

class Asm:
    def __init__(self):
        self.sym={}; self.pc=0; self.pass2=False; self.out={}; self.errors=[]

    # ---------- expressions ----------
    def val(self, e):
        e=e.strip()
        if not e: return 0
        toks=re.findall(r"'.'|\$|[A-Za-z_][A-Za-z0-9_]*H?|[0-9][0-9A-Fa-f]*H|[0-9]+|[-+()]", e)
        # rebuild python expression
        py=''
        for t in toks:
            if t in '+-()': py+=t
            elif t=='$': py+=str(self.pc)
            elif len(t)==3 and t[0]=="'" and t[2]=="'": py+=str(ord(t[1]))
            elif re.fullmatch(r'[0-9][0-9A-Fa-f]*[Hh]',t): py+=str(int(t[:-1],16))
            elif re.fullmatch(r'[0-9]+',t): py+=t
            else:
                nm=t.upper()
                if nm in self.sym: py+=str(self.sym[nm])
                elif self.pass2: self.errors.append('undef %s'%nm); py+='0'
                else: py+='0'
        try: return eval(py) & 0xFFFF
        except Exception: 
            if self.pass2: self.errors.append('expr %r'%e)
            return 0

    def emit(self, bs):
        if self.pass2:
            for i,b in enumerate(bs): self.out[(self.pc+i)&0xFFFF]=b&0xFF
        self.pc=(self.pc+len(bs))&0xFFFF

    # ---------- operand classification ----------
    def idx(self, o):
        m=re.fullmatch(r'\((I[XY])\s*([+-][^)]*)?\)', o)
        if not m: return None
        return (0xDD if m.group(1)=='IX' else 0xFD, self.val(m.group(2) or '0')&0xFF)

    def asm(self, mn, ops):
        o=[x.strip() for x in split_ops(ops)] if ops else []
        A=o[0].upper() if len(o)>0 else ''
        B=o[1].upper() if len(o)>1 else ''
        raw0=o[0] if o else ''; raw1=o[1] if len(o)>1 else ''

        if mn in NOARG: return self.emit(NOARG[mn])

        if mn=='LD':  return self.ld(A,B,raw0,raw1)
        if mn in ALU: return self.alu(mn,A,B,raw0,raw1)
        if mn=='INC' or mn=='DEC': return self.incdec(mn,A,raw0)
        if mn=='PUSH' or mn=='POP':
            if A in ('IX','IY'): return self.emit([0xDD if A=='IX' else 0xFD, 0xE5 if mn=='PUSH' else 0xE1])
            return self.emit([(0xC5 if mn=='PUSH' else 0xC1)|(RP2[A]<<4)])
        if mn=='JP':
            if A=='(HL)': return self.emit([0xE9])
            if A in ('(IX)','(IY)'): return self.emit([0xDD if A=='(IX)' else 0xFD,0xE9])
            if A in CC:
                v=self.val(raw1); return self.emit([0xC2|(CC[A]<<3),v&0xFF,v>>8])
            v=self.val(raw0); return self.emit([0xC3,v&0xFF,v>>8])
        if mn=='CALL':
            if A in CC:
                v=self.val(raw1); return self.emit([0xC4|(CC[A]<<3),v&0xFF,v>>8])
            v=self.val(raw0); return self.emit([0xCD,v&0xFF,v>>8])
        if mn=='RET':
            if A=='': return self.emit([0xC9])
            return self.emit([0xC0|(CC[A]<<3)])
        if mn=='JR':
            if A in ('NZ','Z','NC','C'):
                t=self.val(raw1); d=(t-(self.pc+2))&0xFF
                return self.emit([{'NZ':0x20,'Z':0x28,'NC':0x30,'C':0x38}[A],d])
            t=self.val(raw0); d=(t-(self.pc+2))&0xFF
            return self.emit([0x18,d])
        if mn=='DJNZ':
            t=self.val(raw0); d=(t-(self.pc+2))&0xFF; return self.emit([0x10,d])
        if mn=='RST': return self.emit([0xC7|(self.val(raw0)&0x38)])
        if mn=='IM':  return self.emit([0xED,{0:0x46,1:0x56,2:0x5E}[self.val(raw0)]])
        if mn in ('BIT','SET','RES'):
            b=self.val(raw0)&7; base={'BIT':0x40,'SET':0xC0,'RES':0x80}[mn]
            ix=self.idx(B)
            if ix: return self.emit([ix[0],0xCB,ix[1],base|(b<<3)|6])
            return self.emit([0xCB, base|(b<<3)|R8[B]])
        if mn in ROT:
            ix=self.idx(A)
            if ix: return self.emit([ix[0],0xCB,ix[1],(ROT[mn]<<3)|6])
            return self.emit([0xCB,(ROT[mn]<<3)|R8[A]])
        if mn=='EX':
            if (A,B)==('DE','HL'): return self.emit([0xEB])
            if (A,B)==('AF',"AF'"): return self.emit([0x08])
            if A=='(SP)':
                if B=='HL': return self.emit([0xE3])
                return self.emit([0xDD if B=='IX' else 0xFD,0xE3])
        if mn=='IN':
            if B=='(C)': return self.emit([0xED,0x40|(R8[A]<<3)])
            return self.emit([0xDB,self.val(raw1.strip('()'))&0xFF])
        if mn=='OUT':
            if A=='(C)': return self.emit([0xED,0x41|(R8[B]<<3)])
            return self.emit([0xD3,self.val(raw0.strip('()'))&0xFF])
        self.errors.append('unknown mnemonic %s %s'%(mn,ops)); return self.emit([])

    def alu(self,mn,A,B,r0,r1):
        # ADD A,x / ADD HL,rr / ADC HL,rr / SBC HL,rr / SUB x / CP x ...
        if mn in ('ADD','ADC','SBC') and A in ('HL','IX','IY'):
            if A=='HL':
                if mn=='ADD': return self.emit([0x09|(RP1[B]<<4)])
                return self.emit([0xED,(0x4A if mn=='ADC' else 0x42)|(RP1[B]<<4)])
            p=0xDD if A=='IX' else 0xFD
            rp=RP1[B if B!=A else 'HL']
            return self.emit([p,0x09|(rp<<4)])
        # normalise "ADD A,x" -> operand x
        if A=='A' and B!='' and mn in ('ADD','ADC','SBC'): x,rx=B,r1
        elif A=='A' and B!='': x,rx=B,r1
        else: x,rx=A,r0
        ix=self.idx(x)
        if ix: return self.emit([ix[0],0x86|(ALU[mn]<<3),ix[1]])
        if x in R8: return self.emit([0x80|(ALU[mn]<<3)|R8[x]])
        return self.emit([0xC6|(ALU[mn]<<3), self.val(rx)&0xFF])

    def incdec(self,mn,A,r0):
        lo=0x04 if mn=='INC' else 0x05
        ix=self.idx(A)
        if ix: return self.emit([ix[0],0x34 if mn=='INC' else 0x35,ix[1]])
        if A in R8: return self.emit([lo|(R8[A]<<3)])
        if A in RP1: return self.emit([(0x03 if mn=='INC' else 0x0B)|(RP1[A]<<4)])
        if A in ('IX','IY'): return self.emit([0xDD if A=='IX' else 0xFD,0x23 if mn=='INC' else 0x2B])
        self.errors.append('INC/DEC %s'%A)

    def ld(self,A,B,r0,r1):
        ixa=self.idx(A); ixb=self.idx(B)
        if ixa and B in R8 and B!='(HL)': return self.emit([ixa[0],0x70|R8[B],ixa[1]])
        if ixa and not ixb and B not in R8: return self.emit([ixa[0],0x36,ixa[1],self.val(r1)&0xFF])
        if ixb and A in R8 and A!='(HL)': return self.emit([ixb[0],0x46|(R8[A]<<3),ixb[1]])
        if A in R8 and B in R8:
            if A=='(HL)' and B=='(HL)': self.errors.append('LD (HL),(HL)'); return
            return self.emit([0x40|(R8[A]<<3)|R8[B]])
        if A in R8 and re.fullmatch(r'\(.*\)',B):
            inner=B[1:-1]
            if A=='A' and inner=='BC': return self.emit([0x0A])
            if A=='A' and inner=='DE': return self.emit([0x1A])
            if A=='A': v=self.val(r1[1:-1]); return self.emit([0x3A,v&0xFF,v>>8])
        if re.fullmatch(r'\(.*\)',A) and B in R8:
            inner=A[1:-1]
            if inner=='BC' and B=='A': return self.emit([0x02])
            if inner=='DE' and B=='A': return self.emit([0x12])
            if B=='A': v=self.val(r0[1:-1]); return self.emit([0x32,v&0xFF,v>>8])
        if A in R8:  # LD r,n
            return self.emit([0x06|(R8[A]<<3), self.val(r1)&0xFF])
        if A in RP1 or A in ('IX','IY'):
            if re.fullmatch(r'\(.*\)',B):
                v=self.val(r1[1:-1])
                if A=='HL': return self.emit([0x2A,v&0xFF,v>>8])
                if A in ('IX','IY'): return self.emit([0xDD if A=='IX' else 0xFD,0x2A,v&0xFF,v>>8])
                return self.emit([0xED,0x4B|(RP1[A]<<4),v&0xFF,v>>8])
            if A=='SP' and B=='HL': return self.emit([0xF9])
            if A=='SP' and B in ('IX','IY'): return self.emit([0xDD if B=='IX' else 0xFD,0xF9])
            v=self.val(r1)
            if A in ('IX','IY'): return self.emit([0xDD if A=='IX' else 0xFD,0x21,v&0xFF,v>>8])
            return self.emit([0x01|(RP1[A]<<4),v&0xFF,v>>8])
        if re.fullmatch(r'\(.*\)',A) and (B in RP1 or B in ('IX','IY')):
            v=self.val(r0[1:-1])
            if B=='HL': return self.emit([0x22,v&0xFF,v>>8])
            if B in ('IX','IY'): return self.emit([0xDD if B=='IX' else 0xFD,0x22,v&0xFF,v>>8])
            return self.emit([0xED,0x43|(RP1[B]<<4),v&0xFF,v>>8])
        if A=='I' and B=='A': return self.emit([0xED,0x47])
        if A=='A' and B=='I': return self.emit([0xED,0x57])
        if A=='R' and B=='A': return self.emit([0xED,0x4F])
        if A=='A' and B=='R': return self.emit([0xED,0x5F])
        self.errors.append('LD %s,%s'%(A,B))

def split_ops(s):
    out=[];cur='';d=0;q=False
    for ch in s:
        if ch=="'": q=not q
        if ch=='(' and not q: d+=1
        if ch==')' and not q: d-=1
        if ch==',' and d==0 and not q: out.append(cur); cur=''
        else: cur+=ch
    out.append(cur); return out

def run(lines):
    a=Asm()
    for p in (1,2):
        a.pass2=(p==2); a.pc=0; a.errors=[]
        for num,txt in lines:
            body=txt[1:] if txt.startswith(' ') else txt
            if body.strip().startswith(';') or not body.strip(): continue
            f=body.split('\t')
            label=f[0].strip()
            mn=f[1].strip().upper() if len(f)>1 else ''
            ops=f[2].strip() if len(f)>2 else ''
            if ops.startswith(';'): ops=''
            if mn=='EQU':
                a.sym[label.upper()]=a.val(ops); continue
            if label: a.sym[label.upper()]=a.pc
            if not mn: continue
            if mn=='ORG': a.pc=a.val(ops); continue
            if mn=='END': break
            if mn=='DEFS': a.pc=(a.pc+a.val(ops))&0xFFFF; continue
            if mn=='DEFB':
                for e in split_ops(ops): a.emit([a.val(e)&0xFF])
                continue
            if mn=='DEFW':
                for e in split_ops(ops):
                    v=a.val(e); a.emit([v&0xFF,v>>8])
                continue
            if mn=='DEFM':
                m=re.search(r"'(.*)'",ops)
                a.emit([ord(c) for c in m.group(1)]); continue
            a.asm(mn,ops)
    return a

if __name__=='__main__':
    lines=pickle.load(open('src.pkl','rb'))
    a=run(lines)
    print('errors:',len(a.errors))
    for e in a.errors[:20]: print('  ',e)
    print('bytes emitted:',len(a.out))
    print('TXTBUF=%04X  START=%04X  TSTBYT=%04X'%(a.sym.get('TXTBUF',0),a.sym.get('START',0),a.sym.get('TSTBYT',0)))
    pickle.dump((a.out,a.sym),open('built.pkl','wb'))

# ---------------------------------------------------------------------------
# edtasm-z80.py — two-pass Z80 assembler for TRS-80 EDTASM source files.
#
# Written 2026 to verify wpand.scr against Craig Lindley's wp.cmd.
#
# Validation: assembling wpand.scr (820 lines, 620 statements, 34 distinct
# mnemonics) emits 1336 bytes with address coverage identical to wp.cmd and
# 5 differing bytes, all traceable to source-text differences rather than
# encoding. Symbols resolve to START=7B49, TXTBUF=8342, TSTBYT=7C21 — exactly
# the values wp.cmd's entry record and installer require.
#
# Scope / known limits:
#   - Only the 34 mnemonics used by that listing are exercised. IN/OUT/IM/EXX
#     and undocumented forms are implemented but untested.
#   - Expressions are rewritten to Python and eval()'d. Adequate for MSG5+31,
#     $, 07AA5H, 'K'. Not hardened.
#   - Directives: ORG EQU DEFB DEFW DEFM DEFS END. No macros/conditionals/DEFL.
#
# Input format (EDTASM ASCII source):
#   D3 + 6-char module name, then per line:
#   five high-bit digits (B0-B9) + ' ' + label + TAB + mnemonic + TAB + operands
#   + TAB + comment, terminated 0D. File ends 1A.
#
# Usage:
#   lines = [(lineno, text), ...]   # text without the 5-digit prefix
#   a = run(lines)
#   a.out   -> {address: byte}
#   a.sym   -> {NAME: value}
#   a.errors
# ---------------------------------------------------------------------------
