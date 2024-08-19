'''
tickwise least squares. im getting tired of this.
'''

'''
Matching sounds to note blocks
-PaiShoFish49
'''

from soundMatchingTemplate import *

target = file2Numpy(defaultPath + 'input/youxyou.mp3', 'mp3')

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

tickIndex = 0
while True:
    currentTickStart = tickIndex * getTickSamples()
    if currentTickStart + maxSampleLength >= len(final):
        break
    currentTargetTick = matchedTarget[currentTickStart:currentTickStart + maxSampleLength]

    coefs = lsq_linear(bases.transpose(), currentTargetTick, (0, 1)).x
    for i in range(len(bases)):
        # print(coefs[i])
        if coefs[i] < 0.005:
            # print(i)
            continue
        # print(i)
        matchedTarget[currentTickStart:currentTickStart + maxSampleLength] -= bases[i] * coefs[i]
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