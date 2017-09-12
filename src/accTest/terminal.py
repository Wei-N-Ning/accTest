

class __Colors(object):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    MAPPING = {'green': OKGREEN,
               'red': FAIL,
               'yellow': WARNING,
               'blue': OKBLUE,
               'pink': HEADER,
               'under': UNDERLINE}


def printC(text, color):
    colorCode = __Colors.MAPPING.get(color, None)
    if not colorCode:
        colorCode = getattr(__Colors, color, None)
    if not colorCode:
        print text
    else:
        print colorCode + text + __Colors.ENDC
