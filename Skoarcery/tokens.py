src = """
<e>:    unused
EOF:    unused
WS:             ^\\s*

MeterS:         <!
MeterE:         !>
MeterSig:       (\\d+(\\+\\d)+/\\d)
TrebleClef:     G:|treble:
BassClef:       F:|bass:
Alto:           C:|alto:



CurNoat:        \\$
Portamento:     ~~~
Slur:           ++
Plus:           \\+
Minus:          -
ZedPlus:        [1-9][0-9]+
Int:            (+|-)?(0|[1-9)[0-9]+)
Float:          (+|-)?(0|[1-9)[0-9]+)\\.[0-9]+

ListS:          <
ListE:          >
ListSep:        ,
Carrots:        \\^+(^\\^\\^\\()
LWing:          \\^\\^\\(
RWing:          \\)\\^\\^
Tuplet:         /\\d+
Crotchets:      }+
Quavers:        o+/
Caesura:        //
DynPiano:       mp|p+
DynForte:       mf|f+
DynSFZ:         sfz
DynFP:          fp
Quarters:       \\]+\\.+
Eighths:        \\]+\\.+
AssOp:          =>
MsgOp:          \\.
AccSharp:       #|sharp
AccNatural:     nat
AccFlat:        flat

NoatSharps:     #
NoatFlats:      b
VectorNoat:     [a-g]#*|b*
BooleanOp:      == | != | <= | >= | in | nin | and | or | xor
Choard:         [A-G]([Mm0-9]|sus|dim)*
CondS:          {
CondSep:        ;
CondE:          }
MsgName:         [a-zA-Z_][a-zA-Z0-9_]*
MsgNameWithArgs: [a-zA-Z_][a-zA-Z0-9_]*<

Nosey:          ,

DaCapo:         D\\.C\\.|Da Capo
DalSegno:       D\\.S\\.|Dal Segno
Fine:           fine
Segno:          %S%|al segno
Coda:           \\(\\+\\)
Rep:            \\./\\.
DubRep:         /\\.\\|\\./
Goto:           :
CondGo:         ::
AlCoda:         al(la)? coda
AlSegno:        al segno
AlFine:         al fine


OttavaA:        8v?a|ottava (alta|sopra)|all' ottava
OttavaB:        8v?b|ottava (bassa|sotto)

QuindicesimaA:   15ma|alla quindicesima
QuindicesimaB:   15mb|alla quindicesimb

Loco:           loco
Volta:          \\[\\d+\\.]

Symbol:         \\[a-zA-Z][a-zA-Z0-9]+
Slash:          /
String:         \'[^']*[^\\]\'
Bars:           [\|]+
Colon:          :
Label:          [a-zA-Z][a-zA-Z0-9_]

PedalDown:      Ped\.
PedalUp:        *

"""


#
#
#

list_of_names = None
tokens = None
Empty = None
EOF = None
WS = None

odd_balls = None


def init():
    from Skoarcery.langoids import Terminal
    global src, list_of_names, tokens, EOF, Empty, WS, odd_balls

    list_of_names = []
    tokens = dict()

    for token_line in src.split("\n"):

        token_line = token_line.strip()
        if len(token_line) > 0:

            (token, v, regex) = token_line.partition(":")

            token = token.strip()
            regex = regex.strip()

            list_of_names.append(token)

            tokens[token] = Terminal(token, regex)

    #print("# tokens initialized.")

    Empty = Terminal("<e>", None)
    EOF = Terminal("EOF", None)
    WS = Terminal("WS", r"^\s*")

    odd_balls = {Empty, EOF, WS}

