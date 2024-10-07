import argparse, os, sys
import numpy as np
import imageio
from scipy import ndimage

from defi import channels, norm_trainDataDir, abnorm_trainDataDir, autoencoderNormPath, autoencoderAbnormPath

import torch
from torchvision.utils import save_image

# from models.VAE import VAE
from models.AE import AE

from utils import get_interpolations

parser = argparse.ArgumentParser(
        description='Main function to call training for different AutoEncoders')
parser.add_argument('--batch-size', type=int, default=128, metavar='N',
                    help='input batch size for training (default: 128)')
parser.add_argument('--epochs', type=int, default=100, metavar='N',
                    help='number of epochs to train (default: 10)')
parser.add_argument('--no-cuda', action='store_true', default=False,
                    help='enables CUDA training')
parser.add_argument('--seed', type=int, default=42, metavar='S',
                    help='random seed (default: 1)')
parser.add_argument('--log-interval', type=int, default=10, metavar='N',
                    help='how many batches to wait before logging training status')
parser.add_argument('--embedding-size', type=int, default=32, metavar='N',
                    help='how many batches to wait before logging training status')
parser.add_argument('--results_path', type=str, default='results/', metavar='N',
                    help='Where to store images')
parser.add_argument('--model', type=str, default='AE', metavar='N',
                    help='Which architecture to use')
parser.add_argument('--dataset', type=str, default='Vibration', metavar='N',
                    help='Which dataset to use')

args = parser.parse_args()
args.cuda = not args.no_cuda and torch.cuda.is_available()
torch.manual_seed(args.seed)

normalPar = (norm_trainDataDir, autoencoderNormPath)
abnormalPar = (abnorm_trainDataDir, autoencoderAbnormPath)

print(args.model)
if __name__ == "__main__":
    try:
        os.stat(args.results_path)
    except :
        os.mkdir(args.results_path)

    try:
        parameters = abnormalPar
        
        ae = AE(args, parameters[0])
        for epoch in range(1, args.epochs + 1):
            ae.train(epoch)
            ae.validate()
            
        ae.printLossResult()
        ae.saveModel(parameters[1])
    except (KeyboardInterrupt, SystemExit):
        print("Manual Interruption")