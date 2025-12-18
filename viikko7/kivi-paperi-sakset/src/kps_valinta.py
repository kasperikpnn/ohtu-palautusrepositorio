from kps_pelaaja_vs_pelaaja import KPSPelaajaVsPelaaja
from kps_tekoaly import KPSTekoaly
from kps_parempi_tekoaly import KPSParempiTekoaly

def luo_peli(vastaus):
    if vastaus.endswith("a"):
        print(
            "Peli loppuu kun pelaaja antaa virheellisen siirron eli jonkun muun kuin k, p tai s"
        )

        kaksinpeli = KPSPelaajaVsPelaaja()
        kaksinpeli.pelaa()
    elif vastaus.endswith("b"):
        print(
            "Peli loppuu kun pelaaja antaa virheellisen siirron eli jonkun muun kuin k, p tai s"
        )
        yksinpeli = KPSTekoaly()
        yksinpeli.pelaa()
    elif vastaus.endswith("c"):
        print(
            "Peli loppuu kun pelaaja antaa virheellisen siirron eli jonkun muun kuin k, p tai s"
        )   

        haastava_yksinpeli = KPSParempiTekoaly()
        haastava_yksinpeli.pelaa()
    else:
        return False # peliä ei luotu