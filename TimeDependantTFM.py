'''
Target First Matching Method
-PaiShoFish49
'''

from soundMatchingTemplate import *

NoteBlockInstruments1 = [i for i in NoteBlockInstruments.keys() if NoteBlockInstruments[i] == 1]
NoteBlockInstruments3 = [i for i in NoteBlockInstruments.keys() if NoteBlockInstruments[i] == 3]
NoteBlockInstruments5 = [i for i in NoteBlockInstruments.keys() if NoteBlockInstruments[i] == 5]

def evaluateAudio(audioData):
    absVals = np.abs(audioData)
    return np.mean(absVals)

def getTickRange(length, tickIndex):
    start = tickIndex * getTickSamples()
    end = start + length
    return start, end

def getTicksEvaluation(audioData):
    numOfTicks = (len(audioData) - getFractionSecond(5)) // getTickSamples()
    evaluation = np.zeros((numOfTicks, 3))

    for i in range(numOfTicks):
        for j in range(3):
            tickRange = getTickRange((j * 2) + 1, i)
            evaluation[i, j] = evaluateAudio(audioData[tickRange[0]:tickRange[1]])

    return evaluation

def getMaxTickCord(tickEvaluation):
    cord = (0, 0)
    maxVal = 0
    for x in range(tickEvaluation.shape[0]):
        for y, j in enumerate(tickEvaluation[x]):
            if j > maxVal:
                cord = (x, (y * 2) + 1)
                maxVal = j

    return cord

target = file2Numpy(defaultPath + 'test.mp3', 'mp3')

target = applyFadeOut(target, getFractionSecond(5))
bases1 = np.zeros((25 * len(NoteBlockInstruments1), getFractionSecond(1)))
bases3 = np.zeros((25 * len(NoteBlockInstruments3), getFractionSecond(3)))
bases5 = np.zeros((25 * len(NoteBlockInstruments5), getFractionSecond(5)))

for i, instr in enumerate(NoteBlockInstruments1):
    duration = 1
    curSample = file2Numpy(getInstrumentPath(instr), 'ogg', getFractionSecond(duration))

    for pi, pitch in enumerate(generatePitches(curSample)):
        bases1[(i*25) + pi] = pitch

for i, instr in enumerate(NoteBlockInstruments3):
    duration = 3
    curSample = file2Numpy(getInstrumentPath(instr), 'ogg', getFractionSecond(duration))

    for pi, pitch in enumerate(generatePitches(curSample)):
        bases3[(i*25) + pi] = pitch

for i, instr in enumerate(NoteBlockInstruments5):
    duration = 5
    curSample = file2Numpy(getInstrumentPath(instr), 'ogg', getFractionSecond(duration))

    for pi, pitch in enumerate(generatePitches(curSample)):
        bases5[(i*25) + pi] = pitch

matchedTarget = target.copy()
final = np.zeros(len(target))

for iter in range(1200):
    tickEvaluation = getTicksEvaluation(matchedTarget)
    worstTickIndex, duration = getMaxTickCord(tickEvaluation)
    worstTickRange = getTickRange(getFractionSecond(duration), worstTickIndex)
    worstTick = matchedTarget[worstTickRange[0]:worstTickRange[1]]
    print(duration)
    print(tickEvaluation[worstTickIndex])

    bestInstrument = 0
    bestInstrumentScore = np.inf

    if duration == 1:
        bases = bases1
    elif duration == 3:
        bases = bases3
    elif duration == 5:
        bases = bases5

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
output_file_path = defaultPath + "finalTestTFM.wav"
sf.write(output_file_path, final, globalSampleRate)
sf.write(defaultPath + 'whatIsThis.wav', matchedTarget, globalSampleRate)