import pyaudio  
import wave  
import numpy as np
import time

#define stream chunk   
chunk = 1024  

#open a wav format music  
f1 = wave.open(r"A1.wav","rb")  
f2 = wave.open(r"A6.wav","rb")
#instantiate PyAudio  
p = pyaudio.PyAudio() 

#open stream  
stream = p.open(format = p.get_format_from_width(f1.getsampwidth()),  
                channels = f1.getnchannels(),  
                rate = f1.getframerate(),  
                output = True)  

import pdb; pdb.set_trace()

#read data  
data1 = f1.readframes(chunk)  
data2 = f2.readframes(chunk) 
data1b = np.frombuffer(data1, np.int32)
data2b = np.frombuffer(data2, np.int32)
data = data1b + data2b

#play stream 
while True:  
    stream.write(data.tobytes())  
    data1 = f1.readframes(chunk)  
    data2 = f2.readframes(chunk) 
    data1b = np.frombuffer(data1, np.int32)
    data2b = np.frombuffer(data2, np.int32)
    data = data1b + data2b
    print(data.shape)

#stop stream  
stream.stop_stream()  
stream.close()  

#close PyAudio  
p.terminate() 