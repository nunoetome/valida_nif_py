# Changelog

Todas as alterações notáveis a este projeto serão documentadas neste ficheiro.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-PT/1.1.0/),
e este projeto segue [Semantic Versioning](https://semver.org/lang/pt-PT/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-09-04

Primeira versão estável (initial stable release). Primeira versão pública do validador de NIF (Número de Identificação Fiscal) português.

### Added
- `valida_nif(nif)` — valida um NIF português (9 dígitos). Implementa validação do dígito de controlo por módulo 11, rejeita `000000000`, valida comprimento e formato numérico, aceita prefixo opcional `PT`/`pt` e espaços envolventes, devolve `False` para `None` ou prefixo inválido (`e54e7d7`).
- `completa_nif(base8)` — completa uma base de 8 dígitos para um NIF completo de 9 dígitos, calculando e anexando o dígito de controlo. Valida comprimento do input (exatamente 8 dígitos), conteúdo numérico e prefixo opcional `PT`/`pt`; lança `ValueError` em caso de input inválido (`e54e7d7`).
- Interface CLI — `python valida_nif_py.py --valida_nif <NIF>` imprime `valido`/`invalido` e termina com código `0`/`1`; `--completa <BASE8>` imprime o NIF completo de 9 dígitos ou erro no stderr e termina com `2` em caso de falha; sem argumentos imprime a ajuda e termina com `2` (`e54e7d7`).
- Helpers `_normalizar(nif)` — normaliza o input (remove espaços, remove prefixo opcional `PT`/`pt`, devolve `None` para prefixo inválido ou input `None`) e `_calcular_controlo(base8)` — calcula o dígito de controlo do NIF via soma ponderada `sum(d * (9 - i)) % 11` (`e54e7d7`).
- Estrutura inicial do projeto — `.gitignore` (template Python) e `README.md` (`3f94740`).

[Unreleased]: https://github.com/nunoetome/valida_nif_py/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/nunoetome/valida_nif_py/releases/tag/v1.0.0

<!-- Full Changelog: https://github.com/nunoetome/valida_nif_py/commits/v1.0.0 -->
