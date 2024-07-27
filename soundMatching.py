'''
Matching sounds to note blocks
-PaiShoFish49
'''

import numpy as np
from scipy.optimize import lsq_linear
from librosa.effects import pitch_shift
from librosa import resample as libresample
from pydub import AudioSegment
from pydub.playback import play
import soundfile as sf
import matplotlib.pyplot as plt

AudioSegment.converter = 'C:\\ffmpeg\\bin\\ffmpeg.exe'

globalSampleRate = 44100
defaultPath = 'soundMatching/'

group1 = [
    'flute', #1
    'bit', #2
    'iron_xylophone', #3
    'didgeridoo', #4
]

group2 = [
    'harp',
    'guitar', #5
    'dbass',
    'cow_bell',
    'bell',
    'pling',
]

group3 = [
    'click',
    'banjo',
    'xylobone',
    'bdrum',
    'sdrum',
]

alldem = group1.copy()
alldem.extend(group1)
alldem.extend(group2)
alldem.extend(group3)

group4 = [
    'icechime'
]

def file_to_numpy(file_path, format):
    audio = AudioSegment.from_file(file_path, format=format)
    data = np.array(audio.get_array_of_samples())
    if audio.channels == 2:
        data = data.reshape((-1, 2))
        data = data.mean(axis=1)
    return resample(normalize_audio(data), audio.frame_rate, globalSampleRate)

def normalize_audio(audio_data, desired_peak=1.0):
    peak = np.max(np.abs(audio_data))
    if peak > 0:
        normalization_factor = desired_peak / peak
        normalized_audio = audio_data * normalization_factor
        return normalized_audio
    else:
        return audio_data

def generate_pitches(audio_data, frame_rate, num_pitches=25):
    pitches = []
    for i in range(num_pitches):
        semitone_shift = i - (num_pitches // 2)
        pitch_shifted = pitch_shift(audio_data.astype(float), sr=frame_rate, n_steps=semitone_shift)
        pitches.append(pitch_shifted)
    return pitches

def create_shifted_bases(base, length, frame_rate, sps, maxShifts = None):
    shiftNumber = int(frame_rate / sps)
    shiftRange = range(length - len(base) + 1)

    shifted_bases = []
    for i, shift in enumerate(shiftRange[::shiftNumber]):
        if maxShifts != None:
            if i == maxShifts:
                break
        shifted = np.zeros(length)
        shifted[shift:shift+len(base)] = base
        shifted_bases.append(shifted)
    return shifted_bases

def cropExtend(base, length):
    if len(base) > length:
        return base[:length]
    else:
        a = np.zeros(length)
        a[:len(base)] = base
        return a

def resample(data, origionalsr, targetsr):
    newData = libresample(data.astype(float), orig_sr=origionalsr, target_sr=targetsr)
    return newData, targetsr

def cofToArray(bases, coefficients):
    arr = np.zeros(bases.shape[1])
    for i, j in enumerate(coefficients):
        arr += bases[i]*j
    return arr

targetPath = defaultPath + 'test.mp3'
target, _ = file_to_numpy(targetPath, 'mp3')
targetLen = len(target)

numOfIters = (targetLen // 22050)
final = np.zeros(targetLen)
matchedTarget = target.copy()

tots = 1
dpoints = [np.std(matchedTarget)]
for killme in range(1):
    for ini, ins in enumerate(alldem):
        print(ins)
        bases = np.zeros((125, globalSampleRate))
        a, _= file_to_numpy(defaultPath + f'noteBlocks/{ins}.ogg', 'ogg')
        for pi, p in enumerate(generate_pitches(a, globalSampleRate)):
            p2 = cropExtend(p, 22050)
            for bi, b in enumerate(create_shifted_bases(p2, globalSampleRate, globalSampleRate, 10, 5)):
                bases[(bi*25) + pi] = b

        basestran = bases.transpose()

        print(numOfIters)
        for i in range(numOfIters):
            start = i * 22050
            # if i >= numOfIters-1:
            #     end = targetLen
            # else:
            end = ((i + 1) * 22050) + 22050

            print(f'I:{i}, Start:{start}, End:{end}, RealStart:{start/globalSampleRate}, RealEnd:{end/globalSampleRate}')

            try:
                xes = lsq_linear(basestran, matchedTarget[start:end], (0, 1)).x
            except:
                break
            xesarr = cofToArray(bases, xes)

            matchedTarget[start:end] -= xesarr
            final[start:end] += xesarr
    
        tots += 1
        print(np.std(matchedTarget))
        dpoints.append(np.std(matchedTarget))

# Save the approximated audio to a file
output_file_path = defaultPath + "finalTest.wav"
sf.write(output_file_path, final, globalSampleRate)

plt.scatter(list(range(tots)), dpoints)
plt.show()

# Load the saved file and play it
# approximated_audio_segment = AudioSegment.from_file(output_file_path, format="wav")
# play(approximated_audio_segment)