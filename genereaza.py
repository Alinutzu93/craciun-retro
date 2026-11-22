# -*- coding: utf-8 -*-
"""Generează addon-ul Stremio static „Crăciun retro” în folderul docs/.

Rulare (Windows):  py genereaza.py
Opțional:          py genereaza.py --data 2026-12-24   (programul TV pentru o anumită zi)

Rezultatul (docs/) se publică pe GitHub Pages. Stremio citește:
  /manifest.json
  /catalog/<tip>/<id>.json
  /meta/series/<id>.json
"""
import argparse
import datetime as dt
import html
import json
import random
import shutil
from pathlib import Path

from date import CANALE, EPISOADE, FILME, SERIALE

RADACINA = Path(__file__).resolve().parent
IESIRE = RADACINA / "docs"
PREFIX = "craciunro_"
VERSIUNE = "1.0.0"


def poster(tt):
    return f"https://images.metahub.space/poster/medium/{tt}/img"


def fundal(tt):
    return f"https://images.metahub.space/background/medium/{tt}/img"


def scrie(cale_rel, obiect):
    cale = IESIRE / cale_rel
    cale.parent.mkdir(parents=True, exist_ok=True)
    cale.write_text(json.dumps(obiect, ensure_ascii=False, indent=1), encoding="utf-8")


def video(ep, sezon, episod, data_falsa=None):
    """Un episod din playlist. id-ul e cel IMDb (tt:sezon:episod), ca addon-urile de stream să-l recunoască."""
    tt, s, e, titlu, data, tip, sigur, nota = ep
    _, serial_ro, _ = SERIALE[tt]
    eticheta = "" if sigur else " (probabil)"
    descriere = f"{serial_ro} · S{s:02d}E{e:02d}" + (f" · {nota}" if nota else "")
    return {
        "id": f"{tt}:{s}:{e}",
        "title": f"{serial_ro} — {titlu}{eticheta}",
        "season": sezon,
        "episode": episod,
        "released": (data_falsa or (data or "2000-01-01")) + "T00:00:00.000Z",
        "thumbnail": fundal(tt),
        "overview": descriere,
    }


def meta_canal(cheie):
    canal = CANALE[cheie]
    eps = [ep for ep in EPISOADE if SERIALE[ep[0]][0] == cheie]
    craciun = sorted([ep for ep in eps if ep[5] == "C"], key=lambda x: (SERIALE[x[0]][1], x[1], x[2]))
    iarna = sorted([ep for ep in eps if ep[5] == "I"], key=lambda x: (SERIALE[x[0]][1], x[1], x[2]))
    videos = [video(ep, 1, i + 1) for i, ep in enumerate(craciun)]
    videos += [video(ep, 2, i + 1) for i, ep in enumerate(iarna)]
    reprezentativ = eps[0][0]
    return {
        "id": PREFIX + cheie,
        "type": "series",
        "name": f"{canal['nume']} — Crăciun",
        "poster": poster(reprezentativ),
        "background": fundal(reprezentativ),
        "description": (
            f"Episoadele de Crăciun (sezonul 1) și de iarnă (sezonul 2) din desenele difuzate pe "
            f"{canal['nume']} ({canal['perioada']}). Video-ul vine de la addon-urile de stream instalate."
        ),
        "releaseInfo": canal["perioada"],
        "genres": ["Crăciun", "Desene animate", "Retro"],
        "videos": videos,
    }


def amesteca_fara_repetari(eps, rnd):
    """Amestecă episoadele astfel încât să nu vină două la rând din același serial sau de pe același canal, cât se poate."""
    rest = eps[:]
    rnd.shuffle(rest)
    rezultat = []
    while rest:
        ultim = rezultat[-1] if rezultat else None
        alegere = None
        for nivel in (2, 1, 0):  # 2 = alt canal și alt serial, 1 = doar alt serial, 0 = oricare
            for ep in rest:
                if ultim is None or nivel == 0:
                    alegere = ep
                elif nivel == 2 and SERIALE[ep[0]][0] != SERIALE[ultim[0]][0] and ep[0] != ultim[0]:
                    alegere = ep
                elif nivel == 1 and ep[0] != ultim[0]:
                    alegere = ep
                if alegere:
                    break
            if alegere:
                break
        rest.remove(alegere)
        rezultat.append(alegere)
    return rezultat


def meta_tv(cheie, nume, descriere, eps, ziua):
    rnd = random.Random(f"{cheie}-{ziua.isoformat()}")
    ordine = amesteca_fara_repetari(eps, rnd)
    # Datele sunt puse crescător, ca Stremio să păstreze ordinea programului.
    start = dt.date(2000, 1, 1)
    videos = [
        video(ep, 1, i + 1, (start + dt.timedelta(days=i)).isoformat())
        for i, ep in enumerate(ordine)
    ]
    return {
        "id": PREFIX + cheie,
        "type": "series",
        "name": nume,
        "poster": poster("tt0118360"),
        "background": fundal("tt0115157"),
        "description": f"{descriere} Programul de azi ({ziua.strftime('%d.%m.%Y')}): {len(videos)} episoade.",
        "releaseInfo": "Fox Kids · Jetix · Cartoon Network",
        "genres": ["Crăciun", "Desene animate", "Retro"],
        "videos": videos,
    }


def preview(meta):
    return {k: meta[k] for k in ("id", "type", "name", "poster", "description", "releaseInfo", "genres")}


def pagina_index(manifest):
    randuri = []
    for ep in sorted(EPISOADE, key=lambda x: (SERIALE[x[0]][0], SERIALE[x[0]][1], x[1], x[2])):
        tt, s, e, titlu, data, tip, sigur, nota = ep
        canal, ro, orig = SERIALE[tt]
        randuri.append(
            "<tr><td>{}</td><td>{}</td><td>S{:02d}E{:02d}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(
                html.escape(CANALE[canal]["nume"]), html.escape(f"{ro} ({orig})"), s, e,
                html.escape(titlu), "Crăciun" if tip == "C" else "Iarnă",
                "da" if sigur else "probabil", html.escape(nota)))
    for tt, canal, ro, orig, an in FILME:
        randuri.append(
            f"<tr><td>{html.escape(CANALE[canal]['nume'])}</td><td>{html.escape(ro)} ({html.escape(orig)})</td>"
            f"<td>film {an}</td><td>{html.escape(orig)}</td><td>Crăciun</td><td>da</td><td>special TV</td></tr>")
    return f"""<!DOCTYPE html>
<html lang="ro"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(manifest['name'])}</title>
<style>
body{{font-family:system-ui,sans-serif;background:#0d1b2a;color:#f1f1f1;margin:0;padding:24px;max-width:1000px;margin:auto}}
h1{{color:#ffcf56}} a.btn{{display:inline-block;background:#c1121f;color:#fff;padding:14px 22px;border-radius:10px;text-decoration:none;font-weight:600;margin:6px 6px 6px 0}}
code{{background:#1b263b;padding:2px 6px;border-radius:4px;word-break:break-all}}
table{{border-collapse:collapse;width:100%;font-size:14px;margin-top:16px}} td,th{{border-bottom:1px solid #2b3a55;padding:6px;text-align:left}}
</style></head><body>
<h1>🎄 {html.escape(manifest['name'])}</h1>
<p>{html.escape(manifest['description'])}</p>
<p><a class="btn" id="inst" href="#">Instalează în Stremio</a></p>
<p>Sau copiază în Stremio → Addons → căsuța de căutare: <code id="url"></code></p>
<table><tr><th>Canal</th><th>Serial</th><th>Ep.</th><th>Titlu</th><th>Tip</th><th>Sigur</th><th>Notă</th></tr>
{''.join(randuri)}
</table>
<script>
const u = location.href.replace(/[^/]*$/, '') + 'manifest.json';
document.getElementById('url').textContent = u;
document.getElementById('inst').href = u.replace(/^https?:/, 'stremio:');
</script>
</body></html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", help="ziua pentru programul TV, AAAA-LL-ZZ (implicit: azi)")
    args = ap.parse_args()
    ziua = dt.date.fromisoformat(args.data) if args.data else dt.date.today()

    if IESIRE.exists():
        shutil.rmtree(IESIRE)
    IESIRE.mkdir()

    metas = [meta_canal(c) for c in CANALE]
    toate_craciun = [ep for ep in EPISOADE if ep[5] == "C"]
    metas.insert(0, meta_tv(
        "tv_craciun", "📺 Canal TV de Crăciun",
        "Episoade de Crăciun de pe Fox Kids, Jetix și Cartoon Network, unul după altul, ca la televizor. "
        "Ordinea se schimbă în fiecare zi.", toate_craciun, ziua))
    metas.insert(1, meta_tv(
        "tv_iarna", "❄️ Canal TV de iarnă",
        "Toate episoadele de Crăciun și de iarnă, amestecate. Ordinea se schimbă în fiecare zi.",
        EPISOADE, ziua))

    manifest = {
        "id": "ro.alin.craciunretro",
        "version": VERSIUNE,
        "name": "Crăciun retro — Fox Kids, Jetix, Cartoon Network",
        "description": "Episoadele de Crăciun din desenele copilăriei (România, 1996–2010), "
                       "pe canale și ca program TV. Video-ul vine de la addon-urile de stream pe care le ai instalate.",
        "logo": poster("tt0118360"),
        "background": fundal("tt0115157"),
        "types": ["series", "movie"],
        "resources": ["catalog", {"name": "meta", "types": ["series"], "idPrefixes": [PREFIX]}],
        "idPrefixes": [PREFIX],
        "catalogs": [
            {"type": "series", "id": "craciunro_canale", "name": "🎄 Crăciun retro"},
            {"type": "movie", "id": "craciunro_filme", "name": "🎄 Speciale de Crăciun retro"},
        ],
        "behaviorHints": {"configurable": False},
    }

    scrie("manifest.json", manifest)
    scrie("catalog/series/craciunro_canale.json", {"metas": [preview(m) for m in metas]})
    scrie("catalog/movie/craciunro_filme.json", {"metas": [
        {"id": tt, "type": "movie", "name": f"{ro} ({orig})", "poster": poster(tt),
         "releaseInfo": str(an), "description": f"Special de Crăciun · {CANALE[canal]['nume']}"}
        for tt, canal, ro, orig, an in FILME]})
    for m in metas:
        scrie(f"meta/series/{m['id']}.json", {"meta": m})

    (IESIRE / "index.html").write_text(pagina_index(manifest), encoding="utf-8")
    (IESIRE / ".nojekyll").write_text("", encoding="utf-8")

    nr_c = sum(1 for e in EPISOADE if e[5] == "C")
    print(f"Gata: {len(EPISOADE)} episoade ({nr_c} de Crăciun), {len(FILME)} filme, program TV pentru {ziua}.")


if __name__ == "__main__":
    main()
