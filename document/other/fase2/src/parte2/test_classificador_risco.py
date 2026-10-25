"""Testes de integridade e isolamento do treino, sem exigir uma acurácia."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path
import pandas as pd
from classificador_risco import BASE_DIR, carregar_dados, criar_modelo


class TestAvaliacao(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        for nome in ('frases_risco.csv', 'proveniencia_frases.csv', 'divisao_avaliacao.csv', 'protocolo_avaliacao.json'):
            shutil.copyfile(BASE_DIR / nome, self.base / nome)

    def test_divisao_cobre_base_sem_sobreposicao(self):
        dados = carregar_dados(self.base)
        self.assertEqual(len(dados), 60)
        grupos = [set(dados.loc[dados.conjunto == parte, 'grupo_avaliacao']) for parte in ('treino', 'teste')]
        self.assertFalse(grupos[0] & grupos[1])

    def test_rejeita_grupo_entre_conjuntos(self):
        p = self.base / 'divisao_avaliacao.csv'
        df = pd.read_csv(p)
        df.loc[df.conjunto == 'treino', 'grupo_avaliacao'] = df.loc[df.conjunto == 'teste', 'grupo_avaliacao'].iloc[0]
        df.to_csv(p, index=False)
        with self.assertRaisesRegex(ValueError, 'Vazamento'):
            carregar_dados(self.base)

    def test_rejeita_proveniencia_divergente(self):
        p = self.base / 'proveniencia_frases.csv'
        df = pd.read_csv(p, keep_default_na=False)
        df.loc[0, 'frase'] = 'Texto diferente do CSV'
        df.to_csv(p, index=False)
        with self.assertRaisesRegex(ValueError, 'divergente'):
            carregar_dados(self.base)

    def test_rejeita_snapshot_modificado(self):
        p = self.base / 'protocolo_avaliacao.json'
        meta = json.loads(p.read_text(encoding='utf-8'))
        meta['sha256']['frases_risco.csv'] = '0' * 64
        p.write_text(json.dumps(meta), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Arquivo alterado'):
            carregar_dados(self.base)

    def test_transform_nao_aprende_vocabulario_do_teste(self):
        modelo = criar_modelo()
        modelo.fit(['pressao toracica suor', 'bem estar melhora'], ['alto risco', 'baixo risco'])
        vocabulario = dict(modelo.named_steps['tfidf'].vocabulary_)
        modelo.predict(['xenotermoteste pressao'])
        self.assertEqual(vocabulario, modelo.named_steps['tfidf'].vocabulary_)
        self.assertNotIn('xenotermoteste', vocabulario)


if __name__ == '__main__':
    unittest.main(verbosity=2)
