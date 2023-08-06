import numpy as np
import torch as torch
import torch.nn as nn
import torch.optim as optim
import sys
import os
import math
from torch.utils.data import DataLoader
import h5py
from .model import Model
from .utils import Timer, Logger, DataLoaderNoCI, Denormalize
torch.backends.cudnn.deterministic = True


def train(train_filename, train_dataset, name, output_folder=None, validation_filename=None,
          validation_dataset=None, size=128, H=None, W=None, train_sinograms=None,
          validation_sinograms=None, down_scale=40, scale=2, stride=1, sub_size=401,
          batch=10, workers=8, num_val_patches=10, stop=60, valfreq=16, display=False, gpu=True):

    if output_folder is None:
        root = name
    else:
        if output_folder[-1] == '/':
            output_folder = output_folder[0:len(output_folder)-1]
        root = output_folder+'/'+name
    if not os.path.isdir(root):
        os.makedirs(root)
    cp_dir = root+'/'+'Checkpoints'
    if not os.path.isdir(cp_dir):
        os.makedirs(cp_dir)

    if validation_filename is None:
        validation_filename = train_filename

    if validation_dataset is None:
        validation_dataset = train_dataset

    if (H is None) or (W is None) or (train_sinograms is None) or (validation_sinograms is None):
        tmpFile = h5py.File(train_filename, 'r')
        shape = tmpFile[train_dataset].shape
        if H is None:
            H = shape[0]
        if W is None:
            W = shape[2]
        if train_sinograms is None:
            train_sinograms = np.arange(0, shape[1], 2)
        if validation_sinograms is None:
            validation_sinograms = np.arange(0, shape[1], 2)
        tmpFile.close()

    num_train_sino = train_sinograms.size
    num_valid_sino = validation_sinograms.size

    torch.manual_seed(1993)
    torch.cuda.manual_seed_all(1993)
    np.random.seed(1993)

    trainIndeces = torch.Tensor(int(((H - sub_size) / stride) + 1), num_train_sino)
    evalIndeces = torch.Tensor(num_val_patches, num_valid_sino)
    testIndeces = torch.Tensor(int(((H - sub_size) / stride) + 1) - num_val_patches, num_valid_sino)

    for i in range(0, num_train_sino):
        trainIndeces[:, i] = torch.randperm(int(((H - sub_size) / stride) + 1))

    for i in range(0, num_valid_sino):
        temp = torch.randperm(int(((H - sub_size) / stride) + 1))
        evalIndeces[:, i] = temp[0:num_val_patches]
        testIndeces[:, i] = temp[num_val_patches:int(((H - sub_size) / stride) + 1)]

    net = Model(scale, size, init=True)
    criterion = nn.MSELoss()
    criterionCI = nn.MSELoss()

    if gpu:
        criterion = criterion.cuda()
        criterionCI = criterionCI.cuda()
        net = net.cuda()
        net = nn.DataParallel(net)

    nev = 1

    learningRate12 = 0.001
    learningRate3 = 0.0001
    learningDecay = 0.1

    if gpu:
        optimizer = optim.Adam([{'params': net.module.conv1.parameters()}, {'params': net.module.conv2.parameters()},
                                {'params': net.module.conv3.parameters(), 'lr': learningRate3}], lr=learningRate12)
    else:
        optimizer = optim.Adam([{'params': net.conv1.parameters()}, {'params': net.conv2.parameters()},
                                {'params': net.conv3.parameters(), 'lr': learningRate3}], lr=learningRate12)
    hist = Logger(root+'/history', 'w')
    evall = Logger(root+'/evaluations', 'w')

    evall.setNames(('Backpropagations', 'MSE', 'MSE_CI', 'Learing_Rate_A', 'Learing_Rate_B', 'Time'))
    hist.setNames(('Epoch', 'MSE', 'MSE_CI', 'Learing_Rate_A', 'Learing_Rate_B', 'Time'))

    backpropagations = 1

    totalepoches = (((H - sub_size) / stride) + 1) * math.ceil(num_train_sino / batch)

    timer = Timer()

    error = 0
    CI = 0
    errorCI = 0
    totalError = 0
    totalErrorCI = 0

    presentMSE = 0
    previousMSE = 0

    i = 0
    totalCItrain = 0
    totalCIval = 0

    while i < (((H - sub_size) / stride) + 1) and nev <= stop:

        sinOrder = torch.randperm(num_train_sino)

        if i % valfreq == 0:
            sys.stdout.write('\n')
            sys.stdout.write('Training')
            sys.stdout.write('\n\n')
            disflagTrain = True
            net.train()

        dataset = DataLoaderNoCI(trainIndeces[i, :], sinOrder, stride, sub_size, down_scale, scale, W, train_filename, train_dataset, train_sinograms, nev == 1)
        datalod = DataLoader(dataset=dataset, batch_size=batch, num_workers=workers)

        for j, data in enumerate(datalod):

            if nev == 1:
                X, CI, Y, avg, std = data
                avg = avg.float()
                std = std.float()
                if gpu:
                    X = X.cuda()
                    Y = Y.cuda()
                    CI = CI.cuda()
                    avg = avg.cuda()
                    std = std.cuda()
            else:
                X, Y, avg, std = data
                avg = avg.float()
                std = std.float()
                if gpu:
                    X = X.cuda()
                    Y = Y.cuda()
                    avg = avg.cuda()
                    std = std.cuda()

            optimizer.zero_grad()

            h_x = net(X)

            h_x = Denormalize(h_x, avg, std)
            loss = criterion(h_x, Y)
            loss.backward()
            optimizer.step()

            intrm = loss.cpu()
            error = float(intrm.detach().numpy())
            totalError += error * avg.shape[0]

            if nev == 1:
                lossCI = criterionCI(CI, Y)
                intrm = lossCI.cpu()
                errorCI = float(intrm.detach().numpy())
                totalErrorCI += errorCI * avg.shape[0]

            if display:
                if disflagTrain:
                    sys.stdout.write(("Epoch: %d/%d,  " % (backpropagations, totalepoches)) + ' MSE: ' + (' %1.8f ' % error) + ' MSE_CI: ' + (' %1.8f ' % errorCI))
                    disflagTrain = False
                else:
                    sys.stdout.write('\r')
                    sys.stdout.write(("Epoch: %d/%d,  " % (backpropagations, totalepoches)) + ' MSE: ' + (' %1.8f ' % error) + ' MSE_CI: ' + (' %1.8f ' % errorCI))
                sys.stdout.flush()

            backpropagations += 1

        # Evaluation

        if i % valfreq == (valfreq - 1):

            totalError = totalError / (num_train_sino * valfreq)
            if nev == 1:
                totalCItrain = totalErrorCI / (num_train_sino * valfreq)
            totalErrorCI = totalCItrain

            time = timer.get_value()

            hist.add((nev, totalError, totalErrorCI, learningRate12, learningRate3, time))

            totalError = 0
            totalErrorCI = totalCIval

            sys.stdout.write('\n\n')
            sys.stdout.write('Evaluation')
            sys.stdout.write('\n\n')
            disflagEval = True
            net.eval()
            for k in range(0, num_val_patches):
                evalSinOrder = torch.randperm(num_valid_sino)
                dataset = DataLoaderNoCI(evalIndeces[k, :], evalSinOrder, stride, sub_size, down_scale, scale, W, validation_filename, validation_dataset, validation_sinograms, nev == 1)
                datalod = DataLoader(dataset=dataset, batch_size=batch, num_workers=workers)
                for l, data in enumerate(datalod):

                    if nev == 1:
                        X, CI, Y, avg, std = data
                        avg = avg.float()
                        std = std.float()
                        if gpu:
                            X = X.cuda()
                            Y = Y.cuda()
                            CI = CI.cuda()
                            avg = avg.cuda()
                            std = std.cuda()
                    else:
                        X, Y, avg, std = data
                        avg = avg.float()
                        std = std.float()
                        if gpu:
                            X = X.cuda()
                            Y = Y.cuda()
                            avg = avg.cuda()
                            std = std.cuda()

                    net.zero_grad()

                    h_x = net(X)

                    h_x = Denormalize(h_x, avg, std)
                    loss = criterion(h_x, Y)
                    intrm = loss.cpu()
                    error = float(intrm.detach().numpy())
                    totalError += error * avg.shape[0]

                    if nev == 1:
                        lossCI = criterionCI(CI, Y)
                        intrm = lossCI.cpu()
                        errorCI = float(intrm.detach().numpy())
                        totalErrorCI += errorCI * avg.shape[0]

                    if display:
                        if disflagEval:
                            sys.stdout.write(("Epoch: %d/%d,  " % ((l + 1) + k * math.ceil(num_valid_sino / batch), num_val_patches * math.ceil(num_valid_sino / batch))) + ' MSE: ' + (' %1.8f ' % error) + ' MSE_CI: ' + (' %1.8f ' % errorCI))
                            disflagEval = False
                        else:
                            sys.stdout.write('\r')
                            sys.stdout.write(("Epoch: %d/%d,  " % ((l + 1) + k * math.ceil(num_valid_sino / batch), num_val_patches * math.ceil(num_valid_sino / batch))) + ' MSE: ' + (' %1.8f ' % error) + ' MSE_CI: ' + (' %1.8f ' % errorCI))
                        sys.stdout.flush()

            totalError = totalError / (num_valid_sino * num_val_patches)
            if nev == 1:
                totalCIval = totalErrorCI / (num_valid_sino * num_val_patches)
            totalErrorCI = totalCIval

            print('\n')

            print('Model Saved with Error:' + (' %1.8f ' % totalError) + 'and MSE_CI:' + (' %1.8f \n' % totalErrorCI))
            time = timer.get_value()
            evall.add((backpropagations, totalError, totalErrorCI, learningRate12, learningRate3, time))
            torch.save(net.state_dict(), cp_dir+('/CP%03d.pt' % nev))

            if nev == 1:
                presentMSE = totalError
            else:
                previousMSE = presentMSE
                presentMSE = totalError
            if nev != 1 and (previousMSE - presentMSE) < 0:
                print('Changing Learing Rates by 0.1\n')
                learningRate12 = learningRate12 * learningDecay
                learningRate3 = learningRate3 * learningDecay
                for r in range(0, 2):
                    optimizer.param_groups[r]['lr'] = learningRate12
                for r in range(2, 3):
                    optimizer.param_groups[r]['lr'] = learningRate3

            nev += 1
            totalError = 0

        i += 1

    minMSE = min(evall.symbols[evall.idx['MSE']])
    maxModel = 1
    for m in range(0, len(evall.symbols[evall.idx['MSE']])):
        if evall.symbols[evall.idx['MSE']][m] == minMSE:
            maxModel = m + 1
    return maxModel

if __name__ == '__main__':

    model = train('../Diamond/tomo_p1_dark_flat_field_correction.h5', '/1-DarkFlatFieldCorrection-tomo/data', 'demo', output_folder='..', validation_filename=None,
                  validation_dataset=None, size=128, H=None, W=None, train_sinograms=np.arange(1,2159,2),
                  validation_sinograms=np.arange(2,2159,2), down_scale=40, scale=2, stride=1, sub_size=401,
                  batch=10, workers=8, num_val_patches=10, stop=60, valfreq=16, display=True, gpu=True)
    print(model)
