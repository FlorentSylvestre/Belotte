SYSTEM_CLEAR = {'linux': 'clear',
                'win32': 'cls',
                'cygwin': 'cls',
                'nt': 'cls',
                'darwin': 'clear',
                'posix': 'clear'}

# GUI Constant
CARD_CHAR = {'SPADE': '\u2664',
             'HEART': '\u2661',
             'DIAMOND': '\u2662',
             'CLUB': '\u2667'}
CARD_CHAR_PLAYABLE = {'SPADE': '\u2660',
                      'HEART': '\u2665',
                      'DIAMOND': '\u2666',
                      'CLUB': '\u2663'}
CARD_PLOT_STRING = {'deck_': "",
                    'dummy_v': "0.0.|.0.1.‾.0.2.‾.0.3.‾.0.4.|.1.0.|.2.0.|.3.0.|.3.1._.3.2._.3.3._.3.4.|.2.4.|.1.4.|",
                    'dummy_h': "0.1._.0.2._.0.3._.0.4._.1.0.|.2.1.‾.2.2.‾.2.3.‾.2.4.‾.1.5.|",
                    'real_h': "0.0.|.0.1.‾.0.2.‾.0.3.‾.0.4.‾.0.5.‾.0.6.‾.0.7.‾.0.8.‾.0.9.‾.0.10.|.1.0.|.1.10.|.2.0." +
                              "|.2.8.|.2.0.|.2.10.|.2.1._.2.2._.2.3._.2.4._.2.5._.2.6._.2.7._.2.8._.2.9._.2.10.|",
                    'real_v': "0.0.|.0.1.‾.0.2.‾.0.3.‾.0.4.‾.0.5.‾.0.6.|.1.0.|.1.6.|.2.0.|.2.6.|" +
                              ".3.0.|.3.6.|.4.0.|.4.6.|.4.1._.4.2._.4.3._.4.4._.4.5._.4.6.|"
                    }
CARD_PLOT_COORD = {'flipped': (16, 43),
                   'real_v_hand_1': (33, 9),
                   'real_v_played_1': (25, 43),
                   'real_h_played_2': (15, 22),
                   'real_v_played_3': (7, 43),
                   'real_h_played_4': (15, 67),
                   'dummy_h_hand_2': (8, 1),
                   'dummy_v_hand_3': (1, 9),
                   "dummy_h_hand_4": (8, 88),
                   'deck': (None, None)}
PLAYER_ORIENTATION = {'1': "v",
                      '2': "h",
                      '3': "v",
                      '4': "h",
                      None: "v"}
OFFSET = {'v': [0, 10],
          'h': [3, 0]}
INIT_OFFSET = {'1': [0, 0], '2': [0, 0], '3': [0, 0], '4': [0, 0], 'flipped': [0, 0],
               'played': [0, 0], 'deck': [0, 0]}

# Game Constant
WIN_SCORE = 1000
TOTAL_SCORE_ROUND = 162
BELOTE_SUITS = 'SPADE HEART DIAMOND CLUB'.split()
BELOTE_VALUES = 'A 10 J Q K 7 8 9'.split()
BELOTE_SCORE = {'A': 11,
                '10': 10,
                'K': 4,
                'Q': 3,
                'J': 2,
                '7': 0,
                '8': 0,
                '9': 0}
BELOTE_TRUMP_SCORE = {'J': 20,
                      '9': 14,
                      'A': 11,
                      '10': 10,
                      'K': 4,
                      'Q': 3,
                      '8': 0,
                      '7': 0}
