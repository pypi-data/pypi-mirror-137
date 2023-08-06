import argparse

from decto.model.trainer import Trainer
from decto.utils.config import Cfg

def train(train_file, test_file, device, resume):
    config = Cfg.load_config_from_name('resnet101_fpn')
    
    train_config = config['train_config']
    train_config['train_file'] = train_file
    train_config['test_file'] = test_file
    train_config['device'] = device

    trainer = Trainer(config)
    
    if resume:
        trainer.load_checkpoint()

    trainer.train()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_file', required=True, help='foo help')
    parser.add_argument('--test_file', required=True, help='foo help')
    parser.add_argument('--device', default='cuda:0', help='foo help')
    parser.add_argument('--resume', action='store_true')
   
    args = parser.parse_args()

    train(args.train_file, args.test_file, args.device, args.resume)     
