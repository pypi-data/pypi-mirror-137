import torch
import torch.nn as nn
import torch.nn.functional as F

class FeaturePyramidNetwork(nn.Module):
    def __init__(self, in_channels_list, out_channels):
        super(FeaturePyramidNetwork, self).__init__()
        self.in_channels_list = in_channels_list
        
        self.lateral_c2 = nn.Conv2d(in_channels=self.in_channels_list[0], out_channels=out_channels, kernel_size=1, stride=1, padding=0)
        self.lateral_c3 = nn.Conv2d(in_channels=self.in_channels_list[1], out_channels=out_channels, kernel_size=1, stride=1, padding=0)
        self.lateral_c4 = nn.Conv2d(in_channels=self.in_channels_list[2], out_channels=out_channels, kernel_size=1, stride=1, padding=0)
        self.lateral_c5 = nn.Conv2d(in_channels=self.in_channels_list[3], out_channels=out_channels, kernel_size=1, stride=1, padding=0)
#         self.lateral_layer3 = nn.Conv2d(in_channels=self.in_channels_list[3], out_channels=256, kernel_size=1, stride=1, padding=0)
        # add smooth layers
        
        self.smooth_p2 = nn.Conv2d(in_channels=out_channels, out_channels=out_channels, kernel_size=3, stride=1, padding=1)
        self.smooth_p3 = nn.Conv2d(in_channels=out_channels, out_channels=out_channels, kernel_size=3, stride=1, padding=1)
        self.smooth_p4 = nn.Conv2d(in_channels=out_channels, out_channels=out_channels, kernel_size=3, stride=1, padding=1)
#         self.smooth_p5 = nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, stride=1, padding=1)
#         self.smooth_layer3 = nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, stride=1, padding=1)
        # add downsample layer
        
    def forward(self, x):
        assert len(self.in_channels_list) == len(x)
        
        c2 = x['c2']
        c3 = x['c3']
        c4 = x['c4']
        c5 = x['c5']
        
        p5 = self.lateral_c5(c5)
        p4 = self.lateral_c4(c4)
        p3 = self.lateral_c3(c3)
        p2 = self.lateral_c2(c2)
        
        p4 = self.upsample_add(p5, p4)
        p3 = self.upsample_add(p4, p3)
        p2 = self.upsample_add(p3, p2)
        
#         p5 = p5
        p4 = self.smooth_p4(p4)
        p3 = self.smooth_p3(p3)
        p2 = self.smooth_p2(p2)
        p6 = F.max_pool2d(p5, 1, 2)
        
        
        return [p2, p3, p4, p5, p6], [p2, p3, p4, p5]
    
    def upsample_add(self, p, c):
        _, _, H, W = c.size()
        
        return F.interpolate(p, size=(H, W), mode='nearest') + c
    
# fpn = FeaturePyramidNetwork((512, 512), 128)

# for yy in fpn(y):
#     print(yy.shape)
