import pyaudio
import wave
import numpy as np
import time
import copy
import shutil

chunk = 1024
class Mixer:

    def __init__(self):
        #define stream chunk


        #open a wav format music
        F = wave.open(r"A1.wav","rb")

        #instantiate PyAudio
        self.p = pyaudio.PyAudio()
        #open stream
        self.stream = self.p.open(format = self.p.get_format_from_width(F.getsampwidth()),
                        rate = 44100,
                        channels = 2,
                        output = True)

        self.waves = []
        self.data = np.zeros(chunk, np.int32)
    #play stream
    def playStream(self):
        while True:
            self.stream.write(self.data.tobytes())
            self.data = np.zeros(chunk, np.int32)
            for keyname, keyplayheads in self.playheads.items():
                #print(self.playheads)
                for n, playhead in enumerate(keyplayheads):
                    if playhead >= self.wavheads[keyname].getnframes():
                    #    print('deleting')
                        del self.playheads[keyname][n]
                    else:
                        self.wavheads[keyname].setpos(playhead)
                        dataf = self.wavheads[keyname].readframes(chunk)
                        self.playheads[keyname][n] += 1024
                        datafb = np.frombuffer(dataf, np.int32)
                        self.data += np.pad(datafb, (0, 1024 - len(datafb)), 'constant')

                    #print(playhead, self.wavheads[keyname].getnframes())




    def Sound(self, keyname, wvfile):
        self.playheads[keyname].append(0)

    def stopStream(self):
        #stop stream
        self.stream.stop_stream()
        self.stream.close()


    def register(self, noteref, wavref):
        self.wavheads = {key:wav for key, wav in wavref.items()}
        self.playheads = {key:[]for key in noteref}

#help
