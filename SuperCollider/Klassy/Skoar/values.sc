// ===========
// Value types
// ===========
SkoarValue {
    var <>val;

    *new { | v | ^super.new.init(v); }
    init { | v | val = v; }

    as_noat { | m | ^val;}

    performer {}

    flatten {^val;}

    skoar_msg {
        | msg |
        var o = msg.get_msg;
        var ret = val.performMsg(o);

        case {ret.isKindOf(SkoarValue)} {
            ^ret;

        } {ret.isKindOf(Integer)} {
"ret int".postln;
            ^SkoarValueInt(ret);

        } {ret.isKindOf(Number)} {
"ret float".postln;
            ^SkoarValueFloat(ret);

        } {ret.isKindOf(String)} {
"ret str".postln;
            ^SkoarValueString(ret);

        } {ret.isKindOf(Symbol)} {
"ret symbol".postln;
            ^SkoarValueSymbol(ret);

        } {ret.isKindOf(Array)} {
"ret array".postln;
            ^SkoarValueArray(ret);

        } {
"ret unknown".post; ret.dump;
            ^SkoarValueUnknown(ret);
        };

    }
}

SkoarValueUnknown : SkoarValue {
}

SkoarValueInt : SkoarValue {
}


SkoarValueFloat : SkoarValue {
}

SkoarValueSkoarpionRef : SkoarValue {

    var config;

    skoar_msg {
        | msg |
        config = msg.get_msg;
        ^this;
    }

    performer {
        | m, nav |
        m.gosub(val, nav, config);
    }
}


SkoarValueString : SkoarValue {
    as_noat { | m | ^nil; }
}

SkoarValueSymbol : SkoarValue {

    lookup {
        | m |
        ^m.voice.skoarboard[val];
    }

    as_noat {
        | m |
        ^this.lookup(m).as_noat(m);
    }

    performer {
        | m, nav |
        var v = this.lookup(m);

        "SYMBOL LOOKEDUP : ".post; v.dump;

        if (v.isKindOf(SkoarValue)) {
            v.performer(m, nav);
        };
    }

}

SkoarValueArray : SkoarValue {

    flatten {
        var out = Array.new(val.size);

        val.do {
            | x |
            out.add(if (x.respondsTo(\flatten)) {x.flatten} {x});
        };

        ^out;
    }

    performer {
        | m, nav |
        m.voice.choard_listy(val);
    }

}

// noaty stuff
SkoarValueNoat : SkoarValue {

    flatten {^this;}

    performer {
        | m, nav |
        m.voice.noat_go(val);
    }

}


SkoarValueChoard : SkoarValue {

    flatten {^this;}

    performer {
        | m, nav |
        m.voice.choard_go(val);
    }

}


// messagy stuff
SkoarValueMsg : SkoarValue {

    var <>args;

    init {
        | t, a |

        val = t.lexeme;
        args = a;

        if (t.isKindOf(Toke_MsgNameWithArgs)) {
            val.pop;
        };

        val = val.asSymbol;
    }

    performer {
        | m, nav |
        //val.postln;
    }

    get_msg {
        var x = Array.new(args.size + 1);
        x.add(val);
        args.flatten.do {
            | y |
            x.add(y);
        };
        ^x;
    }

}