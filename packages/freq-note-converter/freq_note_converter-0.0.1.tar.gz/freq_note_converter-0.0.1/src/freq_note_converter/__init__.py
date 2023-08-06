"""
convert frequency to note and note to frequency.
currently, can only input frequency and note index, and not supporting note name and octave as input


usage example:
    input:
        import freq_note_converter

        val = freq_note_converter.convert(freq=449)
        print(val.note)
    output:
        'A'
    input:
        print(val)
    output:
                    freq : 449
             note_number : 49
                    note : A
                  octave : 4
        offset_from_note : 0.351
        --------------------------------------------------
    input:
        freq_note_converter.convert(note_number=49).print_me()
    output:
                    freq : 440.0
             note_number : 49
                    note : A
                  octave : 4
        offset_from_note : 0
        --------------------------------------------------
"""
from freq_note_converter import converter_code


def convert(freq=None, note_number=None):
    if freq is not None:
        converter = converter_code.FreqNoteConverter(freq=freq)
    elif note_number is not None:
        converter = converter_code.FreqNoteConverter(note_number=note_number)
    else:
        print('no valid input')
    return converter
