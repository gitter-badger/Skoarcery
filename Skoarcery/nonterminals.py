
src = """

# Skoar Nonterminals
#
# like_this for nonterminals, LikeThis for terminals
#
# + before a nonterminal indicates this is an intermediate step that can be
# skipped in the constructed parse tree, it will not create a new skoarnode,
# instead appending its noads to its parent's children list.
#
# * after a nonterminal means there is corresponding semantic code for this,
# defined in skoarmantics.py

skoar              : branches
+branches          : branch branches | <e>
branch*            : optional_voice phrases Newline
+optional_voice    : Voice | <e>

+phrases           : phrasey phrases | <e>
+phrasey           : Comment | marker | Meter | stmt | dal_goto | beat

skoarpion          : SkoarpionStart skrp_sig SkoarpionSep skrp_suffix
skrp_sig           : args | SymbolName optional_args | <e>
skrp_suffix        : skrp_lines SkoarpionEnd
+skrp_lines        : optional_voice phrases skrp_moar_lines
+skrp_moar_lines   : skrp_sep_or_nl skrp_lines | <e>
+skrp_sep_or_nl    : Newline | SkoarpionSep

+optional_args     : args | <e>
args*              : ListS args_suffix
args_suffix        : args_entries ListE
+args_entries      : SymbolName moar_args_entries
+moar_args_entries : ListSep args_entries | <e>

listy*             : ListS listy_suffix
+listy_suffix      : listy_entries ListE | ListE
+listy_entries     : skoaroid moar_listy_entries
+moar_listy_entries: ListSep listy_entries | Newline | <e>

marker*            : Segno | Fine | coda | Volta | Bars
coda*              : Coda optional_al_coda
optional_al_coda   : AlCoda | <e>
dal_goto*          : DaCapo al_x | DalSegno al_x
al_x               : AlCoda | AlSegno | AlFine | <e>

beat*              : Crotchets | Quavers | Quarters | Eighths | Slash

musical_keyword      : dynamic | ottavas | pedally | musical_keyword_misc
musical_keyword_misc*: Rep | Portamento | Carrot
pedally*             : PedalDown | PedalUp
ottavas*             : OctaveShift | OttavaA | OttavaB | QuindicesimaA | QuindicesimaB | Loco
dynamic*             : DynPiano | DynForte | DynSFZ | DynFP

nouny*           : cthulhu | conditional | loop | nouny_literal | musical_keyword | listy | deref | skoarpion
+nouny_literal   : Tuplet | Caesura | Int | Float | String | Choard | NamedNoat | Symbol

deref*           : Deref deref_prime
+deref_prime     : MsgNameWithArgs listy_suffix | MsgName

stmt*            : skoaroid stmt_prime
+stmt_prime      : assignment stmt_prime | math | <e>

+math            : MathOp skoaroid stmt_prime
assignment*      : AssOp settable
+settable        : Caesura | Symbol | listy | Quarters | Eighths

skoaroid*        : nouny msg_chain_node
+msg_chain_node  : MsgOp msg msg_chain_node | <e>
msg*             : MsgNameWithArgs listy_suffix | MsgName | listy | loop

boolean*         : skoaroid BooleanOp skoaroid
cthulhu*         : LWing Semicolon cthulhu_prime
+cthulhu_prime   : boolean Semicolon RWing | Nosey Semicolon RWing

conditional      : CondS cond_ifs CondE
+cond_ifs        : cond_if cond_ifs_suffix
+cond_ifs_suffix : Newline cond_ifs | <e>
cond_if          : optional_voice boolean CondIf if_body cond_else
+cond_else       : CondIf if_body | <e>

if_body          : phrases

loop             : LoopS loop_body loop_condition LoopE
loop_body        : phrases
loop_condition   : LoopSep boolean | <e>

"""


SKOAR = None
nonterminals = None


def init():
    global nonterminals, SKOAR
    nonterminals = dict()

    from Skoarcery import terminals
    from Skoarcery.langoids import Nonterminal

    # create and track as they appear
    def hello(name):

        try:
            xoid = nonterminals[name]
        except KeyError:
            xoid = Nonterminal(name)
            nonterminals[name] = xoid

        return xoid

    for bnf_line in src.split("\n"):
        if len(bnf_line) == 0 or bnf_line.lstrip().startswith("#"):
            continue

        #print(bnf_line)
        a = bnf_line.split(":")

        name = a[0].strip()

        if name.startswith("+"):
            name = name.lstrip("+")
            intermediate = True
        else:
            intermediate = False

        if name.endswith("*"):
            name = name.rstrip("*")
            has_semantics = True
        else:
            has_semantics = False

        for production in a[1].split("|"):

            p = []
            for langoid in production.split():

                if len(langoid) == 0:
                    continue

                toke = terminals.tokens.get(langoid)

                if toke:
                    p.append(toke)
                else:

                    if langoid[0].isupper():
                        raise Exception("Unknown token " + langoid)

                    X = hello(langoid)

                    p.append(X)

            X = hello(name)
            X.intermediate = intermediate
            X.has_semantics = has_semantics
            X.add_production(p)

    SKOAR = nonterminals["skoar"]

    print("nonterminals initialized.")
