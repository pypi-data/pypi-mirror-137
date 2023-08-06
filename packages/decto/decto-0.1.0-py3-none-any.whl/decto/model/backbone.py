import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision

from collections import OrderedDict
from math import isclose

def set_bn_fix(m):
    classname = m.__class__.__name__
    if classname.find('BatchNorm') != -1:
        for p in m.parameters():
            p.requires_grad = False

def set_bn_eval(m):
    classname = m.__class__.__name__
    if classname.find('BatchNorm') != -1:
        m.eval()
                    
class Resnet(nn.Module):
    def __init__(self, strides, **kwargs):
        super(Resnet, self).__init__()
        self.model = torchvision.models.resnet101(pretrained=True)
#         self.model.layer4[0].conv2.stride = (1, 1)
#         self.model.layer4[0].downsample[0].stride = (1, 1)

        del self.model.avgpool, self.model.fc
        
        self.model.apply(set_bn_fix)
        
        for p in self.model.conv1.parameters():
            p.requires_grad = False
        
        for p in self.model.layer1.parameters():
            p.requires_grad = False
            
    def forward(self, x):
        self.model.apply(set_bn_eval)
        activations = OrderedDict()
        
        x = self.model.conv1(x)
        
        x = self.model.bn1(x)
        x = self.model.relu(x)
        x = self.model.maxpool(x)

        x = self.model.layer1(x)
        activations['c2'] = x
        x = self.model.layer2(x)
        activations['c3'] = x
        x = self.model.layer3(x)
        activations['c4'] = x
        x = self.model.layer4(x)
        activations['c5'] = x
        
        return activations

class Backbone(nn.Module):
    def __init__(self, strides, **kwargs):
        super(Backbone, self).__init__()
#         self.model = VGGBackbone(strides=strides, **kwargs)
        self.model = Resnet(strides=strides, **kwargs)

        self.strides = strides

    def forward(self, x):
        fts = self.model(x)

        for i, ft in enumerate(fts.values()):
            assert isclose(x.size(2)/self.strides[i], ft.size(2), abs_tol=2)

        return fts

