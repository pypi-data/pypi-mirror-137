import numpy as np
import torch
from torch.utils.data import DataLoader
from torch.nn import functional as F
import os

from decto.model.faster_rcnn import FasterRCNN
from decto.model.rpn import AnchorTargetCreator
from decto.model.roihead import ProposalTargetCreator
from decto.dataset.loader import Dataset, TestDataset
from decto.utils.visualize import visualize_prediction
from decto.utils.metrics import eval_detection_voc
from decto.utils.logger import Logger

def smooth_l1_loss(x, t, in_weight, sigma):
    sigma2 = sigma**2
    diff = in_weight * (x -t)
    abs_diff = diff.abs()

    flag = (abs_diff < (1./sigma2)).float()
    loss = (flag*sigma2/2) * (diff**2) + (1-flag) * (abs_diff -.5/sigma2)

#     x = x[in_weight==1]
#     t = t[in_weight==1]

#     if sigma < 1e-5:
#         loss = torch.abs(x - t)
#     else:
#         n = torch.abs(x - t)
#         cond = n < sigma
#         loss = torch.where(cond, 0.5 * n ** 2 / sigma, n - 0.5 * sigma)

    return loss.sum()

def faster_rcnn_loc_loss(pred_loc, gt_loc, gt_label, sigma):
    in_weight = torch.zeros(gt_loc.shape, device=gt_loc.device)
    in_weight[(gt_label > 0).view(-1, 1).expand_as(in_weight)] = 1

    loc_loss = smooth_l1_loss(pred_loc, gt_loc, in_weight, sigma)

    loc_loss = 0.25*loc_loss/((gt_label > 0).sum() + 1e-8)
    return loc_loss

class Trainer():
    def __init__(self, config):
        
        self.train_config = config['train_config']
        self.dataset_config = config['dataset_config']
        self.device = self.train_config['device']
        
        self.min_size_test = self.dataset_config['min_size_test']
        self.max_size_test = self.dataset_config['max_size_test']
        self.rpn_sigma = self.train_config['rpn_sigma']
        self.roi_sigma = self.train_config['roi_sigma']
        
        self.model = FasterRCNN(config['backbone'], 
                                config['fpn_config'], 
                                config['rpn_config'], 
                                config['roi_pooler_config'],
                                config['roi_head_config'])
        
        
        if self.device.startswith('cuda'):
            self.model = self.model.to(self.device)
        
        self.anchor_target_creator = AnchorTargetCreator()
        self.proposal_target_creator = ProposalTargetCreator()
        
        self.optimizer = self.get_optimizer()
    
        self.trainset = Dataset(**self.dataset_config, split=self.train_config['train_file'])
        self.train_loader = DataLoader(self.trainset,
                                      batch_size=1,
                                      shuffle=True,                              
                                      num_workers=3)
        self.train_iter = iter(self.train_loader)
        
        self.testset = TestDataset(**self.dataset_config, split=self.train_config['test_file'])
        self.test_loader = DataLoader(self.testset,
                                           batch_size=1,
                                           num_workers=3,
                                           shuffle=False, 
                                           pin_memory=True)
        
        self.num_iters = self.train_config['num_iters']
        self.current_iter = 0
        self.eval_steps = self.train_config['eval_steps']
        self.classes = self.dataset_config['classes']
        self.log_dir = self.train_config['log_dir']
        self.num_eval_samples = self.train_config['num_eval_samples']
        
        self.verbose = self.train_config['verbose']
        if self.log_dir != None:
            os.makedirs(self.log_dir, exist_ok=True)
            self.log = Logger(os.path.join(self.log_dir, 'log.txt'))
            
    def forward_step(self, imgs, bboxes, labels, preprocess_scale):        
        """
        imgs: torch, NxCxHxW
        bboxes: numpy, NxRx4
        labels: numpy, NxR
        preprocess_scale: 
        """
        n = bboxes.shape[0]                
        if n != 1:
            raise ValueError('currently only support batch size 1')
        
        _, _, H, W = imgs.shape
        img_size = (H, W)
        
        fts = self.model.extractor(imgs)
        rpn_fts, roi_fts = self.model.fpn(fts)
        
        rpn_locs, rpn_scores, rois, roi_fg_scores, roi_indices, anchors = self.model.rpn(rpn_fts, img_size, preprocess_scale)
        
        bboxes = bboxes[0]
        labels = labels[0]
        rois   = rois.cpu().numpy()
        roi_fg_scores = roi_fg_scores.cpu().numpy()
        
        gt_rpn_locs, gt_rpn_labels = self.anchor_target_creator(bboxes, anchors, img_size)
        
        gt_rpn_locs = gt_rpn_locs.to(self.device)
        gt_rpn_labels = gt_rpn_labels.to(self.device)
              
        sample_rois, gt_roi_locs, gt_roi_labels = self.proposal_target_creator(rois, bboxes, labels)
        sample_roi_indices  = torch.zeros((sample_rois.shape[0],), device=self.device)
        
        sample_rois = sample_rois.to(self.device)
        gt_roi_locs = gt_roi_locs.to(self.device)
        gt_roi_labels = gt_roi_labels.to(self.device)
        
        pooling_fts = self.model.pooler(roi_fts, sample_rois, sample_roi_indices)
        roi_cls_locs, roi_scores = self.model.roi_head(pooling_fts)        
                        
        rpn_loc_loss, rpn_cls_loss = self.train_rpn(rpn_locs, rpn_scores, gt_rpn_locs, gt_rpn_labels)
        roi_loc_loss, roi_cls_loss = self.train_roi_head(roi_cls_locs, roi_scores, gt_roi_locs, gt_roi_labels)
        
        total_loss = rpn_loc_loss + rpn_cls_loss + roi_loc_loss + roi_cls_loss
        loss_items = (rpn_loc_loss.item(), rpn_cls_loss.item(), roi_loc_loss.item(), roi_cls_loss.item())                                 
            
        return total_loss, loss_items
    
    
    def train_rpn(self, rpn_locs, rpn_scores, gt_rpn_locs, gt_rpn_labels):
        rpn_locs = rpn_locs[0]
        rpn_scores = rpn_scores[0]        
        
        loc_loss = faster_rcnn_loc_loss(rpn_locs, gt_rpn_locs, gt_rpn_labels, self.rpn_sigma)
        cls_loss = F.cross_entropy(rpn_scores, gt_rpn_labels, ignore_index=-1)

        return loc_loss, cls_loss
    
    def train_roi_head(self, roi_cls_locs, roi_scores, gt_roi_locs, gt_roi_labels):        
        n_sample = roi_cls_locs.size(0)
                
        roi_cls_loc = roi_cls_locs.view(n_sample, roi_cls_locs.size(1)//4, 4)
        roi_loc = roi_cls_loc[torch.arange(n_sample), gt_roi_labels]
                
        loc_loss = faster_rcnn_loc_loss(roi_loc, gt_roi_locs, gt_roi_labels, self.roi_sigma)
        cls_loss = F.cross_entropy(roi_scores, gt_roi_labels)
            
        return loc_loss, cls_loss
    
    def train(self):
        
        for i in range(self.current_iter, self.num_iters):
            self.current_iter = i
            try:
                batch = next(self.train_iter)
            except StopIteration:
                self.train_iter = iter(self.train_loader)
                batch = next(self.train_iter)
            
            imgs, bboxes, labels, preprocess_scale = batch
            imgs = imgs.to(self.device)
            bboxes = bboxes.numpy()
            labels = labels.numpy()
            preprocess_scale = preprocess_scale.numpy()
            
            self.optimizer.zero_grad()
            
            self.model.train()
            total_loss, loss_items = self.forward_step(imgs, bboxes, labels, preprocess_scale)
            total_loss.backward()

            self.optimizer.step()  
            
            if i == 50000:
                self.scale_lr()                            
            
            if self.verbose > 0 and i % self.verbose == 0:
                current_lr = self.optimizer.param_groups[0]['lr']
                str_log = 'iter: {:06d} total_loss:{:.4f} rpn_loc: {:.6f} rpn_cls: {:.5f} roi_loc: {:.6f} roi_cls: {:.5f} lr: {:.2e}'.format(
                    i, total_loss.item(), loss_items[0], loss_items[1], loss_items[2], loss_items[3], current_lr)
                self.log(str_log)
            
                
            if (i+0) % self.eval_steps == 0:
                self.model.eval()
                self.sample()
                
                ap, eval_total_loss, eval_loss_items = self.evaluate()
                str_log = 'eval iter: {:06d} total_loss: {:.4f} rpn_loc: {:.6f} rpn_cls: {:.5f} roi_loc: {:.6f} roi_cls: {:.5f}'.format(
                    i, eval_total_loss, eval_loss_items[0], eval_loss_items[1], eval_loss_items[2], eval_loss_items[3])
                self.log(str_log)
                self.log('eval iter: {:06d} ap: {}'.format(i, ap))
                
        
    def sample(self):
        max_items = min(len(self.testset), 32)
        for i in range(max_items):
            img, bbox, label, difficult = self.testset[i]
            detail_prediction = self.model.predict(img, self.min_size_test, self.max_size_test, return_roi=True)
            fname = '{:03d}_{:06d}'.format(i, self.current_iter)
            img = img.transpose((1, 2, 0))
            visualize_prediction(img, detail_prediction, self.classes, self.log_dir, fname)
    
    def evaluate(self):
        pred_bboxes, pred_labels, pred_scores = [], [], []
        gt_bboxes, gt_labels,gt_difficults = [], [], []
        total_losses = []
        total_loss_items = []
        self.model.eval()
        
        for i in range(len(self.testset)):
            if i >= self.num_eval_samples: 
                break
                
            ori_img, gt_bbox, gt_label, gt_difficult = self.testset[i]
                        
            imgs = torch.from_numpy(ori_img[None])
            
            imgs, bboxes, labels, preprocess_scale = self.trainset.tsf((imgs, gt_bbox, gt_label))
            
            imgs = imgs.to(self.device)
            bboxes = bboxes[None]
            labels = labels[None]
            
            with torch.no_grad():
                total_loss, loss_items = self.forward_step(imgs, bboxes, labels, preprocess_scale)             
                total_losses.append(total_loss.item())
                total_loss_items.append(loss_items)
                
            old_score_thresh = self.model.score_thresh
            self.model.score_thresh = 0.05
            pred_bbox, pred_label, pred_score = self.model.predict(ori_img, self.min_size_test, self.max_size_test)
            self.model.score_thresh = old_score_thresh
            
            pred_bboxes.append(pred_bbox)
            pred_labels.append(pred_label)
            pred_scores.append(pred_score)
            
            gt_bboxes.append(gt_bbox)
            gt_labels.append(gt_label)
            gt_difficults.append(gt_difficult)
        
        result = eval_detection_voc(
            pred_bboxes, pred_labels, pred_scores,
            gt_bboxes, gt_labels, gt_difficults,
            use_07_metric=True)
        
        total_losses = np.mean(total_losses)        
        total_loss_items = np.mean(total_loss_items, axis=0)
        
        return result, total_losses, total_loss_items
    
    def get_optimizer(self):
        """
        return optimizer, It could be overwriten if you want to specify 
        special optimizer
        """
        params = []
        for key, value in dict(self.model.named_parameters()).items():
            if value.requires_grad:
                if 'bias' in key:
                    params += [{'params': [value], 'lr': self.train_config['learning_rate'] * 2, 'weight_decay': 0}]
                else:
                    params += [{'params': [value], 'lr': self.train_config['learning_rate'], 'weight_decay': self.train_config['weight_decay']}]
        if self.train_config['use_adam']:
            self.optimizer = torch.optim.AdamW(params)
        else:
            self.optimizer = torch.optim.SGD(params, momentum=0.9)
        return self.optimizer

    def scale_lr(self):
        for param_group in self.optimizer.param_groups:
            param_group['lr'] *= self.train_config['lr_decay']
        return self.optimizer
