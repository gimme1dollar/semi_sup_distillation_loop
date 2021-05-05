from typing import Union, Optional, List, Tuple, Text, BinaryIO
from torchvision.utils import make_grid
import numpy as np
import cv2
import torch
from PIL import Image
import torch.nn.functional as F
import wandb

def renormalize_float(vector, range_t : tuple):

    row = torch.Tensor(vector)
    r = torch.max(row) - torch.min(row)
    row_0_to_1 = (row - torch.min(row)) / r
    r2 = range_t[1] - range_t[0]
    row_normed = (row_0_to_1 * r2) + range_t[0]

    return row_normed.numpy()

def un_normalize(img, mean, std):
    for t, m, s in zip(img, mean, std):
        t.mul_(s).add_(m)
    return img

def visualize_rescale_image(mean, std, image, tag): # vis image itself with mean train
    # features : B x C x H x W
    origin_image = image
    for batch_idx in range(image.shape[0]):
        image = origin_image[batch_idx].detach().cpu()
        X = un_normalize(image, mean, std)
        X = image.numpy().squeeze()

        # Normalised [0,255] as integer: don't forget the parenthesis before astype(int)
        original_image = (255*(X - np.min(X))/np.ptp(X)).astype(np.uint8)

        #print("original image shape : ", original_image.shape)
        wandb.log({str(tag)+"_"+str(batch_idx) : [wandb.Image(np.transpose(original_image, (1,2,0)))]})
