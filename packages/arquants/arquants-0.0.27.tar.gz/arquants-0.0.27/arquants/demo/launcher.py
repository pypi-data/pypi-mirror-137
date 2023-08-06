import sys
import os

print('python version : {}'.format(sys.version))
os.environ['USERNAME'] = 'ibrunel'
os.environ['PASSWORD'] = 'Creteil1+'

from arquants.initiator import Symbol, MDSubsType, Initiator
from demostrat import DemoStrat



sym = Symbol(market='Remarket', symbol='MERV - XMEV - AL30 - 48hs', md_type=MDSubsType.TOP)
symbols = list()
symbols.append(sym)

initiator = Initiator(symbols=symbols, strat_cls=DemoStrat)
initiator.start()