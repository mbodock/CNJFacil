from unittest import TestCase

from cnjtools.extrator import ExtratorCNJ


class ExtratorTestCase(TestCase):

    def test_encontra_cnj_simples(self):
        texto = 'aqui está o cnj 0053087-35.2013.8.13.0693 veja bem'
        extrator = ExtratorCNJ(texto)
        self.assertEqual(extrator.cnjs, {'0053087-35.2013.8.13.0693'})

    def test_encontra_multiplos_cnjs(self):
        texto = '''
        Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod
        tempor invidunt ut labore et 0053087-35.2013.8.13.0693dolore magna
        aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo
        dolores et ea rebum. 0516710-11.2017.8.13.0000Stet clita kasd
        gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.
        '''
        extrator = ExtratorCNJ(texto)
        self.assertEqual(extrator.cnjs, {'0053087-35.2013.8.13.0693',
                                         '0516710-11.2017.8.13.0000'})

    def test_encontra_cnj_sem_hifen(self):
        texto = 'aqui está o cnj 005308735.2013.8.13.0693 veja bem'
        extrator = ExtratorCNJ(texto)
        self.assertEqual(extrator.cnjs, {'0053087-35.2013.8.13.0693'})

    def test_encontra_cnj_sem_pontuacao(self):
        texto = 'aqui está o cnj 530873520138130693 veja bem'
        extrator = ExtratorCNJ(texto)
        self.assertEqual(extrator.cnjs, {'0053087-35.2013.8.13.0693'})

    def test_cnj_sem_zeros_esquerda(self):
        texto = 'aqui está o cnj 5308735.2013.8.13.0693 veja bem'
        extrator = ExtratorCNJ(texto)
        self.assertEqual(extrator.cnjs, {'0053087-35.2013.8.13.0693'})

    def test_cnj_quebra_de_linha(self):
        texto = '''aqui está o cnj 53087
        3520138.13.0693 veja bem'''
        extrator = ExtratorCNJ(texto)
        self.assertEqual(extrator.cnjs, {'0053087-35.2013.8.13.0693'})

    def test_cnj_incorrigivel(self):
        texto = '''aqui está o cnj 530873
        520138.13.0693 veja bem'''
        extrator = ExtratorCNJ(texto, maximo_tentativas=0)
        self.assertEqual(extrator.cnjs, set())
