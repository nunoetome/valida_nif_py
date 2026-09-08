# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2026-09-08

### Added
- `valida_nif_es` — Spanish NIF validator (`src/valida_nif_es.py` + `valida_nif_es.py` shim): `valida_dni` (mod23 `TRWAGMYFPDXBNJZSQVHLCKE`), `valida_nie` (`XYZ`→`0/1/2` + mod23), `valida_cif` (weighted sum + `JABCDEFGHI`, rules `ABEH` digit-only / `PQSNW` letter-only / rest both), `valida_nif_es`/`valida_nif` dispatcher, `completa_dni`/`completa_nie`/`completa_cif` and `completa_nif_es`/`completa_nif`, normalization `ES`/`es` + strip `-`/space + `upper()`.
- ES CLI — `--valida_nif`/`--valida_dni`/`--valida_nie`/`--valida_cif` and `--completa`/`--completa_dni`/`--completa_nie`/`--completa_cif` (exit `0` valid / `1` invalid / `2` error).
- Docs — `docs/tabela-nif-es.md` (DNI/NIE/CIF + state diagram), updated `docs/arquitetura.md` (ES flow + component/class diagrams), `docs/guia-utilizador.md` (ES module+CLI), `README.md` (ES quick-start + PT vs ES comparison).

### Changed
- `pyproject.toml` bump to `1.2.0`, `py-modules = ["valida_nif", "valida_nif_es"]`, new entry points `valida-nif-es` / `valida_nif_es`.

## [1.1.0] - 2026-09-04

### Added
- `classifica_nif(nif)` — classifies a valid NIF and returns a 1-char index `A-G` or `X` for invalid/unknown. Reuses `valida_nif`/`_normalizar`, handles `PT`/`pt` prefix, 2-digit priority `45` and sub-ranges `70/71/72/74/75/77/79/90/91/98/99` before 1-digit fallback; `X` on checksum/format/prefix error (`A`=1-3 Singular Resident, `B`=45 Non-resident with income, `C`=5 Legal Entity, `D`=6 Public Bodies, `E`=7* Heritages/Funds/AT, `F`=8 ENI deprecated, `G`=9* Condos/Irregular/Non-resident, `X`=invalid).
- `classifica_nif_detalhado(nif)` — returns `{"indice","categoria","descricao","valido","nif"}` using `TABELA_NIF` dict and `_carregar_tabela_csv()` CSV fallback.
 - `TABELA_NIF` + `src/tabela_nif.csv` — alphabetical lookup table `indice,categoria,prefixos,descricao,base_legal,estado` UTF-8.
- CLI `--classifica <NIF>` + `--csv` — prints `A - Categoria` or CSV line, exits `0` valid / `1` invalid.
- Docs — `docs/arquitetura.md` (mermaid flow), `docs/guia-utilizador.md` (module+CLI examples), `docs/tabela-nif.md` (A-G/X table + sub-ranges + mermaid), `src` layout and `pyproject.toml`.

### Changed
 - Refactor to `src` layout — `valida_nif_py.py` → `src/valida_nif.py`; root shims keep compatibility; add `pyproject.toml` (PEP 621, `package-dir "" = "src"`).
- Update `README.md` with structure, quick-start, classification table and docs links.

## [1.0.0] - 2026-09-04

Initial stable release. First public version of the Portuguese NIF (Número de Identificação Fiscal) validator.

### Added
- `valida_nif(nif)` — validates a Portuguese NIF (9 digits). Implements modulo 11 check digit validation, rejects `000000000`, validates length and numeric format, accepts optional `PT`/`pt` prefix and surrounding whitespace, returns `False` for `None` or invalid prefix (`e54e7d7`).
- `completa_nif(base8)` — completes an 8-digit base to a full 9-digit NIF by calculating and appending the control digit. Validates input length (exactly 8 digits), numeric content and optional `PT`/`pt` prefix; raises `ValueError` on invalid input (`e54e7d7`).
- CLI interface — `python valida_nif_py.py --valida_nif <NIF>` prints `valido`/`invalido` and exits with `0`/`1`; `--completa <BASE8>` prints the completed 9-digit NIF or an error to stderr and exits with `2` on failure; no arguments prints help and exits with `2` (`e54e7d7`).
- Helpers `_normalizar(nif)` — normalises input (trims whitespace, strips optional `PT`/`pt` prefix, returns `None` for invalid prefix or `None` input) and `_calcular_controlo(base8)` — calculates the NIF control digit via weighted sum `sum(d * (9 - i)) % 11` (`e54e7d7`).
- Project scaffolding from initial commit — `.gitignore` (Python template) and `README.md` (`3f94740`).

[Unreleased]: https://github.com/nunoetome/valida_nif_py/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/nunoetome/valida_nif_py/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/nunoetome/valida_nif_py/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/nunoetome/valida_nif_py/releases/tag/v1.0.0

<!-- Full Changelog: https://github.com/nunoetome/valida_nif_py/commits/v1.0.0 -->
