import numpy as np
import torch
from torch.utils.data import Dataset
import h5py
from PIL import Image
import torch.multiprocessing

def Denormalize(im, avg, std):
    result = torch.Tensor(im.shape)
    result = result.cuda()
    for itr in range(im.shape[0]):
        for channel in range(im.shape[1]):
            result[itr, channel, :, :] = (im[itr, channel, :, :] - 0.5) * (4 * std[itr]) + avg[itr]
    return result


class DataLoaderUpscaler(Dataset):

    def __init__(self, sino, stride, sub_size, down_scale, scale, W, filename, loc_dataset, size, sinOrder, normalize=True):
        super(DataLoaderUpscaler, self).__init__()
        self.down_scale = down_scale  # scale
        self.filename = filename
        self.loc_dataset = loc_dataset
        self.sino = sino
        self.stride = stride
        self.sub_size = sub_size
        self.W = W
        self.scale = scale
        self.size = int(size)
        self.sinOrder = sinOrder
        self.normalize = normalize

    @staticmethod
    def Normalize(im):
        N = im.size
        avg = im.sum() / N
        std = np.sqrt(np.power(im - avg, 2).sum() / (N - 1))
        result = (im - avg) / (4 * std)
        return result, avg, std

    def __getitem__(self, index):
        myFile = h5py.File(self.filename, 'r', libver='latest', swmr=True)
        data = myFile[self.loc_dataset][
               int(index * self.stride):int(index * self.stride + self.sub_size):(int(self.down_scale)),
               self.sinOrder[self.sino], 0:self.W]
        myFile.close()
        # d = data[0::self.scale, :]
        data2 = np.array(
            Image.fromarray(data).resize((self.W, int((self.sub_size - 1) * (self.scale / self.down_scale) + 1)),
                                      Image.BICUBIC))
        if self.normalize:
            d, avg, std = DataLoaderUpscaler.Normalize(data)
            d = d + 0.5
        else:
            d = data
            avg = 0.5
            std = 1/float(4)	
        X = torch.Tensor(1, d.shape[0], d.shape[1])
        X[0, :, :] = torch.from_numpy(d)
        X2 = torch.Tensor(1, data.shape[0], data.shape[1])
        X2[0, :, :] = torch.from_numpy(data)
        CI = torch.Tensor(int(self.scale - 1), int((self.sub_size - 1) * ((self.scale - 1) / self.down_scale)), self.W)
        c = 0
        for i in range(0, int((self.sub_size - 1) * (self.scale / self.down_scale) + 1)):
            if i % self.scale != 0:
                CI[int((i % self.scale) - 1), int(i // self.scale), :] = torch.from_numpy(data2[i, :])
        return X, CI, X2, avg, std

    def __len__(self):
        return self.size


class DataLoaderNoCI(Dataset):

    def __init__(self, partition, sino, stride, sub_size, down_scale, scale, W, filename, loc_dataset, sinoCount, rCI):
        super(DataLoaderNoCI, self).__init__()
        self.down_scale = down_scale  # scale
        self.filename = filename
        self.loc_dataset = loc_dataset
        self.partition = partition
        self.sino = sino
        self.stride = stride
        self.sub_size = sub_size
        self.W = W
        self.scale = scale
        self.sinoCount = sinoCount
        self.rCI = rCI

    @staticmethod
    def Normalize(im):
        N = im.size
        avg = im.sum() / N
        std = np.sqrt(np.power(im - avg, 2).sum() / (N - 1))
        result = (im - avg) / (4 * std)
        return result, avg, std

    def __getitem__(self, index):
        myFile = h5py.File(self.filename, 'r', libver='latest', swmr=True)
        data = myFile[self.loc_dataset][int((self.partition[self.sino[index]]) * self.stride):int(
            (self.partition[self.sino[index]]) * self.stride + self.sub_size):(int(self.down_scale / self.scale)),
               self.sinoCount[self.sino[index]], 0:self.W]
        myFile.close()
        d = data[0::self.scale, :]
        if self.rCI:
            data2 = np.array(
                Image.fromarray(d).resize((self.W, int((self.sub_size - 1) * (self.scale / self.down_scale) + 1)),
                                          Image.BICUBIC))
        d, avg, std = DataLoaderNoCI.Normalize(d)
        d = d + 0.5
        X = torch.Tensor(1, d.shape[0], d.shape[1])
        X[0, :, :] = torch.from_numpy(d)
        Y = torch.Tensor(int(self.scale - 1), int((self.sub_size - 1) / self.down_scale), self.W)
        if not self.rCI:
            for i in range(0, int((self.sub_size - 1) * (self.scale / self.down_scale) + 1)):
                if i % self.scale != 0:
                    Y[int((i % self.scale) - 1), int(i // self.scale), :] = torch.from_numpy(data[i, :])
            return X, Y, avg, std
        else:
            CI = torch.Tensor(int(self.scale - 1), int((self.sub_size - 1) / self.down_scale), self.W)
            for i in range(0, int((self.sub_size - 1) * (self.scale / self.down_scale) + 1)):
                if i % self.scale != 0:
                    Y[int((i % self.scale) - 1), int(i // self.scale), :] = torch.from_numpy(data[i, :])
                    CI[int((i % self.scale) - 1), int(i // self.scale), :] = torch.from_numpy(data2[i, :])
            return X, CI, Y, avg, std

    def __len__(self):
        return self.partition.shape[0]
