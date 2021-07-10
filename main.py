from pydub import AudioSegment
import wave
import matplotlib.pyplot as plt
import numpy as np
from os import listdir
from os.path import isfile, join


def mp3_analyse(relative_file_path):
    
    # converting mp3 to wav
    sound = AudioSegment.from_mp3(relative_file_path)
    filename = relative_file_path[0: len(relative_file_path) - 4]
    sound.export(filename + '.wav', format='wav')

    # opening the wav file
    audio = wave.open(filename + '.wav')
    frames = audio.readframes(-1)
    length_sec = audio.getnframes() / audio.getframerate()

    # Time Domain {
    time_range = np.linspace(0, length_sec, audio.getnframes())
    amplitude = np.frombuffer(frames, 'int16')

    # plotting
    plt.figure(1)
    plt.title('Time Domain')
    plt.xlabel('Seconds')
    plt.ylabel('Amplitude')
    plt.plot(time_range, amplitude)
    # }

    # Frequency Domain {
    # FFT
    freq_magnitude_spectrum = np.abs(np.fft.rfft(amplitude))
    freq_power_spectrum = [i**2 for i in freq_magnitude_spectrum]
    freq_range = np.linspace(0, audio.getframerate() / 2, len(freq_power_spectrum))

    # to limit the frequency range to 0-1000Hz
    freq_power_spectrum = freq_power_spectrum[: int(len(freq_power_spectrum) * 1000 / (audio.getframerate() / 2))]
    freq_range = freq_range[: int(len(freq_range) * 1000 / (audio.getframerate() / 2))]

    # calculating the peak frequency
    pick = -1
    pick_frequency = -1
    for i in range(len(freq_power_spectrum)):
        if freq_power_spectrum[i] > pick:
            pick = freq_power_spectrum[i]
            pick_frequency = freq_range[i]

    # checking if it is a man's voice or a woman's
    if pick_frequency >= 172:
        print(relative_file_path, ': Pick Frequency=', pick_frequency, ', Woman')
    else:
        print(relative_file_path, ': Pick Frequency= ', pick_frequency, ', Man')

    # plotting
    plt.figure(2)
    plt.title('Power Spectrum')
    plt.xlabel('Frequency')
    plt.ylabel('Power')
    plt.plot(freq_range, freq_power_spectrum)
    plt.show()
    # }

    audio.close()


def folder_analyse(relative_dir_name):
    # listing all mp3 files
    files = [f for f in listdir(relative_dir_name) if isfile(join(relative_dir_name, f))
             and f[len(f) - 4: len(f)] == '.mp3']

    # dealing with all mp3 files
    for file in files:
        mp3_analyse(join(relative_dir_name, file))


# mp3_analyse('./voices/v4.mp3')
folder_analyse('./voices')
