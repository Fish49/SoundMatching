# SoundMatching
Im trying to find a way to match a target song as closely as possible using a finite collection of shorter sound files (in this case minecraft noteblocks)

## Current Methods
1. Target - First Matching
 - it finds the tick of the target sound wave that is least solved (highest average), and it chooses the base sound that matches it best. it repeats this for a set number of iterations.
2. Time - Dependant TFM
 - same as target - first matching, except it does it seperately for different length bases.
3. Random TFM
 - same as TFM exept instead of choosing the least solved tick, it chooses a random tick.
4. SAI Matching
 - SAI stands for space alien invasion, because the process kinda looks the same as the game. for each base wave, it looks at each tick of the target wave, and if combining the base and that section of the target would result in an improvement, it does so. it repeats this process until no further improvements can be made.
5. Picky SAI
 - Same as SAI, exept instead of adding the waves immediately, it adds them to a list. at the end of each iteration, it uses the list to add all the best non - overlapping ticks for that instrument. again it repeats until no further improvements can be made.

## Future
Im planning on looking into using FFTs (Fast - Fourier Transforms) instead of the base waveform. hopefully this will help match the essence of the target instead of trying to match the specific waveform.
