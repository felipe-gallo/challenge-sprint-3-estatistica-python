# ARTHUR MAZIVIERO FARIA - RM 573928
# JUN UEHARA - RM 570537
# FELIPE DE SOUZA GALLO - RM 569680
# ROBERSON REGUERO LUIZ JUNIOR - RM 573031
# TOMMASO CONCEIÇÃO NAGLIATTI - RM 572147
# MATHEUS MARTINS LACERDA - RM 570843

"""Testes automatizados dos cálculos principais."""

import sys
import unittest
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from analise_estatistica import (  # noqa: E402
    ajustar_regressao,
    calcular_probabilidades,
    carregar_dados,
    classificar_evento,
)


class TestAnaliseEstatistica(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dados = carregar_dados(RAIZ / "dados" / "dados_familias.csv")

    def test_base_tem_50_registros(self):
        self.assertEqual(len(self.dados), 50)

    def test_probabilidade_acima_mediana(self):
        resultado = calcular_probabilidades(self.dados)
        self.assertAlmostEqual(resultado["mediana"], 2127.0, places=2)
        self.assertAlmostEqual(
            resultado["probabilidade_acima_mediana"], 0.443619, places=5
        )
        self.assertEqual(resultado["classificacao_acima_mediana"], "provável")

    def test_probabilidade_intervalo_dois_desvios(self):
        resultado = calcular_probabilidades(self.dados)
        self.assertAlmostEqual(resultado["probabilidade_intervalo_2s"], 0.9545, places=4)
        self.assertEqual(resultado["classificacao_intervalo_2s"], "quase certo")

    def test_regressao_linear(self):
        _, metricas = ajustar_regressao(self.dados)
        self.assertAlmostEqual(metricas["intercepto"], 207.9033, places=3)
        self.assertAlmostEqual(metricas["coeficiente_angular"], 0.2973, places=3)
        self.assertAlmostEqual(metricas["r_quadrado"], 0.9699, places=3)

    def test_classificacao_rejeita_probabilidade_invalida(self):
        with self.assertRaises(ValueError):
            classificar_evento(1.1)


class TestValidacaoEntrega(unittest.TestCase):
    def test_autoria_no_csv(self):
        dados = carregar_dados(RAIZ / 'dados/dados_familias.csv')
        autores = (RAIZ / 'integrantes.txt').read_text(encoding='utf-8-sig').strip().splitlines()
        for autor in autores:
            self.assertTrue(dados['autores_trabalho'].str.contains(autor, regex=False).all())

    def test_limites_classificacao(self):
        for valor, esperado in [(0, 'raro'), (0.05, 'raro'), (0.25, 'pouco provável'),
                                (0.75, 'provável'), (1, 'quase certo')]:
            self.assertEqual(classificar_evento(valor), esperado)
        for valor in [-1, 2, float('nan')]:
            with self.assertRaises(ValueError):
                classificar_evento(valor)

    def test_bases_invalidas(self):
        import tempfile
        casos = ['renda_familiar,gasto_familiar\n1,2\n',
                 'renda_familiar,outro\n1,2\n3,4\n',
                 'renda_familiar,gasto_familiar\n1,\n3,4\n',
                 'renda_familiar,gasto_familiar\n1,abc\n3,4\n',
                 'renda_familiar,gasto_familiar\n1,inf\n3,4\n']
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / 'invalida.csv'
            for conteudo in casos:
                with self.subTest(conteudo=conteudo):
                    caminho.write_text(conteudo, encoding='utf-8')
                    with self.assertRaises(ValueError):
                        carregar_dados(caminho)

    def test_normal_sem_variacao(self):
        dados = carregar_dados(RAIZ / 'dados/dados_familias.csv')
        dados['gasto_familiar'] = 100
        with self.assertRaises(ValueError):
            calcular_probabilidades(dados)

    def test_regressao_sem_variacao(self):
        dados = carregar_dados(RAIZ / 'dados/dados_familias.csv')
        dados['renda_familiar'] = 100
        with self.assertRaises(ValueError):
            ajustar_regressao(dados)


if __name__ == "__main__":
    unittest.main()
