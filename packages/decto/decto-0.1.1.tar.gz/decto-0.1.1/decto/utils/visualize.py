import numpy as np

import matplotlib 
import matplotlib.pyplot as plt
from matplotlib import figure

def visualize_bbox(img, bbox, label, label_names, score=None, ax=None, bbox_style={'linewidth':2, 'alpha':1.0}):
    label_names = label_names + ['bg']
    cmap = plt.cm.get_cmap("hsv", len(label_names)+1)
    
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        
#    img = img.transpose((1,2,0)).astype(np.uint8)
    img = img.astype(np.uint8)

    ax.imshow(img)    
    
    for i, bb in enumerate(bbox):
        xy = (bb[1], bb[0])
        height = bb[2] - bb[0]
        width = bb[3] - bb[1]
        
        ax.add_patch(plt.Rectangle(xy, width, height, fill=False, edgecolor=cmap(label[i]), **bbox_style))
        
        lb = label_names[label[i]]
        
        if score is not None:
            sc = score[i]
            caption = '{}: {:.2f}'.format(lb, sc)
        else:
            caption = lb
        
        ax.text(bb[1], bb[0], caption, style='italic',
               bbox={'facecolor': 'white', 'alpha':0.5, 'pad':0})
    
    return ax

def visualize_prediction(img, detail_prediction, label_names, log_dir, figname):
        bbox, label, score, roi, roi_fg_score = detail_prediction
        
        keep = roi_fg_score.argsort()[-50:]
        
        roi = roi[keep]
        roi_fg_score = roi_fg_score[keep]
        
        fig = figure.Figure(figsize=(20, 12), tight_layout=True)
        axs = fig.subplots(1, 2)

        visualize_bbox(img, roi, [0]*len(roi), ['roi'], roi_fg_score, axs[0])
        visualize_bbox(img, bbox, label, label_names, score, axs[1])
        
        fig.savefig('{}/{}.jpg'.format(log_dir, figname))
        plt.close()
