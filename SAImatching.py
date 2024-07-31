'''
Matching sounds to note blocks
-PaiShoFish49
'''

from soundMatchingTemplate import *

target = file2Numpy(defaultPath + 'input/test.mp3', 'mp3')

maxSampleLength = 0
for i in NoteBlockInstruments:
    curSampleLength = len(file2Numpy(getInstrumentPath(i), 'ogg'))
    if curSampleLength > maxSampleLength:
        maxSampleLength = curSampleLength

target = applyFadeOut(target, maxSampleLength)
bases = np.zeros((25*len(NoteBlockInstruments), maxSampleLength))

for i, instr in enumerate(NoteBlockInstruments.keys()):
    curSample = file2Numpy(getInstrumentPath(instr), 'ogg', maxSampleLength)

    for pi, pitch in enumerate(generatePitches(curSample)):
        bases[(i*25) + pi] = pitch

matchedTarget = target.copy()
final = np.zeros(len(target))

while True:
    globalProgress = 0
    for i, base in enumerate(bases):
        print(i)
        progress = False
        currentTickIndex = 0
        while True:
            # print(currentTickIndex)
            currentTickStart = (currentTickIndex * getTickSamples())

            if (currentTickStart + maxSampleLength) >= len(matchedTarget):
                if progress:
                    currentTickIndex = 0
                    progress = False
                    continue
                else:
                    break

            currentTick = matchedTarget[currentTickStart:(currentTickStart + maxSampleLength)]
            fixedBase = findCoefficient(base, currentTick) * base

            newTick = currentTick - fixedBase
            if (np.max(np.abs(newTick)) < np.max(np.abs(currentTick))) and (np.mean(np.abs(newTick)) < np.mean(np.abs(currentTick))):
                progress = True
                globalProgress += 1
                matchedTarget[currentTickStart:(currentTickStart + maxSampleLength)] = newTick
                final[currentTickStart:(currentTickStart + maxSampleLength)] += fixedBase

            currentTickIndex += 1
            # time.sleep(0.01)

    print('oxoxoaosod', globalProgress)
    if globalProgress == 0:
        break

plt.plot(list(range(len(final))), final)
plt.show()
plt.plot(list(range(len(matchedTarget))), matchedTarget)
plt.show()
output_file_path = defaultPath + "output/finalTestSAI.wav"
sf.write(output_file_path, final, globalSampleRate)
sf.write(defaultPath + 'output/whatIsThis.wav', matchedTarget, globalSampleRate)