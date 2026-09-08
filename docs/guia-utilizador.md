# Guia de Utilizador

## Instalação

```bash
pip install -e .
# ou sem instalar
PYTHONPATH=src python -m valida_nif
PYTHONPATH=src python -m valida_nif_es
```

## Uso como Módulo — PT

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

## Uso como Módulo — ES (DNI/NIE/CIF)

```python
from valida_nif_es import valida_nif_es, valida_dni, valida_nie, valida_cif
from valida_nif_es import completa_dni, completa_nie, completa_cif, completa_nif_es

valida_dni("12345678Z")          # True  (mod23 TRWAGMYFPDXBNJZSQVHLCKE)
valida_dni("12345678z")          # True  (case-insensitive)
valida_dni("12345678-Z")         # True  (hífen/espaço ignorado)
valida_dni("ES12345678Z")        # True  (ES/es)
valida_dni("Es12345678Z")        # False (prefixo case-sensitive)

valida_nie("X1234567L")          # True  (X→0 + mod23)
valida_nie("Y1234567X")          # True  (Y→1)
valida_nie("Z1234567R")          # True  (Z→2)
valida_nie("ESX1234567L")        # True

valida_cif("A58818501")          # True  (A só dígito)
valida_cif("Q2826000H")          # True  (Q só letra)
valida_cif("C12345674")          # True  (C ambos: dígito)
valida_cif("C1234567D")          # True  (C ambos: letra)
valida_cif("A5881850J")          # False (A não aceita letra)
valida_cif("Q28260004")          # False (Q não aceita dígito)

valida_nif_es("12345678Z")       # True (dispatcher DNI|NIE|CIF)
valida_nif_es("X1234567L")       # True
valida_nif_es("A58818501")       # True
valida_nif_es("ESA58818501")     # True

completa_dni("12345678")         # "12345678Z"
completa_nie("X1234567")         # "X1234567L"
completa_cif("A5881850")         # "A58818501"
completa_cif("Q2826000")         # "Q2826000H" (só letra)
completa_nif_es("12345678")      # "12345678Z" (infere DNI)
completa_nif_es("X1234567")      # "X1234567L" (infere NIE)
completa_nif_es("A5881850")      # "A58818501" (infere CIF)
```

## CLI — PT

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

## CLI — ES

```bash
python -m valida_nif_es --valida_nif 12345678Z       # valido/invalido
python -m valida_nif_es --valida_dni 12345678Z
python -m valida_nif_es --valida_nie X1234567L
python -m valida_nif_es --valida_cif A58818501
python -m valida_nif_es --completa 12345678          # 12345678Z (infere)
python -m valida_nif_es --completa_dni 12345678
python -m valida_nif_es --completa_nie X1234567
python -m valida_nif_es --completa_cif A5881850
python src/valida_nif_es.py --valida_nif 12345678Z   # ficheiro direto em src/
python valida_nif_es.py --valida_nif 12345678Z       # via shim raiz
# após pip install -e . (requer venv ativo):
valida-nif-es --valida_nif 12345678Z
valida_nif_es --valida_nif 12345678Z
valida-nif-es --valida_cif Q2826000H
valida-nif-es --completa S1234567  # S1234567D
```

## Códigos de Saída

- `0` valido/encontrado
- `1` invalido/classificacao X
- `2` erro de argumentos/completa invalida

Válido para PT e ES (mesmo `argparse` + `sys.exit`).

## Notas

- PT: aceita `PT`/`pt` apenas; `Pt`/`pT`/`ES` = invalido.
- ES: aceita `ES`/`es` apenas; `Es`/`eS` = invalido; remove `-` e espaço e aplica `upper()` (ex: `12345678-Z`, `X-1234567-L` válidos).
- PT `classifica_nif` valida checksum primeiro; NIF com prefixo certo mas digito errado = `X`.
- ES CIF: `ABEH` só dígito, `PQSNW` só letra, resto (`C,D,F,G,J,R,U,V`) ambos — ver [tabela-nif-es.md](tabela-nif-es.md).
