# -*- coding: utf-8 -*-

import torch
from torch import nn, Tensor

from torchnorms.tconorms.base import BaseTCoNorm

from typing import Optional


class DombiTCoNorm(BaseTCoNorm):
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


            if self.p == 0:
                self.p += self.eps # eps is added to avoid 0


            res = 1.0 - (((1-a) * (1-b)) / torch.maximum(torch.maximum(1.0 - a, 1.0 - b), self.p))


            return res
