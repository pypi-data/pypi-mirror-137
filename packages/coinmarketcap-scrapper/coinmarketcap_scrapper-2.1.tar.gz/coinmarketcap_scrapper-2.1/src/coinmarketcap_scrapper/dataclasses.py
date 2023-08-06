#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#+ Autor:  	Ran#
#+ Creado: 	2022/01/30 12:54:52.834338
#+ Editado:	2022/01/30 13:03:14.874110
# ------------------------------------------------------------------------------
from dataclasses import dataclass
from typing import List
# ------------------------------------------------------------------------------
@dataclass
class Dominancia:
    moeda: str
    porcentaxe: str

@dataclass
class Info:
    cryptos: str
    exchanges: str
    market_cap: str
    vol_24h: str
    dominance: List[Dominancia]
    eth_gas: str
# ------------------------------------------------------------------------------
