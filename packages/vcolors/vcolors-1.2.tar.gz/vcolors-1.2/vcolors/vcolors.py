
from Color_Console import *

# import colored
# p_fail = colored.fg('red') + colored.attr('bold')
# p_fail_bg = colored.bg('dark_red_1') + colored.fg('red')
# p_sucess = colored.fg('green') + colored.attr('bold')
# p_sucess_bg = colored.bg('dark_green') + colored.fg('green')
# p_warning = colored.fg('yellow') + colored.attr('bold')
# p_warning_bg = colored.bg('dark_goldenrod') + colored.fg('yellow')


def printF(text) -> str('Red text'):
    '''Print fail, red text'''
    return ctext(text, "red")


def printFBG(text) -> str('Red background'):
    '''Print fail, red text and dark red background'''
    return ctext(text, "yellow",'red')


def printS(text) -> str('Green text'):
    '''Print sucess, green text'''
    return ctext(text, "green")


def printSBG(text) -> str('Green background'):
    '''Print sucess, green text and dark green background'''
    return ctext(text, "red",'green')


def printW(text) -> str('Yellow text'):
    '''Print warning, yellow text'''
    return ctext(text, "yellow")


def printWBG(text) -> str:
    '''Print warning, yellow text and dark yellow background'''
    return ctext(text, "red",'yellow')


