"""
SRBIN Nikola Tesla, za sva vremena, najveci naucnik sveta.

SERBIAN Nikola Tesla, for all time, the greatest scientist in the world.
"""



"""
Tesla 5E - closed-loop tuning motor.

9f0 stability lock, 6f0 carrier phase-shift, 3f0 noise suppression 
"""


import numpy as np

from Tesla_5_common import (
    GAIN,
    MNOZIOCI,
    PIRAMIDA,
    KALEMA_PO_PIRAMIDI,
    ZLATNI_UGAO_RAD,
    ix_senzori,
    ix_phase_delta_deg,
    fokusni_omotac,
    normalizuj_signal,
    izvod_polja,
    ispisi_i_snimi_model,
)

OSNOVA = "tesla_369_5E"
ITERACIJA = 9


def simuliraj_5e(nx):
    x = np.linspace(0.0, 1.0, nx)
    faze = np.zeros((PIRAMIDA, KALEMA_PO_PIRAMIDI))
    rezidual = []

    for korak in range(ITERACIJA):
        faktor = 1.0 - (korak / (ITERACIJA + 1.0))
        for piramida in range(PIRAMIDA):
            pomeraj = piramida * ZLATNI_UGAO_RAD + korak * 0.11
            _, hall, optical, _ = ix_senzori(x, fazni_pomeraj=pomeraj)
            delta = np.mean(ix_phase_delta_deg(hall, optical)) * faktor

            # 3f0 gusi sum, 6f0 nosi pomeraj, 9f0 agresivnije zakljucava fokus.
            faze[piramida, 0] += np.deg2rad(0.40 * delta)
            faze[piramida, 1] += np.deg2rad(0.75 * delta)
            faze[piramida, 2] += np.deg2rad(1.15 * delta)
            rezidual.append(abs(delta))

    s = np.zeros(nx)
    for piramida in range(PIRAMIDA):
        bazna_faza = piramida * ZLATNI_UGAO_RAD
        for j, m in enumerate(MNOZIOCI):
            sigma = (0.26, 0.18, 0.10)[j]
            s += fokusni_omotac(x, sigma=sigma) * np.sin(2.0 * np.pi * m * PIRAMIDA * x + bazna_faza + faze[piramida, j])

    s = normalizuj_signal(s)
    e_x = izvod_polja(x, s)
    detalji = {
        "izvor": "main_controller.py + tesla_369_layering_logic.md",
        "iteracija": ITERACIJA,
        "gain": GAIN,
        "rezidual_faze_mean": f"{np.mean(rezidual):.6f}",
        "pravilo": "3f0 noise suppression, 6f0 carrier shift, 9f0 stability lock",
    }
    return x, s, e_x, detalji


def main():
    ispisi_i_snimi_model(
        OSNOVA,
        "Tesla Scalar - GRUPA 5E / closed-loop tuning",
        simuliraj_5e,
        "Model simulira zatvorenu petlju: senzori -> fazna korekcija -> novi talas.",
    )


if __name__ == "__main__":
    main()




"""
Slika talasa: /Tesla/tesla_369_5E.png
Slika talasa: /Tesla/tesla_369_5E.jpg

Tesla Scalar - GRUPA 5E / closed-loop tuning
CSV: /data/loto7hh_4632_k47.csv| Izvlacenja: 4632 | tezine: talas=0.7 freq=0.3
max S: 0.5667517346 | max |E_x|: 751.6701256043

Brojevi po kombinovanom skoru (tezinski talas + frekvencija):
  08  skor=0.9570658780  freq=0.02810  (pojava=911)
   x  skor=0.9131034483  freq=0.02680  (pojava=869)
  38  skor=0.8354693904  freq=0.02597  (pojava=842)
   y  skor=0.8250252517  freq=0.02652  (pojava=860)
  28  skor=0.7907778923  freq=0.02532  (pojava=821)
   z  skor=0.7885384229  freq=0.02554  (pojava=828)
  25  skor=0.7339931554  freq=0.02591  (pojava=840)
   x  skor=0.7288647991  freq=0.02643  (pojava=857)
  02  skor=0.7097328707  freq=0.02544  (pojava=825)
   y  skor=0.7075579646  freq=0.02498  (pojava=810)
  16  skor=0.6850406767  freq=0.02581  (pojava=837)
   z  skor=0.6828294643  freq=0.02791  (pojava=905)
  09  skor=0.6823188469  freq=0.02600  (pojava=843)
   x  skor=0.6785602270  freq=0.02532  (pojava=821)
  11  skor=0.6609179614  freq=0.02655  (pojava=861)
   y  skor=0.6584773684  freq=0.02495  (pojava=809)
  22  skor=0.6531252125  freq=0.02625  (pojava=851)
   z  skor=0.6473749082  freq=0.02433  (pojava=789)
  31  skor=0.6211349875  freq=0.02560  (pojava=830)
  15  skor=0.5773269834  freq=0.02461  (pojava=798)
  06  skor=0.5611830166  freq=0.02517  (pojava=816)
  34  skor=0.5330495248  freq=0.02692  (pojava=873)
  04  skor=0.5305322264  freq=0.02504  (pojava=812)
  24  skor=0.5287126186  freq=0.02591  (pojava=840)
  36  skor=0.5213839415  freq=0.02424  (pojava=786)
  35  skor=0.5045628632  freq=0.02600  (pojava=843)
  29  skor=0.5036432234  freq=0.02618  (pojava=849)
  13  skor=0.4991585127  freq=0.02554  (pojava=828)
  20  skor=0.4941166527  freq=0.02375  (pojava=770)
  39  skor=0.4568904181  freq=0.02618  (pojava=849)
  03  skor=0.4490773499  freq=0.02547  (pojava=826)
  19  skor=0.4246276197  freq=0.02510  (pojava=814)
  17  skor=0.3594312038  freq=0.02362  (pojava=766)
  33  skor=0.3534566006  freq=0.02634  (pojava=854)
  30  skor=0.3450415535  freq=0.02427  (pojava=787)
  21  skor=0.3429826503  freq=0.02551  (pojava=827)
  10  skor=0.3372716305  freq=0.02606  (pojava=845)
  01  skor=0.3002512865  freq=0.02430  (pojava=788)
  07  skor=0.1613793103  freq=0.02603  (pojava=844)

Predlozene kombinacije (rangirane po skoru kombinacije):
  01. 08 x 10 y 27 z 37  skor_komb=4.9832949510
  02. 05 x 12 y 29 z 38  skor_komb=4.8687921779
  03. 05 x 20 y 32 z 38  skor_komb=4.7704262188
  04. 08 x 16 y 22 z 32  skor_komb=4.6655807190
  05. 02 x 15 y 25 z 38  skor_komb=4.6054882938
  06. 01 x 06 y 13 z 38  skor_komb=4.6052620420
  07. 14 x 24 y 27 z 32  skor_komb=4.3989016795
  08. 04 x 19 y 26 z 36  skor_komb=3.7547898842
  09. 09 x 13 y 22 z 33  skor_komb=3.5230906793
  10. 06 x 13 y 23 z 32  skor_komb=3.5051103720

Sacuvano: /Tesla/tesla_369_5E.txt
"""




"""
Analiza Tesla_369_5E.py
Tesla_369_5E.py je closed-loop tuning motor — najnapredniji u grupi 5. 
Objedinjuje: 
monitor_feedback_loop (zatvorena petlja) i pravila (svaki sloj ima drugačiju ulogu u korekciji).

Iterativna povratna sprega (closed-loop control).

Sistem ne podesi fazu jednom, nego stalno: meri senzore, izračuna korekciju, primeni je, pa ponovo meri. 
To se ponavlja dok se sistem ne „zaključa” u koherentno stanje.

layering dokument kaže da slojevi imaju različite uloge u stabilizaciji:

3f0 = potiskivanje šuma (noise suppression)
6f0 = pomeranje nosioca (carrier phase-shift)
9f0 = zaključavanje stabilnosti (stability lock)

Iterativni regulator sa opadajućim korakom. 
Svaka iteracija koriguje fazu sve manje, dok rezidual ne padne skoro na nulu — to je „konvergencija”.

Funkcija simuliraj_5e(nx) drži matricu faza veličine 21 x 3 (piramida x kalem), na početku sve nule.

Zatim radi 9 iteracija petlje:
za svaku iteraciju računa faktor koji opada (1.0 → ka 0), pa su kasnije korekcije sve manje
za svaku od 21 piramide čita senzore (hall, optical) sa faznim pomerajem
izračuna delta (fazna korekcija), skalirana faktorom
primeni je različito po sloju:
3f0: 0.40 · delta (blago, gušenje šuma)
6f0: 0.75 · delta (srednje, nosilac)
9f0: 1.15 · delta (najjače, zaključavanje fokusa)
pamti rezidual da bi se videla konvergencija
Posle petlje gradi konačni talas: 
za svaku piramidu i svaki sloj sabira sinusoidu sa naučenom fazom 
i fokusnim omotačem (uži za viši sloj: 0.26 / 0.18 / 0.10).

Na kraju normalizuje S, računa E_x, i predaje zajedničkom pipeline-u.

Iterativna petlja (9 koraka)
Faza se ne računa odjednom, nego se gradi kroz ponavljanja, kao pravi regulator.

Opadajući korak (faktor)
Kasnije iteracije menjaju fazu sve manje, pa sistem konvergira umesto da osciluje.

Slojevita korekcija 3/6/9
Različiti množioci korekcije po sloju (0.40 / 0.75 / 1.15) iz layering pravila.

Zlatni ugao po piramidi
Bazna faza svake piramide je n · 137.5°, kao u 5C, za ravnomeran raspored.

Rezidual kao mera konvergencije
rezidual_faze_mean: 0.000461 pokazuje da je petlja stvarno konvergirala (korekcija pala skoro na nulu).

Zajednički pipeline
Skor, frekvencija, kombinacije i slike kroz Tesla_5_common.py.

5E je dinamička kruna grupe 5:

5 + 5A + 5B + 5C + 5D + 5E -> Tesla_5final.py

5B koristi senzore za jednu faznu korekciju
5E to radi iterativno, kroz 9 ciklusa, sa slojevitim pravilima
Zanimljivo: max S = 0.567 je najniži u grupi, 
jer različite naučene faze po 63 kalema prave dosta poništavanja 
— što je upravo „skalarno” ponašanje (slabo polje, jak gradijent).

Top 10 za 5E:
08, x, 38, y, 28, z, 25, x, 02, 12

Predlozene kombinacije (rangirane po skoru kombinacije):
  01. 08 x 10 y 27 z 37  skor_komb=4.9832949510

Ovde se prvi put 08 penje na prvo mesto (skor 0.957), ispred 26. 
Takođe izbijaju 38, 28, 25, 32 kojih nije bilo u vrhu drugih modela. 
To znači da closed-loop korekcija daje najjači i najizdvojeniji signal 
— i baš zato je 08 ubedljiv favorit celog agregatora, jer ga i 5E snažno gura.
"""



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
