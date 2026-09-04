# Guia de Utilizador

## Instalação

```bash
pip install -e .
# ou sem instalar
PYTHONPATH=src python -m valida_nif_py
```

## Uso como Módulo

```python
from valida_nif_py import valida_nif, completa_nif, classifica_nif, classifica_nif_detalhado
from src.valida_nif_py import valida_nif  # layout src

valida_nif("123456789")          # True
valida_nif("PT123456789")        # True
valida_nif("Pt123456789")        # False (prefixo case-sensitive)
valida_nif(123456789)            # True (int aceite)

completa_nif("12345678")         # "123456789"
completa_nif("PT12345678")       # "123456789"

classifica_nif("123456789")      # "A"
classifica_nif("500000001")      # "C" - Pessoa Coletiva
classifica_nif("600000001")      # "D" - Organismos Publicos
classifica_nif("000000000")      # "X" - invalido

classifica_nif_detalhado("123456789")
# {"indice":"A","categoria":"Pessoa Singular - Residente",...,"valido":True,"nif":"123456789"}
```

## CLI

```bash
python valida_nif_py.py --valida_nif 123456789        # valido (exit 0) / invalido (exit 1)
python valida_nif_py.py --valida_nif PT123456789
python valida_nif_py.py --completa 12345678           # 123456789
python valida_nif_py.py --classifica 123456789        # A - Pessoa Singular - Residente
python valida_nif_py.py --classifica 500000001 --csv  # csv header + linha
python -m src.valida_nif_py --classifica 123456789    # via src
```

## Códigos de Saída

- `0` valido/encontrado
- `1` invalido/classificacao X
- `2` erro de argumentos/completa invalida

## Notas

- Aceita `PT`/`pt` apenas; `Pt`/`pT`/`ES` = invalido.
- `classifica_nif` valida checksum primeiro; NIF com prefixo certo mas digito errado = `X`.
