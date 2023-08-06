# Copyright (C) 2021 Majormode.  All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import re
import unidecode

from majormode.perseus.model.enum import Enum


class IncompleteFullNameException(Exception):
    """
    If none of the first name or the last name parts are in the full name
    of a person
    """


class InvalidLexicalNameOrderException(Exception):
    """
    Indicate that the full name of a person is not formatted according to
    the lexical order of the person's culture
    """


LexicalNameOrder = Enum(
    # The family name comes first, while the given name comes last. This
    # order is primarily used in East Asia (for example in China, Japan and
    # Korea), as well as in Southeast Asia (Cambodia and Vietnam), and
    # southern and north eastern parts of India.  Also in Central Europe is
    # used by Hungarians.
    'EasternOrder',

    # The given name comes first, while the family name comes last.  This
    # order is usually used in most European countries and in countries that
    # have cultures predominantly influenced by Western Europe (e.g. North
    # and South America, North, East, Central and West India, Thailand,
    # Australia, New Zealand and the Philippines).
    'WesternOrder',
)

# Lexical name orders simplistically deduced from the order of genitive
# and noun:
#
# Matthew S. Dryer. 2013. Order of Genitive and Noun.
# In: Dryer, Matthew S. & Haspelmath, Martin (eds.)
# The World Atlas of Language Structures Online.
# Leipzig: Max Planck Institute for Evolutionary Anthropology.
# (Available online at http://wals.info/chapter/86, Accessed on 2021-03-24.)
LEXICAL_NAME_ORDERS = {
    'aar': LexicalNameOrder.EasternOrder,
    'aba': LexicalNameOrder.EasternOrder,
    'abk': LexicalNameOrder.EasternOrder,
    'abo': LexicalNameOrder.WesternOrder,
    'abu': LexicalNameOrder.EasternOrder,
    'abv': LexicalNameOrder.EasternOrder,
    'ace': LexicalNameOrder.WesternOrder,
    'acg': LexicalNameOrder.EasternOrder,
    'acl': LexicalNameOrder.WesternOrder,
    'acn': LexicalNameOrder.EasternOrder,
    'aco': LexicalNameOrder.EasternOrder,
    'acu': LexicalNameOrder.EasternOrder,
    'adg': LexicalNameOrder.EasternOrder,
    'adi': LexicalNameOrder.EasternOrder,
    'adk': LexicalNameOrder.EasternOrder,
    'adn': LexicalNameOrder.EasternOrder,
    'adz': LexicalNameOrder.EasternOrder,
    'aeg': LexicalNameOrder.WesternOrder,
    'aga': LexicalNameOrder.EasternOrder,
    'agb': LexicalNameOrder.WesternOrder,
    'agc': LexicalNameOrder.WesternOrder,
    'agd': LexicalNameOrder.WesternOrder,
    'agh': LexicalNameOrder.WesternOrder,
    'agm': LexicalNameOrder.EasternOrder,
    'ain': LexicalNameOrder.EasternOrder,
    'aja': LexicalNameOrder.WesternOrder,
    'akh': LexicalNameOrder.EasternOrder,
    'akn': LexicalNameOrder.EasternOrder,
    'ala': LexicalNameOrder.EasternOrder,
    'alb': LexicalNameOrder.WesternOrder,
    'all': LexicalNameOrder.EasternOrder,
    'aln': LexicalNameOrder.EasternOrder,
    'als': LexicalNameOrder.EasternOrder,
    'aly': LexicalNameOrder.WesternOrder,
    'amb': LexicalNameOrder.EasternOrder,
    'amc': LexicalNameOrder.EasternOrder,
    'ame': LexicalNameOrder.EasternOrder,
    'amh': LexicalNameOrder.EasternOrder,
    'ami': LexicalNameOrder.WesternOrder,
    'aml': LexicalNameOrder.WesternOrder,
    'amm': LexicalNameOrder.EasternOrder,
    'amn': LexicalNameOrder.EasternOrder,
    'amq': LexicalNameOrder.EasternOrder,
    'amr': LexicalNameOrder.WesternOrder,
    'ams': LexicalNameOrder.WesternOrder,
    'amt': LexicalNameOrder.EasternOrder,
    'amx': LexicalNameOrder.EasternOrder,
    'ana': LexicalNameOrder.EasternOrder,
    'anc': LexicalNameOrder.WesternOrder,
    'ang': LexicalNameOrder.EasternOrder,
    'ani': LexicalNameOrder.EasternOrder,
    'anj': LexicalNameOrder.WesternOrder,
    'ano': LexicalNameOrder.EasternOrder,
    'anu': LexicalNameOrder.EasternOrder,
    'any': LexicalNameOrder.WesternOrder,
    'aoj': LexicalNameOrder.WesternOrder,
    'api': LexicalNameOrder.EasternOrder,
    'apl': LexicalNameOrder.EasternOrder,
    'apt': LexicalNameOrder.EasternOrder,
    'apu': LexicalNameOrder.EasternOrder,
    'ara': LexicalNameOrder.EasternOrder,
    'arc': LexicalNameOrder.EasternOrder,
    'arg': LexicalNameOrder.WesternOrder,
    'ari': LexicalNameOrder.EasternOrder,
    'arj': LexicalNameOrder.WesternOrder,
    'arm': LexicalNameOrder.EasternOrder,
    'aro': LexicalNameOrder.WesternOrder,
    'arq': LexicalNameOrder.WesternOrder,
    'arw': LexicalNameOrder.EasternOrder,
    'asm': LexicalNameOrder.EasternOrder,
    'ass': LexicalNameOrder.EasternOrder,
    'asy': LexicalNameOrder.WesternOrder,
    'ata': LexicalNameOrder.WesternOrder,
    'ath': LexicalNameOrder.EasternOrder,
    'atk': LexicalNameOrder.EasternOrder,
    'ava': LexicalNameOrder.EasternOrder,
    'awa': LexicalNameOrder.EasternOrder,
    'awe': LexicalNameOrder.WesternOrder,
    'awi': LexicalNameOrder.EasternOrder,
    'awp': LexicalNameOrder.EasternOrder,
    'awt': LexicalNameOrder.EasternOrder,
    'ayi': LexicalNameOrder.EasternOrder,
    'aym': LexicalNameOrder.EasternOrder,
    'ayo': LexicalNameOrder.EasternOrder,
    'ayr': LexicalNameOrder.EasternOrder,
    'ayw': LexicalNameOrder.WesternOrder,
    'aze': LexicalNameOrder.EasternOrder,
    'baa': LexicalNameOrder.EasternOrder,
    'bae': LexicalNameOrder.EasternOrder,
    'bag': LexicalNameOrder.WesternOrder,
    'bai': LexicalNameOrder.EasternOrder,
    'baj': LexicalNameOrder.WesternOrder,
    'bak': LexicalNameOrder.WesternOrder,
    'bam': LexicalNameOrder.EasternOrder,
    'baq': LexicalNameOrder.WesternOrder,
    'bar': LexicalNameOrder.WesternOrder,
    'bas': LexicalNameOrder.WesternOrder,
    'baw': LexicalNameOrder.EasternOrder,
    'bbu': LexicalNameOrder.WesternOrder,
    'bbw': LexicalNameOrder.EasternOrder,
    'bch': LexicalNameOrder.WesternOrder,
    'bco': LexicalNameOrder.WesternOrder,
    'bdm': LexicalNameOrder.EasternOrder,
    'bdu': LexicalNameOrder.WesternOrder,
    'bej': LexicalNameOrder.EasternOrder,
    'bel': LexicalNameOrder.EasternOrder,
    'bfg': LexicalNameOrder.WesternOrder,
    'bfi': LexicalNameOrder.WesternOrder,
    'bga': LexicalNameOrder.WesternOrder,
    'bgo': LexicalNameOrder.WesternOrder,
    'bgr': LexicalNameOrder.WesternOrder,
    'bho': LexicalNameOrder.EasternOrder,
    'bhu': LexicalNameOrder.EasternOrder,
    'bid': LexicalNameOrder.WesternOrder,
    'bii': LexicalNameOrder.EasternOrder,
    'bik': LexicalNameOrder.EasternOrder,
    'bil': LexicalNameOrder.EasternOrder,
    'bin': LexicalNameOrder.EasternOrder,
    'bio': LexicalNameOrder.EasternOrder,
    'bir': LexicalNameOrder.WesternOrder,
    'bka': LexicalNameOrder.WesternOrder,
    'bkr': LexicalNameOrder.WesternOrder,
    'bkt': LexicalNameOrder.EasternOrder,
    'bku': LexicalNameOrder.WesternOrder,
    'bla': LexicalNameOrder.EasternOrder,
    'bln': LexicalNameOrder.EasternOrder,
    'blr': LexicalNameOrder.WesternOrder,
    'blx': LexicalNameOrder.EasternOrder,
    'blz': LexicalNameOrder.WesternOrder,
    'bma': LexicalNameOrder.WesternOrder,
    'bmb': LexicalNameOrder.EasternOrder,
    'bnb': LexicalNameOrder.EasternOrder,
    'bni': LexicalNameOrder.WesternOrder,
    'bnk': LexicalNameOrder.WesternOrder,
    'bnn': LexicalNameOrder.WesternOrder,
    'bob': LexicalNameOrder.WesternOrder,
    'bod': LexicalNameOrder.EasternOrder,
    'bok': LexicalNameOrder.EasternOrder,
    'bol': LexicalNameOrder.WesternOrder,
    'bon': LexicalNameOrder.EasternOrder,
    'bra': LexicalNameOrder.WesternOrder,
    'bre': LexicalNameOrder.WesternOrder,
    'brf': LexicalNameOrder.WesternOrder,
    'bri': LexicalNameOrder.EasternOrder,
    'brm': LexicalNameOrder.EasternOrder,
    'brn': LexicalNameOrder.WesternOrder,
    'brp': LexicalNameOrder.WesternOrder,
    'brq': LexicalNameOrder.WesternOrder,
    'brs': LexicalNameOrder.EasternOrder,
    'bry': LexicalNameOrder.EasternOrder,
    'bsk': LexicalNameOrder.EasternOrder,
    'bsq': LexicalNameOrder.EasternOrder,
    'bsr': LexicalNameOrder.WesternOrder,
    'btk': LexicalNameOrder.WesternOrder,
    'bto': LexicalNameOrder.WesternOrder,
    'bud': LexicalNameOrder.WesternOrder,
    'bug': LexicalNameOrder.WesternOrder,
    'bum': LexicalNameOrder.WesternOrder,
    'bur': LexicalNameOrder.EasternOrder,
    'bus': LexicalNameOrder.EasternOrder,
    'but': LexicalNameOrder.EasternOrder,
    'buu': LexicalNameOrder.EasternOrder,
    'buw': LexicalNameOrder.WesternOrder,
    'bvi': LexicalNameOrder.WesternOrder,
    'bwc': LexicalNameOrder.WesternOrder,
    'bya': LexicalNameOrder.EasternOrder,
    'cah': LexicalNameOrder.EasternOrder,
    'cai': LexicalNameOrder.WesternOrder,
    'cak': LexicalNameOrder.WesternOrder,
    'can': LexicalNameOrder.EasternOrder,
    'car': LexicalNameOrder.EasternOrder,
    'cas': LexicalNameOrder.EasternOrder,
    'cav': LexicalNameOrder.EasternOrder,
    'cax': LexicalNameOrder.EasternOrder,
    'cay': LexicalNameOrder.EasternOrder,
    'cba': LexicalNameOrder.WesternOrder,
    'cbo': LexicalNameOrder.EasternOrder,
    'ccm': LexicalNameOrder.WesternOrder,
    'cct': LexicalNameOrder.EasternOrder,
    'cde': LexicalNameOrder.EasternOrder,
    'ceb': LexicalNameOrder.WesternOrder,
    'cem': LexicalNameOrder.WesternOrder,
    'cha': LexicalNameOrder.WesternOrder,
    'chc': LexicalNameOrder.EasternOrder,
    'che': LexicalNameOrder.EasternOrder,
    'chg': LexicalNameOrder.EasternOrder,
    'chh': LexicalNameOrder.EasternOrder,
    'chi': LexicalNameOrder.EasternOrder,
    'chj': LexicalNameOrder.WesternOrder,
    'chk': LexicalNameOrder.EasternOrder,
    'chn': LexicalNameOrder.EasternOrder,
    'chq': LexicalNameOrder.WesternOrder,
    'chr': LexicalNameOrder.WesternOrder,
    'chs': LexicalNameOrder.EasternOrder,
    'chv': LexicalNameOrder.EasternOrder,
    'chx': LexicalNameOrder.WesternOrder,
    'cic': LexicalNameOrder.WesternOrder,
    'cld': LexicalNameOrder.WesternOrder,
    'cle': LexicalNameOrder.WesternOrder,
    'cln': LexicalNameOrder.EasternOrder,
    'cme': LexicalNameOrder.WesternOrder,
    'cmh': LexicalNameOrder.EasternOrder,
    'cml': LexicalNameOrder.EasternOrder,
    'cmn': LexicalNameOrder.EasternOrder,
    'cmr': LexicalNameOrder.EasternOrder,
    'cmx': LexicalNameOrder.WesternOrder,
    'cmy': LexicalNameOrder.WesternOrder,
    'cnl': LexicalNameOrder.EasternOrder,
    'cnm': LexicalNameOrder.EasternOrder,
    'cnt': LexicalNameOrder.EasternOrder,
    'coa': LexicalNameOrder.EasternOrder,
    'coc': LexicalNameOrder.EasternOrder,
    'cop': LexicalNameOrder.WesternOrder,
    'cpl': LexicalNameOrder.WesternOrder,
    'cpn': LexicalNameOrder.EasternOrder,
    'cpy': LexicalNameOrder.EasternOrder,
    'cqt': LexicalNameOrder.WesternOrder,
    'crn': LexicalNameOrder.WesternOrder,
    'cro': LexicalNameOrder.EasternOrder,
    'cso': LexicalNameOrder.WesternOrder,
    'cti': LexicalNameOrder.EasternOrder,
    'ctl': LexicalNameOrder.WesternOrder,
    'ctm': LexicalNameOrder.EasternOrder,
    'ctw': LexicalNameOrder.EasternOrder,
    'cub': LexicalNameOrder.EasternOrder,
    'cup': LexicalNameOrder.EasternOrder,
    'cya': LexicalNameOrder.WesternOrder,
    'cyv': LexicalNameOrder.WesternOrder,
    'dag': LexicalNameOrder.EasternOrder,
    'dan': LexicalNameOrder.EasternOrder,
    'daw': LexicalNameOrder.EasternOrder,
    'day': LexicalNameOrder.WesternOrder,
    'dds': LexicalNameOrder.EasternOrder,
    'der': LexicalNameOrder.EasternOrder,
    'des': LexicalNameOrder.EasternOrder,
    'deu': LexicalNameOrder.EasternOrder,
    'dga': LexicalNameOrder.EasternOrder,
    'dgb': LexicalNameOrder.EasternOrder,
    'dgo': LexicalNameOrder.WesternOrder,
    'dgr': LexicalNameOrder.EasternOrder,
    'dha': LexicalNameOrder.EasternOrder,
    'dhb': LexicalNameOrder.EasternOrder,
    'dhi': LexicalNameOrder.EasternOrder,
    'dhm': LexicalNameOrder.EasternOrder,
    'did': LexicalNameOrder.WesternOrder,
    'die': LexicalNameOrder.EasternOrder,
    'dig': LexicalNameOrder.EasternOrder,
    'din': LexicalNameOrder.WesternOrder,
    'dio': LexicalNameOrder.WesternOrder,
    'diy': LexicalNameOrder.EasternOrder,
    'dji': LexicalNameOrder.WesternOrder,
    'djn': LexicalNameOrder.EasternOrder,
    'dlm': LexicalNameOrder.EasternOrder,
    'dmi': LexicalNameOrder.EasternOrder,
    'dni': LexicalNameOrder.EasternOrder,
    'dom': LexicalNameOrder.EasternOrder,
    'doy': LexicalNameOrder.EasternOrder,
    'dre': LexicalNameOrder.WesternOrder,
    'drg': LexicalNameOrder.EasternOrder,
    'drm': LexicalNameOrder.EasternOrder,
    'dsh': LexicalNameOrder.EasternOrder,
    'dua': LexicalNameOrder.WesternOrder,
    'duk': LexicalNameOrder.WesternOrder,
    'dul': LexicalNameOrder.EasternOrder,
    'dum': LexicalNameOrder.EasternOrder,
    'dun': LexicalNameOrder.EasternOrder,
    'dut': LexicalNameOrder.WesternOrder,
    'dyi': LexicalNameOrder.EasternOrder,
    'edo': LexicalNameOrder.EasternOrder,
    'ega': LexicalNameOrder.EasternOrder,
    'egn': LexicalNameOrder.WesternOrder,
    'eip': LexicalNameOrder.EasternOrder,
    'emb': LexicalNameOrder.EasternOrder,
    'eme': LexicalNameOrder.EasternOrder,
    'eng': LexicalNameOrder.WesternOrder,
    'eno': LexicalNameOrder.WesternOrder,
    'epe': LexicalNameOrder.EasternOrder,
    'erk': LexicalNameOrder.WesternOrder,
    'err': LexicalNameOrder.WesternOrder,
    'ese': LexicalNameOrder.EasternOrder,
    'esm': LexicalNameOrder.WesternOrder,
    'est': LexicalNameOrder.EasternOrder,
    'eud': LexicalNameOrder.EasternOrder,
    'eve': LexicalNameOrder.EasternOrder,
    'ewe': LexicalNameOrder.EasternOrder,
    'ewo': LexicalNameOrder.WesternOrder,
    'fas': LexicalNameOrder.EasternOrder,
    'fij': LexicalNameOrder.WesternOrder,
    'fin': LexicalNameOrder.EasternOrder,
    'fon': LexicalNameOrder.WesternOrder,
    'for': LexicalNameOrder.EasternOrder,
    'fqs': LexicalNameOrder.EasternOrder,
    'fra': LexicalNameOrder.WesternOrder,
    'fua': LexicalNameOrder.WesternOrder,
    'ful': LexicalNameOrder.EasternOrder,
    'fur': LexicalNameOrder.EasternOrder,
    'fut': LexicalNameOrder.WesternOrder,
    'fye': LexicalNameOrder.WesternOrder,
    'gae': LexicalNameOrder.WesternOrder,
    'gam': LexicalNameOrder.EasternOrder,
    'gan': LexicalNameOrder.EasternOrder,
    'gap': LexicalNameOrder.EasternOrder,
    'gar': LexicalNameOrder.EasternOrder,
    'gav': LexicalNameOrder.EasternOrder,
    'gbb': LexicalNameOrder.WesternOrder,
    'gbs': LexicalNameOrder.WesternOrder,
    'gds': LexicalNameOrder.EasternOrder,
    'gel': LexicalNameOrder.WesternOrder,
    'geo': LexicalNameOrder.EasternOrder,
    'ger': LexicalNameOrder.WesternOrder,
    'gjj': LexicalNameOrder.EasternOrder,
    'gln': LexicalNameOrder.EasternOrder,
    'gmw': LexicalNameOrder.EasternOrder,
    'gmz': LexicalNameOrder.WesternOrder,
    'gnd': LexicalNameOrder.WesternOrder,
    'gnn': LexicalNameOrder.EasternOrder,
    'goa': LexicalNameOrder.WesternOrder,
    'god': LexicalNameOrder.EasternOrder,
    'goe': LexicalNameOrder.WesternOrder,
    'gok': LexicalNameOrder.WesternOrder,
    'gon': LexicalNameOrder.EasternOrder,
    'grb': LexicalNameOrder.EasternOrder,
    'grf': LexicalNameOrder.WesternOrder,
    'grj': LexicalNameOrder.EasternOrder,
    'grk': LexicalNameOrder.WesternOrder,
    'grr': LexicalNameOrder.EasternOrder,
    'grw': LexicalNameOrder.EasternOrder,
    'gto': LexicalNameOrder.WesternOrder,
    'gua': LexicalNameOrder.EasternOrder,
    'gud': LexicalNameOrder.WesternOrder,
    'gul': LexicalNameOrder.WesternOrder,
    'gur': LexicalNameOrder.EasternOrder,
    'gwa': LexicalNameOrder.EasternOrder,
    'gwo': LexicalNameOrder.WesternOrder,
    'gyc': LexicalNameOrder.EasternOrder,
    'hai': LexicalNameOrder.EasternOrder,
    'hal': LexicalNameOrder.WesternOrder,
    'har': LexicalNameOrder.EasternOrder,
    'hat': LexicalNameOrder.EasternOrder,
    'hau': LexicalNameOrder.WesternOrder,
    'haw': LexicalNameOrder.WesternOrder,
    'hay': LexicalNameOrder.EasternOrder,
    'hdi': LexicalNameOrder.WesternOrder,
    'heb': LexicalNameOrder.WesternOrder,
    'hei': LexicalNameOrder.WesternOrder,
    'hhu': LexicalNameOrder.EasternOrder,
    'hid': LexicalNameOrder.EasternOrder,
    'hil': LexicalNameOrder.WesternOrder,
    'hin': LexicalNameOrder.EasternOrder,
    'hix': LexicalNameOrder.EasternOrder,
    'hma': LexicalNameOrder.EasternOrder,
    'hmo': LexicalNameOrder.EasternOrder,
    'hna': LexicalNameOrder.WesternOrder,
    'hnd': LexicalNameOrder.WesternOrder,
    'hoa': LexicalNameOrder.WesternOrder,
    'hop': LexicalNameOrder.EasternOrder,
    'hpd': LexicalNameOrder.EasternOrder,
    'htc': LexicalNameOrder.WesternOrder,
    'hua': LexicalNameOrder.EasternOrder,
    'huc': LexicalNameOrder.EasternOrder,
    'hui': LexicalNameOrder.EasternOrder,
    'hum': LexicalNameOrder.EasternOrder,
    'hun': LexicalNameOrder.EasternOrder,
    'hup': LexicalNameOrder.EasternOrder,
    'hve': LexicalNameOrder.WesternOrder,
    'hzb': LexicalNameOrder.EasternOrder,
    'iaa': LexicalNameOrder.WesternOrder,
    'iau': LexicalNameOrder.EasternOrder,
    'iba': LexicalNameOrder.WesternOrder,
    'ice': LexicalNameOrder.WesternOrder,
    'idn': LexicalNameOrder.EasternOrder,
    'ifm': LexicalNameOrder.WesternOrder,
    'ifu': LexicalNameOrder.WesternOrder,
    'igb': LexicalNameOrder.WesternOrder,
    'ign': LexicalNameOrder.WesternOrder,
    'igs': LexicalNameOrder.WesternOrder,
    'ijo': LexicalNameOrder.EasternOrder,
    'ika': LexicalNameOrder.EasternOrder,
    'ila': LexicalNameOrder.WesternOrder,
    'imo': LexicalNameOrder.EasternOrder,
    'ina': LexicalNameOrder.EasternOrder,
    'ind': LexicalNameOrder.WesternOrder,
    'ing': LexicalNameOrder.EasternOrder,
    'iqu': LexicalNameOrder.EasternOrder,
    'iri': LexicalNameOrder.WesternOrder,
    'irq': LexicalNameOrder.WesternOrder,
    'irr': LexicalNameOrder.EasternOrder,
    'irx': LexicalNameOrder.EasternOrder,
    'isa': LexicalNameOrder.WesternOrder,
    'ita': LexicalNameOrder.WesternOrder,
    'iwa': LexicalNameOrder.EasternOrder,
    'izi': LexicalNameOrder.WesternOrder,
    'jab': LexicalNameOrder.EasternOrder,
    'jak': LexicalNameOrder.WesternOrder,
    'jaq': LexicalNameOrder.EasternOrder,
    'jar': LexicalNameOrder.WesternOrder,
    'jeb': LexicalNameOrder.WesternOrder,
    'jel': LexicalNameOrder.EasternOrder,
    'jiv': LexicalNameOrder.EasternOrder,
    'jlu': LexicalNameOrder.WesternOrder,
    'jmo': LexicalNameOrder.WesternOrder,
    'jms': LexicalNameOrder.EasternOrder,
    'jng': LexicalNameOrder.EasternOrder,
    'jpn': LexicalNameOrder.EasternOrder,
    'juh': LexicalNameOrder.EasternOrder,
    'juk': LexicalNameOrder.WesternOrder,
    'jva': LexicalNameOrder.EasternOrder,
    'kaa': LexicalNameOrder.EasternOrder,
    'kab': LexicalNameOrder.EasternOrder,
    'kad': LexicalNameOrder.WesternOrder,
    'kae': LexicalNameOrder.EasternOrder,
    'kan': LexicalNameOrder.WesternOrder,
    'kar': LexicalNameOrder.WesternOrder,
    'kas': LexicalNameOrder.EasternOrder,
    'kay': LexicalNameOrder.EasternOrder,
    'kba': LexicalNameOrder.WesternOrder,
    'kbl': LexicalNameOrder.WesternOrder,
    'kbt': LexicalNameOrder.EasternOrder,
    'kbu': LexicalNameOrder.WesternOrder,
    'kbw': LexicalNameOrder.EasternOrder,
    'kby': LexicalNameOrder.EasternOrder,
    'kch': LexicalNameOrder.EasternOrder,
    'kdz': LexicalNameOrder.WesternOrder,
    'kel': LexicalNameOrder.WesternOrder,
    'kem': LexicalNameOrder.EasternOrder,
    'ken': LexicalNameOrder.WesternOrder,
    'ker': LexicalNameOrder.WesternOrder,
    'ket': LexicalNameOrder.EasternOrder,
    'kew': LexicalNameOrder.EasternOrder,
    'kfe': LexicalNameOrder.EasternOrder,
    'kga': LexicalNameOrder.WesternOrder,
    'kgu': LexicalNameOrder.EasternOrder,
    'kgy': LexicalNameOrder.EasternOrder,
    'kha': LexicalNameOrder.EasternOrder,
    'khd': LexicalNameOrder.EasternOrder,
    'khg': LexicalNameOrder.EasternOrder,
    'khi': LexicalNameOrder.EasternOrder,
    'khl': LexicalNameOrder.EasternOrder,
    'khm': LexicalNameOrder.WesternOrder,
    'kho': LexicalNameOrder.EasternOrder,
    'khs': LexicalNameOrder.WesternOrder,
    'khw': LexicalNameOrder.EasternOrder,
    'kik': LexicalNameOrder.WesternOrder,
    'kim': LexicalNameOrder.EasternOrder,
    'kio': LexicalNameOrder.EasternOrder,
    'kir': LexicalNameOrder.EasternOrder,
    'kis': LexicalNameOrder.WesternOrder,
    'kiw': LexicalNameOrder.EasternOrder,
    'kje': LexicalNameOrder.EasternOrder,
    'kkp': LexicalNameOrder.EasternOrder,
    'kkq': LexicalNameOrder.EasternOrder,
    'kkt': LexicalNameOrder.WesternOrder,
    'kku': LexicalNameOrder.EasternOrder,
    'kkv': LexicalNameOrder.EasternOrder,
    'kla': LexicalNameOrder.EasternOrder,
    'klg': LexicalNameOrder.EasternOrder,
    'kll': LexicalNameOrder.EasternOrder,
    'klm': LexicalNameOrder.EasternOrder,
    'klq': LexicalNameOrder.EasternOrder,
    'klr': LexicalNameOrder.EasternOrder,
    'kls': LexicalNameOrder.WesternOrder,
    'klv': LexicalNameOrder.EasternOrder,
    'kma': LexicalNameOrder.EasternOrder,
    'kmb': LexicalNameOrder.EasternOrder,
    'kmh': LexicalNameOrder.EasternOrder,
    'kmj': LexicalNameOrder.WesternOrder,
    'kmk': LexicalNameOrder.EasternOrder,
    'kmo': LexicalNameOrder.EasternOrder,
    'kmp': LexicalNameOrder.EasternOrder,
    'kms': LexicalNameOrder.EasternOrder,
    'kmu': LexicalNameOrder.WesternOrder,
    'kmz': LexicalNameOrder.EasternOrder,
    'knb': LexicalNameOrder.EasternOrder,
    'knc': LexicalNameOrder.WesternOrder,
    'knd': LexicalNameOrder.EasternOrder,
    'kng': LexicalNameOrder.EasternOrder,
    'kni': LexicalNameOrder.EasternOrder,
    'knk': LexicalNameOrder.WesternOrder,
    'knm': LexicalNameOrder.EasternOrder,
    'knn': LexicalNameOrder.EasternOrder,
    'kno': LexicalNameOrder.EasternOrder,
    'knr': LexicalNameOrder.WesternOrder,
    'knw': LexicalNameOrder.EasternOrder,
    'knz': LexicalNameOrder.EasternOrder,
    'koa': LexicalNameOrder.EasternOrder,
    'kob': LexicalNameOrder.EasternOrder,
    'koe': LexicalNameOrder.WesternOrder,
    'kok': LexicalNameOrder.EasternOrder,
    'kol': LexicalNameOrder.EasternOrder,
    'kom': LexicalNameOrder.WesternOrder,
    'kon': LexicalNameOrder.WesternOrder,
    'kop': LexicalNameOrder.EasternOrder,
    'kor': LexicalNameOrder.EasternOrder,
    'kos': LexicalNameOrder.WesternOrder,
    'koy': LexicalNameOrder.EasternOrder,
    'kpe': LexicalNameOrder.EasternOrder,
    'kpm': LexicalNameOrder.WesternOrder,
    'kpw': LexicalNameOrder.EasternOrder,
    'kqq': LexicalNameOrder.EasternOrder,
    'krb': LexicalNameOrder.WesternOrder,
    'krc': LexicalNameOrder.EasternOrder,
    'krd': LexicalNameOrder.WesternOrder,
    'kre': LexicalNameOrder.WesternOrder,
    'kri': LexicalNameOrder.WesternOrder,
    'krk': LexicalNameOrder.EasternOrder,
    'krn': LexicalNameOrder.EasternOrder,
    'kro': LexicalNameOrder.WesternOrder,
    'krr': LexicalNameOrder.WesternOrder,
    'krw': LexicalNameOrder.EasternOrder,
    'kry': LexicalNameOrder.EasternOrder,
    'krz': LexicalNameOrder.EasternOrder,
    'ksa': LexicalNameOrder.EasternOrder,
    'kse': LexicalNameOrder.EasternOrder,
    'ksg': LexicalNameOrder.EasternOrder,
    'kta': LexicalNameOrder.EasternOrder,
    'ktc': LexicalNameOrder.WesternOrder,
    'kti': LexicalNameOrder.EasternOrder,
    'ktl': LexicalNameOrder.WesternOrder,
    'ktu': LexicalNameOrder.WesternOrder,
    'kty': LexicalNameOrder.EasternOrder,
    'kum': LexicalNameOrder.EasternOrder,
    'kuo': LexicalNameOrder.WesternOrder,
    'kut': LexicalNameOrder.WesternOrder,
    'kuv': LexicalNameOrder.EasternOrder,
    'kwk': LexicalNameOrder.WesternOrder,
    'kwm': LexicalNameOrder.WesternOrder,
    'kwn': LexicalNameOrder.WesternOrder,
    'kwo': LexicalNameOrder.EasternOrder,
    'kwt': LexicalNameOrder.EasternOrder,
    'kwz': LexicalNameOrder.EasternOrder,
    'kxo': LexicalNameOrder.EasternOrder,
    'kyl': LexicalNameOrder.EasternOrder,
    'kyn': LexicalNameOrder.EasternOrder,
    'kyo': LexicalNameOrder.WesternOrder,
    'kyr': LexicalNameOrder.EasternOrder,
    'kyz': LexicalNameOrder.EasternOrder,
    'kzy': LexicalNameOrder.EasternOrder,
    'laa': LexicalNameOrder.WesternOrder,
    'lab': LexicalNameOrder.EasternOrder,
    'lac': LexicalNameOrder.WesternOrder,
    'lad': LexicalNameOrder.EasternOrder,
    'lag': LexicalNameOrder.WesternOrder,
    'lah': LexicalNameOrder.EasternOrder,
    'lai': LexicalNameOrder.EasternOrder,
    'lal': LexicalNameOrder.EasternOrder,
    'lan': LexicalNameOrder.WesternOrder,
    'lao': LexicalNameOrder.WesternOrder,
    'lar': LexicalNameOrder.WesternOrder,
    'lat': LexicalNameOrder.EasternOrder,
    'lav': LexicalNameOrder.EasternOrder,
    'lbu': LexicalNameOrder.WesternOrder,
    'lda': LexicalNameOrder.WesternOrder,
    'ldo': LexicalNameOrder.WesternOrder,
    'ldu': LexicalNameOrder.EasternOrder,
    'len': LexicalNameOrder.WesternOrder,
    'lep': LexicalNameOrder.EasternOrder,
    'let': LexicalNameOrder.EasternOrder,
    'lew': LexicalNameOrder.WesternOrder,
    'lez': LexicalNameOrder.EasternOrder,
    'lgi': LexicalNameOrder.WesternOrder,
    'lgt': LexicalNameOrder.EasternOrder,
    'lgu': LexicalNameOrder.WesternOrder,
    'lil': LexicalNameOrder.WesternOrder,
    'lim': LexicalNameOrder.EasternOrder,
    'lin': LexicalNameOrder.WesternOrder,
    'lis': LexicalNameOrder.EasternOrder,
    'lit': LexicalNameOrder.EasternOrder,
    'llm': LexicalNameOrder.EasternOrder,
    'lmb': LexicalNameOrder.WesternOrder,
    'lmg': LexicalNameOrder.WesternOrder,
    'lmn': LexicalNameOrder.EasternOrder,
    'lmp': LexicalNameOrder.WesternOrder,
    'lmu': LexicalNameOrder.WesternOrder,
    'lnd': LexicalNameOrder.WesternOrder,
    'lng': LexicalNameOrder.EasternOrder,
    'lon': LexicalNameOrder.WesternOrder,
    'lot': LexicalNameOrder.EasternOrder,
    'lou': LexicalNameOrder.WesternOrder,
    'lug': LexicalNameOrder.EasternOrder,
    'lui': LexicalNameOrder.EasternOrder,
    'lul': LexicalNameOrder.EasternOrder,
    'luo': LexicalNameOrder.WesternOrder,
    'luv': LexicalNameOrder.WesternOrder,
    'maa': LexicalNameOrder.WesternOrder,
    'mac': LexicalNameOrder.EasternOrder,
    'mae': LexicalNameOrder.WesternOrder,
    'mag': LexicalNameOrder.EasternOrder,
    'maj': LexicalNameOrder.WesternOrder,
    'mal': LexicalNameOrder.WesternOrder,
    'mam': LexicalNameOrder.WesternOrder,
    'man': LexicalNameOrder.EasternOrder,
    'mao': LexicalNameOrder.WesternOrder,
    'map': LexicalNameOrder.EasternOrder,
    'mar': LexicalNameOrder.EasternOrder,
    'mas': LexicalNameOrder.WesternOrder,
    'mau': LexicalNameOrder.EasternOrder,
    'maw': LexicalNameOrder.EasternOrder,
    'mba': LexicalNameOrder.EasternOrder,
    'mbl': LexicalNameOrder.WesternOrder,
    'mbm': LexicalNameOrder.WesternOrder,
    'mbo': LexicalNameOrder.EasternOrder,
    'mbr': LexicalNameOrder.WesternOrder,
    'mby': LexicalNameOrder.WesternOrder,
    'mcc': LexicalNameOrder.EasternOrder,
    'mch': LexicalNameOrder.WesternOrder,
    'mco': LexicalNameOrder.EasternOrder,
    'mda': LexicalNameOrder.WesternOrder,
    'mde': LexicalNameOrder.EasternOrder,
    'mdg': LexicalNameOrder.WesternOrder,
    'mdm': LexicalNameOrder.EasternOrder,
    'mdn': LexicalNameOrder.EasternOrder,
    'mdo': LexicalNameOrder.WesternOrder,
    'mdw': LexicalNameOrder.WesternOrder,
    'mea': LexicalNameOrder.EasternOrder,
    'mee': LexicalNameOrder.WesternOrder,
    'meh': LexicalNameOrder.WesternOrder,
    'mei': LexicalNameOrder.EasternOrder,
    'mek': LexicalNameOrder.EasternOrder,
    'men': LexicalNameOrder.EasternOrder,
    'mer': LexicalNameOrder.EasternOrder,
    'mey': LexicalNameOrder.EasternOrder,
    'mga': LexicalNameOrder.WesternOrder,
    'mgg': LexicalNameOrder.EasternOrder,
    'mgo': LexicalNameOrder.WesternOrder,
    'mgq': LexicalNameOrder.WesternOrder,
    'mgu': LexicalNameOrder.WesternOrder,
    'mhi': LexicalNameOrder.EasternOrder,
    'mie': LexicalNameOrder.EasternOrder,
    'mii': LexicalNameOrder.EasternOrder,
    'mik': LexicalNameOrder.EasternOrder,
    'min': LexicalNameOrder.WesternOrder,
    'mis': LexicalNameOrder.EasternOrder,
    'miy': LexicalNameOrder.WesternOrder,
    'miz': LexicalNameOrder.EasternOrder,
    'mka': LexicalNameOrder.EasternOrder,
    'mke': LexicalNameOrder.EasternOrder,
    'mkg': LexicalNameOrder.EasternOrder,
    'mkl': LexicalNameOrder.EasternOrder,
    'mku': LexicalNameOrder.EasternOrder,
    'mla': LexicalNameOrder.WesternOrder,
    'mlg': LexicalNameOrder.WesternOrder,
    'mlm': LexicalNameOrder.EasternOrder,
    'mme': LexicalNameOrder.EasternOrder,
    'mmn': LexicalNameOrder.WesternOrder,
    'mna': LexicalNameOrder.WesternOrder,
    'mnd': LexicalNameOrder.EasternOrder,
    'mne': LexicalNameOrder.EasternOrder,
    'mng': LexicalNameOrder.WesternOrder,
    'mni': LexicalNameOrder.EasternOrder,
    'mnm': LexicalNameOrder.WesternOrder,
    'mno': LexicalNameOrder.EasternOrder,
    'mns': LexicalNameOrder.EasternOrder,
    'mnt': LexicalNameOrder.WesternOrder,
    'mnv': LexicalNameOrder.EasternOrder,
    'mny': LexicalNameOrder.EasternOrder,
    'mnz': LexicalNameOrder.WesternOrder,
    'mof': LexicalNameOrder.WesternOrder,
    'moh': LexicalNameOrder.EasternOrder,
    'mom': LexicalNameOrder.EasternOrder,
    'mon': LexicalNameOrder.WesternOrder,
    'moo': LexicalNameOrder.EasternOrder,
    'mor': LexicalNameOrder.EasternOrder,
    'mos': LexicalNameOrder.EasternOrder,
    'mot': LexicalNameOrder.EasternOrder,
    'mou': LexicalNameOrder.WesternOrder,
    'mpa': LexicalNameOrder.WesternOrder,
    'mpr': LexicalNameOrder.EasternOrder,
    'mpt': LexicalNameOrder.EasternOrder,
    'mrd': LexicalNameOrder.EasternOrder,
    'mrg': LexicalNameOrder.WesternOrder,
    'mri': LexicalNameOrder.EasternOrder,
    'mrl': LexicalNameOrder.WesternOrder,
    'mro': LexicalNameOrder.WesternOrder,
    'mrq': LexicalNameOrder.WesternOrder,
    'mrr': LexicalNameOrder.EasternOrder,
    'mru': LexicalNameOrder.EasternOrder,
    'mrw': LexicalNameOrder.EasternOrder,
    'msc': LexicalNameOrder.EasternOrder,
    'msg': LexicalNameOrder.EasternOrder,
    'msk': LexicalNameOrder.WesternOrder,
    'msl': LexicalNameOrder.WesternOrder,
    'msn': LexicalNameOrder.EasternOrder,
    'msq': LexicalNameOrder.WesternOrder,
    'mtb': LexicalNameOrder.WesternOrder,
    'mts': LexicalNameOrder.EasternOrder,
    'mtt': LexicalNameOrder.WesternOrder,
    'mtu': LexicalNameOrder.EasternOrder,
    'mua': LexicalNameOrder.WesternOrder,
    'mud': LexicalNameOrder.WesternOrder,
    'mun': LexicalNameOrder.EasternOrder,
    'mup': LexicalNameOrder.WesternOrder,
    'mur': LexicalNameOrder.WesternOrder,
    'mus': LexicalNameOrder.WesternOrder,
    'mut': LexicalNameOrder.EasternOrder,
    'mwb': LexicalNameOrder.WesternOrder,
    'mwe': LexicalNameOrder.WesternOrder,
    'mxa': LexicalNameOrder.WesternOrder,
    'mxc': LexicalNameOrder.WesternOrder,
    'mxo': LexicalNameOrder.WesternOrder,
    'mxp': LexicalNameOrder.WesternOrder,
    'mxx': LexicalNameOrder.EasternOrder,
    'mxy': LexicalNameOrder.WesternOrder,
    'myg': LexicalNameOrder.WesternOrder,
    'mym': LexicalNameOrder.EasternOrder,
    'myn': LexicalNameOrder.WesternOrder,
    'myr': LexicalNameOrder.EasternOrder,
    'nab': LexicalNameOrder.EasternOrder,
    'nad': LexicalNameOrder.EasternOrder,
    'naj': LexicalNameOrder.WesternOrder,
    'nak': LexicalNameOrder.WesternOrder,
    'nam': LexicalNameOrder.EasternOrder,
    'nan': LexicalNameOrder.WesternOrder,
    'nar': LexicalNameOrder.EasternOrder,
    'nav': LexicalNameOrder.EasternOrder,
    'nbd': LexicalNameOrder.EasternOrder,
    'nbr': LexicalNameOrder.EasternOrder,
    'nca': LexicalNameOrder.WesternOrder,
    'ncm': LexicalNameOrder.EasternOrder,
    'ndb': LexicalNameOrder.WesternOrder,
    'nde': LexicalNameOrder.WesternOrder,
    'ndi': LexicalNameOrder.WesternOrder,
    'ndo': LexicalNameOrder.WesternOrder,
    'ndr': LexicalNameOrder.WesternOrder,
    'ndt': LexicalNameOrder.WesternOrder,
    'ndu': LexicalNameOrder.WesternOrder,
    'neh': LexicalNameOrder.WesternOrder,
    'nep': LexicalNameOrder.EasternOrder,
    'nev': LexicalNameOrder.EasternOrder,
    'new': LexicalNameOrder.EasternOrder,
    'ney': LexicalNameOrder.EasternOrder,
    'nez': LexicalNameOrder.EasternOrder,
    'ngb': LexicalNameOrder.WesternOrder,
    'ngd': LexicalNameOrder.WesternOrder,
    'ngi': LexicalNameOrder.EasternOrder,
    'ngm': LexicalNameOrder.WesternOrder,
    'ngo': LexicalNameOrder.WesternOrder,
    'ngt': LexicalNameOrder.EasternOrder,
    'ngu': LexicalNameOrder.WesternOrder,
    'ngz': LexicalNameOrder.WesternOrder,
    'nhh': LexicalNameOrder.WesternOrder,
    'nht': LexicalNameOrder.WesternOrder,
    'nia': LexicalNameOrder.WesternOrder,
    'nis': LexicalNameOrder.EasternOrder,
    'niu': LexicalNameOrder.WesternOrder,
    'niv': LexicalNameOrder.EasternOrder,
    'nkb': LexicalNameOrder.WesternOrder,
    'nkn': LexicalNameOrder.EasternOrder,
    'nko': LexicalNameOrder.WesternOrder,
    'nku': LexicalNameOrder.EasternOrder,
    'nma': LexicalNameOrder.EasternOrder,
    'nnc': LexicalNameOrder.WesternOrder,
    'nne': LexicalNameOrder.WesternOrder,
    'nng': LexicalNameOrder.WesternOrder,
    'nnk': LexicalNameOrder.EasternOrder,
    'noc': LexicalNameOrder.EasternOrder,
    'non': LexicalNameOrder.WesternOrder,
    'noo': LexicalNameOrder.WesternOrder,
    'nph': LexicalNameOrder.EasternOrder,
    'nrg': LexicalNameOrder.EasternOrder,
    'nsg': LexicalNameOrder.WesternOrder,
    'nsn': LexicalNameOrder.EasternOrder,
    'nti': LexicalNameOrder.EasternOrder,
    'ntj': LexicalNameOrder.EasternOrder,
    'ntu': LexicalNameOrder.EasternOrder,
    'nua': LexicalNameOrder.EasternOrder,
    'nue': LexicalNameOrder.WesternOrder,
    'nun': LexicalNameOrder.WesternOrder,
    'nup': LexicalNameOrder.WesternOrder,
    'nwd': LexicalNameOrder.EasternOrder,
    'nyi': LexicalNameOrder.EasternOrder,
    'nym': LexicalNameOrder.WesternOrder,
    'nza': LexicalNameOrder.WesternOrder,
    'obo': LexicalNameOrder.WesternOrder,
    'oji': LexicalNameOrder.EasternOrder,
    'oks': LexicalNameOrder.EasternOrder,
    'omh': LexicalNameOrder.EasternOrder,
    'omi': LexicalNameOrder.EasternOrder,
    'ong': LexicalNameOrder.EasternOrder,
    'ord': LexicalNameOrder.EasternOrder,
    'orh': LexicalNameOrder.WesternOrder,
    'ori': LexicalNameOrder.WesternOrder,
    'ork': LexicalNameOrder.EasternOrder,
    'oro': LexicalNameOrder.EasternOrder,
    'orw': LexicalNameOrder.WesternOrder,
    'ory': LexicalNameOrder.EasternOrder,
    'osa': LexicalNameOrder.EasternOrder,
    'oss': LexicalNameOrder.EasternOrder,
    'otm': LexicalNameOrder.WesternOrder,
    'otr': LexicalNameOrder.WesternOrder,
    'owi': LexicalNameOrder.EasternOrder,
    'paa': LexicalNameOrder.WesternOrder,
    'pae': LexicalNameOrder.EasternOrder,
    'pai': LexicalNameOrder.WesternOrder,
    'pal': LexicalNameOrder.WesternOrder,
    'pan': LexicalNameOrder.EasternOrder,
    'par': LexicalNameOrder.WesternOrder,
    'pat': LexicalNameOrder.EasternOrder,
    'pau': LexicalNameOrder.EasternOrder,
    'pba': LexicalNameOrder.EasternOrder,
    'pdp': LexicalNameOrder.EasternOrder,
    'per': LexicalNameOrder.WesternOrder,
    'pga': LexicalNameOrder.WesternOrder,
    'pia': LexicalNameOrder.EasternOrder,
    'pip': LexicalNameOrder.WesternOrder,
    'pir': LexicalNameOrder.EasternOrder,
    'pis': LexicalNameOrder.EasternOrder,
    'pit': LexicalNameOrder.EasternOrder,
    'pkt': LexicalNameOrder.WesternOrder,
    'plg': LexicalNameOrder.WesternOrder,
    'plh': LexicalNameOrder.EasternOrder,
    'plk': LexicalNameOrder.EasternOrder,
    'pme': LexicalNameOrder.EasternOrder,
    'pmn': LexicalNameOrder.EasternOrder,
    'pms': LexicalNameOrder.WesternOrder,
    'pnn': LexicalNameOrder.WesternOrder,
    'pno': LexicalNameOrder.EasternOrder,
    'pnu': LexicalNameOrder.EasternOrder,
    'pnx': LexicalNameOrder.EasternOrder,
    'pod': LexicalNameOrder.WesternOrder,
    'pok': LexicalNameOrder.EasternOrder,
    'pol': LexicalNameOrder.WesternOrder,
    'por': LexicalNameOrder.WesternOrder,
    'ppc': LexicalNameOrder.EasternOrder,
    'ppi': LexicalNameOrder.EasternOrder,
    'pra': LexicalNameOrder.EasternOrder,
    'pre': LexicalNameOrder.WesternOrder,
    'prh': LexicalNameOrder.EasternOrder,
    'prs': LexicalNameOrder.WesternOrder,
    'psh': LexicalNameOrder.EasternOrder,
    'pso': LexicalNameOrder.EasternOrder,
    'psw': LexicalNameOrder.WesternOrder,
    'ptt': LexicalNameOrder.EasternOrder,
    'pul': LexicalNameOrder.EasternOrder,
    'pum': LexicalNameOrder.EasternOrder,
    'pun': LexicalNameOrder.EasternOrder,
    'pwn': LexicalNameOrder.EasternOrder,
    'qaf': LexicalNameOrder.EasternOrder,
    'qaw': LexicalNameOrder.EasternOrder,
    'qhu': LexicalNameOrder.EasternOrder,
    'qia': LexicalNameOrder.EasternOrder,
    'qim': LexicalNameOrder.EasternOrder,
    'qui': LexicalNameOrder.WesternOrder,
    'qum': LexicalNameOrder.WesternOrder,
    'rag': LexicalNameOrder.WesternOrder,
    'ral': LexicalNameOrder.EasternOrder,
    'ram': LexicalNameOrder.EasternOrder,
    'rao': LexicalNameOrder.EasternOrder,
    'rap': LexicalNameOrder.WesternOrder,
    'ras': LexicalNameOrder.WesternOrder,
    'raw': LexicalNameOrder.EasternOrder,
    'rem': LexicalNameOrder.EasternOrder,
    'res': LexicalNameOrder.EasternOrder,
    'ret': LexicalNameOrder.EasternOrder,
    'rga': LexicalNameOrder.WesternOrder,
    'rgc': LexicalNameOrder.EasternOrder,
    'rny': LexicalNameOrder.WesternOrder,
    'rom': LexicalNameOrder.WesternOrder,
    'ron': LexicalNameOrder.WesternOrder,
    'rot': LexicalNameOrder.WesternOrder,
    'rov': LexicalNameOrder.WesternOrder,
    'rsu': LexicalNameOrder.WesternOrder,
    'ruk': LexicalNameOrder.WesternOrder,
    'rum': LexicalNameOrder.EasternOrder,
    'run': LexicalNameOrder.EasternOrder,
    'rus': LexicalNameOrder.WesternOrder,
    'rut': LexicalNameOrder.EasternOrder,
    'rwe': LexicalNameOrder.EasternOrder,
    'saa': LexicalNameOrder.WesternOrder,
    'sah': LexicalNameOrder.EasternOrder,
    'sak': LexicalNameOrder.WesternOrder,
    'sal': LexicalNameOrder.WesternOrder,
    'sam': LexicalNameOrder.WesternOrder,
    'san': LexicalNameOrder.WesternOrder,
    'sar': LexicalNameOrder.EasternOrder,
    'sav': LexicalNameOrder.EasternOrder,
    'sdw': LexicalNameOrder.EasternOrder,
    'seb': LexicalNameOrder.WesternOrder,
    'sec': LexicalNameOrder.EasternOrder,
    'sed': LexicalNameOrder.WesternOrder,
    'see': LexicalNameOrder.WesternOrder,
    'sem': LexicalNameOrder.EasternOrder,
    'ser': LexicalNameOrder.EasternOrder,
    'ses': LexicalNameOrder.WesternOrder,
    'sgb': LexicalNameOrder.EasternOrder,
    'sgu': LexicalNameOrder.WesternOrder,
    'sha': LexicalNameOrder.WesternOrder,
    'she': LexicalNameOrder.EasternOrder,
    'shi': LexicalNameOrder.EasternOrder,
    'shk': LexicalNameOrder.EasternOrder,
    'shl': LexicalNameOrder.WesternOrder,
    'shn': LexicalNameOrder.WesternOrder,
    'sht': LexicalNameOrder.WesternOrder,
    'shu': LexicalNameOrder.WesternOrder,
    'sia': LexicalNameOrder.EasternOrder,
    'sid': LexicalNameOrder.EasternOrder,
    'sil': LexicalNameOrder.WesternOrder,
    'sim': LexicalNameOrder.WesternOrder,
    'sin': LexicalNameOrder.EasternOrder,
    'sio': LexicalNameOrder.EasternOrder,
    'sir': LexicalNameOrder.WesternOrder,
    'sis': LexicalNameOrder.WesternOrder,
    'skk': LexicalNameOrder.EasternOrder,
    'sko': LexicalNameOrder.EasternOrder,
    'skp': LexicalNameOrder.EasternOrder,
    'sla': LexicalNameOrder.EasternOrder,
    'slb': LexicalNameOrder.EasternOrder,
    'sle': LexicalNameOrder.EasternOrder,
    'slp': LexicalNameOrder.EasternOrder,
    'sme': LexicalNameOrder.EasternOrder,
    'sml': LexicalNameOrder.WesternOrder,
    'smn': LexicalNameOrder.EasternOrder,
    'sna': LexicalNameOrder.EasternOrder,
    'sng': LexicalNameOrder.EasternOrder,
    'snm': LexicalNameOrder.EasternOrder,
    'sno': LexicalNameOrder.EasternOrder,
    'snt': LexicalNameOrder.EasternOrder,
    'sob': LexicalNameOrder.EasternOrder,
    'sod': LexicalNameOrder.EasternOrder,
    'son': LexicalNameOrder.WesternOrder,
    'spa': LexicalNameOrder.WesternOrder,
    'squ': LexicalNameOrder.WesternOrder,
    'src': LexicalNameOrder.EasternOrder,
    'sre': LexicalNameOrder.WesternOrder,
    'srn': LexicalNameOrder.EasternOrder,
    'sro': LexicalNameOrder.EasternOrder,
    'sta': LexicalNameOrder.EasternOrder,
    'sti': LexicalNameOrder.WesternOrder,
    'stl': LexicalNameOrder.EasternOrder,
    'stn': LexicalNameOrder.WesternOrder,
    'sud': LexicalNameOrder.EasternOrder,
    'sue': LexicalNameOrder.EasternOrder,
    'sug': LexicalNameOrder.EasternOrder,
    'suk': LexicalNameOrder.EasternOrder,
    'sun': LexicalNameOrder.WesternOrder,
    'sup': LexicalNameOrder.EasternOrder,
    'sus': LexicalNameOrder.EasternOrder,
    'svs': LexicalNameOrder.EasternOrder,
    'swa': LexicalNameOrder.WesternOrder,
    'swe': LexicalNameOrder.EasternOrder,
    'swt': LexicalNameOrder.WesternOrder,
    'tab': LexicalNameOrder.EasternOrder,
    'tac': LexicalNameOrder.EasternOrder,
    'taf': LexicalNameOrder.WesternOrder,
    'tag': LexicalNameOrder.WesternOrder,
    'tai': LexicalNameOrder.WesternOrder,
    'taj': LexicalNameOrder.WesternOrder,
    'tak': LexicalNameOrder.EasternOrder,
    'tam': LexicalNameOrder.EasternOrder,
    'tar': LexicalNameOrder.EasternOrder,
    'tas': LexicalNameOrder.WesternOrder,
    'tat': LexicalNameOrder.WesternOrder,
    'tau': LexicalNameOrder.EasternOrder,
    'taw': LexicalNameOrder.EasternOrder,
    'tba': LexicalNameOrder.EasternOrder,
    'tbo': LexicalNameOrder.WesternOrder,
    'tbt': LexicalNameOrder.EasternOrder,
    'tbu': LexicalNameOrder.WesternOrder,
    'tbw': LexicalNameOrder.WesternOrder,
    'tdi': LexicalNameOrder.EasternOrder,
    'tee': LexicalNameOrder.WesternOrder,
    'tel': LexicalNameOrder.EasternOrder,
    'ten': LexicalNameOrder.WesternOrder,
    'teo': LexicalNameOrder.WesternOrder,
    'tep': LexicalNameOrder.WesternOrder,
    'ter': LexicalNameOrder.WesternOrder,
    'tes': LexicalNameOrder.WesternOrder,
    'tet': LexicalNameOrder.WesternOrder,
    'tgh': LexicalNameOrder.WesternOrder,
    'tgk': LexicalNameOrder.WesternOrder,
    'tgl': LexicalNameOrder.EasternOrder,
    'tgn': LexicalNameOrder.EasternOrder,
    'tgr': LexicalNameOrder.WesternOrder,
    'tha': LexicalNameOrder.WesternOrder,
    'thk': LexicalNameOrder.EasternOrder,
    'thn': LexicalNameOrder.EasternOrder,
    'tho': LexicalNameOrder.EasternOrder,
    'thu': LexicalNameOrder.EasternOrder,
    'thy': LexicalNameOrder.WesternOrder,
    'tia': LexicalNameOrder.WesternOrder,
    'tib': LexicalNameOrder.EasternOrder,
    'tid': LexicalNameOrder.EasternOrder,
    'tik': LexicalNameOrder.WesternOrder,
    'tim': LexicalNameOrder.WesternOrder,
    'tin': LexicalNameOrder.WesternOrder,
    'tir': LexicalNameOrder.EasternOrder,
    'tis': LexicalNameOrder.EasternOrder,
    'tiv': LexicalNameOrder.WesternOrder,
    'tiw': LexicalNameOrder.EasternOrder,
    'tja': LexicalNameOrder.EasternOrder,
    'tkl': LexicalNameOrder.EasternOrder,
    'tkm': LexicalNameOrder.EasternOrder,
    'tla': LexicalNameOrder.WesternOrder,
    'tlf': LexicalNameOrder.EasternOrder,
    'tli': LexicalNameOrder.EasternOrder,
    'tlo': LexicalNameOrder.EasternOrder,
    'tlp': LexicalNameOrder.WesternOrder,
    'tls': LexicalNameOrder.EasternOrder,
    'tma': LexicalNameOrder.EasternOrder,
    'tml': LexicalNameOrder.EasternOrder,
    'tmm': LexicalNameOrder.WesternOrder,
    'tmn': LexicalNameOrder.WesternOrder,
    'tmo': LexicalNameOrder.EasternOrder,
    'tna': LexicalNameOrder.WesternOrder,
    'tnb': LexicalNameOrder.EasternOrder,
    'tnc': LexicalNameOrder.EasternOrder,
    'tne': LexicalNameOrder.WesternOrder,
    'tng': LexicalNameOrder.WesternOrder,
    'tnk': LexicalNameOrder.WesternOrder,
    'tnn': LexicalNameOrder.WesternOrder,
    'tno': LexicalNameOrder.WesternOrder,
    'tob': LexicalNameOrder.WesternOrder,
    'ton': LexicalNameOrder.EasternOrder,
    'tou': LexicalNameOrder.EasternOrder,
    'toz': LexicalNameOrder.WesternOrder,
    'tpn': LexicalNameOrder.EasternOrder,
    'tpt': LexicalNameOrder.EasternOrder,
    'trb': LexicalNameOrder.EasternOrder,
    'tri': LexicalNameOrder.WesternOrder,
    'trr': LexicalNameOrder.EasternOrder,
    'trt': LexicalNameOrder.EasternOrder,
    'tru': LexicalNameOrder.EasternOrder,
    'trw': LexicalNameOrder.EasternOrder,
    'tsf': LexicalNameOrder.EasternOrder,
    'tsg': LexicalNameOrder.WesternOrder,
    'tsh': LexicalNameOrder.EasternOrder,
    'tsi': LexicalNameOrder.WesternOrder,
    'tsk': LexicalNameOrder.WesternOrder,
    'tsm': LexicalNameOrder.EasternOrder,
    'tsz': LexicalNameOrder.EasternOrder,
    'ttd': LexicalNameOrder.EasternOrder,
    'tte': LexicalNameOrder.EasternOrder,
    'ttn': LexicalNameOrder.EasternOrder,
    'tts': LexicalNameOrder.EasternOrder,
    'ttu': LexicalNameOrder.EasternOrder,
    'tuk': LexicalNameOrder.WesternOrder,
    'tul': LexicalNameOrder.EasternOrder,
    'tun': LexicalNameOrder.EasternOrder,
    'tur': LexicalNameOrder.EasternOrder,
    'tuv': LexicalNameOrder.EasternOrder,
    'tvl': LexicalNameOrder.WesternOrder,
    'tvo': LexicalNameOrder.EasternOrder,
    'twe': LexicalNameOrder.EasternOrder,
    'txj': LexicalNameOrder.WesternOrder,
    'tye': LexicalNameOrder.EasternOrder,
    'tzo': LexicalNameOrder.WesternOrder,
    'tzu': LexicalNameOrder.WesternOrder,
    'uby': LexicalNameOrder.EasternOrder,
    'udh': LexicalNameOrder.EasternOrder,
    'udm': LexicalNameOrder.EasternOrder,
    'uhi': LexicalNameOrder.EasternOrder,
    'uld': LexicalNameOrder.WesternOrder,
    'uli': LexicalNameOrder.EasternOrder,
    'una': LexicalNameOrder.EasternOrder,
    'ura': LexicalNameOrder.WesternOrder,
    'urd': LexicalNameOrder.EasternOrder,
    'urk': LexicalNameOrder.EasternOrder,
    'url': LexicalNameOrder.WesternOrder,
    'urn': LexicalNameOrder.EasternOrder,
    'urt': LexicalNameOrder.WesternOrder,
    'usa': LexicalNameOrder.EasternOrder,
    'usr': LexicalNameOrder.EasternOrder,
    'ute': LexicalNameOrder.EasternOrder,
    'uzb': LexicalNameOrder.EasternOrder,
    'vaf': LexicalNameOrder.WesternOrder,
    'vai': LexicalNameOrder.EasternOrder,
    'vie': LexicalNameOrder.EasternOrder,
    'vif': LexicalNameOrder.WesternOrder,
    'vnm': LexicalNameOrder.WesternOrder,
    'wah': LexicalNameOrder.EasternOrder,
    'wai': LexicalNameOrder.EasternOrder,
    'wak': LexicalNameOrder.EasternOrder,
    'wao': LexicalNameOrder.EasternOrder,
    'wap': LexicalNameOrder.EasternOrder,
    'war': LexicalNameOrder.WesternOrder,
    'was': LexicalNameOrder.EasternOrder,
    'wat': LexicalNameOrder.EasternOrder,
    'way': LexicalNameOrder.EasternOrder,
    'wbn': LexicalNameOrder.EasternOrder,
    'wch': LexicalNameOrder.EasternOrder,
    'wed': LexicalNameOrder.EasternOrder,
    'wel': LexicalNameOrder.WesternOrder,
    'wem': LexicalNameOrder.EasternOrder,
    'wik': LexicalNameOrder.EasternOrder,
    'win': LexicalNameOrder.EasternOrder,
    'wiy': LexicalNameOrder.EasternOrder,
    'wlf': LexicalNameOrder.WesternOrder,
    'wlo': LexicalNameOrder.WesternOrder,
    'wly': LexicalNameOrder.EasternOrder,
    'wma': LexicalNameOrder.EasternOrder,
    'wme': LexicalNameOrder.EasternOrder,
    'wmu': LexicalNameOrder.EasternOrder,
    'wna': LexicalNameOrder.EasternOrder,
    'wog': LexicalNameOrder.EasternOrder,
    'woi': LexicalNameOrder.EasternOrder,
    'wom': LexicalNameOrder.EasternOrder,
    'wra': LexicalNameOrder.EasternOrder,
    'wrk': LexicalNameOrder.WesternOrder,
    'wrm': LexicalNameOrder.EasternOrder,
    'wrn': LexicalNameOrder.WesternOrder,
    'wrw': LexicalNameOrder.EasternOrder,
    'wsk': LexicalNameOrder.EasternOrder,
    'wwa': LexicalNameOrder.EasternOrder,
    'xam': LexicalNameOrder.EasternOrder,
    'xas': LexicalNameOrder.EasternOrder,
    'xav': LexicalNameOrder.EasternOrder,
    'xbi': LexicalNameOrder.WesternOrder,
    'xer': LexicalNameOrder.EasternOrder,
    'xho': LexicalNameOrder.WesternOrder,
    'xoo': LexicalNameOrder.EasternOrder,
    'yag': LexicalNameOrder.EasternOrder,
    'yal': LexicalNameOrder.EasternOrder,
    'yap': LexicalNameOrder.WesternOrder,
    'yaq': LexicalNameOrder.EasternOrder,
    'yar': LexicalNameOrder.EasternOrder,
    'yay': LexicalNameOrder.WesternOrder,
    'ybi': LexicalNameOrder.EasternOrder,
    'ycn': LexicalNameOrder.EasternOrder,
    'yei': LexicalNameOrder.EasternOrder,
    'yel': LexicalNameOrder.EasternOrder,
    'ygr': LexicalNameOrder.EasternOrder,
    'yid': LexicalNameOrder.EasternOrder,
    'yim': LexicalNameOrder.EasternOrder,
    'yin': LexicalNameOrder.EasternOrder,
    'yiw': LexicalNameOrder.EasternOrder,
    'yko': LexicalNameOrder.EasternOrder,
    'ykt': LexicalNameOrder.EasternOrder,
    'yns': LexicalNameOrder.WesternOrder,
    'yor': LexicalNameOrder.WesternOrder,
    'yqy': LexicalNameOrder.EasternOrder,
    'yrm': LexicalNameOrder.EasternOrder,
    'ytu': LexicalNameOrder.EasternOrder,
    'yuc': LexicalNameOrder.EasternOrder,
    'yuk': LexicalNameOrder.EasternOrder,
    'yul': LexicalNameOrder.WesternOrder,
    'yur': LexicalNameOrder.EasternOrder,
    'yus': LexicalNameOrder.EasternOrder,
    'ywr': LexicalNameOrder.WesternOrder,
    'yyg': LexicalNameOrder.EasternOrder,
    'zai': LexicalNameOrder.WesternOrder,
    'zap': LexicalNameOrder.WesternOrder,
    'zar': LexicalNameOrder.EasternOrder,
    'zay': LexicalNameOrder.EasternOrder,
    'zch': LexicalNameOrder.EasternOrder,
    'zen': LexicalNameOrder.WesternOrder,
    'zpr': LexicalNameOrder.EasternOrder,
    'zqc': LexicalNameOrder.EasternOrder,
    'zqs': LexicalNameOrder.EasternOrder,
    'zul': LexicalNameOrder.WesternOrder,
    'zun': LexicalNameOrder.EasternOrder,
    'zya': LexicalNameOrder.WesternOrder,
}


def __find(full_name_components, name_components):
    """
    Return the lowest and the greatest indices in the full name components
    where a name component is found, starting from the beginning.


    :param full_name_components: A list of names (words) that composed the
        full name of a person.

    :param name_components: A list of names that composed part of the full
        name of a person, such as the names that composed the first name
        or the last name of this person.

    :return: A tuple representing the lowest and the greatest indices in
        the full name components where one of the name components is found,
        or `None` if none of the name components has been found in the full name components.
    """
    indices = []
    for name_component in name_components:
        for i in range(len(full_name_components)):
            if unidecode.unidecode(name_component).lower() == unidecode.unidecode(full_name_components[i]).lower():
                indices.append(i)
                break

    return (min(indices), max(indices)) if indices else None


def __rfind(full_name_components, name_components):
    """
    Return the lowest and the greatest indices in the full name components
    where a name component is found, starting from the end


    :param full_name_components: A list of names (words) that composed the
        full name of a person.

    :param name_components: A list of names that composed part of the full
        name of a person, such as the names that composed the first name
        or the last name of this person.

    :return: A tuple representing the lowest and the greatest indices in
        the full name components where one of the name components is found,
        or `None` if none of the name components has been found in the full name components.
    """
    indices = []
    for name_component in name_components:
        for i in reversed(range(len(full_name_components))):
            if unidecode.unidecode(name_component).lower() == unidecode.unidecode(full_name_components[i]).lower():
                indices.append(i)
                break

    return (min(indices), max(indices)) if indices else None


def format_first_name(first_name, locale=None):
    """
    Format the first name according to the locale

    All the name components of French, English, and Vietnamese first names
    are capitalized, while the rest of the words are lower cased.  Korean
    personal names are not transformed.


    :param first_name: Forename (also known as *given name*) of the person.
        The first name can be used to alphabetically sort a list of users.

    :param locale: An object `Locale` that supposedly refers to the name
        of this person.


    :return: The formatted first name of the person.
    """
    if first_name is None:
        return None

    first_name = normalize_name(first_name)
    return ' '.join([
        component.lower().capitalize()
        for component in first_name.split()
    ])


def format_full_name(
        first_name,
        last_name,
        locale,
        full_name=None,
        strict=True):
    """
    Format the full name according to the locale

    For instance, for French and English personal names, first name comes
    first and last name comes last (western order).  While for Vietnamese
    and Korean, this order is reversed (eastern order).


    :param full_name: Complete name of a person.

    :param first_name: Forename (also known as *given name*) of the person.

    :param last_name: Surname (also known as *family name*) of the person.

    :param locale: An object `Locale` referencing the preferred language
        of the person, supposedly the language defining the personal
        naming system (more specifically the lexical name order) which
        will be used to format the first name, the last name, and the full
        name of this person.

        For instance, providing the following name components:

        - first name: "Aline Minh Anh Maria"
        - last name: "Caune"
        - full name: "Aline Maria Caune Ly"

        Specifying the locale `vie`, the full name will be formatted as:

            "CAUNE LY Aline Maria"

        Specifying the locale `fra`, the full name will be formatted as:

           "Aline Maria CAUNE LY"

    :param strict: Indicate whether the full name MUST be formatted
        according to the lexical name related to the culture of the person.


    :return: The formatted full name of the person.


    :raise ValueError: When a full name is provided, while none of the
        words of the first name or the last name is part of this full name.
    """
    lexical_name_order = LEXICAL_NAME_ORDERS.get(locale.to_string()) or LexicalNameOrder.WesternOrder

    first_name = normalize_name(first_name)
    last_name = normalize_name(last_name)
    full_name = full_name and normalize_name(full_name)

    if full_name is None or len(full_name) == 0:
        return f'{format_last_name(last_name)} {format_first_name(first_name)}' if lexical_name_order == LexicalNameOrder.EasternOrder \
            else f'{format_first_name(first_name)} {format_last_name(last_name)}'
    else:
        full_name_components = full_name.split()

        # Decompose the first name in words.
        first_name_components = first_name.split()
        indices = \
            __find(full_name_components, first_name_components) if lexical_name_order == LexicalNameOrder.WesternOrder \
            else __rfind(full_name_components, first_name_components)
        if indices is None:
            if strict:
                raise IncompleteFullNameException(
                    f'None of the first name parts "{first_name}" has been found in the full name "{full_name}"')
            return full_name

        first_name_lowest_index, first_name_greatest_index = indices

        # Decompose the last name in words.
        last_name_components = last_name.split()
        indices = \
            __rfind(full_name_components, last_name_components) if lexical_name_order == LexicalNameOrder.WesternOrder \
            else __find(full_name_components, last_name_components)
        if indices is None:
            if strict:
                raise IncompleteFullNameException(
                    f'None of the last name parts "{last_name}" has been found in the full name "{full_name}"')
            return full_name

        last_name_lowest_index, last_name_greatest_index = indices

        # Check whether the parts of the full name are written in the expected
        # order.  For instance:
        #
        # - First name: "Aline"
        # - Last name: "Caune"
        # - Full name: "Aline Minh Anh Maria Caune Ly"
        # - Locale: "fra"
        #
        # - First name: "Truc"
        # - Last name: "Nguyen"
        # - Full Name: "Nguyen thi Thanh Truc"
        # - Locale: "vie"
        if (lexical_name_order == LexicalNameOrder.EasternOrder and last_name_lowest_index > first_name_lowest_index) or \
           (lexical_name_order == LexicalNameOrder.WesternOrder and last_name_lowest_index < first_name_lowest_index):
            if strict:
                raise InvalidLexicalNameOrderException(
                    f'The parts of the full name "{full_name}" are not written in the expected order')
            return full_name

        if lexical_name_order == LexicalNameOrder.WesternOrder:
            full_name_first_name_components = [
                format_first_name(full_name_components[i], locale)
                for i in range(0, last_name_lowest_index)
            ]
            full_name_last_name_components = [
                format_last_name(full_name_components[i], locale)
                for i in range(last_name_lowest_index, len(full_name_components))
            ]
            reordered_full_name_components = full_name_first_name_components + full_name_last_name_components
        else:
            full_name_last_name_components = [
                format_last_name(full_name_components[i], locale)
                for i in range(0, last_name_greatest_index + 1)
            ]
            full_name_first_name_components = [
                format_first_name(full_name_components[i], locale)
                for i in range(last_name_greatest_index + 1, len(full_name_components))
            ]
            reordered_full_name_components = full_name_last_name_components + full_name_first_name_components

        # # CAUNE LY Aline Minh Maria
        # if last_name_lowest_index < first_name_lowest_index:
        #     full_name_last_name_components = [
        #         format_last_name(full_name_components[i], locale)
        #         for i in range(0, first_name_lowest_index)
        #     ]
        #     full_name_first_name_components = [
        #         format_first_name(full_name_components[i], locale)
        #         for i in range(first_name_lowest_index, len(full_name_components))
        #     ]
        #
        # # Aline Minh Maria CAUNE LY
        # else:
        #     full_name_first_name_components = [
        #         format_first_name(full_name_components[i], locale)
        #         for i in range(0, last_name_lowest_index)
        #     ]
        #     full_name_last_name_components = [
        #         format_last_name(full_name_components[i], locale)
        #         for i in range(last_name_lowest_index, len(full_name_components))
        #     ]
        #
        # reordered_full_name_components = \
        #     full_name_first_name_components + full_name_last_name_components if lexical_name_order == LexicalNameOrder.WesternOrder \
        #         else full_name_last_name_components + full_name_first_name_components

        reformatted_full_name = ' '.join(reordered_full_name_components)

        return reformatted_full_name


def format_last_name(last_name, locale=None):
    """
    Format the last name according to the locale

    French, English, and Vietnamese personal names are converted to upper
    case.  However, Korean personal names are not upper cased.


    :param last_name: Surname (also known as *family name*) of the person.
        The last name can be used to alphabetically sort a list of users.

    :param locale: An object `Locale` that supposedly refers to the name
        of this person.


    :return: The formatted last name of the person.
    """
    if last_name is None:
        return None

    last_name = normalize_name(last_name)
    return last_name.upper()


def normalize_name(name):
    """
    Remove any punctuation and duplicated space characters.


    :param name: A surname, a forename, or a full name of a person.


    :return: The given name that has been cleansed from useless characters.
    """
    if name is None:
        raise ValueError("The argument `name` MUST not be null")

    # Replace any punctuation character with space.
    punctuationless_string = re.sub(r'[.,\\/#!$%^&*;:{}=\-_`~()<>"\']', ' ', name)

    # Remove any duplicate space characters.
    return ' '.join(punctuationless_string.split())

