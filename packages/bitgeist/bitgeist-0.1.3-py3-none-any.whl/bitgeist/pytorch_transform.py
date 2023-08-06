"""C converter for deep neural network pytorch models

This script provides a toolkit to convert pytorch deepl learning models to c.

This file can also be imported as a module and contains the following
functions:

    * transform - transforms a (trained) pytorch module to _C_ source code.


"""
from typing import Callable

import torch.nn as nn

import bitgeist.transform as gs
from bitgeist.layers import Linear
from bitgeist.transform import MetaObjects


def transform(model: nn.Module, template: str = "./bitgeist/resources/ctemplate.tpl.c"):
    """Initializes the deep neural net layer builder

    Parameters
    ----------
    model : nn.Module
        The root pytorch module to be transformed

    template : str
        _C_ text template

    Returns
    -------
    str
        the transformed c source code.
    """
    meta_info = gs.MetaInfo()
    layers: list[Callable[[str, str, int], MetaObjects]] = [meta_info(gs.entry())]
    for layer in model.children():
        if type(layer) == Linear:
            values = layer.lin.binary_weights.numpy()
            bias = layer.bias.bias_values(1000)
            m, n = values.shape
            layers += [
                meta_info.enrich(gs.activation_binarization(bias)),
                meta_info.enrich(gs.dense(m, list(values))),
            ]
        if type(layer) == nn.PReLU:
            layers += [meta_info.enrich(gs.relu())]
    layers += [meta_info.enrich(gs.argmax())]

    return gs.model_transform(layers, 28 * 28, template)
