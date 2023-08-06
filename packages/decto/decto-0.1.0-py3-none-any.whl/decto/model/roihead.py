import torch
import torch.nn as nn
import torch.nn.functional as F

import math
import numpy as np

from decto.utils.box import bbox2loc, bbox_iou
from decto.utils.initialize import normal_init

class ROIHead(nn.Module):
    def __init__(self, in_channels, n_class, roi_size, dropout=0.1):
        super(ROIHead, self).__init__()
        
        self.classifier = nn.Sequential(
                    nn.Linear(in_channels * roi_size * roi_size, 1024),
                    nn.ReLU(True),
#                     nn.Dropout(p=dropout),
#                     nn.Linear(1024, 1024),
#                     nn.ReLU(True),
#                     nn.Dropout(p=dropout),
#                     nn.Linear(4096, num_classes),
                )
        
        
        self.cls_loc = nn.Linear(1024, n_class * 4)
        self.score = nn.Linear(1024, n_class)
        
        self.n_class = n_class
        self.roi_size = roi_size
        
        normal_init(self.cls_loc, 0, 0.001)
        normal_init(self.score, 0, 0.01)
        
    
    def forward(self, pool):        
        
        pool = pool.flatten(start_dim=1)
        h = self.classifier(pool)
        roi_cls_locs = self.cls_loc(h)
        roi_scores = self.score(h)
        
        return roi_cls_locs, roi_scores 

class ProposalTargetCreator():
    def __init__(self, n_sample=128, pos_ratio=0.25,
                 pos_iou_thresh=0.5,
                 neg_iou_thresh_hi=0.5, neg_iou_thresh_lo=0.0):

        self.n_sample = n_sample
        self.pos_ratio = pos_ratio
        self.pos_iou_thresh = pos_iou_thresh
        self.neg_iou_thresh_hi = neg_iou_thresh_hi
        self.neg_iou_thresh_lo = neg_iou_thresh_lo


    def __call__(self, roi, roi_fg_scores, bbox, label,
                 loc_normalize_mean= (0.,0.,0.,0.),
                 loc_normalize_std = (0.1, 0.1, 0.2, 0.2)):
        n_bbox, _ = bbox.shape
        # importance
        roi = np.concatenate((roi, bbox), axis=0)
        roi_fg_scores = np.concatenate((roi_fg_scores, np.ones(n_bbox)), axis=0)

        pos_roi_per_image = int(self.n_sample*self.pos_ratio)
        iou = bbox_iou(roi, bbox)

        gt_assignment = iou.argmax(axis=1)
        max_iou = iou.max(axis=1)
        gt_roi_label = label[gt_assignment] + 1

        pos_index = np.where(max_iou>=self.pos_iou_thresh)[0]
        pos_roi_per_this_image = int(min(pos_roi_per_image, pos_index.size))
        if pos_index.size > 0:
            pos_index = np.random.choice(pos_index, size=pos_roi_per_this_image, replace=False)

        neg_index = np.where((max_iou < self.neg_iou_thresh_hi) &
                            (max_iou >= self.neg_iou_thresh_lo))[0]
        neg_roi_per_this_image = self.n_sample - pos_roi_per_this_image
        neg_roi_per_this_image = int(min(neg_roi_per_this_image, neg_index.size))
        if neg_index.size > 0:
            neg_index = np.random.choice(neg_index, size=neg_roi_per_this_image, replace=False)


        keep_index = np.append(pos_index, neg_index)
        gt_roi_label = gt_roi_label[keep_index]
        gt_roi_label[pos_roi_per_this_image:] = 0

        sample_roi = roi[keep_index]

        gt_roi_loc = bbox2loc(sample_roi, bbox[gt_assignment[keep_index]])


        gt_roi_loc = (gt_roi_loc - np.array(loc_normalize_mean, dtype=np.float32))/np.array(loc_normalize_std, dtype=np.float32)

        sample_roi = torch.from_numpy(sample_roi).float()
        gt_roi_loc = torch.from_numpy(gt_roi_loc).float()
        gt_roi_label = torch.from_numpy(gt_roi_label).long()

#         print('roi', gt_roi_label.unique(return_counts=True))

        return sample_roi, gt_roi_loc, gt_roi_label
