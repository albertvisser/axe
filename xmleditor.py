import sys
## from axe_ppg import MainGui
## from axe_tk import MainGui - NB werkt niet op deze manier
from axe.axe_wx import MainGui

def main(args):
    x = MainGui(args)

if __name__ == '__main__':
    main(sys.argv)