import torch

from omegaconf import OmegaConf

from models import HashModel
from utils import get_loader

torch.multiprocessing.set_sharing_strategy("file_system")

conf_root = "./configs/hashing.yaml"
conf = OmegaConf.load(conf_root)

dataset = conf.dataset
model = HashModel(conf)

train_loader, test_loader, database_loader = get_loader(
    dataset, conf.batch_size, conf.num_workers
)

if __name__ == "__main__":
    if conf.train:
        model.train(train_loader, test_loader, database_loader)
    if conf.test:
        model.load_model()
        model.test(test_loader, database_loader)
