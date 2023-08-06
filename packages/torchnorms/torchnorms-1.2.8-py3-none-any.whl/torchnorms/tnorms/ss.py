# -*- coding: utf-8 -*-

import torch
from torch import nn, Tensor

from torchnorms.tnorms.base import BaseTNorm

from typing import Optional


class SchweizerSklarTNorm(BaseTNorm):
    def __init__(self,
                 p: Optional[Tensor] = None,
                 default_p: float = 0.1) -> None:
        super().__init__()
        self.p = p
        if self.p is None:
            self.p = nn.Parameter(torch.tensor(default_p))
        assert len(self.p.shape) == 0

        self.relu = torch.nn.ReLU()
        self.eps = 0.001

    def __call__(self,
                 a: Tensor,
                 b: Tensor) -> Tensor:
        res: Optional[Tensor] = None


        # Careful that the value of parametr p can be 10e-8, thus maybe add eps.

        if torch.isnan(self.p):
            print("NAN a BRAT")
            self.p.data = torch.tensor(0.1)
        # print(res)
        # print(a,b)
        # print(self.p)
        if self.p.item() < 0.0:
            # print(1)
            res: Tensor = (a ** self.p + b ** self.p - 1.0) ** (1.0 / self.p)
            # print(res)
        elif self.p.item() == 0.0:
            # print(2)
            res: Tensor = a * b
            # print(res)
        elif self.p.item() > 0.0:
            # print(3)
            res: Tensor = (a ** self.p + b ** self.p - 1.0)
            res: Tensor = torch.max(res, torch.tensor(0.0))
            res: Tensor = res ** (1.0 / self.p)
            # print(res)

        return res
