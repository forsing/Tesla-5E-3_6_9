"""
SRBIN Nikola Tesla, za sva vremena, najveci naucnik sveta.

Tesla_369_5.py  —  GRUPA 5: Tesla 3-6-9 harmonijski motor
"""


"""
Zajednicki alati za GRUPU 5 (Tesla 3-6-9).

Svaki 5A-5E model vrati samo talas (x, S, E_x), a ovaj fajl radi isti loto
pipeline kao prethodne grupe: talasni skor, prava frekvencija, kombinacije,
txt i png/jpg izlaz.
"""

from pathlib import Path
import re

import numpy as np

from Tesla_Scalar_1 import (
    SEED,
    W_TALAS,
    W_FREQ,
    CSV_PATH,
    OUTPUT_DIR,
    MIN_BROJ,
    MAX_BROJ,
    ucitaj_izvlacenja,
    glavne_mere,
    ne_frekvencijski_skor,
    frekvencija_brojeva,
    kombinovani_skor,
    izaberi_kombinacije,
    skor_kombinacije,
    nacrtaj_polje,
)

BROJEVA_U_KOMBINACIJI = 7
MNOZIOCI = (3, 6, 9)
BAZA_HZ = 432.0
PIRAMIDA = 21
KALEMA_PO_PIRAMIDI = 3
GAIN = 0.35
ZLATNI_ODNOS_INV = 0.618
ZLATNI_UGAO_RAD = np.deg2rad(137.5)
SOLID_ANGLE = 0.598


def normalizuj_signal(s):
    s = np.asarray(s, dtype=float)
    m = float(np.max(np.abs(s)))
    if m > 0:
        return s / m
    return s


def izvod_polja(x, s):
    return -np.gradient(s, x[1] - x[0])


def fokusni_omotac(x, sigma=0.16, centar=0.5):
    return np.exp(-((x - centar) ** 2) / (2.0 * sigma ** 2))


def ix_senzori(x, fazni_pomeraj=0.0):
    """Sinteticki senzori: fazna greska, hall/magnetno, optika, temperatura."""
    phase_error_deg = 9.0 * np.sin(2 * np.pi * 3 * x + fazni_pomeraj) + 3.0 * np.sin(2 * np.pi * 9 * x)
    hall = 0.006 * np.sin(2 * np.pi * 6 * x + fazni_pomeraj)
    optical = 0.75 + 0.08 * np.cos(2 * np.pi * 9 * x - fazni_pomeraj)
    temp = 24.0 + 0.45 * np.sin(2 * np.pi * x + fazni_pomeraj)
    return phase_error_deg, hall, optical, temp


def ix_phase_delta_deg(hall, optical, gain=GAIN):
    """Formula iz phase_control.py: drift = hall*100 + (optical-0.75)*200."""
    scalar_drift = (hall * 100.0) + (optical - 0.75) * 200.0
    return -scalar_drift * gain


def ispisi_i_snimi_model(osnova, naslov, generator, napomena):
    izvlacenja = ucitaj_izvlacenja()
    n = len(izvlacenja)
    x, s, e_x, detalji = generator(n)
    mere = glavne_mere(s, e_x)

    energija = 0.5 * (s ** 2 + e_x ** 2)
    talas_skor, _ = ne_frekvencijski_skor(izvlacenja, energija)
    udeo, pojave = frekvencija_brojeva(izvlacenja)
    skor = kombinovani_skor(talas_skor, udeo)
    poredak = sorted(skor.items(), key=lambda kv: kv[1], reverse=True)
    freq_poredak = sorted(pojave, key=lambda b: (pojave[b], b), reverse=True)
    kombinacije = izaberi_kombinacije(skor, broj_kombinacija=10, seed=SEED)
    rangirane_kombinacije = sorted(
        ((k, skor_kombinacije(k, skor)) for k in kombinacije),
        key=lambda kv: kv[1],
        reverse=True,
    )
    png, jpg = nacrtaj_polje(x, s, e_x, osnova=osnova)

    txt_path = OUTPUT_DIR / f"{osnova}.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"{naslov}\n")
        f.write(f"CSV: {CSV_PATH}\n")
        f.write(f"Izvlacenja: {n} | Seed: {SEED} | tezine: talas={W_TALAS} freq={W_FREQ}\n")
        f.write(f"{napomena}\n")
        for k, v in detalji.items():
            f.write(f"{k}: {v}\n")
        f.write("\n")

        f.write("Brojevi po kombinovanom skoru (tezinski talas + frekvencija):\n")
        for b, vrednost in poredak:
            f.write(f"  {b:02d}  skor={vrednost:.10f}  freq={udeo[b]:.5f}  (pojava={pojave[b]})\n")

        f.write("\nTabela pravih frekvencija (opadajuce po freq, pa po broju):\n")
        f.write("  broj | pojava |   udeo\n")
        f.write("  -----+--------+--------\n")
        for b in freq_poredak:
            f.write(f"   {b:02d}  |  {pojave[b]:4d}  | {udeo[b]:.5f}\n")
        f.write(f"  ukupno pojava: {sum(pojave.values())}\n")

        f.write("\nPredlozene kombinacije (rangirane po skoru kombinacije):\n")
        for i, (k, s_komb) in enumerate(rangirane_kombinacije, start=1):
            f.write(f"  {i:02d}. " + " ".join(f"{v:02d}" for v in k) + f"  skor_komb={s_komb:.10f}\n")

        f.write("\nSlike talasa/polja:\n")
        f.write(f"  PNG: {png}\n")
        f.write(f"  JPG: {jpg}\n")

    print()
    print(naslov)
    print(f"CSV: {CSV_PATH} | Izvlacenja: {n} | tezine: talas={W_TALAS} freq={W_FREQ}")
    print(f"max S: {mere['max_S']:.10f} | max |E_x|: {mere['max_abs_E_x']:.10f}")

    print("\nBrojevi po kombinovanom skoru (tezinski talas + frekvencija):")
    for b, vrednost in poredak:
        print(f"  {b:02d}  skor={vrednost:.10f}  freq={udeo[b]:.5f}  (pojava={pojave[b]})")

    print("\nPredlozene kombinacije (rangirane po skoru kombinacije):")
    for i, (k, s_komb) in enumerate(rangirane_kombinacije, start=1):
        print(f"  {i:02d}. " + " ".join(f"{v:02d}" for v in k) + f"  skor_komb={s_komb:.10f}")

    print(f"\nSacuvano: {txt_path}")
    return txt_path


def ucitaj_model_iz_txt(path):
    tekst = Path(path).read_text(encoding="utf-8")
    skorovi = {}
    kombinacije = []
    citaj_brojeve = False
    citaj_kombinacije = False

    for linija in tekst.splitlines():
        if linija.startswith("Brojevi po"):
            citaj_brojeve = True
            citaj_kombinacije = False
            continue
        if linija.startswith("Tabela pravih frekvencija") or linija.startswith("Predlozene kombinacije"):
            citaj_brojeve = False
        if linija.startswith("Predlozene kombinacije"):
            citaj_kombinacije = True
            continue
        if linija.startswith("Slike"):
            citaj_kombinacije = False

        if citaj_brojeve:
            m = re.match(r"\s*(\d{2})\s+skor=([0-9.]+)", linija)
            if m:
                skorovi[int(m.group(1))] = float(m.group(2))

        if citaj_kombinacije:
            m = re.match(r"\s*\d+\.\s+((?:\d{2}\s+){6}\d{2})\s+skor_komb=([0-9.]+)", linija)
            if m:
                kombinacije.append((tuple(int(x) for x in m.group(1).split()), float(m.group(2))))

    if len(skorovi) != (MAX_BROJ - MIN_BROJ + 1):
        raise ValueError(f"Ne mogu da procitam svih 39 skorova iz: {path}")
    return skorovi, kombinacije


def minmax_recnik(skorovi):
    brojevi = list(skorovi.keys())
    vrednosti = np.array([skorovi[b] for b in brojevi], dtype=float)
    raspon = vrednosti.max() - vrednosti.min()
    if raspon <= 0:
        norm = np.zeros_like(vrednosti)
    else:
        norm = (vrednosti - vrednosti.min()) / raspon
    return dict(zip(brojevi, norm))



"""
source ~/tesla_env/bin/activate

Bitne verzije za tesla_env:

Paket	Verzija
python  3.11.13
numpy   2.2.6
scipy   1.15.3
pandas  3.0.3
matplotlib    3.10.9
k-Wave-python 0.6.2
pycharge      2.0.1
jax        0.10.1
jaxlib     0.10.1
jaxtyping  0.3.7
equinox    0.13.8
lineax     0.1.1
optimistix 0.1.0
ml-dtypes
(uz jax)
opencv-python 4.13.0.92
h5py          3.16.0
"""
