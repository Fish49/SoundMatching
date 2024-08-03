'''
Matching sounds to note blocks Template
-PaiShoFish49
'''

import numpy as np
from scipy.optimize import lsq_linear, minimize
from scipy.signal import stft
from librosa.effects import pitch_shift
from librosa import resample as libresample
from pydub import AudioSegment
from pydub.playback import play
import soundfile as sf
import matplotlib.pyplot as plt
import time
import random
import math

AudioSegment.converter = 'C:\\ffmpeg\\bin\\ffmpeg.exe'

globalSampleRate = 44100
tickRate = 10
defaultPath = ''

NoteBlockInstruments = {
    'flute': 3,
    'bit': 3,
    'iron_xylophone': 3,
    'didgeridoo': 3,
    'harp': 5,
    'guitar': 5,
    'dbass': 3,
    'cow_bell': 1,
    'bell': 3,
    'pling': 5,
    'click': 1,
    'banjo': 3,
    'xylobone': 1,
    'bdrum': 1,
    'sdrum': 1,
}

ones = [
    'bdrum',
    'click',
    'cow_bell',
    'sdrum',
    'xylobone'
]

threes = [
    'banjo',
    'bell',
    'bit',
    'dbass',
    'didgeridoo',
    'flute',
    'iron_xylophone',
]

def getTickSamples():
    return globalSampleRate // tickRate

def getFractionSecond(tenths):
    return globalSampleRate * tenths // 10

def getInstrumentPath(instrument):
    return defaultPath + f'noteBlocks/{instrument}.ogg'

def file2Numpy(file_path, format, length = None):
    audio = AudioSegment.from_file(file_path, format=format)
    data = np.array(audio.get_array_of_samples())
    if audio.channels == 2:
        data = data.reshape((-1, 2))
        data = data.mean(axis=1)

    data = resample(data, audio.frame_rate, globalSampleRate)[0]
    data = normalizeAudio(data)

    if length != None:
        return cropExtend(data, length)
    return data

#16000
def normalizeAudio(audio_data, desired_peak = 1.0):
    minVal = np.min(audio_data)
    maxVal = np.max(audio_data)

    middle = np.mean(audio_data)
    scaleFactor = (desired_peak / (maxVal - minVal))

    return (audio_data - middle) * scaleFactor

def applyFadeOut(audioData, fadeOutSamples):
    # Calculate the number of samples for the fade-out duration

    # Create a linear ramp from 1 to 0
    ramp = np.linspace(1, 0, fadeOutSamples)

    # Apply the ramp to the end of the audio data
    faded_audio = audioData.copy()
    faded_audio[-fadeOutSamples:] *= ramp

    return faded_audio

def resample(data, origionalsr, targetsr):
    newData = libresample(data.astype(float), orig_sr=origionalsr, target_sr=targetsr)
    return newData, targetsr

def cropExtend(base, length):
    if len(base) > length:
        return base[:length]
    else:
        a = np.zeros(length)
        a[:len(base)] = base
        return a

def generatePitches(audio_data, frame_rate = globalSampleRate, num_pitches=25):
    pitches = []

    for i in range(num_pitches):
        semitone_shift = i - (num_pitches // 2)
        pitch_shifted = pitch_shift(audio_data.astype(float), sr=frame_rate, n_steps=semitone_shift)
        pitches.append(pitch_shifted)
    return pitches

def cofToArray(bases, coefficients):
    arr = np.zeros(bases.shape[1])
    for i, j in enumerate(coefficients):
        arr += bases[i]*j
    return arr

def findCoefficient(A, B):
    # Ensure A and B are numpy arrays
    A = np.array(A)
    B = np.array(B)
    if len(A.shape) == 3:
        A = A[:, :, 0].flatten()
        B = B[:, :, 0].flatten()

    # Calculate the dot products
    dot_product_AB = np.dot(A, B)
    dot_product_AA = np.dot(A, A)

    # Calculate the coefficient
    coefficient = dot_product_AB / dot_product_AA

    # Ensure the coefficient is non-negative
    if coefficient < 0:
        coefficient = 0

    return coefficient