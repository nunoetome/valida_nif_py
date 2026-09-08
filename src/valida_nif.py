#!/usr/bin/env python3
import argparse
import csv
import sys
from pathlib import Path

TABELA_NIF = {
    "A": {"categoria": "Pessoa Singular - Residente", "prefixos": ["1", "2", "3"], "descricao": "Cidadaos nacionais e estrangeiros residentes"},
    "B": {"categoria": "Pessoa Singular - Nao Residente com Rendimentos", "prefixos": ["45"], "descricao": "Nao residentes apenas com rendimentos com retencao definitiva"},
    "C": {"categoria": "Pessoa Coletiva - Residente", "prefixos": ["5"], "descricao": "Sociedades comerciais e empresas privadas residentes"},
    "D": {"categoria": "Organismos Publicos", "prefixos": ["6"], "descricao": "Estado camaras escolas administracao publica"},
    "E": {"categoria": "Herancas Fundos e Entidades Especiais (AT)", "prefixos": ["70", "71", "72", "74", "75", "77", "79", "7"], "descricao": "Herancas indivisas fundos investimento atribuicao oficiosa regime Expo98"},
    "F": {"categoria": "Empresario em Nome Individual (ENI)", "prefixos": ["8"], "descricao": "ENI historico hoje migrado para 1-3"},
    "G": {"categoria": "Condominios Sociedades Irregulares e Nao Residentes Coletivos", "prefixos": ["90", "91", "98", "99", "9"], "descricao": "Condominios sociedades irregulares civis e nao residentes s/ estabelecimento"},
    "X": {"categoria": "Invalido ou Desconhecido", "prefixos": ["0", "4"], "descricao": "Prefixo nao atribuido formato invalido ou digito controlo errado"},
}

def _carregar_tabela_csv():
    p = Path(__file__).with_name("tabela_nif.csv")
    if not p.exists():
        return TABELA_NIF
    try:
        out = {}
        with p.open(encoding="utf-8") as f:
            for row in csv.DictReader(f):
                out[row["indice"]] = {"categoria": row["categoria"], "prefixos": row["prefixos"].split(";"), "descricao": row["descricao"]}
        return out
    except Exception:
        return TABELA_NIF


def _normalizar(nif):
    if nif is None:
        return None
    s = str(nif).strip()
    if len(s) >= 2 and s[:2].upper() == "PT":
        prefix = s[:2]
        resto = s[2:].strip()
        if prefix != "PT" and prefix != "pt":
            return None
        s = resto
    return s


def _calcular_controlo(base8):
    soma = sum(int(d) * (9 - i) for i, d in enumerate(base8))
    resto = soma % 11
    if resto <= 1:
        return 0
    return 11 - resto


def valida_nif(nif):
    s = _normalizar(nif)
    if s is None:
        return False
    s = s.strip()
    if len(s) != 9:
        return False
    if not s.isdigit():
        return False
    if s == "000000000":
        return False
    base8 = s[:8]
    try:
        esperado = _calcular_controlo(base8)
    except ValueError:
        return False
    return esperado == int(s[8])


def completa_nif(base):
    s = _normalizar(base)
    if s is None:
        raise ValueError("NIF com prefixo invalido (so PT/pt permitido)")
    s = s.strip()
    if len(s) != 8:
        raise ValueError("base deve ter exatamente 8 digitos")
    if not s.isdigit():
        raise ValueError("base deve conter apenas digitos")
    controlo = _calcular_controlo(s)
    return s + str(controlo)


def _classificar_prefixo(s):
    if s.startswith("45"):
        return "B"
    if s.startswith("70") or s.startswith("74") or s.startswith("75"):
        return "E"
    if s.startswith("71") or s.startswith("72") or s.startswith("77") or s.startswith("79"):
        return "E"
    if s.startswith("90") or s.startswith("91") or s.startswith("98") or s.startswith("99"):
        return "G"
    c = s[0]
    if c in ("1", "2", "3"):
        return "A"
    if c == "5":
        return "C"
    if c == "6":
        return "D"
    if c == "7":
        return "E"
    if c == "8":
        return "F"
    if c == "9":
        return "G"
    return "X"


def classifica_nif(nif):
    s = _normalizar(nif)
    if s is None:
        return "X"
    s = s.strip()
    if len(s) != 9 or not s.isdigit() or s == "000000000":
        return "X"
    if not valida_nif(s):
        return "X"
    return _classificar_prefixo(s)


def classifica_nif_detalhado(nif):
    idx = classifica_nif(nif)
    info = TABELA_NIF.get(idx, TABELA_NIF["X"])
    s = _normalizar(nif)
    valido = idx != "X"
    return {"indice": idx, "categoria": info["categoria"], "descricao": info["descricao"], "valido": valido, "nif": s.strip() if s else None}


def main():
    parser = argparse.ArgumentParser(description="Valida NIF portugues")
    parser.add_argument("--valida_nif", metavar="NIF", help="valida NIF (ex: 500500500 ou PT500500500)")
    parser.add_argument("--completa", metavar="BASE8", help="dado 8 digitos devolve NIF de 9 digitos (ex: 50050050)")
    parser.add_argument("--classifica", metavar="NIF", help="classifica NIF e devolve indice A-G/X (ex: 123456789 -> A)")
    parser.add_argument("--csv", action="store_true", help="com --classifica imprime csv do NIF classificado")
    args = parser.parse_args()

    if args.valida_nif is not None:
        valido = valida_nif(args.valida_nif)
        print("valido" if valido else "invalido")
        sys.exit(0 if valido else 1)

    if args.completa is not None:
        try:
            nif = completa_nif(args.completa)
            print(nif)
            sys.exit(0)
        except ValueError as e:
            print(f"erro: {e}", file=sys.stderr)
            sys.exit(2)

    if args.classifica is not None:
        d = classifica_nif_detalhado(args.classifica)
        if args.csv:
            print("indice,categoria,descricao,valido,nif")
            print(f"{d['indice']},{d['categoria']},{d['descricao']},{d['valido']},{d['nif']}")
        else:
            if d["valido"]:
                print(f"{d['indice']} - {d['categoria']}")
            else:
                print(f"{d['indice']} - {d['categoria']}: {d['descricao']}")
        sys.exit(0 if d["valido"] else 1)

    parser.print_help()
    sys.exit(2)


if __name__ == "__main__":
    main()
