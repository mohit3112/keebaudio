# python -m pip install pyaudio
import pyaudio
import wave
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from scipy.fftpack import fft, fftfreq, rfft, rfftfreq
import sys

FRAMES_PER_BUFFER = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 48000

pa = pyaudio.PyAudio()

stream = pa.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAMES_PER_BUFFER
)

print('start recording')
seconds = 0.5

def live_audio(i):
    frames = []
    for j in range(0, int(RATE/FRAMES_PER_BUFFER*seconds)):
        data = stream.read(FRAMES_PER_BUFFER,exception_on_overflow = False)
        frames.append(data)
    audio_array = np.frombuffer(bytes(b''.join(frames)), dtype=np.int16)
    current_audio_cunk_ch0 = np.frombuffer(frames[-1], dtype=np.int16)[1::2]
    audio_ch0 = audio_array[1::2]

    times = np.linspace(0, seconds*i, num=frames.__len__()*FRAMES_PER_BUFFER)

    xf = rfftfreq(current_audio_cunk_ch0.__len__(),1/RATE)
    yf = rfft(current_audio_cunk_ch0)
    ax1.cla()
    ax1.plot(times, audio_ch0,linewidth=0.1)
    ax2.cla()
    ax2.plot(xf,np.abs(yf), linewidth=0.1)

def on_close(event):
    fig.canvas.mpl_disconnect('close_event')
    print("close recording")
    stream.stop_stream()
    stream.close()
    pa.terminate()
    # save wave file
    """
    obj = wave.open('Keeb.wav', 'wb')
    obj.setnchannels(CHANNELS)
    obj.setsampwidth(pa.get_sample_size(FORMAT))
    obj.setframerate(RATE)
    obj.writeframes(b''.join(frames))
    obj.close()
    """

def on_key_pressed(event):
    sys.stdout.flush()
    if event.key == 'p':
       animation.pause()
    if event.key == 'r':
       animation.resume()
    """
    file = wave.open('lemaster_tech.wav', 'rb')

    sample_freq = file.getframerate()
    signal_wave = frames
    nframes = file.getnframes()
    print(nframes)

    file.close()

    time = nframes / sample_freq
    print(time)
    """

fig, (ax1, ax2) = plt.subplots(2)
fig.canvas.mpl_connect('close_event',on_close)
fig.canvas.mpl_connect('key_press_event',on_key_pressed)
fig.set_figwidth(15)
fig.set_figheight(10)

ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Signal Wave')
ax1.set_title('Keeb Audio')

animation = FuncAnimation(plt.gcf(), live_audio, interval=500)
plt.show()
