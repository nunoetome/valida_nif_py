# Guia de Utilizador

## Instalação

```bash
pip install -e .
# ou sem instalar
PYTHONPATH=src python -m valida_nif
PYTHONPATH=src python -m valida_nif_es
PYTHONPATH=src python -m valida_nif_fr
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

## Uso como Módulo — FR (SIREN/SIRET/TVA/NIR)

```python
from valida_nif_fr import valida_siren, valida_siret, valida_tva_fr, valida_nir, valida_nif_fr
from valida_nif_fr import completa_siren, completa_siret, completa_tva_fr, completa_nir, completa_nif_fr

valida_siren("732829320")          # True  (Luhn)
valida_siren("FR732829320")        # True  (FR/fr + espaço/-/. )
valida_siren("732829321")          # False (Luhn)
valida_siret("73282932000074")     # True  (14 Luhn + SIREN)
valida_siret("73282932000075")     # False
valida_siret("FR73282932000074")   # True
valida_tva_fr("FR40303265045")     # True  # SIREN 303265045 clé 40
valida_tva_fr("FR96552100554")     # True  # SIREN 552100554 clé 96
valida_tva_fr("fr 40 303265045")   # True  (case/espaco)
valida_tva_fr("Fr40303265045")     # False (prefixo case-sensitive)
valida_nir("184127500112356")      # True  # 97-(n%97)
valida_nir("1841275A0112347")      # False

valida_nif_fr("732829320")         # True (dispatcher SIREN|SIRET|TVA|NIR)
valida_nif_fr("FR40303265045")     # True
valida_nif_fr("184127500112356")   # True

completa_siren("73282932")         # "732829320"
completa_siret("7328293200007")    # "73282932000074"
completa_tva_fr("303265045")       # "FR40303265045"
completa_tva_fr("552100554")       # "FR96552100554"
completa_nir("1841275001123")      # "184127500112356"
completa_nif_fr("73282932")        # "732829320" (infere SIREN)
completa_nif_fr("303265045")       # "FR40303265045" (infere TVA)
```

## CLI — FR

```bash
python -m valida_nif_fr --valida_nif 732829320              # valido/invalido
python -m valida_nif_fr --valida_siren 732829320
python -m valida_nif_fr --valida_siret 73282932000074
python -m valida_nif_fr --valida_tva FR40303265045
python -m valida_nif_fr --valida_nir 184127500112356
python -m valida_nif_fr --completa 73282932                 # 732829320 (infere)
python -m valida_nif_fr --completa_siren 73282932
python -m valida_nif_fr --completa_siret 7328293200007
python -m valida_nif_fr --completa_tva 303265045            # FR40303265045
python -m valida_nif_fr --completa_nir 1841275001123        # 184127500112356
python src/valida_nif_fr.py --valida_siren 732829320       # ficheiro direto em src/
python valida_nif_fr.py --valida_siren 732829320           # via shim raiz
python valida_siret_fr.py --valida_siret 73282932000074    # alias shim
# após pip install -e . (requer venv ativo):
valida-nif-fr --valida_siren 732829320
valida_nif_fr --valida_siret 73282932000074
valida-siret-fr --valida_tva FR40303265045
valida_siret_fr --valida_nir 184127500112356
```

## Códigos de Saída

- `0` valido/encontrado
- `1` invalido/classificacao X
- `2` erro de argumentos/completa invalida

Válido para PT, ES e FR (mesmo `argparse` + `sys.exit`).

## Notas

- PT: aceita `PT`/`pt` apenas; `Pt`/`pT`/`ES`/`FR` = invalido.
- ES: aceita `ES`/`es` apenas; `Es`/`eS` = invalido; remove `-` e espaço e aplica `upper()` (ex: `12345678-Z`, `X-1234567-L` válidos).
- FR: aceita `FR`/`fr` apenas; `Fr`/`fR` = invalido; remove `-`, espaço e `.` e aplica `upper()` (ex: `FR 40 303265045`, `732-829-320`, `732.829.320.00074` válidos).
- PT `classifica_nif` valida checksum primeiro; NIF com prefixo certo mas digito errado = `X`.
- ES CIF: `ABEH` só dígito, `PQSNW` só letra, resto (`C,D,F,G,J,R,U,V`) ambos — ver [tabela-nif-es.md](tabela-nif-es.md).
- FR SIRET exige SIREN válido nos 9 primeiros; TVA exige SIREN válido + `clé=(12+3*(siren%97))%97`; NIR `2A`→`19` / `2B`→`18` — ver [tabela-nif-fr.md](tabela-nif-fr.md).
