'''
Target First Matching Method
-PaiShoFish49
'''

from soundMatchingTemplate import *

def evaluateAudio(audioData):
    absVals = np.abs(audioData)
    return np.mean(absVals)

def getTickRange(length, tickIndex):
    start = tickIndex * getTickSamples()
    end = start + length
    return start, end

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

evals = np.zeros(1000)
for iter in range(1000):
    numOfTicks = (len(matchedTarget) - maxSampleLength) // getTickSamples()
    randomTickIndex = random.randrange(0, numOfTicks - 1)
    randomTickRange = getTickRange(maxSampleLength, randomTickIndex)
    randomTick = matchedTarget[randomTickRange[0]:randomTickRange[1]]

    bestInstrument = 0
    bestInstrumentScore = np.inf

    for i, j in enumerate(bases):
        currentInstrumentCoef = findCoefficient(j, randomTick)
        currentInstrumentFinalSound = j * currentInstrumentCoef
        currentInstrumentScore = evaluateAudio(randomTick - currentInstrumentFinalSound)

        if (currentInstrumentScore < bestInstrumentScore):
            bestInstrument = i
            bestInstrumentScore = currentInstrumentScore

            bestInstrumentCoef = currentInstrumentCoef
            bestInstrumentFinalSound = currentInstrumentFinalSound

    # print(bestInstrument)
    # print(bestInstrumentCoef)
    # if iter > 500:
        # time.sleep(0.5)
    print(bestInstrumentScore)
    evals[iter] = bestInstrumentScore

    matchedTarget[randomTickRange[0]:randomTickRange[1]] -= bestInstrumentFinalSound

    final[randomTickRange[0]:randomTickRange[1]] += bestInstrumentFinalSound

# Save the approximated audio to a file
plt.plot(list(range(1000)), evals)
plt.show()
output_file_path = defaultPath + "output/finalTestTFM.wav"
sf.write(output_file_path, final, globalSampleRate)
sf.write(defaultPath + 'output/whatIsThis.wav', matchedTarget, globalSampleRate)