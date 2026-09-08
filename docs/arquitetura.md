# Arquitetura

## Visão Geral

```
src/valida_nif.py      -> valida_nif, completa_nif, classifica_nif
src/tabela_nif.csv     -> mapeamento indice->categoria
docs/                  -> documentação técnica e utilizador
```

## Fluxo de Validação e Classificação

```mermaid
flowchart TD
    A[Input NIF str/int/None] --> B[_normalizar]
    B -->|None / Pt/pT| X[X - Invalido]
    B --> C{s.strip 9 digitos? isdigit? !=000000000}
    C -->|Nao| X
    C -->|Sim| D[_calcular_controlo base8]
    D --> E{controlo == d9?}
    E -->|Nao| X
    E -->|Sim| F[_classificar_prefixo]
    F --> G{A-G categoria}
    G -->|1/2/3| A1[A Pessoa Singular Residente]
    G -->|45| B1[B Nao Residente com Rendimentos]
    G -->|5| C1[C Pessoa Coletiva]
    G -->|6| D1[D Organismos Publicos]
    G -->|7*| E1[E Herancas/Fundos/AT]
    G -->|8| F1[F ENI obsoleto]
    G -->|9*| G1[G Condominios/Irregulares]
```

## Módulos

| Módulo | Responsabilidade |
|---|---|
| `_normalizar` | trim, PT/pt, None para prefixo invalido |
| `_calcular_controlo` | soma ponderada 9..2 mod11 |
| `valida_nif` | bool 9 digitos + controlo |
| `completa_nif` | 8->9 digitos |
| `classifica_nif` | reutiliza valida_nif, devolve A-G/X |
| `_classificar_prefixo` | prioridade 45/70/71... antes de 1-char |
| `TABELA_NIF` | dict em memoria, fallback CSV |

## Decisões

- `classifica_nif` retorna `X` em vez de levantar, para uso batch CLI.
- `45` verificado antes de `4` (4 isolado = X).
- `8` mapeado para `F` com estado obsoleto, não erro.
- CSV carregavel mas não obrigatório; dict hardcoded garante offline.
