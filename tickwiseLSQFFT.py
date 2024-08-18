'''
tickwise least squares. im getting tired of this.
'''

'''
Matching sounds to note blocks
-PaiShoFish49
'''

from soundMatchingTemplate import *

def getTickSegs():
    return getTickSamples() // 128

def extractMags(fft):
    return np.abs(fft)

target = file2Numpy(defaultPath + 'input/youxyou.mp3', 'mp3')
_, _, targetFT = stft(target, globalSampleRate)
targetFT = extractMags(np.transpose(targetFT))

maxSampleLength = 0
for i in NoteBlockInstruments:
    curSampleLength = len(file2Numpy(getInstrumentPath(i), 'ogg'))
    if curSampleLength > maxSampleLength:
        maxSampleLength = curSampleLength
maxSegLength = (maxSampleLength // 128) + 2

bases = np.zeros((25*len(NoteBlockInstruments), maxSampleLength))
baseFT = np.zeros((25*len(NoteBlockInstruments), maxSegLength * 129))

for i, instr in enumerate(NoteBlockInstruments.keys()):
    curSample = file2Numpy(getInstrumentPath(instr), 'ogg', maxSampleLength)

    for pi, pitch in enumerate(generatePitches(curSample)):
        _, _, pitchFT = stft(curSample, globalSampleRate)
        pitchFT = extractMags(np.transpose(pitchFT)).flatten()

        bases[(i*25) + pi] = pitch
        baseFT[(i*25) + pi] = pitchFT

matchedTarget = targetFT.copy()
final = np.zeros(len(target))

tickIndex = 0
while True:
    currentTickStart = tickIndex * getTickSamples()
    currentTickStartSegs = tickIndex * getTickSegs()
    if currentTickStart + maxSampleLength >= len(final):
        break
    currentTargetTick: np.ndarray = matchedTarget[currentTickStartSegs:currentTickStartSegs + maxSegLength]
    currentTargetTick = currentTargetTick.flatten()

    coefs = lsq_linear(baseFT.transpose(), currentTargetTick, (0, 1)).x
    for i in range(len(bases)):
        matchedTarget[currentTickStartSegs:currentTickStartSegs + maxSegLength] -= (baseFT[i] * coefs[i]).reshape(224, 129)
        final[currentTickStart:currentTickStart + maxSampleLength] += bases[i] * coefs[i]
    print(tickIndex)
    tickIndex += 1

plt.plot(list(range(len(final))), final)
plt.show()
plt.plot(list(range(len(matchedTarget))), matchedTarget)
plt.show()
output_file_path = defaultPath + "output/finalTest.wav"
sf.write(output_file_path, final, globalSampleRate)
sf.write(defaultPath + 'output/whatIsThis.wav', matchedTarget, globalSampleRate)