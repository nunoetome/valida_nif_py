# Guia de Utilizador

## Instalação

```bash
pip install -e .
# ou sem instalar
PYTHONPATH=src python -m valida_nif
```

## Uso como Módulo

```python
from valida_nif import valida_nif, completa_nif, classifica_nif, classifica_nif_detalhado

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
python -m valida_nif --valida_nif 123456789        # valido (exit 0) / invalido (exit 1)
python -m valida_nif --valida_nif PT123456789
python -m valida_nif --completa 12345678           # 123456789
python -m valida_nif --classifica 123456789        # A - Pessoa Singular - Residente
python -m valida_nif --classifica 500000001 --csv  # csv header + linha
python src/valida_nif.py --classifica 123456789    # ficheiro direto em src/
# após pip install -e . (requer venv ativo):
valida-nif --valida_nif 123456789
valida-nif --completa 12345678
```

## Códigos de Saída

- `0` valido/encontrado
- `1` invalido/classificacao X
- `2` erro de argumentos/completa invalida

## Notas

- Aceita `PT`/`pt` apenas; `Pt`/`pT`/`ES` = invalido.
- `classifica_nif` valida checksum primeiro; NIF com prefixo certo mas digito errado = `X`.
