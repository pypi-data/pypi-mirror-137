#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#+ Autor:  	Ran#
#+ Creado: 	2022/01/02 13:32:22.843158
#+ Editado:	2022/01/15 23:10:45.395878
# ------------------------------------------------------------------------------
from .excepcions import ErroTipado
# ------------------------------------------------------------------------------
def lazy_check_types(varis, tipos) -> bool:
    """
    Dada unha lista de variables e outra de tipos vai mirando que estén correctos.
    Ante listas compostas tan só mira que os contidos da lista sexan todos iguais ó
    tipo especificado.

    @entrada:
        varis    -   Requirido   -   Lista de ou variable solitaria.
        └ Lista coas variables.
        tipos   -   Requirido   -   Lista de ou tipo solitario.
        └ Lista cos tipos das variables.

    @saída:
        Bool    -   Sempre
        └ Indicando se todo está correcto (True) ou se non (False)
    """

    # caso 1: '' e str
    if (type(varis) != list) and (type(tipos) != list):
        if type(varis) != tipos:
            return False
    # caso 2: ['', ''] e str
    elif (type(varis) == list) and (type(tipos) != list):
        # se a lista ten algo
        if varis:
            for vari in varis:
                if type(vari) != tipos:
                    return False
        # se está baleira e non é list: [] e !=list
        elif (not varis) and (tipos != list):
            return False
    # caso 3: ['', 0 ,['', '']] e [str, int, str]
    else:
        if len(varis) != len(tipos):
            raise ErroTipado('As listas tenhen que ter a mesma lonxitude')
        for vari, tipo in zip(varis, tipos):
            if not lazy_check_types(vari, tipo):
                return False
    return True
# ------------------------------------------------------------------------------
