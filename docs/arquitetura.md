# Arquitetura

## Visão Geral

```
src/valida_nif.py      -> PT: valida_nif, completa_nif, classifica_nif
src/valida_nif_es.py   -> ES: valida_nif_es, valida_dni/nie/cif, completa_*
src/tabela_nif.csv     -> mapeamento PT indice->categoria
valida_nif_es.py       -> shim raiz (re-exporta src/valida_nif_es.py)
docs/                  -> documentação técnica e utilizador
```

## Fluxo de Validação e Classificação — PT

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

## Fluxo de Validação — ES (DNI/NIE/CIF)

```mermaid
flowchart TD
    A[Input ES str/int/None] --> B[_normalizar ES/es + strip -/space + upper]
    B -->|None / Es/eS| X[False]
    B --> C{len==9?}
    C -->|Nao| X
    C -->|Sim| D{tipo?}
    D -->|8 digitos+letra| E[valida_dni mod23 TRWAGMYFPDXBNJZSQVHLCKE]
    D -->|XYZ+7+letra| F[valida_nie XYZ->0/1/2 + mod23]
    D -->|letra CIF+7+d/l| G[valida_cif soma ponderada + JABCDEFGHI]
    E --> H{letra==Tabela[n%23]?}
    F --> H
    G --> I{ABEH so digito? PQSNW so letra? resto ambos}
    H -->|Sim| V[True]
    H -->|Nao| X
    I -->|Sim| V
    I -->|Nao| X
```

## Componentes

```mermaid
graph TD
    CLI_PT[valida-nif CLI] --> MOD_PT[src/valida_nif.py]
    CLI_ES[valida-nif-es CLI] --> MOD_ES[src/valida_nif_es.py]
    MOD_PT --> CSV[src/tabela_nif.csv]
    MOD_PT --> TABELA[TABELA_NIF dict]
    MOD_ES --> T_DNI[TRWAGMYFPDXBNJZSQVHLCKE]
    MOD_ES --> M_CIF[JABCDEFGHI]
    MOD_ES --> TIPOS[_TIPOS_CIF ABCDEFGHJNPQRSUVW]
```

## Classes (PT vs ES)

```mermaid
classDiagram
    class ValidaNifPT {
        +valida_nif(nif) bool
        +completa_nif(base8) str
        +classifica_nif(nif) A-G/X
        +classifica_nif_detalhado(nif) dict
        -_normalizar() str?
        -_calcular_controlo() int
        -_classificar_prefixo() A-G/X
    }
    class ValidaNifES {
        +valida_nif_es(nif) bool
        +valida_dni(nif) bool
        +valida_nie(nif) bool
        +valida_cif(nif) bool
        +completa_dni/nie/cif() str
        +completa_nif_es() str
        -_normalizar() str?
        -_letra_dni() char
        -_calcular_controlo_cif() digito,letra
    }
    ValidaNifPT ..> ValidaNifES : estilo comum _normalizar + CLI 0/1/2
```

## Módulos

| Módulo | Responsabilidade |
|---|---|
| `_normalizar` (PT) | trim, PT/pt, None para prefixo invalido |
| `_calcular_controlo` (PT) | soma ponderada 9..2 mod11 |
| `valida_nif` (PT) | bool 9 digitos + controlo |
| `completa_nif` (PT) | 8->9 digitos |
| `classifica_nif` (PT) | reutiliza valida_nif, devolve A-G/X |
| `_classificar_prefixo` (PT) | prioridade 45/70/71... antes de 1-char |
| `TABELA_NIF` (PT) | dict em memoria, fallback CSV |
| `_normalizar` (ES) | trim, ES/es, remove -/espaco, upper |
| `_letra_dni` (ES) | TRWAGMYFPDXBNJZSQVHLCKE[n%23] |
| `_calcular_controlo_cif` (ES) | soma pares + dobra impares + JABCDEFGHI |
| `valida_dni` (ES) | 8 digitos+letra mod23 |
| `valida_nie` (ES) | XYZ+7+letra XYZ->0/1/2 |
| `valida_cif` (ES) | letra+7+d/l ABEH so digito PQSNW so letra |
| `valida_nif_es` (ES) | dispatcher DNI/NIE/CIF |
| `completa_dni/nie/cif` (ES) | 8->9 chars por tipo |

## Decisões

- `classifica_nif` retorna `X` em vez de levantar, para uso batch CLI.
- `45` verificado antes de `4` (4 isolado = X).
- `8` mapeado para `F` com estado obsoleto, não erro.
- CSV carregavel mas não obrigatório; dict hardcoded garante offline.
- ES `Es/eS` rejeitado (apenas `ES`/`es`), coerente com PT `Pt/pT`.
- CIF `ABEH` só dígito, `PQSNW` só letra, resto ambos — regra AEAT pós-2008.
- ES remove `-` e espaço e aplica `upper()` para aceitar `12345678-Z` / `X-1234567-L`.
