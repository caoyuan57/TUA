from omegaconf import OmegaConf

import torch

from utils import get_loader
from models import TUA, HashModel

from models import AlexNet

torch.multiprocessing.set_sharing_strategy("file_system")

attack_conf_root = "./configs/attack.yaml"
attack_conf = OmegaConf.load(attack_conf_root)

attacked_model = AlexNet(num_bits=attack_conf.num_bits)
checkpoint = torch.load("./checkpoints/csq_nuswide_21_32.pt")
attacked_model.load_state_dict(checkpoint)

model = None
model = TUA(attack_conf, attacked_model)

dataset = attack_conf.dataset

train_loader, test_loader, database_loader = get_loader(
    dataset, attack_conf.batch_size, attack_conf.num_workers
)

label_list = []
with open(f"./test_{attack_conf.dataset}.txt", "r") as f:
    for line in f:
        label = line.split()
        label_list.append(torch.tensor(list(map(int, label))))

if __name__ == "__main__":
    mAP = 0.0
    for label in label_list:
        AP = model.train(train_loader, test_loader, database_loader, label)
        mAP += AP
    mAP /= len(label_list)
    print(mAP)
a
