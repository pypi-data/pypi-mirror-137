import torch
import torch.nn as nn
import torch.nn.functional as F

from torchvision.ops import RoIPool, RoIAlign

import math

def level_assign(bboxes, min_level, max_level, base_level=4, base_size=224):
        hs = bboxes[:, 2] - bboxes[:, 0]
        ws = bboxes[:, 3] - bboxes[:, 1]
        box_sizes = torch.sqrt(hs*ws)
        
        level_assignment = torch.floor(base_level + torch.log2(box_sizes/base_size))
        level_assignment = torch.clamp(level_assignment, min=min_level, max=max_level)
        level_assignment = level_assignment.to(torch.int64) - min_level
        
        return level_assignment


class ROIPooler(nn.Module):
    def __init__(self, roi_size, strides, base_level=4, base_size=224):
        super(ROIPooler, self).__init__()
        
        self.strides = strides
        self.base_level = base_level
        self.base_size = base_size
        self.roi_size = roi_size
        
        self.poolers = nn.ModuleList()
        
        for scale in strides:
            self.poolers.append(RoIPool(output_size=(self.roi_size, self.roi_size), spatial_scale=1.0/scale))
        
    def __call__(self, fts, rois, roi_indices):
        min_level = math.log2(self.strides[0])
        max_level = math.log2(self.strides[-1])
        
        assert len(fts) == len(self.strides) == max_level - min_level + 1
        
        level_assignments = level_assign(rois, min_level, max_level, base_level=self.base_level, base_size=self.base_size)
#         print(level_assignments.unique(return_counts=True))
#         pool_fts = []
        
        num_boxes = len(level_assignments)
        num_channels = fts[0].shape[1]
        dtype = fts[0].dtype
        device = fts[0].device
        
        pool_fts = torch.zeros((num_boxes, num_channels, self.roi_size, self.roi_size), dtype=dtype, device=device)
        
        for level, (ft, pooler) in enumerate(zip(fts, self.poolers)):
            inds = torch.nonzero(level_assignments == level, as_tuple=True)[0]    
#             print(inds)
            roi = rois[inds]
            roi_index = roi_indices[inds]
            pooling_ft = self.pooling(ft, roi, roi_index, pooler)
            pool_fts[inds] = pooling_ft
#             print(pooling_ft)
#             print(i, len(roi), pooling_ft.mean())
#             pool_fts.append(pooling_ft)
#         print(pool_fts.mean(axis=(1, 2, 3)))
#         pool_fts = torch.cat(pool_fts, dim=0)
        
        return pool_fts
    
    def pooling(self, ft, rois, roi_indices, pooler):
        
        indices_and_rois = torch.cat((roi_indices[:, None], rois), dim=1)
        xy_indices_and_rois = indices_and_rois[:, [0, 2, 1, 4, 3]]
        indices_and_rois =  xy_indices_and_rois.contiguous()
                
        pooling_ft = pooler(ft, indices_and_rois)
        
        return pooling_ft
