# base datasets
from .base import BaseDataset, CVDataset, CVClassificationDataset, SegmentationDataset

# computer vision datasets

# classification tasks
from .mnist import MNIST
from .fashion_mnist import FashionMNIST

from .cifar10 import CIFAR10
from .cifar100 import CIFAR100

from .svhn import SVHN

from .tiny_imagenet import TinyImageNet

# segmentation
from .voc import VOCSegmentationDataset
