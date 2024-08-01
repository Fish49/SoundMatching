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
            currentTickStart = (currentTickIndex * getTickSamples())

            if (currentTickStart + maxSampleLength) >= len(matchedTarget):
                break

            currentTick = matchedTarget[currentTickStart:(currentTickStart + maxSampleLength)]
            fixedBase = findCoefficient(base, currentTick) * base

            newTick = currentTick - fixedBase
            if (np.max(np.abs(newTick)) < np.max(np.abs(currentTick))) and (np.mean(np.abs(newTick)) < np.mean(np.abs(currentTick))):
                print(i)
                globalProgress += 1
                observeList.append((np.mean(np.abs(currentTick)) / np.mean(np.abs(newTick)), currentTickStart, fixedBase.copy()))

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
                condition1 = (observeList[0][1] <= match[1] <= observeList[0][1] + maxSampleLength)
                condition2 = (observeList[0][1] <= match[1] + maxSampleLength <= observeList[0][1] + maxSampleLength)
                if not (condition1 or condition2):
                    temp.append(match)

            observeList = temp

        for add in addList:
            matchedTarget[add[1]:add[1] + maxSampleLength] -= add[2]
            final[add[1]:add[1] + maxSampleLength] += add[2]

    print('oxoxoaosod', globalProgress)
    if globalProgress == 0:
        break

    additionsPerPass.append(globalProgress)
    totalNoteBlocks += globalProgress

plt.plot(list(range(len(final))), final)
plt.show()
plt.plot(list(range(len(matchedTarget))), matchedTarget)
plt.show()
plt.plot(list(range(len(additionsPerPass))), additionsPerPass)
plt.show()
print(f'Total Note Blocks: {totalNoteBlocks}, NoteBlocksPerTick: {totalNoteBlocks / (len(target) // getTickSamples())}')
output_file_path = defaultPath + "output/finalTestSAI.wav"
sf.write(output_file_path, final, globalSampleRate)
sf.write(defaultPath + 'output/whatIsThis.wav', matchedTarget, globalSampleRate)