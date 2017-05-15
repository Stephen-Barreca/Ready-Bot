"""
    keywords that get triggers and their responses
    dictionaries of lists
"""
from responses import *

keywords = {
    ###################################################
    # FOOD-THEMED KEYWORDS
    ###################################################
    'lunch': lunch + specific_food,
    'food?': lunch + specific_food,
    'ht?': lunch + ht,
    'harris teeter': lunch + specific_food + ht,
    ' ht': lunch + ht,
    'chipotle': lunch + chipotle,
    'chipotole': chiptole,
    'chiptole': chiptole,


    ###################################################
    # MISC THEMED KEYWORDS
    ###################################################
    'meeting': scurry,
}

###################################################
# CHAT ENHANCER GIFS KEYWORDS
###################################################
gifs = {
    'nice': nice,
    'noice': nice + noice,
    'run away': flee + scurry,
    '...': blank_eyed_stare,
    'yes': yes,


}