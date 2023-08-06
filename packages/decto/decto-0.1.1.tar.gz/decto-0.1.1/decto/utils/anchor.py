import numpy as np
import math

def generate_anchor_base(base_size=16, aspect_ratios=[0.5, 1, 2],
                         sizes=[8, 16, 32]):
    
    anchor_base = np.zeros((len(aspect_ratios)*len(sizes), 4), dtype=np.float32)
    
    py = base_size//2
    px = base_size//2
    
    for i in range(len(aspect_ratios)):
        for j in range(len(sizes)):
            h = base_size * sizes[j] * np.sqrt(aspect_ratios[i])            
            w = base_size * sizes[j] * np.sqrt(1.0/aspect_ratios[i])
            
            index = i*len(sizes) + j
            anchor_base[index, 0] = py - h/2
            anchor_base[index, 1] = px - w/2
            anchor_base[index, 2] = py + h/2
            anchor_base[index, 3] = px + w/2
    
    return anchor_base

def enumerate_shifted_anchor(anchor_base, feat_stride, ft_height, ft_width):
    shift_y = np.arange(0, ft_height*feat_stride, feat_stride)
    shift_x = np.arange(0, ft_width*feat_stride, feat_stride)

    shift_x, shift_y = np.meshgrid(shift_x, shift_y)
    shift = np.stack((shift_y.ravel(), shift_x.ravel(), shift_y.ravel(), shift_x.ravel()), axis=1)

    A = anchor_base.shape[0]
    K = shift.shape[0]

    anchor = anchor_base.reshape((1, A, 4)) + shift.reshape((1, K, 4)).transpose((1, 0, 2))
    anchor = anchor.reshape((K*A, 4)).astype(np.float32)

    return anchor
