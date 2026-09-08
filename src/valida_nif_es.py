#!/usr/bin/env python3
import argparse
import sys

_TABELA_DNI = "TRWAGMYFPDXBNJZSQVHLCKE"
_MAP_CIF = "JABCDEFGHI"
_TIPOS_CIF = set("ABCDEFGHJNPQRSUVW")
_SOLO_DIGITO = set("ABEH")
_SOLO_LETRA = set("PQSNW")


def _normalizar(nif):
    if nif is None:
        return None
    s = str(nif).strip()
    if len(s) >= 2 and s[:2].upper() == "ES":
        prefix = s[:2]
        resto = s[2:].strip()
        if prefix != "ES" and prefix != "es":
            return None
        s = resto
    s = s.replace("-", "").replace(" ", "").upper()
    return s


def _letra_dni(numero):
    return _TABELA_DNI[numero % 23]


def _calcular_controlo_cif(digitos7):
    soma_par = sum(int(digitos7[i]) for i in [1, 3, 5])
    soma_impar = 0
    for i in [0, 2, 4, 6]:
        v = int(digitos7[i]) * 2
        soma_impar += v // 10 + v % 10
    total = soma_par + soma_impar
    digito = (10 - (total % 10)) % 10
    letra = _MAP_CIF[digito]
    return digito, letra


def valida_dni(nif):
    s = _normalizar(nif)
    if s is None:
        return False
    if len(s) != 9:
        return False
    if not s[:8].isdigit():
        return False
    if not s[8].isalpha():
        return False
    try:
        esperado = _letra_dni(int(s[:8]))
    except ValueError:
        return False
    return s[8] == esperado


def valida_nie(nif):
    s = _normalizar(nif)
    if s is None:
        return False
    if len(s) != 9:
        return False
    if s[0] not in "XYZ":
        return False
    if not s[1:8].isdigit():
        return False
    if not s[8].isalpha():
        return False
    mapa = {"X": "0", "Y": "1", "Z": "2"}
    try:
        numero = int(mapa[s[0]] + s[1:8])
        esperado = _letra_dni(numero)
    except ValueError:
        return False
    return s[8] == esperado


def valida_cif(nif):
    s = _normalizar(nif)
    if s is None:
        return False
    if len(s) != 9:
        return False
    if s[0] not in _TIPOS_CIF:
        return False
    if not s[1:8].isdigit():
        return False
    controlo = s[8]
    digito, letra = _calcular_controlo_cif(s[1:8])
    if controlo.isdigit():
        if s[0] in _SOLO_LETRA:
            return False
        return int(controlo) == digito
    if controlo.isalpha():
        if s[0] in _SOLO_DIGITO:
            return False
        return controlo == letra
    return False


def valida_nif_es(nif):
    return valida_dni(nif) or valida_nie(nif) or valida_cif(nif)


def valida_nif(nif):
    return valida_nif_es(nif)


def completa_dni(base8):
    s = _normalizar(base8)
    if s is None:
        raise ValueError("NIF com prefixo invalido (so ES/es permitido)")
    s = s.strip()
    if len(s) != 8:
        raise ValueError("base deve ter exatamente 8 digitos")
    if not s.isdigit():
        raise ValueError("base deve conter apenas digitos")
    return s + _letra_dni(int(s))


def completa_nie(base8):
    s = _normalizar(base8)
    if s is None:
        raise ValueError("NIF com prefixo invalido (so ES/es permitido)")
    s = s.strip()
    if len(s) != 8:
        raise ValueError("base NIE deve ter 1 letra [XYZ] + 7 digitos")
    if s[0] not in "XYZ":
        raise ValueError("base NIE deve comecar por X, Y ou Z")
    if not s[1:].isdigit():
        raise ValueError("base NIE deve conter 7 digitos apos a letra")
    mapa = {"X": "0", "Y": "1", "Z": "2"}
    numero = int(mapa[s[0]] + s[1:])
    return s + _letra_dni(numero)


def completa_cif(base8):
    s = _normalizar(base8)
    if s is None:
        raise ValueError("NIF com prefixo invalido (so ES/es permitido)")
    s = s.strip()
    if len(s) != 8:
        raise ValueError("base CIF deve ter 1 letra + 7 digitos")
    if s[0] not in _TIPOS_CIF:
        raise ValueError("letra inicial invalida para CIF")
    if not s[1:].isdigit():
        raise ValueError("base CIF deve conter 7 digitos apos a letra")
    digito, letra = _calcular_controlo_cif(s[1:])
    if s[0] in _SOLO_LETRA:
        return s + letra
    if s[0] in _SOLO_DIGITO:
        return s + str(digito)
    return s + str(digito)


def completa_nif_es(base):
    s = _normalizar(base)
    if s is None:
        raise ValueError("NIF com prefixo invalido (so ES/es permitido)")
    s = s.strip()
    if len(s) != 8:
        raise ValueError("base deve ter 8 caracteres")
    if s.isdigit():
        return completa_dni(s)
    if s[0] in "XYZ" and s[1:].isdigit():
        return completa_nie(s)
    if s[0] in _TIPOS_CIF and s[1:].isdigit():
        return completa_cif(s)
    raise ValueError("formato de base desconhecido (use 8 digitos para DNI, XYZ+7 digitos para NIE, letra+7 digitos para CIF)")


def completa_nif(base):
    return completa_nif_es(base)


def main():
    parser = argparse.ArgumentParser(description="Valida NIF espanhol (DNI/NIE/CIF)")
    parser.add_argument("--valida_nif", metavar="NIF", help="valida NIF espanhol (ex: 12345678Z, X1234567L, A58818501)")
    parser.add_argument("--valida_dni", metavar="DNI", help="valida apenas DNI")
    parser.add_argument("--valida_nie", metavar="NIE", help="valida apenas NIE")
    parser.add_argument("--valida_cif", metavar="CIF", help="valida apenas CIF")
    parser.add_argument("--completa", metavar="BASE8", help="completa base de 8 chars (ex: 12345678, X1234567, A5881850)")
    parser.add_argument("--completa_dni", metavar="BASE8", help="completa DNI a partir de 8 digitos")
    parser.add_argument("--completa_nie", metavar="BASE8", help="completa NIE a partir de XYZ+7 digitos")
    parser.add_argument("--completa_cif", metavar="BASE8", help="completa CIF a partir de letra+7 digitos")
    args = parser.parse_args()

    if args.valida_nif is not None:
        valido = valida_nif_es(args.valida_nif)
        print("valido" if valido else "invalido")
        sys.exit(0 if valido else 1)

    if args.valida_dni is not None:
        valido = valida_dni(args.valida_dni)
        print("valido" if valido else "invalido")
        sys.exit(0 if valido else 1)

    if args.valida_nie is not None:
        valido = valida_nie(args.valida_nie)
        print("valido" if valido else "invalido")
        sys.exit(0 if valido else 1)

    if args.valida_cif is not None:
        valido = valida_cif(args.valida_cif)
        print("valido" if valido else "invalido")
        sys.exit(0 if valido else 1)

    if args.completa is not None:
        try:
            nif = completa_nif_es(args.completa)
            print(nif)
            sys.exit(0)
        except ValueError as e:
            print(f"erro: {e}", file=sys.stderr)
            sys.exit(2)

    if args.completa_dni is not None:
        try:
            print(completa_dni(args.completa_dni))
            sys.exit(0)
        except ValueError as e:
            print(f"erro: {e}", file=sys.stderr)
            sys.exit(2)

    if args.completa_nie is not None:
        try:
            print(completa_nie(args.completa_nie))
            sys.exit(0)
        except ValueError as e:
            print(f"erro: {e}", file=sys.stderr)
            sys.exit(2)

    if args.completa_cif is not None:
        try:
            print(completa_cif(args.completa_cif))
            sys.exit(0)
        except ValueError as e:
            print(f"erro: {e}", file=sys.stderr)
            sys.exit(2)

    parser.print_help()
    sys.exit(2)


if __name__ == "__main__":
    main()
