# -*- coding: utf-8 -*-
"""Lista completă a desenelor (pe canale) și tabelul cu episoadele de Crăciun, în .xlsx."""
from openpyxl import Workbook
from openpyxl.styles import Font

from date import CANALE, EPISOADE, FILME, SERIALE

F = "Listă de fani RO (blog 2013, lulutoys.ro)"
J = "Catalog Jetix Europe; difuzare în RO neconfirmată"
JR = "Listă de fani RO / Wikipedia (Disney Channel RO)"
C = "Catalog Cartoon Network; difuzare în RO neconfirmată"

DESENE = [
    # Fox Kids România (1 aprilie 1999 – 31 decembrie 2004)
    ("Fox Kids", "Omul Păianjen", "Spider-Man (1994)", F),
    ("Fox Kids", "Spider-Man fără limite", "Spider-Man Unlimited", F),
    ("Fox Kids", "Incredibilul Hulk", "The Incredible Hulk (1996)", F),
    ("Fox Kids", "X-Men", "X-Men (1992)", F),
    ("Fox Kids", "Cei Patru Fantastici", "Fantastic Four (1994)", F),
    ("Fox Kids", "Omul de fier", "Iron Man (1994)", F),
    ("Fox Kids", "Nemaipomenitul Tick", "The Tick (1994)", F),
    ("Fox Kids", "Walter Melon", "Walter Melon", F),
    ("Fox Kids", "Diabolik", "Diabolik", F),
    ("Fox Kids", "Big Bad Beetleborgs", "Big Bad Beetleborgs", F),
    ("Fox Kids", "Biroul de detectare a extratereștrilor", "Bureau of Alien Detectors", F),
    ("Fox Kids", "Pokémon", "Pokémon", F),
    ("Fox Kids", "Power Rangers", "Mighty Morphin Power Rangers", F),
    ("Fox Kids", "Prințesa Sissi", "Princess Sissi", F),
    ("Fox Kids", "Prințesa Tenko și gardienii magiei", "Tenko and the Guardians of the Magic", F),
    ("Fox Kids", "Inspector Gadget", "Inspector Gadget", F),
    ("Fox Kids", "Gadget și Gadgetinii", "Gadget & the Gadgetinis", F),
    ("Fox Kids", "Heathcliff", "Heathcliff", F),
    ("Fox Kids", "Dennis, pericol public", "Dennis the Menace (1986)", F),
    ("Fox Kids", "Aventurile lui Oliver Twist", "Saban's Adventures of Oliver Twist", F),
    ("Fox Kids", "Aventurile lui Peter Pan", "Peter Pan & the Pirates", F),
    ("Fox Kids", "Jim Button", "Jim Button", F),
    ("Fox Kids", "Wunschpunsch", "Wunschpunsch", F),
    ("Fox Kids", "Ce-i cu Andy?", "What's with Andy?", F),
    ("Fox Kids", "Piloții NASCAR", "NASCAR Racers", F),
    ("Fox Kids", "Copiii de la 402", "The Kids from Room 402", F),
    ("Fox Kids", "Ferma monștrilor", "Monster Farm", F),
    ("Fox Kids", "Dosarele secrete ale câinilor detectivi", "The Secret Files of the Spy Dogs", F),
    ("Fox Kids", "Câine rău", "Bad Dog", F),
    ("Fox Kids", "Piratul Jack cel Teribil", "Mad Jack the Pirate", F),
    ("Fox Kids", "Lumea lui Bobby", "Bobby's World", F),
    ("Fox Kids", "Viața cu Louie", "Life with Louie", F),
    ("Fox Kids", "Pisoiul Eek", "Eek! The Cat", F),
    ("Fox Kids", "Tunetozaurii", "(titlul original neverificat)", F),
    ("Fox Kids", "Familia De ce?", "The Why Why Family", F),
    ("Fox Kids", "Șoricelul de preerie", "The Little Mouse on the Prairie", F),
    ("Fox Kids", "Pinocchio", "The Adventures of Pinocchio (1992)", F),
    ("Fox Kids", "Jin Jin și Patrula Panda", "Jin Jin and the Panda Patrol", F),
    ("Fox Kids", "Mica sirenă", "Saban's The Little Mermaid", F),
    ("Fox Kids", "Sonic X", "Sonic X", F),
    ("Fox Kids", "Eerie, Indiana", "Eerie, Indiana", F),
    ("Fox Kids", "Noua Familie Addams", "The New Addams Family", F),
    ("Fox Kids", "Creepy Crawlers", "Creepy Crawlers", F),
    ("Fox Kids", "Orășelul purceilor", "Pig City", F),
    ("Fox Kids", "Tutenstein", "Tutenstein", F),
    ("Fox Kids", "Klutter", "Klutter!", F),
    ("Fox Kids", "Spioanele", "Totally Spies!", F),
    # Jetix România (1 ianuarie 2005 – 19 septembrie 2009)
    ("Jetix", "Spioanele", "Totally Spies!", JR),
    ("Jetix", "A.T.O.M.", "A.T.O.M.", JR),
    ("Jetix", "Gadget și Gadgetinii", "Gadget & the Gadgetinis", JR),
    ("Jetix", "Copiii de la 402", "The Kids from Room 402", JR),
    ("Jetix", "Heathcliff", "Heathcliff", JR),
    ("Jetix", "Jin Jin și Patrula Panda", "Jin Jin and the Panda Patrol", JR),
    ("Jetix", "Peter Pan și pirații", "Peter Pan & the Pirates", JR),
    ("Jetix", "Prințesa Tenko și gardienii magiei", "Tenko and the Guardians of the Magic", JR),
    ("Jetix", "Tic și Tac", "The Wacky World of Tic & Tac", JR),
    ("Jetix", "Phineas și Ferb", "Phineas and Ferb", JR),
    ("Jetix", "Kim Possible", "Kim Possible", JR),
    ("Jetix", "Dragonul American: Jake Long", "American Dragon: Jake Long", JR),
    ("Jetix", "Hannah Montana", "Hannah Montana (serial cu actori)", JR),
    ("Jetix", "Regele Șaman", "Shaman King", JR),
    ("Jetix", "Sonic X", "Sonic X", JR),
    ("Jetix", "Pokémon", "Pokémon", JR),
    ("Jetix", "X-Men", "X-Men (1992)", JR),
    ("Jetix", "Omul Păianjen", "Spider-Man (1994)", JR),
    ("Jetix", "Transformers: Animated", "Transformers: Animated", JR),
    ("Jetix", "H2O: Adaugă apă", "H2O: Just Add Water (serial cu actori)", JR),
    ("Jetix", "W.I.T.C.H.", "W.I.T.C.H.", J),
    ("Jetix", "Super Robot Monkey Team Hyperforce Go!", "Super Robot Monkey Team Hyperforce Go!", J),
    ("Jetix", "Galactik Football", "Galactik Football", J),
    ("Jetix", "Yin Yang Yo!", "Yin Yang Yo!", J),
    ("Jetix", "Pucca", "Pucca", J),
    ("Jetix", "Monster Buster Club", "Monster Buster Club", J),
    ("Jetix", "Get Ed", "Get Ed", J),
    ("Jetix", "Martin Mystery", "Martin Mystery", J),
    ("Jetix", "Shuriken School", "Shuriken School", J),
    ("Jetix", "Captain Flamingo", "Captain Flamingo", J),
    ("Jetix", "Kid vs. Kat", "Kid vs. Kat", J),
    ("Jetix", "Combo Niños", "Combo Niños", J),
    ("Jetix", "Monster Warriors", "Monster Warriors", J),
    ("Jetix", "Ōban Star-Racers", "Ōban Star-Racers", J),
    ("Jetix", "Power Rangers (sezoanele noi)", "Power Rangers", J),
    # Cartoon Network (în engleză până la 30.09.2002, apoi și în română)
    ("Cartoon Network", "Laboratorul lui Dexter", "Dexter's Laboratory", C),
    ("Cartoon Network", "Johnny Bravo", "Johnny Bravo", C),
    ("Cartoon Network", "Văcuța și Puiul", "Cow and Chicken", C),
    ("Cartoon Network", "Eu sunt Nevăstuica", "I Am Weasel", C),
    ("Cartoon Network", "Fetițele Powerpuff", "The Powerpuff Girls", C),
    ("Cartoon Network", "Ed, Edd și Eddy", "Ed, Edd n Eddy", C),
    ("Cartoon Network", "Curaj, câinele cel fricos", "Courage the Cowardly Dog", C),
    ("Cartoon Network", "Mike, Lu și Og", "Mike, Lu & Og", C),
    ("Cartoon Network", "Sheep in the Big City", "Sheep in the Big City", C),
    ("Cartoon Network", "Time Squad", "Time Squad", C),
    ("Cartoon Network", "Aventurile lui Billy și Mandy", "The Grim Adventures of Billy & Mandy", C),
    ("Cartoon Network", "Samuraiul Jack", "Samurai Jack", C),
    ("Cartoon Network", "Clanul Nebunaticilor de Alături", "Codename: Kids Next Door", C),
    ("Cartoon Network", "Robot Jones", "Whatever Happened to... Robot Jones?", C),
    ("Cartoon Network", "Evil Con Carne", "Evil Con Carne", C),
    ("Cartoon Network", "Megas XLR", "Megas XLR", C),
    ("Cartoon Network", "Casa Foster pentru prieteni imaginari", "Foster's Home for Imaginary Friends", C),
    ("Cartoon Network", "Tabăra Lazlo", "Camp Lazlo!", C),
    ("Cartoon Network", "Colegul meu de sală e o maimuță", "My Gym Partner's a Monkey", C),
    ("Cartoon Network", "Ben 10", "Ben 10", C),
    ("Cartoon Network", "Ben 10: Forța extraterestră", "Ben 10: Alien Force", C),
    ("Cartoon Network", "Class of 3000", "Class of 3000", C),
    ("Cartoon Network", "Squirrel Boy", "Squirrel Boy", C),
    ("Cartoon Network", "Chowder", "Chowder", C),
    ("Cartoon Network", "Peripețiile lui Flapjack", "The Marvelous Misadventures of Flapjack", C),
    ("Cartoon Network", "Hi Hi Puffy AmiYumi", "Hi Hi Puffy AmiYumi", C),
    ("Cartoon Network", "Robotboy", "Robotboy", C),
    ("Cartoon Network", "Atomic Betty", "Atomic Betty", C),
    ("Cartoon Network", "Batman: Seria animată", "Batman: The Animated Series", C),
    ("Cartoon Network", "Superman: Seria animată", "Superman: The Animated Series", C),
    ("Cartoon Network", "Liga Dreptății", "Justice League", C),
    ("Cartoon Network", "Tinerii Titani", "Teen Titans", C),
    ("Cartoon Network", "Batman (2004)", "The Batman", C),
    ("Cartoon Network", "Duck Dodgers", "Duck Dodgers", C),
    ("Cartoon Network", "Scooby-Doo, unde ești?", "Scooby-Doo, Where Are You!", C),
    ("Cartoon Network", "Ce e nou, Scooby-Doo?", "What's New, Scooby-Doo?", C),
    ("Cartoon Network", "Familia Flintstone", "The Flintstones", C),
    ("Cartoon Network", "Familia Jetson", "The Jetsons", C),
    ("Cartoon Network", "Tom și Jerry", "Tom and Jerry", C),
    ("Cartoon Network", "Looney Tunes", "Looney Tunes", C),
    ("Cartoon Network", "Pinky și Creierul", "Pinky and the Brain", C),
    ("Cartoon Network", "Animaniacii", "Animaniacs", C),
    ("Cartoon Network", "Ursul Yogi", "Yogi Bear", C),
    ("Cartoon Network", "Top Cat", "Top Cat", C),
    ("Cartoon Network", "2 Stupid Dogs", "2 Stupid Dogs", C),
    ("Cartoon Network", "Căpitanul Planetă", "Captain Planet and the Planeteers", C),
    ("Cartoon Network", "Swat Kats", "SWAT Kats", C),
    ("Cartoon Network", "Jonny Quest", "The Real Adventures of Jonny Quest", C),
    ("Cartoon Network", "Dragon Ball Z", "Dragon Ball Z", C),
    ("Cartoon Network", "Bakugan", "Bakugan Battle Brawlers", C),
]


def main():
    seriale_cu_ep = {SERIALE[ep[0]][2].split(" (")[0] for ep in EPISOADE}
    wb = Workbook()
    a = wb.active
    a.title = "Toate desenele"
    a.append(["Canal", "Titlu în română", "Titlu original", "Are episod de Crăciun/iarnă", "Sursa listei"])
    for canal, ro, orig, sursa in DESENE:
        baza = orig.split(" (")[0]
        a.append([canal, ro, orig, "da" if baza in seriale_cu_ep else "", sursa])
    b = wb.create_sheet("Episoade de Crăciun")
    b.append(["Canal", "Serial", "Sezon", "Episod", "Titlu episod (original)", "Tip", "Sigur", "Notă", "IMDb (pentru Stremio)", "Data premierei"])
    for ep in sorted(EPISOADE, key=lambda x: (list(CANALE).index(SERIALE[x[0]][0]), SERIALE[x[0]][1], x[1], x[2])):
        tt, s, e, titlu, data, tip, sigur, nota = ep
        canal, ro, orig = SERIALE[tt]
        b.append([CANALE[canal]["nume"], ro, s, e, titlu, "Crăciun" if tip == "C" else "Iarnă",
                  "da" if sigur else "probabil", nota, f"{tt}:{s}:{e}", data or None])
    for tt, canal, ro, orig, an in FILME:
        b.append([CANALE[canal]["nume"], ro, None, None, orig, "Crăciun", "da", f"film TV, {an}", tt, None])
    for ws in (a, b):
        for c in ws[1]:
            c.font = Font(bold=True)
    wb.save("liste_craciun_retro.xlsx")
    print(len(DESENE), "desene;", len(EPISOADE) + len(FILME), "episoade/filme")


if __name__ == "__main__":
    main()
