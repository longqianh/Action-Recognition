import torch
import torch.nn as nn
class Pass(nn.Module):
    """docstring for myBatchNorm"""
    def __init__(self,shape):
        super(Pass, self).__init__()
        self.placeholder=nn.Parameter(torch.randn(shape))


    def forward(self,x):
        return x
            


if __name__ == '__main__':
    m=Pass((108,50))
    x=torch.randn(1,108,50)
    print(m(x).shape)
    
    # print(pretrained_state_dict)
    
    # for t in m.state_dict():
        # print(t)
    print(m.state_dict()['placeholder'].shape)
    
    # x=x.unsqueeze(3)
    # print(x.shape)
    # print(x.squeeze(3).shape)
    