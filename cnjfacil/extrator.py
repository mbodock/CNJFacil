# encoding: utf-8

import datetime
import re

from .exceptions import CNJIncorrigivel, CNJPontuacaoIncorreta


class ExtratorCNJ:
    """
    Busca em um texto por um possível número  CNJ e os extrai, corrigindo
    quando possível

    Args:
        Texto (str): Texto em que os CNJs serão encontrados
    """

    LOOKBEHIND = r'(?:(?<=\A)|(?<=[\sA-ü:ºª°.\-]))'

    ORDEM = r'\d\s*\d?\s*\d?\s*\d?\s*\d?\s*\d?\s*\d?\s*'
    VERIFICADOR = r'[- .]?\d\s*\d\s*'
    ANO = r'\.?\d\s*\d\s*\d\s*\d\s*'
    DIGITO = r'\.?\d\s*'
    TRIBUNAL = r'\.?\d\s*\d\s*'
    ORIGEM = r'\.?\d\s*\d\s*\d\s*\d'
    REGEX = re.compile(''.join(
        [LOOKBEHIND, ORDEM, VERIFICADOR, ANO, DIGITO, TRIBUNAL, ORIGEM]))
    FORMATO_CNJ = re.compile(r'(\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4})')

    def __init__(self, texto, maximo_tentativas=10):
        self.texto = texto
        self._buscador = self.REGEX
        self._cnjs = []
        self.maximo_tentativas = maximo_tentativas

    @property
    def cnjs(self):
        """Obtem a lista de cnjs encontrados no texto"""
        if not self._cnjs:
            self._busca_cnjs()
        self._valida_ano_do_cnj()

        return self._cnjs

    def _valida_ano_do_cnj(self):
        limite_inferior = 1895  # Ano do primeiro processo ajuizado do Brasil
        limite_superior = datetime.datetime.utcnow().year + 2  # Dois anos na frente
        self._cnjs = filter(
            lambda cnj: int(cnj[11::][:4]) <= limite_superior and int(cnj[11::][:4]) >= limite_inferior,
            self._cnjs
        )
        self._cnjs = list(self._cnjs)

    def _busca_cnjs(self):
        cnjs = self._buscador.findall(self.texto)
        return self._corrige_cnjs(cnjs)

    def _valida_cnj(self, cnj):
        if self.FORMATO_CNJ.match(cnj):
            return
        elif len(re.sub('[- .]', '', cnj)) >= 14:
            raise CNJPontuacaoIncorreta
        else:
            raise CNJIncorrigivel

    def _corrige_cnjs(self, cnjs):
        for cnj in cnjs:
            cnj = re.sub('\s', '', cnj, flags=re.M | re.I)
            try:
                cnj_corrigido = self._corrige_cnj(cnj)
            except CNJIncorrigivel:
                continue
            if cnj_corrigido not in self._cnjs:
                self._cnjs.append(cnj_corrigido)

    def _corrige_cnj(self, cnj, tentativas=0):
        if tentativas > self.maximo_tentativas:
            raise CNJIncorrigivel

        try:
            self._valida_cnj(cnj)
        except CNJPontuacaoIncorreta:
            cnj = re.sub('[- .]', '', cnj)
            return self._corrige_cnj(self._adiciona_pontuacao(cnj), tentativas + 1)
        return cnj

    def _adiciona_pontuacao(self, cnj):
        diferenca_tamanho = 20 - len(cnj)
        zeros_a_adicionar = '0' * diferenca_tamanho
        cnj = zeros_a_adicionar + cnj

        ordem = cnj[0:7]
        digito_verificador = cnj[7:9]
        ano = cnj[9:13]
        segmento = cnj[13]
        tribunal = cnj[14:16]
        origem = cnj[16:]
        return '{ordem}-{digito_verificador}.{ano}.{segmento}.{tribunal}.{origem}'.format(
            ordem=ordem, digito_verificador=digito_verificador, ano=ano,
            segmento=segmento, tribunal=tribunal, origem=origem)
