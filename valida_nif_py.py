#!/usr/bin/env python3
import argparse
import sys


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


def main():
    parser = argparse.ArgumentParser(description="Valida NIF portugues")
    parser.add_argument("--valida_nif", metavar="NIF", help="valida NIF (ex: 500500500 ou PT500500500)")
    parser.add_argument("--completa", metavar="BASE8", help="dado 8 digitos devolve NIF de 9 digitos (ex: 50050050)")
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

    parser.print_help()
    sys.exit(2)


if __name__ == "__main__":
    main()
