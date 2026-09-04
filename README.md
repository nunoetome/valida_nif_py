# valida-nif
Valida a estrutura de NIF português — validação, compleção e classificação.

## Instalação

```bash
pip install -e .
```

## Estrutura

```
src/valida_nif.py      # código (valida_nif, completa_nif, classifica_nif)
src/tabela_nif.csv
docs/arquitetura.md            # técnica + mermaid
docs/guia-utilizador.md        # exemplos módulo e CLI
docs/tabela-nif.md             # tabela A-G/X
```

## Uso Rápido

```python
from valida_nif import valida_nif, completa_nif, classifica_nif

valida_nif("123456789")          # True
valida_nif("PT123456789")        # True (PT/pt apenas)
completa_nif("12345678")         # "123456789"
classifica_nif("123456789")      # "A" -> Pessoa Singular - Residente
classifica_nif("450000001")      # "B" (45) / "X" se invalido
```

CLI:

```bash
valida-nif --valida_nif 123456789
valida-nif --completa 12345678
valida-nif --classifica 123456789
valida-nif --classifica 123456789 --csv
python -m valida_nif --valida_nif 123456789
python src/valida_nif.py --valida_nif 123456789
```

Mais exemplos em [docs/guia-utilizador.md](docs/guia-utilizador.md).

## Classificação (índice 1-char)

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

## Documentação

- [Arquitetura](docs/arquitetura.md) — fluxos e mermaid
- [Guia de Utilizador](docs/guia-utilizador.md)
- [Tabela NIF](docs/tabela-nif.md)

## Changelog

Ver [CHANGELOG.md](CHANGELOG.md) (EN-GB) e [CHANGELOG.pt-PT.md](CHANGELOG.pt-PT.md) (PT-PT). Formato [Keep a Changelog](https://keepachangelog.com/) + [SemVer](https://semver.org/).
