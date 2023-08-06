import torch
import numpy as np

def Interlace(inp,intermediate,scale):

    if (inp.shape[1]!=intermediate.shape[1]):

        print('Wrong Dimensions')
        return 0

    else:

        if repr(type(inp[8:8+5])) == 'torch':
            output=torch.Tensor(inp.shape[0]+intermediate.shape[0],inp.shape[1])
        else:
            output=np.zeros((inp.shape[0]+intermediate.shape[0],inp.shape[1]))

        for i in range(0,inp.shape[0]-1):

            output[int(i*scale),:]=inp[i,:]
            output[int(i*scale+1):int((i+1)*scale),:]=intermediate[int(i*(scale-1)):int((i+1)*(scale-1)),:]

        output[-1,:]=inp[-1,:]

        return output
