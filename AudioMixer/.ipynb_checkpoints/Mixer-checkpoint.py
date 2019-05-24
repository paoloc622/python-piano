import pyaudio  
import wave  
import numpy as np
import time

#define stream chunk   
chunk = 1024  

#open a wav format music  
F = [wave.open(r"A1.wav","rb"),  wave.open(r"A6.wav","rb")]

#instantiate PyAudio  
p = pyaudio.PyAudio() 

#open stream  
stream = p.open(format = p.get_format_from_width(F[0].getsampwidth()),  
                channels = F[0].getnchannels(),  
                rate = 44100,  
                output = True)  
#read data 
data = np.zeros(chunk, np.int32)
for f in F:
    dataf = f.readframes(chunk)  
    datafb = np.frombuffer(dataf, np.int32)
    data += datafb
print(list(data))
#play stream 
while True:  
    stream.write(data.tobytes())  
    data = np.zeros(chunk, np.int32)   
    for f in F: 
        dataf = f.readframes(chunk)  
        datafb = np.frombuffer(dataf, np.int32)
        data += datafb

#stop stream  
stream.stop_stream()  
stream.close()  

#close PyAudio  
p.terminate() 