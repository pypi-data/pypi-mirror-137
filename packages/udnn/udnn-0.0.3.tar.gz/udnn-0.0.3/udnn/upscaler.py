import h5py
import numpy as np
import torch as torch
import sys
from torch.utils.data import DataLoader

from .model import Model
from .utils import Interlace, DataLoaderUpscaler, Denormalize


def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()


def upscale(filename, in_dataset, model, name, out_dataset=None, size=128, H=None, W=None, sinograms=None,
            down_scale=40, scale=2, stride=1, sub_size=401, batch=10, workers=8, do_CI=True, gpu=True):
    if name[-3:] == '.h5':
        name = name[0:-3]

    if out_dataset is None:
        out_dataset = in_dataset

    if (H is None) or (W is None) or (sinograms is None):
        tmpFile = h5py.File(filename, 'r')
        shape = tmpFile[in_dataset].shape
        if H is None:
            H = shape[0]
        if W is None:
            W = shape[2]
        if sinograms is None:
            sinograms = np.arange(0, shape[1])
        tmpFile.close()

    num_sino = sinograms.size

    sub_output_size = int((sub_size - 1) * (scale / down_scale) + 1)

    f1 = h5py.File(('%s.h5' % name), 'w')
    upscaled = f1.create_dataset(out_dataset, (int((H - 1) * (scale / down_scale) + 1), num_sino, W), chunks=True)
    f2 = []
    cub = []
    if do_CI:
        f2 = h5py.File(('%s_ci.h5' % name), 'w')
        cub = f2.create_dataset(out_dataset, (int((H - 1) * (scale / down_scale) + 1), num_sino, W), chunks=True)

    net = Model(scale, size, init=False)
    if gpu:
        net.cuda()
        net = torch.nn.DataParallel(net)
    net.load_state_dict(torch.load(model))

    for k in range(0, num_sino):
        output = np.zeros((int((H - 1) * (scale / down_scale) + 1), W))
        output2 = np.zeros((int((H - 1) * (scale / down_scale) + 1), W))
        denominator = np.zeros((int((H - 1) * (scale / down_scale) + 1), W))
        plusOne = np.ones((sub_output_size, W))

        i = 0

        dataset = DataLoaderUpscaler(k, stride * down_scale, sub_size, down_scale, scale, W, filename, in_dataset,
                                     (H - sub_size) / (stride * down_scale) + 1, sinograms)
        datalod = DataLoader(dataset=dataset, batch_size=batch, num_workers=workers)

        for l, data in enumerate(datalod):
            X, CI, X2, avg, std = data
            avg = avg.float()
            std = std.float()

            if gpu:
                X = X.cuda()
                avg = avg.cuda()
                std = std.cuda()

            h_x = net(X)

            hyB = Denormalize(h_x, avg, std)

            for j in range(0, avg.shape[0]):
                hy = (hyB[j, :, :, :].cpu().detach().numpy()).reshape(hyB.shape[1] * hyB.shape[2], hyB.shape[3], order='F')
                x = X2[j, 0, :, :].detach().numpy()

                res = Interlace(x, hy, scale)
                output[i * stride * scale:i * stride * scale + sub_output_size, :] = output[i * stride * scale:i * stride * scale + sub_output_size, :] + res
                denominator[i * stride * scale:i * stride * scale + sub_output_size, :] = denominator[i * stride * scale:i * stride * scale + sub_output_size, :] + plusOne

                if do_CI:
                    ci = (CI[j, :, :, :].detach().numpy()).reshape(CI.shape[1] * CI.shape[2], CI.shape[3], order='F')
                    res2 = Interlace(x, ci, scale)
                    output2[i * stride * scale:i * stride * scale + sub_output_size, :] = output2[i * stride * scale:i * stride * scale + sub_output_size, :] + res2

                i += 1

        output = output / denominator
        upscaled[:, k, :] = output
        if do_CI:
            output2 = output2 / denominator
            cub[:, k, :] = output2
        progress(k, num_sino, status=' Upscaling')

    f1.close()
    if do_CI:
        f2.close()
    return

if __name__ == '__main__':

    upscale('../Diamond/tomo_p1_dark_flat_field_correction_2.h5', '/1-DarkFlatFieldCorrection-tomo/data', '../demo/Checkpoints/CP035.pt', 'test.h5',
            out_dataset=None, size=128, H=None, W=None, sinograms=np.arange(1,2160,10), down_scale=40, scale=2, stride=1, sub_size=401, batch=10, workers=8, do_CI=True, gpu=True)
