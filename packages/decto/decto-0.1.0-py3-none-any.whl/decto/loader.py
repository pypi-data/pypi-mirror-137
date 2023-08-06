from torch.nn import functional as F

from torchvision import transforms as tvtsf

def normalize(img):
    """
    https://github.com/pytorch/vision/issues/223
    return appr -1~1 RGB
    """
    normalize = tvtsf.Normalize(mean=[0.485, 0.456, 0.406],
                                std=[0.229, 0.224, 0.225])
    img = normalize(img)
    return img

def resize_image(img, min_size=600, max_size=1000):
    _, C, H, W = img.shape
    scale1 = min_size / min(H, W)
    scale2 = max_size / max(H, W)
    scale = min(scale1, scale2)    
    new_H = int(H * scale)
    new_W = int(W * scale)
    
    img = F.interpolate(img, (new_H, new_W))
    
    return img

def preprocess(img, min_size=600, max_size=1000):
    """Preprocess an image for feature extraction.
    The length of the shorter edge is scaled to :obj:`self.min_size`.
    After the scaling, if the length of the longer edge is longer than
    :param min_size:
    :obj:`self.max_size`, the image is scaled to fit the longer edge
    to :obj:`self.max_size`.
    After resizing the image, the image is subtracted by a mean image value
    :obj:`self.mean`.
    Args:
        img (~numpy.ndarray): An image. This is in CHW and RGB format.
            The range of its value is :math:`[0, 255]`.
    Returns:
        ~numpy.ndarray: A preprocessed image.
    """
    img = resize_image(img, min_size, max_size)
    img = img / 255.
    img = normalize(img)

    # both the longer and shorter should be less than
    # max_size and min_size

    return img
