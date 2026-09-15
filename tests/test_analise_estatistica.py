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


if __name__ == "__main__":
    unittest.main()
