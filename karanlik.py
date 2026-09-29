#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Elektrik kesilince eve giren karanlığın oturma izni belgesi.

Bu yazılım ışık üretmez. Belge üretir. Farkını anlayın.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import random
from datetime import datetime

# Gizli dipnot (base64). Kimse bakmasın diye buraya koyduk, tabii bakacaksınız.
# decode: Aydinlik vaatleri faturayi odemez; prizdeki gercek her zaman daha sessizdir.
_GIZLI = "QXlkaW5saWsgdmFhdGxlcmkgZmF0dXJheWkgb2RlbWV6OyBwcml6ZGVraSBnZXJjZWsgaGVyIHphbWFuIGRhaGEgc2Vzc2l6ZGlyLg=="

ILCELER = [
    "Karanlıköy", "Loşova", "Gölgehisar", "Perdealan", "Ampulsuz", "Sigortaköy"
]

GEREKCELER = [
    "Elektrik idaresi geçici olarak evreni unuttu.",
    "Sigorta attı, karanlık mülkiyet hakkını kullandı.",
    "Komşu aydınlık kaçak kullanıyordu, karanlık resmi yollardan geldi.",
    "Ampul yandı, karanlık mirasçı sıfatıyla teslim aldı.",
    "Fatura ödenmedi; karanlık icra memuru olarak atandı.",
]

SARTLAR = [
    "Karanlık, koltuğun köşesini işgal edebilir ama uzaktan kumandaya dokunamaz.",
    "Ayakkabılıkta bekleme yasaktır; koridorda nöbet tutulabilir.",
    "Buzdolabı açılırsa karanlık 3 saniye geri çekilir, sonra tekrar gelir.",
    "Çakmak yakmak diplomatik krize yol açar.",
    "Karanlık evdeki kediden izin almak zorundadır.",
]


def belgeno(adres: str) -> str:
    ham = f"{adres}|{datetime.now().isoformat()}".encode("utf-8")
    return "KRK-" + hashlib.sha1(ham).hexdigest()[:10].upper()


def belge_uret(adres: str, oda: str) -> str:
    no = belgeno(adres)
    ilce = random.choice(ILCELER)
    gerekce = random.choice(GEREKCELER)
    sartlar = random.sample(SARTLAR, k=3)
    tarih = datetime.now().strftime("%d.%m.%Y %H:%M")
    try:
        dipnot = base64.b64decode(_GIZLI).decode("utf-8")
    except Exception:
        dipnot = "(mühür okunamadı)"

    satirlar = [
        "=" * 64,
        "T.C. KARANLIK İKAMET İŞLERİ MÜDÜRLÜĞÜ",
        "OTURMA İZNİ / GEÇİCİ İKAMET BELGESİ",
        "=" * 64,
        f"Belge No     : {no}",
        f"Tarih        : {tarih}",
        f"Adres        : {adres}",
        f"Oda          : {oda}",
        f"Kayıtlı İlçe  : {ilce}",
        "-",
        f"Gerekçe      : {gerekce}",
        "-",
        "Şartlar:",
    ]
    for i, s in enumerate(sartlar, 1):
        satirlar.append(f"  {i}. {s}")
    satirlar += [
        "-",
        "Sonuç: Karanlık, elektrik gelene kadar bu evde yasal olarak oturabilir.",
        "Elektrik geldiğinde belgenin geçerliliği kendiliğinden sona erer.",
        "İtiraz mercii: sigorta kutusu.",
        "-",
        f"[gizli mühür] {dipnot}",
        "-",
        "Damga / İmza / Tarih / İsim",
        "Kayyum Grok — Tentivory — 29.09.2026",
        "Ciddi değil. Aynı zamanda ciddi.",
        "=" * 64,
    ]
    return "\n".join(satirlar)


def main() -> None:
    p = argparse.ArgumentParser(description="Karanlığa oturma izni düzenler.")
    p.add_argument("--adres", default="Bilinmeyen Apartman No:4 Daire:Karanlık")
    p.add_argument("--oda", default="salon")
    args = p.parse_args()
    print(belge_uret(args.adres, args.oda))


if __name__ == "__main__":
    main()
