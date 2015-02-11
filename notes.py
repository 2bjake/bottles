from colors import *

F3 = {'freq': 174.61, 'name': 'F3', 'color': PINK}
G3 = {'freq': 196,    'name': 'G3', 'color': RED}
A3 = {'freq': 220,    'name': 'A3', 'color': ORANGE}
B3 = {'freq': 246.94, 'name': 'B3', 'color': YELLOW}
C4 = {'freq': 261.63, 'name': 'C4', 'color': GREEN}
D4 = {'freq': 293.66, 'name': 'D4', 'color': BLUE}
E4 = {'freq': 329.63, 'name': 'E4', 'color': PURPLE}
F4 = {'freq': 349.23, 'name': 'F4', 'color': BROWN}

FREQUENCY_LIST = [F3, G3, A3, B3, C4, D4, E4, F4]

def get_frequency_color_by_name(name):
    for freq in FREQUENCY_LIST:
        if freq['name'] == name:
            return freq['color']


def get_frequency_color(freq):
    if type(freq) is str:
        return get_frequency_color_by_name(freq)

    for idx, val in enumerate(FREQUENCY_LIST):
        if freq < val['freq']:
            return FREQUENCY_LIST[idx - 1]['color'] if idx > 0 else WHITE
    return BROWN
