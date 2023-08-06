import json
import os
import numpy as np

from decto.dataset.preprocess import read_image

class VIADataset(object):
    def __init__(self, data_dir, split):
        self.data_dir = data_dir
        self.split = split
        anns = json.load(open('{}/{}_annotation.json'.format(data_dir, split)))
        data = list(anns['_via_img_metadata'].values())
        self.data = self.filter_annotation(data)
        
    def filter_annotation(self, anns):
        data = []
        for ann in anns:
            fname = ann['filename']
            bbox = []
            label = []
            difficult = []
            for r in ann['regions']:
                shape_att = r['shape_attributes']
                region_att = r['region_attributes']
                
                if shape_att['name'] == 'rect' and 'x' in shape_att and 'loai_thong_tin' in region_att:
                    x, y, w, h = shape_att['x'], shape_att['y'], shape_att['width'], shape_att['height']
                    region_type = int(region_att['loai_thong_tin'])
                    
                    if x and y and w and h:
                        bbox.append((y, x, y+h, x+w))
                        label.append(region_type)
                        difficult.append(0)
            
            if len(bbox) > 0:
                data.append({'fname':fname, 'bbox':bbox, 'label':label, 'difficult':difficult})
                    
        
        return data
            
    def __len__(self):
        return len(self.data)
    
    def get_example(self, i):
        item = self.data[i]
        
        fname = item['fname']
        fname = os.path.join(self.data_dir, 'img', fname)
        bbox = item['bbox']
        label = item['label']
        difficult = item['difficult']
            
        img = read_image(fname, color=True)
        bbox = np.stack(bbox).astype(np.float32)
        label = np.stack(label).astype(np.int32)
        difficult = np.array(difficult, dtype=np.bool).astype(np.uint8)
        
        return img, bbox, label, difficult
