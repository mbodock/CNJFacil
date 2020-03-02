# encoding: utf-8

import datetime
from unittest import TestCase

from cnjfacil.extrator import ExtratorCNJ


class ExtratorTestCase(TestCase):

    def test_encontra_cnj_simples(self):
        texto = 'aqui está o cnj 0053087-35.2013.8.13.0693 veja bem'
        extrator = ExtratorCNJ(texto)
        self.assertEqual(extrator.cnjs, ['0053087-35.2013.8.13.0693'])

    def test_encontra_cnj_sem_char_entre_justica_tribunal(self):
        texto = 'aqui está o cnj 0053087-35.2013.813.0693 veja bem'
        extrator = ExtratorCNJ(texto)
        self.assertEqual(extrator.cnjs, ['0053087-35.2013.8.13.0693'])

    def test_encontra_multiplos_cnjs(self):
        texto = '''
        Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod
        tempor invidunt ut labore et 0053087-35.2013.8.13.0693dolore magna
        aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo
        dolores et ea rebum. 0516710-11.2017.8.13.0000Stet clita kasd
        gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.
        '''
        extrator = ExtratorCNJ(texto)
        self.assertEqual(extrator.cnjs, ['0053087-35.2013.8.13.0693',
                                         '0516710-11.2017.8.13.0000'])

    def test_encontra_cnj_sem_hifen(self):
        texto = 'aqui está o cnj 005308735.2013.8.13.0693 veja bem'
        extrator = ExtratorCNJ(texto)
        self.assertEqual(extrator.cnjs, ['0053087-35.2013.8.13.0693'])

    def test_encontra_cnj_sem_pontuacao(self):
        texto = 'aqui está o cnj 530873520138130693 veja bem'
        extrator = ExtratorCNJ(texto)
        self.assertEqual(extrator.cnjs, ['0053087-35.2013.8.13.0693'])

    def test_cnj_sem_zeros_esquerda(self):
        texto = 'aqui está o cnj 5308735.2013.8.13.0693 veja bem'
        extrator = ExtratorCNJ(texto)
        self.assertEqual(extrator.cnjs, ['0053087-35.2013.8.13.0693'])

    def test_cnj_quebra_de_linha(self):
        texto = '''aqui está o cnj 53087
        3520138.13.0693 veja bem'''
        extrator = ExtratorCNJ(texto)
        self.assertEqual(extrator.cnjs, ['0053087-35.2013.8.13.0693'])

    def test_cnj_incorrigivel(self):
        texto = '''aqui está o cnj 530873
        520138.13.0693 veja bem'''
        extrator = ExtratorCNJ(texto, maximo_tentativas=0)
        self.assertEqual(extrator.cnjs, list())

    def test_cnjs_repetidos_aparecem_apenas_uma_vez(self):
        texto = '''0053087-35.2013.8.13.0693 texto
                0516710-11.2017.8.13.0000 e 0516710-11.2017.8.13.0000
                '''
        extrator = ExtratorCNJ(texto)
        self.assertEqual(extrator.cnjs, ['0053087-35.2013.8.13.0693',
                                         '0516710-11.2017.8.13.0000'])

    def test_nao_adiciona_valores_com_ano_do_cnj_invalido(self):
        texto = '''
        tempor invidunt ut labore et 0053087-35.2013.8.13.0693dolore magna
        dolores et ea rebum. 0000020-03.8100.0.04.2970Stet clita kasd
        tempor invidunt ut labore et 0064198-46.0013.9.24.1704dolore magna
        '''
        extrator = ExtratorCNJ(texto)
        self.assertEqual(extrator.cnjs, ['0053087-35.2013.8.13.0693'])

    def test_valida_cnj_ano_atual(self):
        ano = datetime.datetime.utcnow().year
        cnj = '0053087-35.{}.8.13.0693'.format(ano)
        extrator = ExtratorCNJ(cnj)
        self.assertEqual(extrator.cnjs, [cnj])

    def test_valida_cnj_ano_no_futuro_proximo(self):
        ano_proximo = datetime.datetime.utcnow().year + 2
        cnj = '0053087-35.{}.8.13.0693'.format(ano_proximo)
        extrator = ExtratorCNJ(cnj)
        self.assertEqual(extrator.cnjs, [cnj])
