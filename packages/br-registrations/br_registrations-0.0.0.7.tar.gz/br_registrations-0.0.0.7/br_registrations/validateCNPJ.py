# _*_ coding: utf-8_*_
import re
"""
@Author       : sliatecinos
@Created Time : 2021-01-19 20:57:00
@Updated Time : 2021-02-07 02:20:00
@BR Registrations
    environments:

"""


class CNPJ:
    """
    A simple Python library containing functions that check Brazilian documents values.
    It is intended to make it easy to verify CNPJ numbers.
    """
    @staticmethod
    def get_cnpj_dv(inscricao: str, regex: bool=False) -> list:
        """Returns a list of last two numbers to registration number of CNPJ.
        Ex: return_cnpj_dv('112223330001') -> 81 
            return_cnpj_dv('46.293.332/0001') -> 02
        """
        if regex:
            inscricao=re.findall("\d+", inscricao)
            inscricao=''.join(inscricao)

        DV = []
        ALINHAMENTO=[6,5,4,3,2,9,8,7,6,5,4,3,2]
        inscricao = list(inscricao.zfill(12))
        # retorna DV_1
        inscricao_1 = list(map(int, inscricao))
        somatorio=list(zip(inscricao_1, ALINHAMENTO[1:]))   # usa parte do alinhamento
        DV_1=sum(map(lambda x: x[0]*x[1], somatorio)) % 11
        DV_1 = 0 if DV_1 < 2 else 11 - DV_1
        DV.append(DV_1)

        # retorna DV_2
        inscricao_2 = list(map(int, inscricao))
        inscricao_2.extend(DV)
        somatorio=list(zip(inscricao_2, ALINHAMENTO[:]))   # usa todo alinhamento
        DV_2=sum(map(lambda x: x[0]*x[1], somatorio)) % 11
        DV_2 = 0 if DV_2 < 2 else 11 - DV_2
        DV.append(DV_2)

        return DV

    @staticmethod
    def valid_cnpj(cnpj: str, regex: bool=False) -> bool:
        """Returns True (valid) or False (invalid) to a full-number of CNPJ.
        Ex: valid_cnpj('11222333000181') -> True
            valid_cnpj('46.293.332/0001-02') -> True
        """
        if regex:
            cnpj=re.findall("\d+", cnpj)
            cnpj=''.join(cnpj)

        inscricao = cnpj[:-2]
        dv = list(map(int, cnpj[-2:]))
        dv_teste=CNPJ.get_cnpj_dv(inscricao)
        
        valida = False
        if dv_teste == dv:
            valida = True

        return valida

