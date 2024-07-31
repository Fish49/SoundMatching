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

def getTicksEvaluation(audioData, endDuration):
    numOfTicks = (len(audioData) - endDuration) // getTickSamples()
    evaluation = np.zeros(numOfTicks)

    for i in range(numOfTicks):
        tickRange = getTickRange(endDuration, i)
        evaluation[i] = evaluateAudio(audioData[tickRange[0]:tickRange[1]])

    return evaluation

def getMaxTickIndex(tickEvaluation):
    ind = 0
    maxVal = 0
    for i, j in enumerate(tickEvaluation):
        if j > maxVal:
            ind = i
            maxVal = j

    return ind

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

for iter in range(500):
    tickEvaluation = getTicksEvaluation(matchedTarget, maxSampleLength)
    worstTickIndex = getMaxTickIndex(tickEvaluation)
    worstTickRange = getTickRange(maxSampleLength, worstTickIndex)
    worstTick = matchedTarget[worstTickRange[0]:worstTickRange[1]]
    print(worstTickIndex)
    print(tickEvaluation[worstTickIndex])

    bestInstrument = 0
    bestInstrumentScore = np.inf

    for i, j in enumerate(bases):
        currentInstrumentCoef = findCoefficient(j, worstTick)
        currentInstrumentFinalSound = j * currentInstrumentCoef
        currentInstrumentScore = evaluateAudio(worstTick - currentInstrumentFinalSound)

        if (currentInstrumentScore < bestInstrumentScore):
            bestInstrument = i
            bestInstrumentScore = currentInstrumentScore

            bestInstrumentCoef = currentInstrumentCoef
            bestInstrumentFinalSound = currentInstrumentFinalSound

    # print(bestInstrument)
    # print(bestInstrumentCoef)
    # if iter > 500:
        # time.sleep(0.5)
    matchedTarget[worstTickRange[0]:worstTickRange[1]] -= bestInstrumentFinalSound

    final[worstTickRange[0]:worstTickRange[1]] += bestInstrumentFinalSound

# Save the approximated audio to a file
plt.plot(list(range(len(final))), final)
plt.show()
output_file_path = defaultPath + "output/finalTestTFM.wav"
sf.write(output_file_path, final, globalSampleRate)
sf.write(defaultPath + 'output/whatIsThis.wav', matchedTarget, globalSampleRate)