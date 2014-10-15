// ============
// Skoarmantics
// ============

/*

This code is applied during the decoration stage of compiling the skoar tree.

For stuff to happen during performing the tree, we set handlers here.

We also shrink the tree, drop some punctuation noads;
   when you see replace_children, that's what's going on. 

absorb_toke assumes the only child is a toke, puts it in 
   noad.toke and removes the child. (and returns the toke)

We went depth first and run the code on the way back,
   so children are processed first.

*/
Skoarmantics {

    *new {

        var dict = Dictionary[

            "branch" -> {
                | skoar, noad |

                var n = 0;
                var x = nil;

                n = noad.n;
                x = noad.children[0];

                if (x != nil && x.toke != nil) {
                    x = x.toke;
                    if (x.isKindOf(Toke_Voice)) {
                        noad.toke = x;
                        noad.voice = skoar.get_voice(x.val);
                        noad.branch = noad;
                        "Voice: ".post; x.val.postln;
                    };
                };

                // drop the newline
                noad.children.pop;
                noad.n = n - 1;

            },

            "msg_chain_node" -> {
                | skoar, noad |
            },
        
            "beat" -> {
                | skoar, noad |
                var t;

                noad.absorb_toke;
                t = noad.toke;

                noad.beat = t;
                noad.is_beat = true;
                noad.is_rest = t.is_rest;
            },

            "listy" -> {
                | skoar, noad |

                var n = noad.children.size;
                var x = nil;
                var items = List.new;

                // skip the first and last tokens
                for (1, n - 2, {
                    | i |
                    x = noad.children[i];

                    // skip the separators
                    if (x.toke.isKindOf(Toke_ListSep) == false) {
                        items.add(x);
                    };
                });

                noad.replace_children(items);

            },
        
            "clef" -> {
                | skoar, noad |
            },

            "stmt" -> {
                | skoar, noad |
            },
        
            "musical_keyword_misc" -> {
                | skoar, noad |
            },

            "accidentally" -> {
                | skoar, noad |
            },

            "boolean" -> {
                | skoar, noad |
            },

            "ottavas" -> {
                | skoar, noad |

                var toke;

                toke = noad.absorb_toke;

                if (toke.isKindOf(Toke_OctaveShift)) {
                    noad.performer = {noad.voice.octave_shift(toke.val);};
                };

                if (toke.isKindOf(Toke_OttavaA)) {
                    noad.performer = {noad.voice.octave_shift(1);};
                };

                if (toke.isKindOf(Toke_OttavaB)) {
                    noad.performer = {noad.voice.octave_shift(-1);};
                };

                if (toke.isKindOf(Toke_QuindicesimaA)) {
                    noad.performer = {noad.voice.octave_shift(1);};
                };

                if (toke.isKindOf(Toke_QuindicesimaB)) {
                    noad.performer = {noad.voice.octave_shift(-1);};
                };


            },

             "assignment" -> {
                | skoar, noad |

                // the settable
                var y = nil;
                var y_toke = nil;

                y = noad.children[1];
                y_toke = y.toke;

                // we prepare the destination here (noad.setter), we'll setup the write in skoaroid

                // set a value on voice's skoarboard, keyed by a symbol
                if (y_toke.isKindOf(Toke_Symbol)) {
                    noad.setter = {
                        | x, v |
                        v.assign_symbol(x, y_toke);
                    };
                };

                // set tempo
                if (y_toke.isKindOf(Toke_Quarters) || y_toke.isKindOf(Toke_Eighths)) {
                    noad.setter = {
                        | x, v |
                        var x_toke = x.next_toke;

                        "XTOKE: ".post; x_toke.dump;

                        if (x_toke.isKindOf(Toke_Int) || x_toke.isKindOf(Toke_Float)) {
                            v.set_tempo(x_toke.val, y_toke);
                        } {
                            SkoarError("Tried to use a " ++ x_toke.name ++ " for tempo.").throw;
                        };
                    };
                };

            },

            "skoaroid" -> {
                | skoar, noad |

                var f = nil;
                var x = nil;
                var y = nil;

                if (noad.children.size > 1) {
                    x = noad.children[0];
                    y = noad.children[1];

                    if (y.name == "assignment") {

                        f = y.setter;

                        noad.performer = {
                            | v |
                            f.(x, v);
                        };

                    };
                };

            },
        
            "msg" -> {
                | skoar, noad |
            },

            "cthulhu" -> {
                | skoar, noad |
                noad.performer = {skoar.cthulhu(noad);};
            },
        
            "dynamic" -> {
                | skoar, noad |
                var toke = noad.absorb_toke;
                noad.performer = {
                    | v |
                    v.dynamic(toke);
                };
            },
        
            "optional_carrots" -> {
                | skoar, noad |
            },

            "dal_goto" -> {
                | skoar, noad |

                var toke = noad.children[0].toke;
                skoar.do_when_voices_ready({noad.voice.add_marker(noad);});

                if (toke.isKindOf(Toke_DaCapo)) {
                    noad.performer = {
                        | v |
                        v.da_capo(noad);
                    };
                };

                if (toke.isKindOf(Toke_DalSegno)) {
                    noad.performer = {
                        | v |
                        v.dal_segno(noad);
                    };
                };

            },

            "marker" -> {
                | skoar, noad |
        
                var toke;

                noad.absorb_toke;
                skoar.do_when_voices_ready({noad.voice.add_marker(noad);});

                toke = noad.toke;
                if (toke != nil && toke.isKindOf(Toke_Bars)) {
                    if (toke.pre_repeat) {
                        noad.performer = {
                            | v |
                            v.jmp_colon(noad);
                        };
                    };

                };

            },

            "coda" -> {
                | skoar, noad |
                skoar.do_when_voices_ready({noad.voice.add_coda(noad);});
            },

            "noaty" -> {
                | skoar, noad |
            },
        
            "noat_literal" -> {
                | skoar, noad |
        
                var noat = noad.absorb_toke;
                noad.noat = noat;
        
                if (noat.isKindOf(Toke_NamedNoat)) {
                    noad.performer = {noad.voice.noat_go(noat)};
                };

                if (noat.isKindOf(Toke_Choard)) {
                    noad.performer = {noad.voice.choard_go(noat)};
                };
            },
        
            "noat_reference" -> {
                | skoar, noad |

                var x = noad.children[0];

                // TODO Symbol | CurNoat | listy
                if (x.name == "listy") {
                    x.performer = {noad.voice.choard_listy(x)};
                };

                if (x.name == "CurNoat") {
                    x.performer = {noad.voice.reload_curnoat(x)};
                };

                if (x.name == "Symbol") {
                    x.performer = {noad.voice.noat_symbol(x)};
                };

            },
        
            "pedally" -> {
                | skoar, noad |

                if (noad.toke.isKindOf(Toke_PedalUp)) {
                    noad.performer = {noad.voice.pedal_up;};
                };

                if (noad.toke.isKindOf(Toke_PedalDown)) {
                    noad.performer = {noad.voice.pedal_down;};
                };

            }

        ];
        ^dict;
    }

}