"""Verificação das regras didáticas da Parte 1 (biblioteca padrão)."""
import unittest
from diagnostico_sintomas import carregar_mapa, analisar_relato, TXT_PATH


class TestExtracao(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mapa = carregar_mapa()

    def analisar(self, frase):
        return analisar_relato(frase, self.mapa)

    def test_dez_relatos_com_cobertura(self):
        frases = TXT_PATH.read_text(encoding="utf-8-sig").splitlines()
        frases = [frase for frase in frases if frase.strip()]
        self.assertEqual(len(frases), 10)
        for frase in frases:
            with self.subTest(frase=frase):
                self.assertTrue(self.analisar(frase)["sugestoes"])

    def test_acentos_e_caixa(self):
        self.assertEqual(self.analisar("PRESSAO NO TORAX")["pontuacoes"],
                         self.analisar("pressão no tórax")["pontuacoes"])

    def test_variantes_do_relato_cinco(self):
        resultado = self.analisar("Meu coração dispara e sinto palpitações.")
        self.assertEqual(len(resultado["encontrados"]), 2)
        self.assertEqual(resultado["pontuacoes"], {"Arritmia": 1})

    def test_desmaiei(self):
        self.assertEqual(self.analisar("Já desmaiei duas vezes.")["sugestoes"], ["Arritmia"])

    def test_sobreposicao(self):
        resultado = self.analisar("fadiga extrema")
        self.assertEqual([x["expressao"] for x in resultado["encontrados"]], ["fadiga extrema"])
        self.assertEqual(resultado["pontuacoes"], {"Angina": 1, "Insuficiência Cardíaca": 1})

    def test_sinonimos_e_repeticoes(self):
        resultado = self.analisar("dor no peito, aperto no peito e dor no peito")
        self.assertEqual(set(resultado["pontuacoes"].values()), {1})

    def test_empate_independente_da_ordem(self):
        frase = "dor no peito"
        primeiro = self.analisar(frase)
        invertido = analisar_relato(frase, list(reversed(self.mapa)))
        self.assertEqual(primeiro["sugestoes"], ["Angina", "Arritmia", "Infarto"])
        self.assertEqual(primeiro["pontuacoes"], invertido["pontuacoes"])
        self.assertEqual(primeiro["sugestoes"], invertido["sugestoes"])

    def test_limites_de_palavra(self):
        self.assertFalse(self.analisar("desmaiosinho")["encontrados"])

    def test_sem_correspondencia(self):
        self.assertEqual(self.analisar("Tenho coceira no pé.")["sugestoes"], [])

    def test_negacao_coordenada(self):
        resultado = self.analisar("Não tenho dor no peito nem falta de ar.")
        self.assertEqual(resultado["sugestoes"], [])
        self.assertEqual(len(resultado["negados"]), 2)

    def test_negacao_com_nova_afirmacao(self):
        for frase in ("Sem dor no peito, sinto palpitações.",
                      "Não tenho dor no peito mas sinto palpitações.",
                      "Não tenho dor no peito e sinto palpitações."):
            with self.subTest(frase=frase):
                self.assertEqual(self.analisar(frase)["sugestoes"], ["Arritmia"])

    def test_dificuldade_afirmada_com_nao(self):
        resultado = self.analisar("Não consigo dormir deitado.")
        self.assertEqual(resultado["sugestoes"], ["Insuficiência Cardíaca"])
        self.assertEqual(resultado["negados"], [])



    def test_adjetivo_no_relato_dez(self):
        resultado = self.analisar("desconforto constante no peito")
        self.assertEqual(len(resultado["encontrados"]), 1)
        self.assertEqual(resultado["encontrados"][0]["grupo"], "dor ou desconforto torácico")
        self.assertEqual(resultado["sugestoes"], ["Angina", "Arritmia", "Infarto"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
