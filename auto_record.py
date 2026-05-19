#===========================# 
#        Description        #
#===========================#
# Main file that we run when auto detecting audio
# The taskflow is to standby on listening until the noise threshold is breached
# After that, record for a certain period of time then save it to the google drive
import wave
import sys
import math
import array

import pyaudio

#===========================# 
#       Global Params       #
#===========================#
# Gotten online
CHUNK           = 1024
FORMAT          = pyaudio.paInt16
CHANNELS        = 1 if sys.platform == 'darwin' else 2
RATE            = 44100
RECORD_SECONDS  = 5

# Defined
NOISE_THRESHOLD = 0.1  # *** TEMPORARY VALUE - figure out the actual value experimentally **** # 
COUNT = 1

#===========================# 
#        Auto-Record        #
#===========================#
# From audio.py we know how to start and make a recording, therefore we need to figure out the condition 
# of how the device starts recording i.e. the threshold
# 
# The most useful way of measuring volume is the root mean square (RMS) of the audio block
# Its formula is the sqrt((x1^2 + x2^2 + ... xn^2)/n) but what  are passing into the RMS function?

# def RMScalc ():
#     rms = 
#     return rms
try:
    p = pyaudio.PyAudio()
    stream = p.open(rate=RATE, channels=CHANNELS, format=FORMAT, input=True, frames_per_buffer=CHUNK)
    print("Listening...")

    while True:
        data = stream.read(CHUNK)
        rms = math.sqrt(sum(x**2 for x in array.array('h', data)) / CHUNK)

        # if the threshold is breached, start the recording
        if rms > NOISE_THRESHOLD: 
            filename = f"recordings/recording_{COUNT}.wav"
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(p.get_sample_size(FORMAT))
                wf.setframerate(RATE)

                print('Recording...')
                wf.writeframes(data)
                for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
                    wf.writeframes(stream.read(CHUNK))
                print('Done')
            COUNT += 1
except KeyboardInterrupt:
    print("\n Program stopped by user")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()

#===========================# 
#        Google Drive       #
#===========================#
# Going to save to a local directory initially, will add Google Drive export after 
