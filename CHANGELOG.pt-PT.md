# Changelog

Todas as alterações notáveis a este projeto serão documentadas neste ficheiro.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-PT/1.1.0/),
e este projeto segue [Semantic Versioning](https://semver.org/lang/pt-PT/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2026-09-08

### Added
- `valida_nif_es` — validador NIF espanhol (`src/valida_nif_es.py` + `valida_nif_es.py` shim): `valida_dni` (mod23 `TRWAGMYFPDXBNJZSQVHLCKE`), `valida_nie` (`XYZ`→`0/1/2` + mod23), `valida_cif` (soma ponderada + `JABCDEFGHI`, regras `ABEH` só dígito / `PQSNW` só letra / resto ambos), `valida_nif_es`/`valida_nif` dispatcher, `completa_dni`/`completa_nie`/`completa_cif` e `completa_nif_es`/`completa_nif`, normalização `ES`/`es` + remove `-`/espaço + `upper()`.
- CLI ES — `--valida_nif`/`--valida_dni`/`--valida_nie`/`--valida_cif` e `--completa`/`--completa_dni`/`--completa_nie`/`--completa_cif` (exit `0` válido / `1` inválido / `2` erro).
- Docs — `docs/tabela-nif-es.md` (DNI/NIE/CIF + diagrama de estados), atualizados `docs/arquitetura.md` (fluxo ES + diagramas componente/classe), `docs/guia-utilizador.md` (módulo+CLI ES), `README.md` (quick-start ES + comparativo PT vs ES).

### Changed
- `pyproject.toml` bump para `1.2.0`, `py-modules = ["valida_nif", "valida_nif_es"]`, novos entry points `valida-nif-es` / `valida_nif_es`.

## [1.1.0] - 2026-09-04

### Added
- `classifica_nif(nif)` — classifica um NIF válido e devolve índice 1-char `A-G` ou `X` para inválido/desconhecido. Reutiliza `valida_nif`/`_normalizar`, trata prefixo `PT`/`pt`, prioridade 2 dígitos `45` e sub-gamas `70/71/72/74/75/77/79/90/91/98/99` antes de fallback 1 dígito; `X` em erro de checksum/formato/prefixo (`A`=1-3 Singular Residente, `B`=45 Não residente c/ rendimentos, `C`=5 Pessoa Coletiva, `D`=6 Organismos Públicos, `E`=7* Heranças/Fundos/AT, `F`=8 ENI obsoleto, `G`=9* Condomínios/Irregulares/Não residentes, `X`=inválido).
- `classifica_nif_detalhado(nif)` — devolve `{"indice","categoria","descricao","valido","nif"}` usando `TABELA_NIF` e `_carregar_tabela_csv()` com fallback CSV.
 - `TABELA_NIF` + `src/tabela_nif.csv` — tabela de correspondência `indice,categoria,prefixos,descricao,base_legal,estado` UTF-8.
- CLI `--classifica <NIF>` + `--csv` — imprime `A - Categoria` ou linha CSV, termina `0` válido / `1` inválido.
- Docs — `docs/arquitetura.md` (fluxo mermaid), `docs/guia-utilizador.md` (exemplos módulo+CLI), `docs/tabela-nif.md` (tabela A-G/X + sub-gamas + mermaid), layout `src` e `pyproject.toml`.

### Changed
 - Refactor para layout `src` — `valida_nif_py.py` → `src/valida_nif.py`; shims na raiz mantêm compatibilidade; adicionado `pyproject.toml` (PEP 621, `package-dir "" = "src"`).
- Atualizado `README.md` com estrutura, quick-start, tabela classificação e links docs.

## [1.0.0] - 2026-09-04

Primeira versão estável (initial stable release). Primeira versão pública do validador de NIF (Número de Identificação Fiscal) português.

### Added
- `valida_nif(nif)` — valida um NIF português (9 dígitos). Implementa validação do dígito de controlo por módulo 11, rejeita `000000000`, valida comprimento e formato numérico, aceita prefixo opcional `PT`/`pt` e espaços envolventes, devolve `False` para `None` ou prefixo inválido (`e54e7d7`).
- `completa_nif(base8)` — completa uma base de 8 dígitos para um NIF completo de 9 dígitos, calculando e anexando o dígito de controlo. Valida comprimento do input (exatamente 8 dígitos), conteúdo numérico e prefixo opcional `PT`/`pt`; lança `ValueError` em caso de input inválido (`e54e7d7`).
- Interface CLI — `python valida_nif_py.py --valida_nif <NIF>` imprime `valido`/`invalido` e termina com código `0`/`1`; `--completa <BASE8>` imprime o NIF completo de 9 dígitos ou erro no stderr e termina com `2` em caso de falha; sem argumentos imprime a ajuda e termina com `2` (`e54e7d7`).
- Helpers `_normalizar(nif)` — normaliza o input (remove espaços, remove prefixo opcional `PT`/`pt`, devolve `None` para prefixo inválido ou input `None`) e `_calcular_controlo(base8)` — calcula o dígito de controlo do NIF via soma ponderada `sum(d * (9 - i)) % 11` (`e54e7d7`).
- Estrutura inicial do projeto — `.gitignore` (template Python) e `README.md` (`3f94740`).

[Unreleased]: https://github.com/nunoetome/valida_nif_py/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/nunoetome/valida_nif_py/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/nunoetome/valida_nif_py/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/nunoetome/valida_nif_py/releases/tag/v1.0.0

<!-- Full Changelog: https://github.com/nunoetome/valida_nif_py/commits/v1.0.0 -->
