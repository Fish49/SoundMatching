'''
Matching sounds to note blocks
-PaiShoFish49
'''

from soundMatchingTemplate import *
from scipy.io.wavfile import write
from scipy.signal import istft

def getTickSegs():
    return getTickSamples() // 128

def complexTo3D(data):
    magnitude = np.abs(data)
    phase = np.angle(data)

    # Create a 3D array with amplitude and phase
    return np.stack((magnitude, phase), axis=-1)

target = file2Numpy(defaultPath + 'input/test.mp3', 'mp3')
_, _, targetFT = stft(target, globalSampleRate)
targetFT = complexTo3D(np.transpose(targetFT))

maxSampleLength = 0
for i in NoteBlockInstruments:
    curSampleLength = len(file2Numpy(getInstrumentPath(i), 'ogg'))
    if curSampleLength > maxSampleLength:
        maxSampleLength = curSampleLength

maxSegLength = (maxSampleLength // 128) + 2

bases = np.zeros((25*len(NoteBlockInstruments), maxSegLength, 129, 2))
baseWaves = np.zeros((25*len(NoteBlockInstruments), maxSampleLength))

for i, instr in enumerate(NoteBlockInstruments.keys()):
    curSample = file2Numpy(getInstrumentPath(instr), 'ogg', maxSampleLength)

    for pi, pitch in enumerate(generatePitches(curSample)):
        _, _, pitchFT = stft(curSample, globalSampleRate)
        pitchFT = complexTo3D(np.transpose(pitchFT))

        baseWaves[(i * 25) + pi] = pitch
        bases[(i*25) + pi] = pitchFT

matchedTarget = targetFT.copy()
final = np.zeros(len(target))
totalNoteBlocks = 0
additionsPerPass = []

while True:
    globalProgress = 0

    for i, base in enumerate(bases):
        currentTickIndex = 0
        observeList = []
        addList = []

        while True:
            # print(currentTickIndex)
            currentTickStart = (currentTickIndex * getTickSegs())
            currentTickStartSamples = (currentTickIndex * getTickSamples())

            if (currentTickStart + maxSegLength) >= len(matchedTarget):
                break

            currentTick = matchedTarget[currentTickStart:(currentTickStart + maxSegLength)]
            fixedBase = findCoefficient(base, currentTick) * base

            newTick = currentTick - fixedBase
            if (np.mean(np.abs(newTick)) < np.mean(np.abs(currentTick))):
                print(i)
                globalProgress += 1
                observeList.append((np.mean(np.abs(currentTick)) / np.mean(np.abs(newTick)), currentTickStart, currentTickStartSamples, fixedBase.copy(), baseWaves[i].copy()))

            currentTickIndex += 1
            # time.sleep(0.01)

        observeList.sort(key=(lambda x: x[0]))

        while True:
            if observeList == []:
                break

            bestInstrumentTick = observeList[0]

            addList.append(observeList[0])

            temp = []
            for match in observeList[1:]:
                condition1 = (observeList[0][1] <= match[1] <= observeList[0][1] + maxSegLength)
                condition2 = (observeList[0][1] <= match[1] + maxSegLength <= observeList[0][1] + maxSegLength)
                if not (condition1 or condition2):
                    temp.append(match)

            observeList = temp

        for add in addList:
            matchedTarget[add[1]:add[1] + maxSegLength] -= add[3]
            final[add[2]:(add[2] + maxSampleLength)] += add[4]

    print('oxoxoaosod', globalProgress)
    if globalProgress == 0:
        break

    additionsPerPass.append(globalProgress)
    totalNoteBlocks += globalProgress

plt.plot(list(range(len(final))), final)
plt.show()
# plt.plot(list(range(len(matchedTarget))), matchedTarget)
# plt.show()
plt.plot(list(range(len(additionsPerPass))), additionsPerPass)
plt.show()
output_file_path = defaultPath + "output/finalTestSAI.wav"
sf.write(output_file_path, final, globalSampleRate)
# sf.write(defaultPath + 'output/whatIsThis.wav', matchedTarget, globalSampleRate)
print(f'Total Note Blocks: {totalNoteBlocks}, NoteBlocksPerTick: {totalNoteBlocks / (len(target) // getTickSamples())}')