import unittest
from Skoarcery import langoids, terminals, nonterminals, dragonsets, parsetable
from Skoarcery.langoids import Terminal, Nonterminal
from Skoarcery.emissions import PY
from Skoarcery.SkoarPyon import apparatus


class Test_Big(unittest.TestCase):

    def setUp(self):
        terminals.init()
        nonterminals.init()
        langoids.init()
        dragonsets.init()
        parsetable.init()

    def test_zelda(self):

        skoar = apparatus.parse("""

c)d)

.alice     <0,3,5> => @detune mp
.bob       <0,3,5> => @detune mp
.bass    @sawpulse => @instrument mp o~~~~
.hats        @hats => @instrument pp
.snare      @snare => @instrument mf
.kick        @kick => @instrument mf

130 => )

{! four_bars_rest !! }}}}} !}
{! eight_bars_rest !! }}}}}} !}
{! twelve_bars_rest !! !four_bars_rest !eight_bars_rest !}

{! bass_fun<x>    !! !x ) ]] ]] ] ) ) !}

{! bass_end<x>    !! !x ) ) ) ] ] !}
{! bass_climb     !! | _e ]] _a# ]] c# ]  e ]] a# ]] ~o c# ] e ) } | f ) o~ _f ]] ]] ] ) } | !}

{! bassline_a !!
  !bass_fun<a#>
  !bass_fun<g#>
  !bass_fun<f#>
  !bass_fun<c#>

  !bass_fun<b>
  !bass_fun<a#>
  !bass_fun<c>
  !bass_end<f>
!}

{! bassline_b !!
  !bass_fun<a#>
  !bass_fun<g#>
  !bass_fun<f#>
  !bass_fun<f>

  !bass_climb
  !bass_climb

  !bass_fun<b>
  !bass_fun<a#>
  !bass_fun<c>
  !bass_end<f>

!}

{! intro !!

  .hats  !four_bars_rest
  .snare !four_bars_rest
  .kick  !four_bars_rest

  .alice | _a# ))        o/. ]]  ]] ]] ] |     ]. _g#  ]] _a# )        o/.  ]]  ]] ]] ] |
  .bob   | _d  ))        o/. ]]  ]] ]] ] | _c  ].      ]]     )        o/.  ]]  ]] ]] ] |
  .bass  |  a# ) ]] ]] ] )       ]] ]] ] |  g# )              ]] ]] ]  )        ]] ]] ] |

  .alice |     ]. _g# ]] _a# )       o/. ]] ]] ]] ] |   ]    _f ]] ]]  ] ]] ]]  ] ]] ]]  ]     ] |
  .bob   | _c# ].     ]]     )       o/. ]] ]] ]] ] |   ] o~ _a ]] ]]  ] ]] ]]  ] ]] ]]  ]     ] |
  .bass  |  f# )             ]] ]] ] )      ]] ]] ] | f )              )        )      g ]   a ] |
!}

{! melody_a !! .bass !bassline_a

  .alice | _a# ) _f )__          o/. _a# ]]  ]]   c ]]  d ]] d# ]] |
  .bob   | _d  )    ]] ]] _c ] _d ].     ]]  ]] _d# ]] _f ]] _g ]] |

  .alice |  f  ))                             o/ ]   f ]  f# ]] g# ]] |
  .bob   | _g# ]. _a# ]] ]] c ]] d ]] d# ]] f )    _g# ] _a# ]] c  ]] |

  .alice |  a# ))                                  o/ a# ]  ]  g# ]]  f# ]] |
  .bob   |  c# ]. _f# ]]  ]] _g# ]] _a# ]] c ]] c# ]. ]]    ]  c  ]] _a# ]] |

  .alice | g# ].  f# ]]  f ))                      )               |
  .bob   | c# ]. _g# ]]    ]] ]] _f# ]  _g# ]. ]]  ]] _f# ]] _g# ] |

  .alice |  d# ] ]]  f ]]  f# ))                   f ] d#  ] |
  .bob   | _f# ] ]] _f ]] _f# ] ]] _g# ]]  _a# ) _g# ] _f# ] |

  .alice |  c# ] ]]  d# ]]  f ))                 d# ]  c# ] |
  .bob   | _f  ] ]] _d# ]] _f ] ]] _f# ]] _g# ) _f# ] _d# ] |

  .alice |  c ] ]]  d ]]  e ))                   g )     |
  .bob   | _e ] ]] _d ]] _e ] ]] _g ] ]] _a ]] _a# ] c ] |

  .alice |  f ]     _f ]] ]]  ] ]] ]]   ] ]] ]]   ]  ]    |
  .bob   | _a ] o~  _a ]] ]]  ] ]] ]]   ] ]] ]]   ]  ] ~o |

!}

{! melody_b !! .bass !bassline_b

  .alice | _a# ) _f )__          o/. _a# ]]  ]]   c ]]  d ]] d# ]] |
  .bob   | _d  )    ]] ]] _c ] _d ].     ]]  ]] _d# ]] _f ]] _g ]] |

  .alice |  f  ))                             o/ ]   f ]  f# ]] g# ]] |
  .bob   | _g# ]. _a# ]] ]] c ]] d ]] d# ]] f )    _g# ] _a# ]] c  ]] |

  .alice | a# )). ~o c# ) | c  ) o~ a )) f  ) |  f# )).  a# ) | a )  f )) ) |
  .bob   | c# )).    e  ) | d# )    c )) _a ) | _b  )).  c# ) | c ) _a )) ) |

  .alice |  f# )). a# ) | a )  f )) d ) |  d# )).  f# ) |  f  )  c# )) _a# ) |
  .bob   | _b  )). c# ) | c ) _a ))   ) | _f# )). _b  ) | _a# ) _f  )) _c# ) |

  .alice |  c ] ]]  d ]]  e ))                        g  )     |
  .bob   | _e ] ]] _d ]] _e ] ]] _f ]] _g ] ]] _a ]] _a# ] c ] |

  .alice |  f ]    _f ]] ]]  ] ]] ]]   ] ]] ]]   ]  ]    |
  .bob   | _a ] o~ _a ]] ]]  ] ]] ]]   ] ]] ]]   ]  ] ~o |

!}

{! fill !!
  .alice |  f ]    _f ]] ]]  ] ]] ]]   ] ]] ]]   ]  ]    |
  .bob   | _a ] o~ _a ]] ]]  ] ]] ]]   ] ]] ]]   ]  ] ~o |
  .snare |    ]       ]] ]]  ] ]] ]]   ] ]] ]]   ]  ]    |
  .hats  |    ]       ]      ] ]       ] ]       ]  ]    |
  .kick  |    )              }         )         }       |
  .bass !bass_end<f>
!}

{! drums !!
.hats  |: ] ] ] ] ] ] ] ]] ]] :| :| :| :| :| :| :| :| :| :| :|
.snare |: } ) } ) :| :| :| :| :| :| :| :| :| :| ] ]] ]]  ] ]] ]]  ] ]] ]]  ]  ] |
.kick  |: ) } ) } :| :| :| :| :| :| :| :| :| :| :|
!}

!intro
!melody_a

.kick !eight_bars_rest
.hats !four_bars_rest }}} }}} }}} ] ] ] ] ] ] ] ]
.snare !eight_bars_rest
!fill

!melody_b
!drums

!fill

        """)
