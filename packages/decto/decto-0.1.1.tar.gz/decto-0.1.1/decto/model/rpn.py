import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision.ops import nms

import numpy as np

from decto.utils.anchor import generate_anchor_base, enumerate_shifted_anchor
from decto.utils.box import loc2bbox, bbox2loc, bbox_iou
from decto.utils.initialize import normal_init

class RegionProposalNetwork(nn.Module):
    def __init__(self, in_channels, mid_channels,
                 aspect_ratios=[[0.5, 1, 2], [0.5, 1, 2], [0.5, 1, 2]],
                 anchor_sizes=[[8, 16, 32], [8, 16, 32], [8, 16, 32]],
                 feat_strides=[4, 8, 16], proposal_creator_config={}):
        super(RegionProposalNetwork, self).__init__()

        assert len(aspect_ratios) == len(anchor_sizes) == len(feat_strides)

        self.feat_strides = feat_strides

        self.anchor_bases = []
        for i in range(len(feat_strides)):
            anchor_base = generate_anchor_base(sizes=anchor_sizes[i], aspect_ratios=aspect_ratios[i])
            self.anchor_bases.append(anchor_base)

        n_anchor = self.anchor_bases[0].shape[0]

        self.conv1 = nn.Conv2d(in_channels, mid_channels, 3, 1, 1)
        self.score = nn.Conv2d(mid_channels, n_anchor * 2, 1, 1, 0)
        self.loc = nn.Conv2d(mid_channels, n_anchor * 4, 1, 1, 0)

        self.proposal_layer = ProposalCreator(self, **proposal_creator_config)

        normal_init(self.conv1, 0, 0.01)
        normal_init(self.score, 0, 0.01)
        normal_init(self.loc, 0, 0.001)

    def forward_each(self, ft, stride, anchor_base):

        n, _, ft_height, ft_width = ft.shape
        anchor = enumerate_shifted_anchor(anchor_base, stride, ft_height, ft_width)

        n_anchor = anchor.shape[0] // (ft_height*ft_width)
        h = F.relu(self.conv1(ft))

        rpn_locs = self.loc(h)
        rpn_locs = rpn_locs.permute(0, 2, 3, 1).reshape(n, -1, 4)

        rpn_scores = self.score(h)
        rpn_scores = rpn_scores.permute(0, 2, 3, 1)
        rpn_softmax_scores = F.softmax(rpn_scores.view(n, ft_height, ft_width, n_anchor, 2), dim=4)
        rpn_fg_scores = rpn_softmax_scores[:, :, :, :, 1]
        rpn_fg_scores = rpn_fg_scores.view(n, -1)
        rpn_scores = rpn_scores.reshape(n, -1, 2)

        return rpn_locs, rpn_scores, rpn_fg_scores, anchor


    def forward(self, fts, img_size, preprocess_scale):

        anchors = []

        rpn_locs, rpn_scores, rpn_fg_scores, anchors = [], [], [], []
        for i in range(len(fts)):

            ft = fts[i]
            stride = self.feat_strides[i]
            anchor_base = self.anchor_bases[i]

            rpn_loc, rpn_score, rpn_fg_score, anchor = self.forward_each(ft, stride, anchor_base)
            rpn_locs.append(rpn_loc)

            rpn_scores.append(rpn_score)
            rpn_fg_scores.append(rpn_fg_score)
            anchors.append(anchor)

        rpn_locs = torch.cat(rpn_locs, dim=1)
        rpn_scores = torch.cat(rpn_scores, dim=1)
        rpn_fg_scores = torch.cat(rpn_fg_scores, dim=1)
        anchors = np.concatenate(anchors, axis=0)

        # only for batch_size = 1
        rois, roi_fg_scores = self.proposal_layer(rpn_locs[0], rpn_fg_scores[0], anchors, img_size, preprocess_scale)
        roi_indices = torch.zeros(len(rois), dtype=torch.int32, device=rois.device)

        return rpn_locs, rpn_scores, rois, roi_fg_scores, roi_indices, anchors

def _unmap(data, count, index, fill):
    if len(data.shape) == 1:
        ret = fill*np.ones((count,), dtype=data.dtype)
        ret[index] = data
    else:
        ret = fill*np.ones((count,) + data.shape[1:], dtype=data.dtype)
        ret[index] = data

    return ret
def _get_inside_index(anchor, H, W):
#     index_inside = np.where(
#         (anchor[:, 0] >= 0) &
#         (anchor[:, 1] >= 0) &
#         (anchor[:, 2] <= H) &
#         (anchor[:, 3] <= W)
#     )[0]

    index_inside = np.arange(len(anchor))

    return index_inside

class ProposalCreator():
    def __init__(self, rpn, nms_thresh=0.7, n_train_pre_nms=12000, n_train_post_nms=2000, n_test_pre_nms=6000, n_test_post_nms=300, min_size=16):
        self.rpn = rpn
        self.nms_thresh = nms_thresh
        self.n_train_pre_nms = n_train_pre_nms
        self.n_train_post_nms = n_train_post_nms
        self.n_test_pre_nms = n_test_pre_nms
        self.n_test_post_nms = n_test_post_nms
        self.min_size = min_size

    def __call__(self, loc, score, anchor, img_size, preprocess_scale=1.0):
        device = loc.device
        loc = loc.cpu().data.numpy()
        score = score.cpu().data.numpy()

        if self.rpn.training:
            n_pre_nms = self.n_train_pre_nms
            n_post_nms = self.n_train_post_nms
        else:
            n_pre_nms = self.n_test_pre_nms
            n_post_nms = self.n_test_post_nms

        roi = loc2bbox(anchor, loc)
        # clip predicted box to image size
        roi[:, [0, 2]] = np.clip(roi[:, [0, 2]], 0, img_size[0])
        roi[:, [1, 3]] = np.clip(roi[:, [1, 3]], 0, img_size[1])
        # remove predicted box with either height or width < threshold
        min_size = self.min_size*preprocess_scale
        hs = roi[:, 2] - roi[:, 0]
        ws = roi[:, 3] - roi[:, 1]
        keep = np.where((hs >= min_size) & (ws >= min_size))[0]
        roi = roi[keep]
        score = score[keep]

        order = score.ravel().argsort()[::-1]
        if n_pre_nms > 0:
            order = order[:n_pre_nms]
        roi = roi[order]
        score = score[order]
        roi = torch.from_numpy(roi).to(device)
        score = torch.from_numpy(score).to(device)
        keep = nms(roi, score, self.nms_thresh)

        if n_post_nms > 0:
            keep = keep[:n_post_nms]

        roi = roi[keep.cpu().numpy()]
        score = score[keep.cpu().numpy()]

        return roi, score

class AnchorTargetCreator():
    def __init__(self, n_sample=256, pos_iou_thresh=0.7, neg_iou_thresh=0.3, pos_ratio=0.5):
        self.n_sample = n_sample
        self.pos_iou_thresh = pos_iou_thresh
        self.neg_iou_thresh = neg_iou_thresh
        self.pos_ratio = pos_ratio


    def __call__(self, bbox, anchor, img_size):
        img_H, img_W = img_size
        n_anchor = len(anchor)

        inside_index = _get_inside_index(anchor, img_H, img_W)

        anchor = anchor[inside_index]
        argmax_ious, label = self._create_label(inside_index, anchor, bbox)

#         print(level_assign(torch.from_numpy(anchor), 3, 5)[label==1])
#         print('bbox', np.sqrt((bbox[:, 2] - bbox[:, 0])*(bbox[:, 3] - bbox[:, 1])))

        loc = bbox2loc(anchor, bbox[argmax_ious])

        label = _unmap(label, n_anchor, inside_index, fill=-1)
        loc = _unmap(loc, n_anchor, inside_index, fill=0)


        label = torch.from_numpy(label).long()
        loc = torch.from_numpy(loc).float()

        return loc, label

    def _create_label(self, inside_index, anchor, bbox):
        label = -1*np.ones((len(inside_index), ), dtype=np.int32)
#         print(anchor, bbox)
        argmax_ious, max_ious, gt_argmax_ious = self._calc_ious(anchor, bbox, inside_index)
#         print('anchor.sum(axis=0), bbox.sum(axis=0)', anchor.sum(axis=0), bbox.sum(axis=0))
#         print('neg, pos anchor: ', (max_ious < self.neg_iou_thresh).sum(), (max_ious >= self.pos_iou_thresh).sum())
        label[max_ious < self.neg_iou_thresh] = 0

        # important
        label[gt_argmax_ious] = 1

        label[max_ious >= self.pos_iou_thresh] = 1

#         print('pos anchor {}'.format((label==1).sum()))

        n_pos = int(self.pos_ratio*self.n_sample)
        pos_index = np.where(label==1)[0]
        if len(pos_index) > n_pos:
            disable_index = np.random.choice(pos_index, size=(len(pos_index) - n_pos), replace=False)
            label[disable_index] = -1

        n_neg = self.n_sample - np.sum(label == 1)
        neg_index = np.where(label==0)[0]
        if len(neg_index) > n_neg:
            disable_index = np.random.choice(neg_index, size=(len(neg_index) - n_neg), replace=False)
            label[disable_index] = -1

        return argmax_ious, label

    def _calc_ious(self, anchor, bbox, inside_index):
        ious = bbox_iou(anchor, bbox)
        argmax_ious = ious.argmax(axis=1)
        max_ious = ious[np.arange(len(inside_index)), argmax_ious]

        gt_argmax_ious = ious.argmax(axis=0)
        gt_max_ious = ious[gt_argmax_ious, np.arange(ious.shape[1])]
        gt_argmax_ious = np.where(ious==gt_max_ious)[0]

        return argmax_ious, max_ious, gt_argmax_ious
