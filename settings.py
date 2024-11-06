import torch
from datetime import datetime

# ---- training selection ----

architechture = 'CNN1D'

# ---- data path definitions ----

dataVerion = 'v3' # v0, v1, v2, v3

norm_sourceDir = f'D:/leveling/leveling_data/{dataVerion}/source/Normal'
abnorm_sourceDir = f'D:/leveling/leveling_data/{dataVerion}/source/Abnormal'

norm_trainDataDir = f'D:/leveling/leveling_data/{dataVerion}/Normal/train/'
abnorm_trainDataDir = f'D:/leveling/leveling_data/{dataVerion}/Abnormal/train/'

norm_testDataDir = f'D:/leveling/leveling_data/{dataVerion}/Normal/test/'
abnorm_testDataDir = f'D:/leveling/leveling_data/{dataVerion}/Abnormal/test/'

current_date = datetime.now().strftime("%y%m%d")
autoencoderNormPath = f'D:/leveling/pytorch-AE/checkpoints/aeNorm_{dataVerion}_{architechture}_{current_date}.pth'
autoencoderAbnormPath = f'D:/leveling/pytorch-AE/checkpoints/aeAbnorm_{dataVerion}_{architechture}_{current_date}.pth'

autoencoderNormPath = f'D:/leveling/pytorch-AE/checkpoints/aeNorm_{dataVerion}_{architechture}_241031.pth'
autoencoderAbnormPath = f'D:/leveling/pytorch-AE/checkpoints/aeAbnorm_{dataVerion}_{architechture}_241031.pth'

cuda = torch.cuda.is_available()

testFileNum = 50

# ---- data preparing ----

sampleRate = 128
sampleRate_origin = 8192

slidingWindow_aeNorm = False    # if true, the window size will be timeStamps, 
slidingWindow_aeAbnorm = False   # if true, the window size will be timeStamps, 
stride = 128             # looping through the data with sampleRate

startChannel = 1    # amp, door-x, door-y, door-z, car-x, car-y, car-z 
channels = 3        # amp, door-x, door-y, door-z, car-x, car-y, car-z 
timeStamps = 256

# ---- hyper parameters ----

epochs = 50
batchSize_aeNorm = 32
batchSize_aeAbnorm = 4

embeddingSize = 128

lr = 0.001
scheduler_stepSize = 6
scheduler_gamma = 0.88

# ---- CNN1D parameters ----

decoderShapeBias = timeStamps - 1 

# ---- LSTM parameters ----

dropout = 0.0
layers  = 1