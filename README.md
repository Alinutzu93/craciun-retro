# 🎄 Crăciun retro — addon Stremio

Addonul aduce în Stremio episoadele de Crăciun și de iarnă din desenele de pe Fox Kids, Jetix și Cartoon Network (România, 1996–2010).

În Stremio apar:
- **📺 Canal TV de Crăciun**: 43 de episoade de Crăciun, puse unul după altul. Ordinea se schimbă în fiecare zi.
- **❄️ Canal TV de iarnă**: toate cele 62 de episoade, de Crăciun și de iarnă.
- **🎲 TV retro amestecat**: toate desenele de pe cele trei canale, amestecate ca la TV în decembrie. După fiecare episod de Crăciun sau de iarnă vin două episoade obișnuite din alte desene (doar episoade apărute până în 2010). Episoadele obișnuite se iau din Cinemeta. Ce seriale au fost găsite se vede în `docs/raport_seriale.json`.
- **Fox Kids / Jetix / Cartoon Network — Crăciun**: câte un canal pentru fiecare. Sezonul 1 are episoadele de Crăciun, sezonul 2 pe cele de iarnă.
- **Speciale de Crăciun retro**: filmele *Inspector Gadget Saves Christmas* și *Yogi's First Christmas*.

Addonul nu găzduiește video și nu caută surse video. Fiecare episod are codul IMDb (`tt…:sezon:episod`), iar Stremio cere video-ul de la addon-urile de stream pe care le ai deja instalate.

## Publicare pe GitHub Pages (o singură dată)

1. Pe github.com fă un repository public nou, de exemplu `craciun-retro`.
2. Urcă în el tot conținutul acestui folder, inclusiv `.github` și `docs`. Poți folosi „Add file → Upload files” sau comenzile de mai jos (cmd, în folderul proiectului):

```
git init
git add .
git commit -m "Crăciun retro"
git branch -M main
git remote add origin https://github.com/Alinutzu93/craciun-retro.git
git push -u origin main
```

3. În repository deschide **Settings → Pages**. La Source alege „Deploy from a branch”, apoi branch `main` și folderul `/docs`. Apasă Save.
4. În **Settings → Actions → General → Workflow permissions** bifează „Read and write permissions”. Fără asta, programul TV nu se poate schimba zilnic.
5. După 1–2 minute deschide `https://alinutzu93.github.io/craciun-retro/`. Apasă „Instalează în Stremio” sau copiază linkul `…/manifest.json` în Stremio → Addons.

Pe televizor (Stremio pentru Android TV sau Samsung/LG) addonul apare singur, dacă ești logat cu același cont.

## Modificare listă

Episoadele de Crăciun sunt în `date.py`, lista tuturor desenelor pentru canalul amestecat în `retro.py`. După ce o modifici, rulează:

```
py genereaza.py --actualizeaza
```

Apoi urcă folderul `docs` pe GitHub. `py genereaza.py --data 2026-12-24` face programul pentru o anumită zi.
