# Code based on https://simpleaudio.readthedocs.io/en/latest/tutorial.html#waveobject-s
# Song composition based on http://www.piano-keyboard-guide.com/how-to-play-the-tetris-theme-song-easy-piano-tutorial-korobeiniki/

import numpy as np
import simpleaudio as sa

# Song improved by Lorenzo Gaifas
song = ["E","B","C"] + ["D","C","B"] + ["A","A","C"] + ["E","D","C"] + ["B","B","C"] + ["D","E","C","A","A"] + \
       ["P","P"] + ["D","F"] + \
       ["Ah","G","F"] + ["E","E","C"] + ["E","D","C"] + ["B","B","C"] + ["D","E","C","A","A"] + \
       ["P"]
timing = [2,1,1] * 5 + [2,2,2,2,2] + [2,1] + [2,1] + [2,1,1] * 4 + [2,2,2,2,2] + [2]

# calculate note frequencies
A_freq = 440

freqs = [0] + [
    A_freq * 2 ** (i / 12)
    for i in range(13)
    ]

notes = ['P','A','A#','B','C','C#','D','D#','E','F','F#','G','G#','Ah']

note_to_freq = {
        n: f
        for n, f in zip(notes, freqs)
        }

# get timesteps for each sample, T is note duration in seconds
sample_rate = 44100
T = 0.25
t = lambda factor: np.linspace(0, T*factor, T*factor * sample_rate, False)

def note_to_sine(note, time):
    f = note_to_freq[note]
    return np.sin(f * t(time) * 2 * np.pi) 

song_sines = [
        note_to_sine(note, time)
        for note, time in zip(song, timing)
        ]

# concatenate notes
audio = np.hstack(song_sines)
# normalize to 16-bit range
audio *= 32767 / np.max(np.abs(audio))
# dampen a bit
audio *= 0.255555
# convert to 16-bit data
audio = audio.astype(np.int16)

# start playback
def start():
    while True:
        play_obj = sa.play_buffer(audio, 1, 2, sample_rate)
        play_obj.wait_done()
