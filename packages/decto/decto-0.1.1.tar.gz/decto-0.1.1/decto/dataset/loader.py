import torch

from decto.dataset.preprocess import preprocess
from decto.dataset.augmentation import resize_bbox, random_flip, flip_bbox
from decto.dataset.VOCDataset import VOCBboxDataset
from decto.dataset.VIADataset import VIADataset

class Transform(object):

    def __init__(self, min_size=600, max_size=1000):
        self.min_size = min_size
        self.max_size = max_size

    def __call__(self, in_data):
        img, bbox, label = in_data
        _, _, H, W = img.shape
        
        img = preprocess(img, self.min_size, self.max_size)
        _, _, o_H, o_W = img.shape
        scale = o_H / H
        bbox = resize_bbox(bbox, (H, W), (o_H, o_W))
        
                # horizontally flip
        img, params = random_flip(
            img, x_random=True, return_param=True)
        bbox = flip_bbox(
            bbox, (o_H, o_W), x_flip=params['x_flip'])
        
        return img, bbox, label, scale


class Dataset:
    def __init__(self, data_dir, split='trainval', min_size=600, max_size=800, **kwargs):
        self.db = VOCBboxDataset(data_dir, split=split)
#         self.db = VIADataset(data_dir, split=split)
    
        self.tsf = Transform(min_size, max_size)

    def __getitem__(self, idx):
        ori_img, bbox, label, difficult = self.db.get_example(idx)
        
        ori_img = torch.from_numpy(ori_img[None])
        
        img, bbox, label, scale = self.tsf((ori_img, bbox, label))
        
        img = img[0]
        # TODO: check whose stride is negative to fix this instead copy all
        # some of the strides of a given numpy array are negative.
        return img, bbox, label, scale

    def __len__(self):
        return len(self.db)

class TestDataset:
    def __init__(self, data_dir, split='test', use_difficult=True, **kwargs):
        self.db = VOCBboxDataset(data_dir, split=split, use_difficult=use_difficult)
#         self.db = VIADataset(data_dir, split=split)
    
    def __getitem__(self, idx):
        img, bbox, label, difficult = self.db.get_example(idx)
        
        return img, bbox, label, difficult

    def __len__(self):
        return len(self.db)
