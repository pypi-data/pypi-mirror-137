import numpy
from numpy import cov
from numpy import trace
from numpy import iscomplexobj
from numpy.random import random
from scipy.linalg import sqrtm

def calculate_fd(act1, act2):
    '''
    Function to calculate the FD given the embeddings.
    
    Parameters:
        act1: features of image distrubution 1
        act2: features of image distrubution 2
    
    Returns:
        score: Computed FD score 
    '''
    mu1, sigma1 = act1.mean(axis=0), cov(act1, rowvar=False)
    mu2, sigma2 = act2.mean(axis=0), cov(act2, rowvar=False)

    ssdiff = numpy.sum((mu1 - mu2)**2.0)
    covmean = sqrtm(sigma1.dot(sigma2))

    if iscomplexobj(covmean):
        covmean = covmean.real

    score = ssdiff + trace(sigma1 + sigma2 - 2.0 * covmean)
    return score

a1 = random(2*2048).reshape((2,2048))
fd = calculate_fd(a1, a1)
feat_model = "torchxrayvision"

import shutil
import os
import argparse
import pickle
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from multiprocessing import cpu_count
import torch
from torch import nn
from torch.autograd import Variable
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torch.nn.functional import adaptive_avg_pool2d
import numpy as np
import random
from PIL import Image, ImageFile
from scipy import linalg
import skimage, skimage.io
from skimage import io, transform
from skimage.color import rgb2gray
import matplotlib.pyplot as plt

import torchxrayvision as xrv
from torchxrayvision.models import *
from torchxrayvision.datasets import *
import torchvision.transforms as transforms
import torchvision.datasets as dset
import torchvision.models as models
from sklearn.cluster import KMeans

import numpy
from numpy import cov
from numpy import trace
from numpy import iscomplexobj
from numpy.random import random
from scipy.linalg import sqrtm
import warnings

warnings.filterwarnings("ignore")
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(x):
        return x

from pytorch_fid.inception import InceptionV3

def mkdir(fname):
    try:
        os.makedirs(fname)
    except OSError:
        pass
    
import math
import os
import timeit
import math

import numpy as np
import ot
import torch
from torch import nn
import torch.nn.functional as F
import torchvision.datasets as dset
import torchvision.transforms as transforms
import torchvision.utils as vutils
from torch.autograd import Variable
import torchvision.models as models
import pdb
from tqdm import tqdm

from numpy.linalg import norm
from scipy import linalg


def distance(X, Y, sqrt=False):
    nX = X.size(0)
    nY = Y.size(0)
    X = X.view(nX,-1).cuda()
    X2 = (X*X).sum(1).resize_(nX,1)
    Y = Y.view(nY,-1).cuda()
    Y2 = (Y*Y).sum(1).resize_(nY,1)

    M = torch.zeros(nX, nY)
    M.copy_(X2.expand(nX,nY) + Y2.expand(nY,nX).transpose(0,1) - 2*torch.mm(X,Y.transpose(0,1)))

    del X, X2, Y, Y2
    
    if sqrt:
        M = ((M+M.abs())/2).sqrt()
    
    return M


def wasserstein(M, sqrt):
    if sqrt:
        M = M.abs().sqrt()
    emd = ot.emd2([],[],M.numpy())
    
    return emd

class Score_knn:
    acc = 0
    acc_real = 0
    acc_fake = 0
    precision = 0
    recall = 0
    tp = 0
    fp = 0
    fn = 0
    ft = 0

def knn(Mxx, Mxy, Myy, k, sqrt):
    n0 = Mxx.size(0)
    n1 = Myy.size(0)
    label = torch.cat((torch.ones(n0),torch.zeros(n1)))
    M = torch.cat((torch.cat((Mxx,Mxy),1), torch.cat((Mxy.transpose(0,1),Myy), 1)), 0)
    if sqrt:
        M = M.abs().sqrt()
    INFINITY = float('inf')
    val, idx = (M+torch.diag(INFINITY*torch.ones(n0+n1))).topk(k, 0, False)

    count = torch.zeros(n0+n1)
    for i in range(0,k):
        count = count + label.index_select(0,idx[i])
    pred = torch.ge(count, (float(k)/2)*torch.ones(n0+n1)).float()

    s = Score_knn()
    s.tp = (pred*label).sum()
    s.fp = (pred*(1-label)).sum()
    s.fn = ((1-pred)*label).sum()
    s.tn = ((1-pred)*(1-label)).sum()
    
    s.precision = s.tp/(s.tp+s.fp)
    s.recall = s.tp/(s.tp+s.fn)
    
    s.acc_t = s.tp/(s.tp+s.fn)
    s.acc_f = s.tn/(s.tn+s.fp)
    s.acc = torch.eq(label, pred).float().mean()
    s.k = k 

    return s

def mmd(Mxx, Mxy, Myy, sigma) :
    scale = Mxx.mean()
    val = scale*2*sigma*sigma
    Mxx = torch.exp(-Mxx/val)
    Mxy = torch.exp(-Mxy/val)
    Myy = torch.exp(-Myy/val)
    a = Mxx.mean()+Myy.mean()-2*Mxy.mean()
    mmd = math.sqrt(max(a, 0))

    return mmd

class Score:
    emd = 0
    mmd = 0
    knn = None
    
    def printScore(self):
        print("\tEMD:",self.emd)
        print("\tMMD:",self.mmd)
        print("\tPrecision:",self.knn.precision.numpy())
        print("\tRecall:",self.knn.recall.numpy())
        print("\tAcc_t:",self.knn.acc_t.numpy())
        print("\tAcc_f:",self.knn.acc_f.numpy())
        

def compute_other(real, fake, k=1, sigma=1, sqrt=True):
    '''
    Function to compute other metric scores like Wasserstein, MMD and KNN.
    
    Returns:
        s: Score object containing computed scores
        
    '''
    Mxx = distance(real, real)
    Mxy = distance(real, fake)
    Myy = distance(fake, fake)

    s = Score()
    s.emd = wasserstein(Mxy, sqrt)
    s.mmd = mmd(Mxx, Mxy, Myy, sigma)
    s.knn = knn(Mxx, Mxy, Myy, k, sqrt)
    
    return s

    
def compute_stat(dataloader, sampsize, device):
    '''
    Function to compute image features using InceptionV3 model.
    
    Returns:
        pred_arr: Image Iv3 features
    '''
    dims = 2048
    
    block_idx = InceptionV3.BLOCK_INDEX_BY_DIM[dims]
    model = InceptionV3([block_idx]).to(device)
        
    pred_arr = np.empty((sampsize, dims))
    model.eval()
    start_idx = 0
    
    for batch in dataloader:
        batch = batch.to(device)
    
        with torch.no_grad():
            pred = model(batch)[0]   
            
        if pred.size(2) != 1 or pred.size(3) != 1:
            pred = adaptive_avg_pool2d(pred, output_size=(1, 1))

        pred = pred.squeeze(3).squeeze(2).cpu().numpy()
        pred_arr[start_idx:start_idx + pred.shape[0]] = pred
        start_idx = start_idx + pred.shape[0]
    
    return pred_arr

def compute_statxrv(dataloader, sampsize, device):
    '''
    Function to compute image features using Torchxrayvision model.

    Returns:
        pred_arr: Image XRV features
    '''
    start_idx = 0
    pred_arr = np.empty((sampsize, 1024))

    model = DenseNet(weights="all")

    for batch in dataloader:
        batch = batch.to(device)
        model = model.to(device)
        with torch.no_grad():
            pred = model.features2(batch)
            
        pred = pred.detach().cpu().numpy()

        pred_arr[start_idx:start_idx + pred.shape[0]] = pred
        start_idx = start_idx + pred.shape[0]
        
    return pred_arr

def standardizer(img, maxval):
    '''
    Function to standardize the image vectors.
    
    Parameters:
        img: Image 
        maxval: maximum value bound
    
    Returns:
        img: standardized image vectors
    '''
    global feat_model
    
    if img.max() > maxval:
        raise Exception("max image value ({}) higher than expected bound ({}).".format(img.max(), maxval))
  
    if img.max() <= 1:
        img = img*maxval
        
    if feat_model == "torchxrayvision":
            img = (2 * (img.astype(np.float32) / maxval) - 1.) * 1024

    img = img[None, :, :] 

    return img

def process_image(img_path, trans):
    '''
    Function to process the images.
    
    Parameters:
        img_path: Path to images
        trans: the transformation required - None | rotate | shift
    
    Returns:
        img: processed image vectors
    '''
    img = rgb2gray(skimage.io.imread(img_path, plugin="matplotlib"))
    img = standardizer(img, 255)   
    
    size = 224

    if trans == None:
        transform = torchvision.transforms.Compose([XRayCenterCrop(), XRayResizer(size)])
        img = transform(img)
        
    elif trans == "rotate":
        img = img.astype(np.float32)
        transform = transforms.Compose([transforms.ToPILImage(), transforms.Scale(
        size), transforms.RandomRotation(15), transforms.CenterCrop(size)])
        img = img[0][:, :, None]
        img = transform(img)
        img = np.array([np.array(img)])
        
    elif trans == "shift":
        img = img.astype(np.float32)
        transform = transforms.Compose([transforms.ToPILImage(), transforms.Scale(size), transforms.Pad(4), transforms.RandomCrop(size)])
        img = img[0][:, :, None]
        img = transform(img)
        img = np.array([np.array(img)])
    
    global feat_model
    if feat_model == "inceptionV3":
        img = np.asarray([img[0], img[0], img[0]])
            
    return img

class XRAYDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        
        self.img_data_array = []
    
        for dir1 in os.listdir(root_dir):
            for file in os.listdir(os.path.join(root_dir,dir1)):
                image_path = os.path.join(root_dir, dir1, file)
                self.img_data_array.append(image_path)

    def __len__(self):
        return len(self.img_data_array)

    def __getitem__(self, idx):
        image_path = self.img_data_array[idx]

        img = process_image(image_path, self.transform)

        return img
    
def getFeat(img_dir, workers, batchSize, device):
    '''
    Function to get the features from the images.
    
    Parameters:
        img_dir: Path to image directory
        workers: Number of workers required
        batchSize: Batch size during featurization
        device: torch.device("cuda" if cuda else "cpu")
    
    Returns:
        act: image features
    
    '''
    global feat_model

    if feat_model == "inceptionV3":
        dataset = XRAYDataset(root_dir=img_dir, transform=None)

        dataloader = torch.utils.data.DataLoader(
            dataset, batch_size=batchSize, shuffle=True, drop_last=False, num_workers=workers)

        act = compute_stat(dataloader, len(dataset), device)

    elif feat_model == "torchxrayvision":
        dataset = XRAYDataset(root_dir=img_dir, transform=None)
        
        dataloader = DataLoader(dataset, batch_size=batchSize,
                        shuffle=True, num_workers=workers, drop_last=False)
        
        act = compute_statxrv(dataloader, len(dataset), device)

    return act

def compute_score(dataroot, metric="fxd", workers=4, batchSize=64, other=False, cuda=False):
    '''
    Function to compute the selected evaluation metric score(s).
    
    Parameters:
        dataroot: Path to folder containing both image directories - real and generated
        metric: Possible options - fxd | fid 
        workers: Number of workers required
        batchSize: Batch size during featurization
        other: True => compute other popular metric scores
        cuda: Setting cuda=True to utilize GPU
    
    Returns:
        score: Returns the computed metric score(s)
               if other=True:
                   score[0] => FD
                   score[1] => other scores
        
    '''
    if torch.cuda.is_available() and not cuda:
        print("WARNING: CUDA device detected, try using --cuda")

    device = torch.device("cuda" if cuda else "cpu")
    
    global feat_model
    if metric == "fxd":
        feat_model = "torchxrayvision"
    elif metric == "fid":
        feat_model = "inceptionV3"
    else:
        print("Invalid metric")
        exit()

#     cmd1 = "/scratch/chexdata/allclasses/chex/"+"real"
#     cmd2 = "/scratch/chexdata/allclasses/chex/"+"fake"

    cmd1 = dataroot + "real"
    cmd2 = dataroot + "fake"

    ac1 = getFeat(cmd1, workers, batchSize, device)
    ac2 = getFeat(cmd2, workers, batchSize, device)

    score = calculate_fd(ac1, ac2)
    if other:
        other_scores = compute_other(torch.from_numpy(ac2), torch.from_numpy(ac1))
        return [score, other_scores]
    
    return score
    
def main():
    a1 = random(2*2048).reshape((2,2048))
    fd = calculate_fd(a1, a1)

    parser = argparse.ArgumentParser()
    parser.add_argument('--metric', help='evaluation metric', default='fxd')
    parser.add_argument('--dataroot', required=True, help='path to folder containing real and generated images')
    parser.add_argument('--workers', type=int, help='number of data loading workers', default=4)
    parser.add_argument('--batchSize', type=int, default=64, help='input batch size')
    parser.add_argument('--cuda', action='store_true', help='enables cuda')
    parser.add_argument('--all', action='store_true', help='computes few other popular metrics')

    opt = parser.parse_args()
    print(opt.__dict__)
    
    result = compute_score(opt.dataroot, opt.metric, opt.workers, opt.batchSize, opt.all, opt.cuda)
    
    if opt.all:
        print("\t-------------------------")
        print("\tEvaluation Scores")
        print("\t-------------------------")
        print("\t",opt.metric,": ", result[0])
        result[1].printScore()
    else:
        print("\t-------------------------")
        print("\tEvaluation Score")
        print("\t-------------------------")
        print("\t",opt.metric,": ", result)
    
if __name__ == "__main__":
    main()
    