from soundMatchingTemplate import *

# Load two audio files
y1, sr1 = librosa.load(defaultPath + 'input/test.mp3')
y2, sr2 = librosa.load(defaultPath + 'input/test.mp3')

# Extract MFCCs
mfcc1 = librosa.feature.mfcc(y=y1, sr=sr1, n_mfcc=13)
mfcc2 = librosa.feature.mfcc(y=y2, sr=sr2, n_mfcc=13)

# Compute similarity (e.g., Euclidean distance)
print(mfcc1)
distance = np.linalg.norm(mfcc1 - mfcc2)
print(f'Similarity score: {distance}')
