# _*_coding     : UTF_8_*_
# Author        :Jie Shen
# CreatTime     :2022/2/2 15:34

import torch


def synthetic_data(w, b, num_examples):
    """
    根据真实w,真实b,生成对应的label
    num_examples为生成的数量
      y = Xw + b + noise
    """
    x = torch.randn(num_examples, len(w))
    y = torch.matmul(x, w) + b
    # noise
    noise = torch.normal(0, 0.01, y.shape)
    y += noise
    return x, y.reshape(-1, 1)


def load_array(features, label, batch_size, shuffle):
    """
    data,label -> iter
    测试集，没必要shuffle，所以这里没有给shuffle指定默认值
    """
    dataset = torch.utils.data.TensorDataset(features, label)
    return torch.utils.data.DataLoader(dataset, batch_size, shuffle)


def train_epoch(net, trainer, loss, data_load, epochs):
    for _ in range(epochs):
        for fea, lab in data_load:
            l = loss(net(fea), lab)
            trainer.zero_grad()
            l.backward()
            trainer.step()
            print('batch loss: {}'.format(l))


