# _*_coding     : UTF_8_*_
# Author        :Jie Shen
# CreatTime     :2022/1/28 17:21

import torch
from src.js_torch.d2l_torch import synthetic_data
true_w = torch.tensor([2, -3.4])
true_b = 4.2
features, labels = synthetic_data(true_w, true_b, 1000)
print(type(features))
print(type(labels))
