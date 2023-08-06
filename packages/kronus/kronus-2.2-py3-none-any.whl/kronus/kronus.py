#! /usr/bin/python3
# ------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
#+ Autor:	Ran#
#+ Creado:	2019/07/20 12:38:02
#+ Editado:	2022/02/05 21:18:24.157507
# ------------------------------------------------------------------------------
from datetime import datetime as dt
import os
import sys

from .kronus_uteis import lazy_check_types
from .excepcions import ErroTipado

# ------------------------------------------------------------------------------
# agora
def agora(separador: str = '') -> str:
    """
    Formatador de datas en texto estándar.
    Devolvese como str porque é máis versátil, pero un simple cast a int sería
    suficiente para convertilo a int.

    Exemplo:
    +20190710095500000000
    → +2019 07 10 09 55 00 000000

    +(1)	→ a.C 			→ 1bit
    ou
    -(0)	→ d.C 			→ Mesmo bit
    2019 	→ ano 			→ Nbits
    07 		→ mes 			→ 2bits
    10 		→ día 			→ 2bits
    55 		→ minuto 		→ 2bits
    00 		→ segundo 		→ 2bits
    000000 	→ microsegundo 	→ 6bits

    Comando para sacar os valores precisos
    echo -n '+';date +"%Y-%m-%d %H:%M:%S:%6N"

    @entradas:
        Ningunha

    @saídas:
        Enteiro -   Sempre
        └ Co timestamp
    """

    agora = dt.now()

    valores = [
            agora.year,
            '%02d' % agora.month,
            '%02d' % agora.day,
            '%02d' % agora.hour,
            '%02d' % agora.minute,
            '%02d' % agora.second,
            '%06d' % agora.microsecond
            ]

    return '+'+f'{separador}'.join([str(ele) for ele in valores])

# separar
def separar(agora: str) -> str:
    """
    Dado un timestamp tipo khronos devolveo de forma máis dixestible.

    @entradas:
        agora   -   Requirido   -   Catex
        └ Co timestamp tipo khronos.

    @saídas:
        Catex   -   Sempre
        └ Co timestamp tipo khronos separado para mellor visibilidade.
    """

    if not lazy_check_types(agora, str):
        raise ErroTipado('O tipo da variable non é o esperado (catex)')

    if len(agora) < 16:
        raise ErroTipado('A lonxitude non é a adecuada.')

    if not agora[1:].isdigit():
        raise ErroTipado('O elemento non é un catex que contén un enteiro')

    return ' '.join([
                agora[0],           # ac/dc
                agora[:-16][1:],    # ano
                agora[-16:-14],     # mes
                agora[-14:-12],     # día
                agora[-12:-10],     # hora
                agora[-10:-8],      # minuto
                agora[-8:-6],       # segundo
                agora[-6:]          # microsegundo
                ])
# ------------------------------------------------------------------------------
