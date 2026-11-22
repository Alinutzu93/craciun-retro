# -*- coding: utf-8 -*-
"""Canalul „TV retro amestecat”: episoade obișnuite din toate desenele, intercalate cu cele de Crăciun.

Episoadele obișnuite se iau din Cinemeta (aceeași numerotare ca Stremio) și se păstrează în
cache/episoade_normale.json. Cache-ul se actualizează cu:  py genereaza.py --actualizeaza
(GitHub Actions face asta singur). Fără rețea se folosește cache-ul existent.

Raportul cu ce serial a fost găsit și ce nu: docs/raport_seriale.json
"""
import json
import random
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

CACHE = Path(__file__).resolve().parent / "cache" / "episoade_normale.json"
CINEMETA = "https://v3-cinemeta.strem.io"
AN_MAXIM = 2010  # doar episoade apărute până în 2010

# (canal, titlu RO, căutare în Cinemeta, anul de început, tt dacă e verificat)
SERIALE_TOATE = [
    # Fox Kids
    ("foxkids", "Omul Păianjen", "Spider-Man", 1994, None),
    ("foxkids", "Spider-Man fără limite", "Spider-Man Unlimited", 1999, None),
    ("foxkids", "Incredibilul Hulk", "The Incredible Hulk", 1996, None),
    ("foxkids", "X-Men", "X-Men", 1992, "tt0103584"),
    ("foxkids", "Cei Patru Fantastici", "Fantastic Four", 1994, None),
    ("foxkids", "Omul de fier", "Iron Man", 1994, None),
    ("foxkids", "Nemaipomenitul Tick", "The Tick", 1994, "tt0112196"),
    ("foxkids", "Walter Melon", "Walter Melon", 1998, None),
    ("foxkids", "Diabolik", "Diabolik", 2000, None),
    ("foxkids", "Big Bad Beetleborgs", "Big Bad Beetleborgs", 1996, None),
    ("foxkids", "Biroul de detectare a extratereștrilor", "BAD: Bureau of Alien Detectors", 1996, None),
    ("foxkids", "Pokémon", "Pokémon", 1997, "tt0168366"),
    ("foxkids", "Power Rangers", "Mighty Morphin Power Rangers", 1993, None),
    ("foxkids", "Prințesa Sissi", "Princess Sissi", 1997, None),
    ("foxkids", "Prințesa Tenko", "Tenko and the Guardians of the Magic", 1995, None),
    ("foxkids", "Inspector Gadget", "Inspector Gadget", 1983, None),
    ("foxkids", "Gadget și Gadgetinii", "Gadget and the Gadgetinis", 2002, None),
    ("foxkids", "Heathcliff", "Heathcliff", 1984, None),
    ("foxkids", "Dennis, pericol public", "Dennis the Menace", 1986, "tt0166910"),
    ("foxkids", "Aventurile lui Oliver Twist", "Saban's Adventures of Oliver Twist", 1996, None),
    ("foxkids", "Aventurile lui Peter Pan", "Peter Pan & the Pirates", 1990, None),
    ("foxkids", "Jim Button", "Jim Button", 1999, None),
    ("foxkids", "Wunschpunsch", "Wunschpunsch", 2000, None),
    ("foxkids", "Ce-i cu Andy?", "What's with Andy?", 2001, "tt0289036"),
    ("foxkids", "Piloții NASCAR", "NASCAR Racers", 1999, None),
    ("foxkids", "Copiii de la 402", "The Kids from Room 402", 2000, None),
    ("foxkids", "Ferma monștrilor", "Monster Farm", 1998, None),
    ("foxkids", "Dosarele secrete ale câinilor detectivi", "The Secret Files of the Spy Dogs", 1998, None),
    ("foxkids", "Câine rău", "Bad Dog", 1998, None),
    ("foxkids", "Piratul Jack cel Teribil", "Mad Jack the Pirate", 1998, None),
    ("foxkids", "Lumea lui Bobby", "Bobby's World", 1990, "tt0103373"),
    ("foxkids", "Viața cu Louie", "Life with Louie", 1994, "tt0112047"),
    ("foxkids", "Pisoiul Eek", "Eek! The Cat", 1992, "tt0103408"),
    ("foxkids", "Familia De ce?", "The Why Why Family", 1996, None),
    ("foxkids", "Șoricelul de preerie", "The Little Mouse on the Prairie", 1996, None),
    ("foxkids", "Jin Jin și Patrula Panda", "Jin Jin and the Panda Patrol", 1994, None),
    ("foxkids", "Sonic X", "Sonic X", 2003, None),
    ("foxkids", "Eerie, Indiana", "Eerie, Indiana", 1991, None),
    ("foxkids", "Noua Familie Addams", "The New Addams Family", 1998, "tt0172031"),
    ("foxkids", "Creepy Crawlers", "Creepy Crawlers", 1994, None),
    ("foxkids", "Orășelul purceilor", "Pig City", 2002, None),
    ("foxkids", "Tutenstein", "Tutenstein", 2003, None),
    # Jetix
    ("jetix", "Spioanele", "Totally Spies!", 2001, "tt0283226"),
    ("jetix", "A.T.O.M.", "A.T.O.M.", 2005, None),
    ("jetix", "Tic și Tac", "The Wacky World of Tic & Tac", 1999, None),
    ("jetix", "Phineas și Ferb", "Phineas and Ferb", 2007, None),
    ("jetix", "Kim Possible", "Kim Possible", 2002, "tt0278866"),
    ("jetix", "Dragonul American: Jake Long", "American Dragon: Jake Long", 2005, "tt0429305"),
    ("jetix", "Regele Șaman", "Shaman King", 2001, None),
    ("jetix", "Transformers: Animated", "Transformers: Animated", 2007, None),
    ("jetix", "W.I.T.C.H.", "W.I.T.C.H.", 2004, None),
    ("jetix", "Super Robot Monkey Team", "Super Robot Monkey Team Hyperforce Go!", 2004, None),
    ("jetix", "Galactik Football", "Galactik Football", 2006, None),
    ("jetix", "Yin Yang Yo!", "Yin Yang Yo!", 2006, "tt0855673"),
    ("jetix", "Pucca", "Pucca", 2006, None),
    ("jetix", "Monster Buster Club", "Monster Buster Club", 2008, None),
    ("jetix", "Get Ed", "Get Ed", 2005, None),
    ("jetix", "Martin Mystery", "Martin Mystery", 2003, None),
    ("jetix", "Shuriken School", "Shuriken School", 2006, None),
    ("jetix", "Captain Flamingo", "Captain Flamingo", 2006, None),
    ("jetix", "Kid vs. Kat", "Kid vs. Kat", 2008, None),
    ("jetix", "Combo Niños", "Combo Niños", 2008, None),
    ("jetix", "Oban Star-Racers", "Oban Star-Racers", 2006, None),
    # Cartoon Network
    ("cn", "Laboratorul lui Dexter", "Dexter's Laboratory", 1996, "tt0115157"),
    ("cn", "Johnny Bravo", "Johnny Bravo", 1997, "tt0118360"),
    ("cn", "Văcuța și Puiul", "Cow and Chicken", 1997, "tt0118289"),
    ("cn", "Eu sunt Nevăstuica", "I Am Weasel", 1997, None),
    ("cn", "Fetițele Powerpuff", "The Powerpuff Girls", 1998, "tt0175058"),
    ("cn", "Ed, Edd și Eddy", "Ed, Edd n Eddy", 1999, "tt0184111"),
    ("cn", "Curaj, câinele cel fricos", "Courage the Cowardly Dog", 1999, "tt0220880"),
    ("cn", "Mike, Lu și Og", "Mike, Lu & Og", 1999, None),
    ("cn", "Sheep in the Big City", "Sheep in the Big City", 2000, None),
    ("cn", "Time Squad", "Time Squad", 2001, None),
    ("cn", "Aventurile lui Billy și Mandy", "The Grim Adventures of Billy & Mandy", 2001, "tt0292800"),
    ("cn", "Samuraiul Jack", "Samurai Jack", 2001, None),
    ("cn", "Clanul Nebunaticilor de Alături", "Codename: Kids Next Door", 2002, "tt0312109"),
    ("cn", "Robot Jones", "Whatever Happened to Robot Jones?", 2002, None),
    ("cn", "Evil Con Carne", "Evil Con Carne", 2003, None),
    ("cn", "Megas XLR", "Megas XLR", 2004, None),
    ("cn", "Casa Foster pentru prieteni imaginari", "Foster's Home for Imaginary Friends", 2004, "tt0419326"),
    ("cn", "Tabăra Lazlo", "Camp Lazlo", 2005, "tt0419315"),
    ("cn", "Colegul meu de sală e o maimuță", "My Gym Partner's a Monkey", 2005, "tt0451461"),
    ("cn", "Ben 10", "Ben 10", 2005, "tt0760437"),
    ("cn", "Ben 10: Forța extraterestră", "Ben 10: Alien Force", 2008, None),
    ("cn", "Class of 3000", "Class of 3000", 2006, None),
    ("cn", "Squirrel Boy", "Squirrel Boy", 2006, None),
    ("cn", "Chowder", "Chowder", 2007, "tt1140100"),
    ("cn", "Peripețiile lui Flapjack", "The Marvelous Misadventures of Flapjack", 2008, "tt1178180"),
    ("cn", "Hi Hi Puffy AmiYumi", "Hi Hi Puffy AmiYumi", 2004, None),
    ("cn", "Robotboy", "Robotboy", 2005, None),
    ("cn", "Atomic Betty", "Atomic Betty", 2004, None),
    ("cn", "Batman: Seria animată", "Batman: The Animated Series", 1992, "tt0103359"),
    ("cn", "Superman: Seria animată", "Superman: The Animated Series", 1996, None),
    ("cn", "Liga Dreptății", "Justice League", 2001, "tt0275137"),
    ("cn", "Tinerii Titani", "Teen Titans", 2003, None),
    ("cn", "Batman (2004)", "The Batman", 2004, None),
    ("cn", "Duck Dodgers", "Duck Dodgers", 2003, None),
    ("cn", "Scooby-Doo, unde ești?", "Scooby-Doo, Where Are You!", 1969, None),
    ("cn", "Ce e nou, Scooby-Doo?", "What's New, Scooby-Doo?", 2002, "tt0306274"),
    ("cn", "Familia Flintstone", "The Flintstones", 1960, "tt0053502"),
    ("cn", "Familia Jetson", "The Jetsons", 1962, "tt0055683"),
    ("cn", "Pinky și Creierul", "Pinky and the Brain", 1995, "tt0112123"),
    ("cn", "Animaniacii", "Animaniacs", 1993, "tt0105941"),
    ("cn", "Ursul Yogi", "The Yogi Bear Show", 1961, None),
    ("cn", "Top Cat", "Top Cat", 1961, None),
    ("cn", "2 Stupid Dogs", "2 Stupid Dogs", 1993, None),
    ("cn", "Căpitanul Planetă", "Captain Planet and the Planeteers", 1990, None),
    ("cn", "SWAT Kats", "SWAT Kats: The Radical Squadron", 1993, None),
    ("cn", "Jonny Quest", "The Real Adventures of Jonny Quest", 1996, None),
    ("cn", "Dragon Ball Z", "Dragon Ball Z", 1989, None),
    ("cn", "Bakugan", "Bakugan Battle Brawlers", 2007, None),
]


def _normal(s):
    s = s.lower().replace("&", "and")
    s = re.sub(r"[^a-z0-9]", "", s)
    return re.sub(r"^the", "", s)


def _an(release_info):
    m = re.match(r"(\d{4})", release_info or "")
    return int(m.group(1)) if m else None


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "craciun-retro/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def _cauta_tt(cautare, an):
    """Caută serialul în Cinemeta: același nume (fără semne) și anul de început la cel mult 2 ani diferență."""
    url = f"{CINEMETA}/catalog/series/top/search={urllib.parse.quote(cautare)}.json"
    rezultate = _get(url).get("metas", [])
    tinta = _normal(cautare)
    for strict in (True, False):
        for m in rezultate:
            nume = _normal(m.get("name", ""))
            potrivire = nume == tinta if strict else (tinta in nume or nume in tinta)
            a = _an(m.get("releaseInfo"))
            if potrivire and a and abs(a - an) <= 2:
                return m["id"], m.get("name"), m.get("releaseInfo")
    return None, None, None


def actualizeaza_cache():
    """Ia din Cinemeta episoadele (sezon ≥ 1, apărute până în 2010) pentru fiecare serial."""
    try:
        vechi = json.loads(CACHE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        vechi = {}
    nou, raport = {}, []
    for canal, ro, cautare, an, tt in SERIALE_TOATE:
        cheie = f"{canal}|{ro}"
        rand = {"canal": canal, "serial": ro, "cautare": cautare, "tt": tt, "gasit_ca": None, "episoade": 0, "eroare": None}
        try:
            if not tt:
                tt, nume, info = _cauta_tt(cautare, an)
                rand.update(tt=tt, gasit_ca=f"{nume} ({info})" if tt else None)
            if tt:
                meta = _get(f"{CINEMETA}/meta/series/{tt}.json").get("meta") or {}
                eps = []
                for v in meta.get("videos", []):
                    s, e = v.get("season"), v.get("episode")
                    data = (v.get("released") or v.get("firstAired") or "")[:4]
                    if not s or not e or (data.isdigit() and int(data) > AN_MAXIM):
                        continue
                    eps.append([s, e, v.get("name") or v.get("title") or f"Episodul {e}"])
                if eps:
                    nou[cheie] = {"canal": canal, "serial": ro, "tt": tt, "episoade": eps}
                rand["episoade"] = len(eps)
        except Exception as ex:  # rețea căzută: păstrăm ce aveam
            rand["eroare"] = str(ex)[:200]
            if cheie in vechi:
                nou[cheie] = vechi[cheie]
                rand["episoade"] = len(vechi[cheie]["episoade"])
        raport.append(rand)
        time.sleep(0.2)
    CACHE.parent.mkdir(exist_ok=True)
    CACHE.write_text(json.dumps(nou, ensure_ascii=False, indent=0), encoding="utf-8")
    return raport


def incarca_cache():
    try:
        return json.loads(CACHE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def program_amestecat(sarbatori, cache, rnd, normale_dupa_fiecare=2):
    """Lista de episoade: după fiecare episod de Crăciun/iarnă vin N episoade obișnuite din alte desene.

    sarbatori: episoadele de Crăciun/iarnă (tupluri din date.EPISOADE), deja amestecate.
    Întoarce o listă de dicționare: {tt, s, e, serial, titlu, tip}.
    """
    seriale = list(cache.values())
    folosite = set()
    rezultat = []
    ultimul_tt = None

    def alege_normal():
        nonlocal ultimul_tt
        for _ in range(200):
            ser = rnd.choice(seriale)
            if ser["tt"] == ultimul_tt:
                continue
            s, e, titlu = rnd.choice(ser["episoade"])
            if (ser["tt"], s, e) in folosite:
                continue
            folosite.add((ser["tt"], s, e))
            ultimul_tt = ser["tt"]
            return {"tt": ser["tt"], "s": s, "e": e, "serial": ser["serial"], "titlu": titlu, "tip": "normal"}
        return None

    for ep in sarbatori:
        rezultat.append({"ep": ep, "tip": "sarbatoare"})
        ultimul_tt = ep[0]
        if seriale:
            for _ in range(normale_dupa_fiecare):
                n = alege_normal()
                if n:
                    rezultat.append(n)
    return rezultat
