from notes import *

class Song:

    def __init__(self):
        self.note_index = 0
        #TODO: hardcoded Mary had a little lamb. Figure out best way to represent songs and support multiple songs
        self.notes = ['D4', 'C4', 'A3', 'C4', 'D4', 'D4', 'D4', 'C4', 'C4', 'C4', 'D4', 'F4', 'F4',
                      'D4', 'C4', 'A3', 'C4', 'D4', 'D4', 'D4', 'D4', 'C4', 'C4' ,'D4', 'C4', 'A3']

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