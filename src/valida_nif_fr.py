#!/usr/bin/env python3
import argparse
import sys


def _normalizar(nif):
    if nif is None:
        return None
    s = str(nif).strip()
    if len(s) >= 2 and s[:2].upper() == "FR":
        prefix = s[:2]
        resto = s[2:].strip()
        if prefix != "FR" and prefix != "fr":
            return None
        s = resto
    s = s.replace("-", "").replace(" ", "").replace(".", "").upper()
    return s


def _luhn_soma(s):
    total = 0
    rev = s[::-1]
    for i, ch in enumerate(rev):
        d = int(ch)
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total


def _luhn_valido(s):
    return _luhn_soma(s) % 10 == 0


def _calcular_luhn(base):
    s = base + "0"
    total = _luhn_soma(s)
    return (10 - (total % 10)) % 10


def valida_siren(nif):
    s = _normalizar(nif)
    if s is None:
        return False
    if len(s) != 9:
        return False
    if not s.isdigit():
        return False
    if s == "000000000":
        return False
    return _luhn_valido(s)


def valida_siret(nif):
    s = _normalizar(nif)
    if s is None:
        return False
    if len(s) != 14:
        return False
    if not s.isdigit():
        return False
    if s == "00000000000000":
        return False
    if not valida_siren(s[:9]):
        return False
    return _luhn_valido(s)


def valida_tva_fr(nif):
    s = _normalizar(nif)
    if s is None:
        return False
    if len(s) != 11:
        return False
    if not s[:2].isdigit():
        return False
    if not s[2:].isdigit():
        return False
    siren = s[2:]
    if not valida_siren(siren):
        return False
    chave = int(s[:2])
    esperado = (12 + 3 * (int(siren) % 97)) % 97
    return chave == esperado


def valida_tva(nif):
    return valida_tva_fr(nif)


def _nir_normalizar(nif):
    if nif is None:
        return None
    s = str(nif).strip()
    if len(s) >= 2 and s[:2].upper() == "FR":
        prefix = s[:2]
        resto = s[2:].strip()
        if prefix != "FR" and prefix != "fr":
            return None
        s = resto
    s = s.replace("-", "").replace(" ", "").replace(".", "").upper()
    return s


def valida_nir(nif):
    s = _nir_normalizar(nif)
    if s is None:
        return False
    if len(s) != 15:
        return False
    base = s[:13]
    chave = s[13:]
    if not chave.isdigit():
        return False
    sexo = base[0]
    if sexo not in "1278":
        return False
    if not base[1:5].isdigit():
        return False
    dep = base[5:7]
    resto_base = base[7:]
    if dep in ("2A", "2B"):
        if not resto_base.isdigit():
            return False
        num_str = base[:5] + ("19" if dep == "2A" else "18") + resto_base
    elif dep.isdigit():
        if not resto_base.isdigit():
            return False
        if not base.isdigit():
            return False
        num_str = base
    else:
        return False
    try:
        resto = int(num_str) % 97
        esperado = 97 - resto
        return int(chave) == esperado
    except ValueError:
        return False


def valida_nif_fr(nif):
    return valida_siren(nif) or valida_siret(nif) or valida_tva_fr(nif) or valida_nir(nif)


def valida_nif(nif):
    return valida_nif_fr(nif)


def completa_siren(base8):
    s = _normalizar(base8)
    if s is None:
        raise ValueError("prefixo invalido (so FR/fr permitido)")
    s = s.strip()
    if len(s) != 8:
        raise ValueError("base SIREN deve ter exatamente 8 digitos")
    if not s.isdigit():
        raise ValueError("base SIREN deve conter apenas digitos")
    return s + str(_calcular_luhn(s))


def completa_siret(base13):
    s = _normalizar(base13)
    if s is None:
        raise ValueError("prefixo invalido (so FR/fr permitido)")
    s = s.strip()
    if len(s) != 13:
        raise ValueError("base SIRET deve ter exatamente 13 digitos")
    if not s.isdigit():
        raise ValueError("base SIRET deve conter apenas digitos")
    if not valida_siren(s[:9]):
        raise ValueError("base SIRET contem SIREN invalido nos 9 primeiros digitos")
    return s + str(_calcular_luhn(s))


def completa_tva_fr(siren):
    s = _normalizar(siren)
    if s is None:
        raise ValueError("prefixo invalido (so FR/fr permitido)")
    s = s.strip()
    if len(s) != 9:
        raise ValueError("SIREN deve ter exatamente 9 digitos")
    if not s.isdigit():
        raise ValueError("SIREN deve conter apenas digitos")
    if not valida_siren(s):
        raise ValueError("SIREN invalido (Luhn)")
    chave = (12 + 3 * (int(s) % 97)) % 97
    return f"FR{chave:02d}{s}"


def completa_nir(base13):
    s = _nir_normalizar(base13)
    if s is None:
        raise ValueError("prefixo invalido (so FR/fr permitido)")
    s = s.strip()
    if len(s) != 13:
        raise ValueError("base NIR deve ter exatamente 13 caracteres")
    sexo = s[0]
    if sexo not in "1278":
        raise ValueError("NIR deve comecar por 1, 2, 7 ou 8")
    dep = s[5:7]
    if dep in ("2A", "2B"):
        if not s[1:5].isdigit() or not s[7:].isdigit():
            raise ValueError("base NIR invalida (formato 2A/2B)")
        num_str = s[:5] + ("19" if dep == "2A" else "18") + s[7:]
    else:
        if not s.isdigit():
            raise ValueError("base NIR deve conter apenas digitos (ou 2A/2B no departamento)")
        num_str = s
    try:
        resto = int(num_str) % 97
    except ValueError:
        raise ValueError("base NIR invalida")
    chave = 97 - resto
    return s + f"{chave:02d}"


def completa_nif_fr(base):
    s = _normalizar(base)
    if s is None:
        raise ValueError("prefixo invalido (so FR/fr permitido)")
    s = s.strip().replace("-", "").replace(" ", "").replace(".", "").upper()
    if len(s) == 8 and s.isdigit():
        return completa_siren(s)
    if len(s) == 13 and (s.isdigit() or (len(s) >= 7 and s[5:7] in ("2A", "2B"))):
        if s[:9].isdigit() and valida_siren(s[:9]):
            try:
                return completa_siret(s)
            except ValueError:
                pass
        try:
            return completa_nir(s)
        except ValueError:
            return completa_siret(s)
    if len(s) == 9 and s.isdigit():
        return completa_tva_fr(s)
    raise ValueError("formato de base desconhecido (use 8 digitos para SIREN, 13 para SIRET/NIR, 9 para TVA)")


def completa_nif(base):
    return completa_nif_fr(base)


def main():
    parser = argparse.ArgumentParser(description="Valida SIREN/SIRET/TVA/NIR frances")
    parser.add_argument("--valida_nif", metavar="NIF", help="valida SIREN/SIRET/TVA/NIR (ex: 732829320, 73282932000074, FR40303265045, 1841275001123)")
    parser.add_argument("--valida_siren", metavar="SIREN", help="valida apenas SIREN (9 digitos Luhn)")
    parser.add_argument("--valida_siret", metavar="SIRET", help="valida apenas SIRET (14 digitos Luhn)")
    parser.add_argument("--valida_tva", metavar="TVA", help="valida apenas TVA FR (FR+2+9)")
    parser.add_argument("--valida_nir", metavar="NIR", help="valida apenas NIR (15 digitos mod97)")
    parser.add_argument("--completa", metavar="BASE", help="completa base (8->SIREN, 13->SIRET/NIR, 9->TVA)")
    parser.add_argument("--completa_siren", metavar="BASE8", help="completa SIREN a partir de 8 digitos")
    parser.add_argument("--completa_siret", metavar="BASE13", help="completa SIRET a partir de 13 digitos")
    parser.add_argument("--completa_tva", metavar="SIREN9", help="completa TVA a partir de SIREN 9 digitos")
    parser.add_argument("--completa_nir", metavar="BASE13", help="completa NIR a partir de 13 chars")
    args = parser.parse_args()

    if args.valida_nif is not None:
        valido = valida_nif_fr(args.valida_nif)
        print("valido" if valido else "invalido")
        sys.exit(0 if valido else 1)

    if args.valida_siren is not None:
        valido = valida_siren(args.valida_siren)
        print("valido" if valido else "invalido")
        sys.exit(0 if valido else 1)

    if args.valida_siret is not None:
        valido = valida_siret(args.valida_siret)
        print("valido" if valido else "invalido")
        sys.exit(0 if valido else 1)

    if args.valida_tva is not None:
        valido = valida_tva_fr(args.valida_tva)
        print("valido" if valido else "invalido")
        sys.exit(0 if valido else 1)

    if args.valida_nir is not None:
        valido = valida_nir(args.valida_nir)
        print("valido" if valido else "invalido")
        sys.exit(0 if valido else 1)

    if args.completa is not None:
        try:
            print(completa_nif_fr(args.completa))
            sys.exit(0)
        except ValueError as e:
            print(f"erro: {e}", file=sys.stderr)
            sys.exit(2)

    if args.completa_siren is not None:
        try:
            print(completa_siren(args.completa_siren))
            sys.exit(0)
        except ValueError as e:
            print(f"erro: {e}", file=sys.stderr)
            sys.exit(2)

    if args.completa_siret is not None:
        try:
            print(completa_siret(args.completa_siret))
            sys.exit(0)
        except ValueError as e:
            print(f"erro: {e}", file=sys.stderr)
            sys.exit(2)

    if args.completa_tva is not None:
        try:
            print(completa_tva_fr(args.completa_tva))
            sys.exit(0)
        except ValueError as e:
            print(f"erro: {e}", file=sys.stderr)
            sys.exit(2)

    if args.completa_nir is not None:
        try:
            print(completa_nir(args.completa_nir))
            sys.exit(0)
        except ValueError as e:
            print(f"erro: {e}", file=sys.stderr)
            sys.exit(2)

    parser.print_help()
    sys.exit(2)


if __name__ == "__main__":
    main()
