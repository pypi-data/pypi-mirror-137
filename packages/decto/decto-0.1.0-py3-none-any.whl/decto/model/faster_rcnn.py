import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision.ops import nms

import numpy as np

from decto.model.backbone import Backbone
from decto.model.fpn import FeaturePyramidNetwork
from decto.model.rpn import RegionProposalNetwork
from decto.model.pooler import ROIPooler
from decto.model.roihead import ROIHead
from decto.utils.box import loc2bbox
from decto.loader import preprocess

class FasterRCNN(nn.Module):
    def __init__(self, backbone_config, 
                    fpn_config, 
                    rpn_config,     
                    roi_pooler_config,
                    roi_head_config,
                    loc_normalize_mean=(0.,0.,0.,0.),
                    loc_normalize_std=(0.1, 0.1, 0.2, 0.2)):
        
        super(FasterRCNN, self).__init__()
        self.extractor = Backbone(**backbone_config)
        
        self.fpn = FeaturePyramidNetwork(**fpn_config)
        
        self.rpn = RegionProposalNetwork(**rpn_config)     
        
        self.pooler = ROIPooler(**roi_pooler_config)
        self.roi_head = ROIHead(**roi_head_config)
        
        self.n_class = self.roi_head.n_class
        
        self.nms_thresh = 0.3
        self.score_thresh = 0.7
        
        self.loc_normalize_mean = loc_normalize_mean
        self.loc_normalize_std = loc_normalize_std
    
    def device(self):
        return self.roi_head.cls_loc.weight.device
        
    def forward(self, x, preprocess_scale=1.0):        
        img_size = x.shape[2:]
        
        fts = self.extractor(x)
        rpn_fts, roi_fts = self.fpn(fts)
        rpn_locs, rpn_scores, rois, roi_fg_scores, roi_indices, anchors = self.rpn(rpn_fts, img_size, preprocess_scale)
        
        pool_fts = self.pooler(roi_fts, rois, roi_indices)
        
        roi_cls_locs, roi_scores = self.roi_head(pool_fts)
        
        return roi_cls_locs, roi_scores, rois, roi_fg_scores, roi_indices
    
    def suppress(self, raw_cls_bbox, raw_prob, include_bg=False):
        bbox, label, score = [], [], []

        
        # 0 is background class
        start_id = 0 if include_bg else 1

        for l in range(start_id, self.n_class):
            cls_bbox_l = raw_cls_bbox.reshape((-1, self.n_class, 4))[:, l]
            prob_l = raw_prob[:, l]
            mask = prob_l > self.score_thresh
                    
            cls_bbox_l = cls_bbox_l[mask]
            prob_l = prob_l[mask]
            keep = nms(cls_bbox_l, prob_l, self.nms_thresh)
            
            bbox.append(cls_bbox_l[keep].cpu().numpy())
            label.append((l-1)*np.ones((len(keep),)))
            score.append(prob_l[keep].cpu().numpy())
        
        
        bbox = np.concatenate(bbox, axis=0).astype(np.float32)
        label = np.concatenate(label, axis=0).astype(np.int32)
        score = np.concatenate(score, axis=0).astype(np.float32)
#         print(bbox.shape)
        return bbox, label, score    
        
    def predict(self, img, min_size, max_size, return_roi=False, include_bg=False):      
        """
        img: CxHxW
        """
        self.eval()
        device = self.device()        
        size = img.shape[1:]
        img = img[None]  
        img = torch.from_numpy(img).to(device)
        
        img = preprocess(img, min_size=min_size, max_size=max_size)        
          
#         img = torch.from_numpy(img).float().to(device)
        
        preprocess_scale = img.shape[3]/size[1]
        
        with torch.no_grad():
            roi_cls_locs, roi_scores, rois, roi_fg_scores, _ = self(img, preprocess_scale=preprocess_scale)
        
#         print('roi_fg_scores', len(roi_fg_scores), roi_fg_scores[0].shape)
        
        detail_prediction = []
        cls_bboxes, probs = [], []

        # scale to input image size
        rois = rois/preprocess_scale       
        roi_fg_scores = roi_fg_scores.cpu().numpy()

        mean = torch.tensor(self.loc_normalize_mean).repeat(self.n_class).to(device)
        std = torch.tensor(self.loc_normalize_std).repeat(self.n_class).to(device)

        roi_cls_locs = roi_cls_locs*std + mean
        roi_cls_locs = roi_cls_locs.view(-1, self.n_class, 4)
        rois = rois.view(-1, 1, 4).expand_as(roi_cls_locs)

        rois = rois.cpu().numpy()
        roi_cls_locs = roi_cls_locs.cpu().numpy()
        cls_bboxes = loc2bbox(rois.reshape((-1, 4)), roi_cls_locs.reshape((-1, 4)))
        cls_bboxes = torch.from_numpy(cls_bboxes).to(device)

        cls_bboxes = cls_bboxes.view(-1, self.n_class*4)
        cls_bboxes[:, [0, 2]] = cls_bboxes[:, [0, 2]].clamp(min=0, max=size[0])
        cls_bboxes[:, [1, 3]] = cls_bboxes[:, [1, 3]].clamp(min=0, max=size[1])

        probs = F.softmax(roi_scores, dim=1)
                
        
        bboxes, labels, scores = self.suppress(cls_bboxes, probs, include_bg=include_bg)
        
        
        if return_roi:
            return bboxes, labels, scores, rois[:, 0], roi_fg_scores
        else:
            return bboxes, labels, scores
