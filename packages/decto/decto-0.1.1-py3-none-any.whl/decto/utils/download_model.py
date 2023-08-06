import gdown
import requests
import yaml

def download_weights(id_or_url, cached=None, md5=None, quiet=False):
    if id_or_url.startswith('http'):
        url = id_or_url
    else:
        url = 'https://drive.google.com/uc?id={}'.format(id_or_url)

    return gdown.cached_download(url=url, path=cached, md5=md5, quiet=quiet)

def download_config(id):
    url = 'https://raw.githubusercontent.com/pbcquoc/config/master/decto/{}.yml'.format(id)
    r = requests.get(url)
    config = yaml.safe_load(r.text)
    return config

def map_state_dict(model, state_dict):
    new_state_dict = {}
    required_state_dict = model.state_dict()
    
    for k, v in required_state_dict.items():
        if k in state_dict:
            if v.size() == state_dict[k].size():
                new_state_dict[k] = state_dict[k]
            else:
                print('pretrained weight dont match current weight shape {}'.format(k))
        else:
            print('not found weight for {}'.format(k))

    return new_state_dict
