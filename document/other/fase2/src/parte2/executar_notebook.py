"""Executa o notebook usando exatamente o Python que chamou este script."""
from pathlib import Path
import json
import sys
import tempfile
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager

BASE = Path(__file__).resolve().parent

def main():
    notebook = BASE / 'classificador_risco.ipynb'
    nb = nbformat.read(notebook, as_version=4)
    with tempfile.TemporaryDirectory(prefix='cardioia-kernel-') as tmp:
        kernel = Path(tmp) / 'python3'
        kernel.mkdir()
        (kernel/'kernel.json').write_text(json.dumps({
            'argv':[sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}'],
            'display_name':'Python 3 (CardioIA)', 'language':'python',
        }), encoding='utf-8')
        manager = KernelManager(kernel_name='python3', kernel_spec_manager=KernelSpecManager(kernel_dirs=[tmp]))
        client = NotebookClient(nb, km=manager, timeout=180, allow_errors=False,
                                resources={'metadata':{'path':str(BASE)}})
        client.execute()
    nbformat.validate(nb)
    if any(o.output_type == 'error' for c in nb.cells if c.cell_type == 'code' for o in c.outputs):
        raise RuntimeError('Notebook contém saída de erro.')
    nbformat.write(nb, notebook)
    print('Notebook executado e salvo com saídas; células com erro: 0.')

if __name__ == '__main__':
    main()
