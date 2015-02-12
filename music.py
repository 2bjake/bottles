import colors

#TODO: add in 'black key' notes
F3 = {'freq': 174.61, 'name': 'F3', 'color': colors.PINK}
G3 = {'freq': 196,    'name': 'G3', 'color': colors.RED}
A3 = {'freq': 220,    'name': 'A3', 'color': colors.ORANGE}
B3 = {'freq': 246.94, 'name': 'B3', 'color': colors.YELLOW}
C4 = {'freq': 261.63, 'name': 'C4', 'color': colors.GREEN}
D4 = {'freq': 293.66, 'name': 'D4', 'color': colors.BLUE}
E4 = {'freq': 329.63, 'name': 'E4', 'color': colors.PURPLE}
F4 = {'freq': 349.23, 'name': 'F4', 'color': colors.BROWN}

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
            return FREQUENCY_LIST[idx - 1]['color'] if idx > 0 else colors.WHITE
    return colors.BROWN

#TODO: figure out a better way to represent songs. Also, add way to select a song from the UI.
HOT_CROSS_BUNS_NOTES = ['D4', 'C4', 'A3', 'D4', 'C4', 'A3', 'A3', 'A3', 'A3', 'A3',
                        'C4', 'C4', 'C4', 'C4', 'D4', 'C4', 'A3']

MARY_HAD_A_LITTLE_LAMB_NOTES = ['D4', 'C4', 'A3', 'C4', 'D4', 'D4', 'D4', 'C4', 'C4', 'C4', 'D4', 'F4', 'F4',
                                'D4', 'C4', 'A3', 'C4', 'D4', 'D4', 'D4', 'D4', 'C4', 'C4' ,'D4', 'C4', 'A3']

AMERICA_THE_BEAUTIFUL_NOTES = ['D4', 'D4', 'B3', 'B3', 'D4', 'D4', 'A3', 'A3', 'B3', 'C4', 'D4']

class Song:
    def __init__(self, notes=MARY_HAD_A_LITTLE_LAMB_NOTES):
        self.note_index = 0
        self.notes = notes

    def get_current_note_index(self):
        return self.note_index if self.note_index < len(self.notes) else None

    def get_current_note(self):
        if self.get_current_note_index() is not None:
            return self.notes[self.get_current_note_index()]
        else:
            return None

    def get_current_phrase(self, phrase_size):
        if phrase_size < 1:
            phrase_size = 1

        cur_idx = self.get_current_note_index()
        if cur_idx is None:
            cur_idx = len(self.notes) - 1

        start = 0
        while (start + phrase_size) <= cur_idx:
            start += phrase_size
        end = start + phrase_size
        phrase_cur_idx = cur_idx - start
        if self.get_current_note_index() is None:
           phrase_cur_idx = None

        return {'notes': self.notes[start:end], 'cur_idx': phrase_cur_idx}

    def play_note(self, note):
        if get_frequency_color(note) == get_frequency_color(self.get_current_note()): #TODO: hack, make this right
            self.note_index += 1