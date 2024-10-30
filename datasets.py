import torch
from torchvision import datasets, transforms
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from torch.utils.data import DataLoader, TensorDataset, random_split
import matplotlib.pyplot as plt
from pathlib import Path
from tqdm import tqdm
from math import floor

from settings import channels, startChannel, timeStamps, batchSize_aeNorm, batchSize_aeAbnorm
from settings import dataVerion, sampleRate, sampleRate_origin
from settings import slidingWindow_aeNorm, slidingWindow_aeAbnorm, stride

class Vibration(object):
    def __init__(self, dir, normalVersion = True, trainDataRatio = 0.85, displayData = False, test = False):
        # read files from a dir, each file represent a sample 
        directory = Path(dir)

        files = [f for f in directory.iterdir() if f.is_file() and f.name != '.DS_Store' ]
        numFiles = len(files)
        # list of samples
        dataList = None
        
        # each file is a stage3 to stage5
        print(f'load csvs in {dir}...')
        for file in tqdm(files):
            path = dir + file.name 
            df = pd.read_csv(path)

            if dataVerion == 'v1': # data v1 sample rate is fixed 16, so we just make it to fit timestampt we set
                data = df.iloc[:, startChannel: startChannel + channels].values

            else: # data v2 sample rate is 8192, so we down sample to our desired sample rate first
                downSampleFactor = sampleRate_origin // sampleRate
                data = df.iloc[::downSampleFactor, startChannel: startChannel + channels].values

            # normalization
            slidingWindow = slidingWindow_aeNorm if normalVersion else slidingWindow_aeAbnorm
            data = self.normalization(data).transpose(1,0) if not slidingWindow else self.normalization(data)

            # visualize or not
            if displayData:
                dataToList = list(data)
                for d in range(startChannel, startChannel + channels):
                    self.displayData(dataToList[d - startChannel], d)

            # if not slidingWindow, a file is a sample(with interploition to desired timeStamps) or a file will make many samples.
            if slidingWindow:
                data = self.slidingWindow(data, timeStamps, stride).transpose(0,2,1)
            else:
                data = self.interpolation(data, timeStamps)
                data = np.expand_dims(data, axis=0)

            dataList = np.concatenate((dataList, data), axis=0) if dataList is not None else data

        dataTensor = torch.tensor(
            dataList, 
            dtype = torch.float32)  

        # testData here is for validation dataset, or in test mode testData is for test dataset
        numSamples = dataTensor.shape[0]

        trainSize = int(trainDataRatio * numSamples) if not test else 0

        trainData, testData = dataTensor[:trainSize], dataTensor[trainSize:]
        
        batchSize = batchSize_aeNorm if normalVersion else batchSize_aeAbnorm
        bs = batchSize if not test else floor(numSamples / numFiles) if slidingWindow else 1
        
        if not test:
            self.train_loader = DataLoader(TensorDataset(trainData), batch_size=bs, shuffle=False)
        self.test_loader = DataLoader(TensorDataset(testData), batch_size=bs, shuffle=False)
        
        print('trainData shape:', trainData.shape, 'testData shape:', testData.shape)
        
    def displayData(self, data, channelID):
        plt.figure(figsize=(10, 6))
        plt.plot(data, label=f'normalized Data with your specified sample rate (channel-{channelID})')
        plt.title(f'channel-{channelID}')
        plt.show()

    def slidingWindow(self, data, sampleLength, stride):
        numWindows = (data.shape[0] - sampleLength) // stride + 1 
        windows = np.array([data[i:i + sampleLength] for i in range(0, numWindows * stride, stride)])
        return windows 
    
    def interpolation(self, data, newDim):
        # data is now shape (channels, timestamp)
        channels, timestamps = data.shape
        x_old = np.linspace(0, 1, timestamps)
        x_new = np.linspace(0, 1, newDim)
        
        # Interpolate for each channel
        interpolated_data = np.zeros((channels, newDim))
        for i in range(channels):
            interpolated_data[i] = np.interp(x_new, x_old, data[i])
    
        return interpolated_data
    
    def normalization(self, data):
        scaler = MinMaxScaler()
        normalized = scaler.fit_transform(data)
        return normalized
    
    def getFlatStart(self, data):
        flat_threshold = 0.01
        window_size = 5

        for i in range(0, data.shape[0], window_size):
            if np.std(data[i: i+window_size]) < flat_threshold:
                return i+window_size*2
        return None
    
# test = Vibration(dir = 'D:/leveling/leveling_data/v2/Normal/train/', displayData=False)


