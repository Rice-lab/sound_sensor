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
import datetime

import pyaudio
from google_drive.drive_methods import file_upload    # drive upload function

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
NOISE_THRESHOLD = 0.7  # *** TEMPORARY VALUE - figure out the actual value experimentally **** # 

#===========================# 
#        Auto-Record        #
#===========================#
# From audio.py we know how to start and make a recording, therefore we need to figure out the condition 
# of how the device starts recording i.e. the threshold
# 
# The most useful way of measuring volume is the root mean square (RMS) of the audio block
# Its formula is the sqrt((x1^2 + x2^2 + ... xn^2)/n) but what  are passing into the RMS function?
try:
    p = pyaudio.PyAudio()
    stream = p.open(rate=RATE, channels=CHANNELS, format=FORMAT, input=True, frames_per_buffer=CHUNK)
    print("Listening...")

    while True:
        data = stream.read(CHUNK)
        rms = math.sqrt(sum(x**2 for x in array.array('h', data)) / CHUNK)

        # If the threshold is breached, start the recording
        if rms > NOISE_THRESHOLD: 
            NOW = datetime.datetime.now()
            fNOW = NOW.strftime("%b_%d_%Y_%H-%M-%S")
            filename = f"recordings/recording_{fNOW}.wav"
            test = "google_drive/" + filename
            with wave.open(test, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(p.get_sample_size(FORMAT))
                wf.setframerate(RATE)

                print('Recording...')
                wf.writeframes(data)
                for _ in range(0, RATE // CHUNK * RECORD_SECONDS):
                    wf.writeframes(stream.read(CHUNK))
                print('Done')
               
                # Upload the file to Google Drive
                file_upload(filename=filename)
except KeyboardInterrupt:
    print("\n Program stopped by user")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
