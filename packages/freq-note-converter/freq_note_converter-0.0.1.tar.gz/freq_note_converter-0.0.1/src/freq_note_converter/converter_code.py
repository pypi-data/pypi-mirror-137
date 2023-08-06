import math


class FreqNoteConverter:
    def __init__(self, freq=None, note_number=None, note=None, octave=None):
        self.note, self.octave, self.offset_from_note, self.note_number, self.offset_from_note = '', 0, 0, 0, 0
        if freq is not None:
            self.freq = freq
            self.note, self.octave, self.offset_from_note, self.note_number = self.freq_to_note(freq)
        elif note is not None and octave is not None:
            print('not implemented')
        elif note_number is not None:
            self.note_number = note_number
            self.note, self.octave, self.freq = self.note_number_to_freq(note_number)
        else:
            print('no valid input')

    def __str__(self):
        d = dict(freq=self.freq,
                 note_number=self.note_number,
                 note=self.note,
                 octave=self.octave,
                 offset_from_note=round(self.offset_from_note, 3))
        output = "\n".join(["{: >16} : {}".format(k, v) for k, v in d.items()])
        output += '\n' + '-' * 50 + '\n'
        return output

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def note_number_to_note_octave(note_number):
        notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

        note = (note_number - 1) % len(notes)
        note = notes[note]

        octave = (note_number + 8) // len(notes)

        return note, octave

    @staticmethod
    def freq_to_note_number(freq):
        if not freq:  # no log value for 0
            freq += 1e-15
        note_number = 12 * math.log2(
            freq / 440) + 49  # formula taken from https://en.wikipedia.org/wiki/Piano_key_frequencies
        offset_from_note = note_number
        note_number = round(note_number)
        offset_from_note -= note_number
        return note_number, offset_from_note

    def freq_to_note(self, freq):
        note_number, offset_from_note = self.freq_to_note_number(freq)
        note, octave = self.note_number_to_note_octave(note_number)

        return note, octave, offset_from_note, note_number

    def note_number_to_freq(self, note_number):
        note, octave = self.note_number_to_note_octave(note_number)
        freq = 2 ** ((note_number - 49) / 12) * 440
        return note, octave, freq

    def print_me(self):
        print(self.__str__(), end='')
