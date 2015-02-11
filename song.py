from notes import *

class Song:

    def __init__(self):
        self.note_index = 0
        self.notes = ['D4', 'C4', 'A3', 'C4', 'D4', 'D4', 'D4', 'C4', 'C4', 'C4', 'D4', 'F4', 'F4']

    def get_current_note_index(self):
        return self.note_index if self.note_index < len(self.notes) else None

    current_note_index = property(get_current_note_index)

    def get_current_note(self):
        if self.current_note_index is not None:
            return self.notes[self.current_note_index]
        else:
            return None

    def play_note(self, note):
        print "current note name: ", self.get_current_note()
        print "note color: ", get_frequency_color(note), " current note color: ", get_frequency_color(self.get_current_note())
        if get_frequency_color(note) == get_frequency_color(self.get_current_note()): #TODO: wow, someone is tired, fix this
            self.note_index += 1