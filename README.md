# valida-nif
Valida NIF português (mod11) e NIF espanhol — DNI/NIE/CIF (mod23/CIF). Validação, compleção e classificação.

## Instalação

```bash
pip install -e .
```

## Estrutura

```
src/valida_nif.py      # PT: valida_nif, completa_nif, classifica_nif
src/valida_nif_es.py   # ES: valida_nif_es, valida_dni/nie/cif, completa_*
src/tabela_nif.csv     # PT: mapeamento A-G/X
valida_nif_es.py       # shim raiz para compatibilidade (re-exporta src/)
docs/arquitetura.md            # técnica + mermaid PT+ES
docs/guia-utilizador.md        # exemplos módulo e CLI PT+ES
docs/tabela-nif.md             # PT: tabela A-G/X
docs/tabela-nif-es.md          # ES: tipos CIF + DNI/NIE
```

## Uso Rápido — PT

```python
from valida_nif import valida_nif, completa_nif, classifica_nif

valida_nif("123456789")          # True
valida_nif("PT123456789")        # True (PT/pt apenas)
completa_nif("12345678")         # "123456789"
classifica_nif("123456789")      # "A" -> Pessoa Singular - Residente
classifica_nif("450000001")      # "B" (45) / "X" se invalido
```

CLI PT:

```bash
python -m valida_nif --valida_nif 123456789
python -m valida_nif --completa 12345678
python -m valida_nif --classifica 123456789
python -m valida_nif --classifica 123456789 --csv
python src/valida_nif.py --valida_nif 123456789  # ficheiro direto em src/
python src/valida_nif.py --completa 12345678     # sem instalar
# após pip install -e . (requer venv ativo e PATH):
valida-nif --valida_nif 123456789
valida-nif --completa 12345678
```

## Uso Rápido — ES

```python
from valida_nif_es import valida_nif_es, valida_dni, valida_nie, valida_cif
from valida_nif_es import completa_dni, completa_nie, completa_cif, completa_nif_es

valida_dni("12345678Z")          # True  (mod23 TRWAGMYFPDXBNJZSQVHLCKE)
valida_dni("ES12345678Z")        # True  (ES/es + hífen/espaço)
valida_nie("X1234567L")          # True  (X→0 + mod23)
valida_nie("Y1234567X")          # True
valida_cif("A58818501")          # True  (A só dígito)
valida_cif("Q2826000H")          # True  (Q só letra)
valida_nif_es("12345678Z")       # True  # dispatcher DNI|NIE|CIF
valida_nif_es("X1234567L")       # True
valida_nif_es("A58818501")       # True
completa_dni("12345678")         # "12345678Z"
completa_nie("X1234567")         # "X1234567L"
completa_cif("A5881850")         # "A58818501"
completa_nif_es("12345678")      # "12345678Z" (infere tipo)
```

CLI ES:

```bash
python -m valida_nif_es --valida_nif 12345678Z
python -m valida_nif_es --valida_dni 12345678Z
python -m valida_nif_es --valida_nie X1234567L
python -m valida_nif_es --valida_cif A58818501
python -m valida_nif_es --completa 12345678
python -m valida_nif_es --completa_dni 12345678
python -m valida_nif_es --completa_nie X1234567
python -m valida_nif_es --completa_cif A5881850
python src/valida_nif_es.py --valida_nif 12345678Z  # sem instalar
# após pip install -e .:
valida-nif-es --valida_nif 12345678Z
valida_nif_es --valida_nif 12345678Z
```

Mais exemplos em [docs/guia-utilizador.md](docs/guia-utilizador.md).

## Comparativo PT vs ES

| Aspeto | PT | ES |
|---|---|---|
| Formato | 9 dígitos mod11 | DNI 8+letra mod23, NIE XYZ+7+letra mod23, CIF letra+7+dígito/letra |
| Prefixo | `PT`/`pt` (Pt/pT inválido) | `ES`/`es` (Es/eS inválido) |
| Normalização | trim + PT/pt | trim + ES/es + remove `-`/espaço + upper |
| Controlo | `sum(d*(9-i))%11` | DNI `TRWAGMYFPDXBNJZSQVHLCKE[n%23]`, CIF soma pares + dobra ímpares + `JABCDEFGHI` |
| Tipos | — | `ABEH` só dígito, `PQSNW` só letra, resto ambos |

## Classificação PT (índice 1-char)

| Índice | Categoria | Prefixos |
|---|---|---|
| A | Pessoa Singular - Residente | 1,2,3 |
| B | Pessoa Singular - Não Residente com Rendimentos | 45 |
| C | Pessoa Coletiva - Residente | 5 |
| D | Organismos Públicos | 6 |
| E | Heranças/Fundos/AT | 7,70,71,72,74,75,77,79 |
| F | ENI (obsoleto) | 8 |
| G | Condomínios/Irregulares/Não Residentes | 9,90,91,98,99 |
| X | Inválido | 0,4,formato,controlo |

Tabela completa em [docs/tabela-nif.md](docs/tabela-nif.md) e [src/tabela_nif.csv](src/tabela_nif.csv).
Tabela ES em [docs/tabela-nif-es.md](docs/tabela-nif-es.md).

## Documentação

- [Arquitetura](docs/arquitetura.md) — fluxos PT+ES e mermaid
- [Guia de Utilizador](docs/guia-utilizador.md) — PT+ES (módulo e CLI)
- [Tabela NIF PT](docs/tabela-nif.md) — A-G/X
- [Tabela NIF ES](docs/tabela-nif-es.md) — DNI/NIE/CIF

## Changelog

Ver [CHANGELOG.md](CHANGELOG.md) (EN-GB) e [CHANGELOG.pt-PT.md](CHANGELOG.pt-PT.md) (PT-PT). Formato [Keep a Changelog](https://keepachangelog.com/) + [SemVer](https://semver.org/).
