try:
    from strenum import StrEnum
except Exception as e:
    import os
    os.system("pip install StrEnum")

class ROOMTYPE(StrEnum):
    
    LASERDANCE = 'laserdance'
    GRANDPIANO = 'grandpiano'
    JUSTDOIT = 'justdoit'
    FUNINTHEBARN = 'funinthebarn'
    BUBBLEBOBBLE = 'bubblebobble'
    LETTERFLOOR = 'letterfloor'
    SPACEJAM = 'spacejam'
    ALLEYOOPS = 'alleyoops'
    GOAL = 'goal'
    SUCKERPUNCH = 'suckerpunch'
    REFLECTIONS = 'reflections'
    JOKER = 'joker'
    SPECTRUMDICE = 'spectrumdice'
    HIGHLIGHTBARS = 'highlightbars'

    CLIMBING = 'climbing'
    RABBITHOLE = 'rabbithole'
    THEFACTORY = 'thefactory'
    PYRAMIDS = 'pyramids'
    THEJUNGLER = 'thejungler'
    SPINTHEWHEEL = 'spinthewheel'
    COLORWALLS = 'colorwalls'
    FILLTHEGAP = 'fillthegap'
    THEGULF = 'thegulf'
    THEPITCHER = 'thepitcher'
    PHARAOH = 'pharaoh'


class EVENTS(StrEnum):
    SCORED = 'SCORED'
    WIN = 'WIN'
    LOSE = 'LOSE'
    DOORCLOSED = 'DOORCLOSED'
    DOOROPENED = 'DOOROPENED'
    PANICBUTTON = 'PANICBUTTON'
    
class PROJECT(StrEnum):
    AF = 'AF'
    MAZE = 'MAZE'

class ROOMSTATE(StrEnum):
    STANDBY = 'STANDBY'
    RESET = 'RESET'
    PLAYING = 'PLAYING'
    TEAMREGISTER = 'TEAMREGISTER'
    