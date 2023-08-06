import argparse
import numpy as np
from PIL import Image

from decto.model.predictor import Predictor
from decto.utils.config import Cfg
from decto.utils.visualize import visualize_prediction

def predict(img, weights, device, out_file):
    config = Cfg.load_config_from_name('resnet101_fpn')
    classes = config['dataset_config']['classes']

    predictor = Predictor(config, weights=weights, device=device)
    
    img = Image.open(img)
    img = np.array(img)

    pred = predictor.predict(img, return_roi=True, include_bg=True)

    visualize_prediction(img, pred, classes, './', out_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--img', required=True, help='foo help')
    parser.add_argument('--weights', required=True, help='foo help')
    parser.add_argument('--device', default='cuda:0', help='foo help')
    parser.add_argument('--out_file', default='out', help='foo help')

    args = parser.parse_args()

    predict(args.img, args.weights, args.device, args.out_file)

