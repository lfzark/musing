#!usr/bin/env python
# coding=utf8

"""
Copyright (c) 2018 ark1ee <onlyarter@gmail.com>
"""

import os
import random
import re
import pretty_midi
from .common_util import make_hash, get_date_time
from .musthe import Chord, Note, scale
from pretty_midi.containers import Note as P_NODE

CHORD_TYPE = ['M', 'm', 'dim', 'aug', 'open5',
              'dim7', 'maj7', 'aug7', 'sus2', 'sus4']
MINUTE = 60.00000
DEFAULT_MIDI_FILE = 'midi_data/40126.mid'
DEFAULT_VELOCITY = 36


class Musing(object):
    '''
    Musing Main Class
    '''
    BPM = 105

    def __init__(self, midifile=None,instrument_name='Bright Acoustic Piano'):
        '''
        Init Musing Class
        '''

        if midifile:
            self.pm = pretty_midi.PrettyMIDI(midifile)
            return 

        self.pm = pretty_midi.PrettyMIDI()
        melody = pretty_midi.Instrument(program=pretty_midi.instrument_name_to_program(instrument_name))
        melody.current_time = 0.0
        self.pm.instruments.append(melody)

    def reset(self):
        '''
        Reset musing status
        '''
        self.__init__()

    def beat_time(self):
        '''
        Get beat time √
        '''
        return MINUTE / self.BPM

    def get_instruments(self):
        '''
        Get instruments from midi √
        '''
        return self.pm.instruments

    def add_track(self, track, is_pattern=True,instrument_name="Bright Acoustic Piano"):
        '''
        add track to raw melody
        '''

        if isinstance(track,pretty_midi.Instrument):
            self.pm.instruments.append(track)

        elif isinstance(track,Clip):

            melody = pretty_midi.Instrument(program=pretty_midi.instrument_name_to_program(instrument_name))
            melody.current_time = 0.0
            melody.notes = track.note_list
            self.pm.instruments.append(melody)

        else:
            raise Exception("Excepted track type is Instrument",type(track))


    def add_rhythm(self, note, is_pattern=True):
        '''
        add rhythm to raw melody
        '''
        pass

    def add_notes(self, note_list, instrument_num=0, interval=.5):
        '''
        add notes to instrum √
        support Note ,Pretty_Note,String
        '''
        if len(self.pm.instruments) - 1 < instrument_num:
            pass

        if note_list:
            curr_time = self.pm.instruments[instrument_num].current_time

            if isinstance(note_list[0], basestring):
                for note_name in note_list:
                    # Retrieve the MIDI note number for this note name
                    note_number = pretty_midi.note_name_to_number(note_name)
                    # Create a Note instance for this note,
                    # starting at 0s and ending at .5s ,velocity random in  45 - 70
                    note = pretty_midi.Note(
                        velocity=random.randint(45, 70), pitch=note_number,
                        start=curr_time, end=curr_time + interval)
                    self.pm.instruments[instrument_num].notes.append(note)
                    curr_time += interval

            elif isinstance(note_list[0], Note) or isinstance(note_list[0], P_NODE):
                for note in note_list:
                    self.pm.instruments[instrument_num].notes.append(note)

            else:
                raise Exception(
                    '[-] Got a type : %s wrong note type ,except Note or String ' % type(note_list[0]))
            self.pm.instruments[instrument_num].current_time = curr_time

    @staticmethod
    def get_track(self, note_list, rhythm):
        pass

    def note_with_rhythm(self, note_list, rhythm, instrument_num=0):
        '''
        note name add
        '''
        curr_time = 0.0
        chord_duration = 1
        duration_list = [0.2, 0.2, 0.2, 0.35, 0.15, 0.25]

        for c in note_list:
            c.extend(c[0:1])
            i = 0

            for note_name in c:
                # Retrieve the MIDI note number for this note name
                note_number = pretty_midi.note_name_to_number(
                    note_name.scientific_notation())
                # Create a Note instance for this note, starting at 0s and ending at .5s
                note = pretty_midi.Note(
                    velocity=66, pitch=note_number, start=curr_time, end=curr_time + duration_list[i])
                self.pm.instruments[instrument_num].notes.append(note)
                curr_time += duration_list[i]
                i += 1
            curr_time += chord_duration

    def seq_to_midi_rhythm(self, rhythm, c=['C5', 'D5']):

        for note_name, _rhythm in zip(c, rhythm):
            # Retrieve the MIDI note number for this note name
            note_number = pretty_midi.note_name_to_number(note_name)
            # Create a Note instance for this note, starting at 0s and ending at .5s
            note = pretty_midi.Note(
                velocity=66, pitch=note_number, start=_rhythm[0], end=_rhythm[1])
            self.pm.instruments[0].notes.append(note)

    def note_with_rhythm_pattern(self, rhythm, c=['C5', 'D5']):
        '''
        A music clip note with rhythm
        '''
        t = 0
        c_len = len(c)

        for r in rhythm:

            note_number = pretty_midi.note_name_to_number(c[t])

            note = pretty_midi.Note(
                velocity=20, pitch=note_number, start=r[0], end=r[1])
            self.pm.instruments[0].notes.append(note)
            note_number = pretty_midi.note_name_to_number(c[t + 1])

            note = pretty_midi.Note(
                velocity=30, pitch=note_number, start=r[0], end=r[1])
            self.pm.instruments[0].notes.append(note)
            note_number = pretty_midi.note_name_to_number(c[t + 2])
            note = pretty_midi.Note(
                velocity=20, pitch=note_number, start=r[0], end=r[1])
            self.pm.instruments[0].notes.append(note)

            if (t + 6) >= c_len:
                break
            t += 3

    def write_to_midi(self, filename='%s_%s.%s' % (get_date_time(), make_hash(), 'midi')):
        '''
        write notes to midi file.
        '''

        file_path = os.sep+'tmp' + os.sep+'musing_midi'
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        self.midi_file_path = file_path+os.sep + filename
        print ("write to : %s"  % (self.midi_file_path))
        self.pm.write(self.midi_file_path)

    def play(self,player_path='cvlc'):
        '''
        play with cvlc(wildmidi or timidity etc).
        '''

        if  not hasattr(self,'midi_file_path'):
            self.write_to_midi()
        os.system('%s %s  --play-and-exit' % (player_path, self.midi_file_path))

    @staticmethod
    def chord_to_notes(note='D5', c_type='dim'):
        '''
        transfer chord to note

        e.g:

        >>> Musing.chord_to_notes('C5', 'maj7')
        [Note("C5"), Note("E5"), Note("G5"), Note("B5")]

        '''

        return Chord(Note(note), c_type).notes

    @staticmethod
    def get_scale(note='C', c_type='major'):
        '''
        get a scale from note
        e.g:

        >>> Musing.get_scale('C5', 'major')
        [Note("C5"), Note("D5"), Note("E5"), Note("F5"), Note("G5"),
         Note("A5"), Note("B5"), Note("C6")]

        '''
        return scale(Note(note), c_type)

    @staticmethod
    def parse_chord(note, is_name=True):
        '''
        Parse a chord name to note name list

        e.g:

        >>> Musing.parse_chord('C4M',is_name= True)
        ['C4', 'E4', 'G4']
        >>> Musing.parse_chord('C4M')
        [Note("C4"), Note("E4"), Note("G4")]

        '''
        chord_type_re = r'(' + '|'.join(CHORD_TYPE)[:-1] + ')$'

        chord_type_pattern = re.compile(chord_type_re)
        chord_type = 'M'

        r_note = chord_type_pattern.search(note)
        if not r_note:
            raise Exception('Could not parse the chord: - ' + note)
        else:
            chord_type = r_note.group(0)
            note = re.sub(chord_type_re, "", note)

        note_pattern = re.compile(
            r'^[A-G]([b#])?\1{0,2}?\d?$')  # raw because of '\'
        if note_pattern.search(note) == None:
            raise Exception('Could not parse the note: ' + note)

        tone = note[0]
        accidental = re.findall('[b#]{1,3}', note)
        octave = re.findall('[0-9]', note)

        if accidental == []:
            accidental = ''
        else:
            accidental = accidental[0]

        if octave == []:
            octave = 4
        else:
            octave = int(octave[0])

        if is_name:
            return Musing.notes_to_note_names(Chord(Note(note), chord_type).notes)
        else:
            return Chord(Note(note), chord_type).notes

    @staticmethod
    def notes_to_note_names(notes):
        '''
        tranfer note list  to note name list
        '''
        return map(lambda x: x.scientific_notation(), notes)

    @staticmethod
    def get_beats(filename=DEFAULT_MIDI_FILE):
        '''
        get the beat from  midi file
        '''
        midi_data = pretty_midi.PrettyMIDI(filename)
        return midi_data.get_beats()

    @staticmethod
    def midi_to_note(filename=DEFAULT_MIDI_FILE, is_name=False, instrument_id=False):
        '''
        Load midi to note name list
        '''
        note_list = []
        try:
            midi_data = pretty_midi.PrettyMIDI(filename)
        except IOError as ioe:
            raise ValueError('PrettyMIDI - IOError: %s' % (ioe))

        if instrument_id:
            for note in midi_data.instruments[instrument_id].notes:
                if is_name:
                    note_list.append(
                        pretty_midi.note_number_to_name(note.pitch))
                else:
                    note_list.append(note)

        else:
            for instrument in midi_data.instruments:
                if not instrument.is_drum:
                    for note in instrument.notes:
                        if is_name:
                            note_list.append(
                                pretty_midi.note_number_to_name(note.pitch))
                        else:
                            note_list.append(note)
        return note_list

    @staticmethod
    def chord_list_to_note(chord_seq, is_name=False):
        '''
        Transfer chord_list to note list
        >>> Musing.chord_list_to_note('D4open5 A#3sus2')
        [Note("D4"), Note("A4"), Note("D5"), Note("A#3"), Note("E#4"), Note("A#4"), Note("B#3")]
        '''

        note_name_list = []
        for chord in chord_seq.split(' '):
            if is_name:
                note_name_list.extend(Musing.parse_chord(chord))
            else:
                note_name_list.extend(
                    Musing.parse_chord(chord, is_name=is_name))

        return note_name_list


class Clip(object):
    '''
    Clip
    '''

    last_time = 0.0

    def __init__(self, rhythms=False, notes=False, velocity_list=[], start_time=.0):

        self.midi = Musing()

        if not isinstance(rhythms, MusingRhythm):
            print 'Unexcept Type %s' % (type(rhythms))

        self.note_list = []

        if not rhythms:
            return
        else:
            self.last_time = rhythms.last_time
        if len(rhythms) != len(notes):
            raise Exception("Not match rhythms : notes =  %s:%s" %(len(rhythms), len(notes)))
        for rhythm, note in zip(rhythms, notes):
            note = pretty_midi.Note(
                velocity=DEFAULT_VELOCITY, pitch=pretty_midi.note_name_to_number(note), start=start_time + rhythm[0], end=start_time + rhythm[1])
            self.note_list.append(note)

    def add_notes(self, notes=False, start_time=.0):
        for note in notes:
            note.start += start_time
            note.end += start_time
            self.note_list.append(note)

    def __str__(self):
        return str(self.note_list)

    def __add__(self, others):
        self.add_notes(others.note_list, start_time=self.last_time)
        return self

    def play(self):
        print self.note_list
        self.midi.add_notes(self.note_list)
        self.midi.write_to_midi()
        self.midi.play()

    def  add_column_chords(self,note_list,beat_time=1.0):

        self.midi = Musing()

        for note in note_list:
            note.start = self.last_time
            note.start = self.last_time + beat_time
            self.note_list.append(note)
        return self

    def  add_arp(self,note_list,beat_time=1.0):

        self.midi = Musing()
        start_time = self.last_time
        for note in note_list:
            note.start = start_time
            note.start = start_time + beat_time
            start_time+=beat_time
            self.note_list.append(note)
        return self

    def dump(self):
        '''
        dump note list from clip
        '''
        return self.note_list


class MusingRhythm(object):
    '''
    Musing Rhythm
    '''

    def __init__(self, rhythm="", unit_time=.5):
        (self.time_list, self.last_time) = self.parse_rhythm(
            rhythm=rhythm, unit_time=unit_time)

    def __str__(self):
        return str(self.time_list)

    def __repr__(self):
        return self.time_list

    def __iter__(self):
        return self.time_list.__iter__()
    def __len__(self):
        return len(self.time_list)

    def parse_rhythm(self, rhythm, unit_time=.5):
        '''
        parse_rhythm
        '''

        now_time = [0.0]
        time_list = []
        for rhy in rhythm.split('|'):
            if rhy.strip():
                time_list.extend(self.parse_rhythm_bar(
                    rhy, now_time, unit_time)[0])

        return time_list, now_time[0]

    def parse_rhythm_bar(self, rhythm_bar, now_time, unit_time=.5):
        '''
        Parse the rhythm
        '''

        # print rhythm_bar
        r_list = rhythm_bar.split(' ')
        t = len(rhythm_bar.replace(' ', ''))

        m_list = []
        s_list = []

        unit = unit_time / float(t)

        for r in r_list:

            if '-' in r:
                start_time = now_time[0]
                last_time = len(r) * unit
                m_list.append((start_time, last_time + start_time))
                now_time[0] += last_time
            elif '.' in r:
                start_time = now_time[0]
                last_time = len(r) * unit
                s_list.append((start_time, last_time + start_time))
                now_time[0] += last_time
            elif r =='':
                pass
            else:
                raise Exception(' Unexcept Expression  [%s] ' % (r))

        return (m_list, s_list)

    def gen_rhythm(self):
        '''
        generate a rhythm randomly
        '''

        rhythm_list = []
        for _ in range(random.randint(2, 100)):
            rhythm_list.append(random.choice(['-', '-', '-', ' ', '.', '|']))
        return ''.join(rhythm_list)


# 1/4,2/4,3/4,4/4,3/8,6/8,7/8,9/8,12/8
# Patterns
