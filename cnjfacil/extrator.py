import re

from .exceptions import CNJIncorrigivel, CNJPontuacaoIncorreta


class ExtratorCNJ:
    """
    Busca em um texto por um possível número  CNJ e os extrai, corrigindo
    quando possível

    Args:
        Texto (str): Texto em que os CNJs serão encontrados
    """

    ORDEM = r'\d\s*\d?\s*\d?\s*\d?\s*\d?\s*\d?\s*\d?\s*'
    VERIFICADOR = r'[- .]?\d\s*\d\s*'
    ANO = r'\.?\d\s*\d\s*\d\s*\d\s*'
    DIGITO = r'\.?\d\s*'
    TRIBUNAL = r'\.?\d\s*\d\s*'
    ORIGEM = r'\.?\d\s*\d\s*\d\s*\d'
    REGEX = re.compile(''.join(
        [ORDEM, VERIFICADOR, ANO, DIGITO, TRIBUNAL, ORIGEM]))
    FORMATO_CNJ = re.compile(r'(\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4})')

    def __init__(self, texto, maximo_tentativas=10):
        self.texto = texto
        self._buscador = self.REGEX
        self._cnjs = set()
        self.maximo_tentativas = maximo_tentativas

    @property
    def cnjs(self):
        if not self._cnjs:
            self._busca_cnjs()

        return self._cnjs

    def _busca_cnjs(self):
        cnjs = self._buscador.findall(self.texto)
        return self._corrige_cnjs(cnjs)

    def _valida_cnj(self, cnj):
        if self.FORMATO_CNJ.match(cnj):
            return
        elif '-' not in cnj or '.' not in cnj:
            raise CNJPontuacaoIncorreta
        else:
            raise CNJIncorrigivel

    def _corrige_cnjs(self, cnjs):
        for cnj in cnjs:
            cnj = re.sub('\s', '', cnj, flags=re.M | re.I)
            try:
                self._cnjs.add(self._corrige_cnj(cnj))
            except CNJIncorrigivel:
                pass

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
