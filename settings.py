import torch
# ---- data path definitions ----

dataVerion = 'v2' # v0, v1, v2

norm_trainDataDir = f'D:/leveling/leveling_data/{dataVerion}/Normal/train/'
abnorm_trainDataDir = f'D:/leveling/leveling_data/{dataVerion}/Abnormal/train/'

norm_testDataDir = f'D:/leveling/leveling_data/{dataVerion}/Normal/test/'
abnorm_testDataDir = f'D:/leveling/leveling_data/{dataVerion}/Abnormal/test/'

autoencoderNormPath = 'D:/leveling/pytorch-AE/checkpoints/autoEncoderNorm.pth'
autoencoderAbnormPath = 'D:/leveling/pytorch-AE/checkpoints/autoEncoderAbnorm.pth'

cuda = torch.cuda.is_available()

# ---- training selection ----

architechture = 'LSTM'



# ---- data preparing ----

sampleRate = 128
sampleRate_origin = 8192

slidingWindow = True
stride = 80

channels = 3
startChannel = 1
timeStamps = 100

# ---- hyper parameters ----

epochs = 50
batchSize = 16

embeddingSize = 128

lr = 0.005
scheduler_stepSize = 10
scheduler_gamma = 0.7

# ---- LSTM parameters ----

dropout = 0.0
layers  = 1