# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-09-04

Initial stable release. First public version of the Portuguese NIF (Número de Identificação Fiscal) validator.

### Added
- `valida_nif(nif)` — validates a Portuguese NIF (9 digits). Implements modulo 11 check digit validation, rejects `000000000`, validates length and numeric format, accepts optional `PT`/`pt` prefix and surrounding whitespace, returns `False` for `None` or invalid prefix (`e54e7d7`).
- `completa_nif(base8)` — completes an 8-digit base to a full 9-digit NIF by calculating and appending the control digit. Validates input length (exactly 8 digits), numeric content and optional `PT`/`pt` prefix; raises `ValueError` on invalid input (`e54e7d7`).
- CLI interface — `python valida_nif_py.py --valida_nif <NIF>` prints `valido`/`invalido` and exits with `0`/`1`; `--completa <BASE8>` prints the completed 9-digit NIF or an error to stderr and exits with `2` on failure; no arguments prints help and exits with `2` (`e54e7d7`).
- Helpers `_normalizar(nif)` — normalises input (trims whitespace, strips optional `PT`/`pt` prefix, returns `None` for invalid prefix or `None` input) and `_calcular_controlo(base8)` — calculates the NIF control digit via weighted sum `sum(d * (9 - i)) % 11` (`e54e7d7`).
- Project scaffolding from initial commit — `.gitignore` (Python template) and `README.md` (`3f94740`).

[Unreleased]: https://github.com/nunoetome/valida_nif_py/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/nunoetome/valida_nif_py/releases/tag/v1.0.0

<!-- Full Changelog: https://github.com/nunoetome/valida_nif_py/commits/v1.0.0 -->
