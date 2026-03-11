# auto-cv

Génère automatiquement un CV et une lettre de motivation en PDF, adaptés à chaque offre d'emploi, via scraping + IA locale.

## Fonctionnement

```
python main.py <site> <nombre> <mot-clé>
```

**Exemple :**
```
python main.py hellowork 5 developpeur
```

Le script :
1. **Scrape** les offres sur le site choisi (Montpellier)
2. **Analyse** la description de chaque offre avec Ollama (LLaMA 3)
3. **Génère** un CV et une lettre de motivation en français, adaptés à l'offre
4. **Exporte** le tout en PDF via Typst dans `generated/<nom_poste>/`

## Sites supportés

| Argument   | Site                        |
|------------|-----------------------------|
| `hellowork`| HelloWork                   |
| `wttj`     | Welcome to the Jungle        |
| `indeed`   | Indeed                      |

## Prérequis

```
pip install playwright typst ollama python-docx
playwright install chromium
```

Ollama doit tourner localement avec le modèle `llama3` :
```
ollama pull llama3
ollama serve
```

## Configuration — `profile.json`

Remplis ce fichier avec tes vraies informations avant de lancer :

```json
{
  "name": "Prénom Nom",
  "title": "Intitulé de ton poste",
  "email": "ton@email.com",
  "phone": "06 12 34 56 78",
  "linkedin": "linkedin.com/in/tonprofil",
  "github": "github.com/tonprofil",
  "photo": "photo.jpg",
  "skills": ["Unity", "C#", "Python", "Git"],
  "projects": [
    {
      "name": "Nom du projet",
      "description": "Description courte",
      "tech": ["Unity", "C#"]
    }
  ]
}
```

### Photo

Place un fichier `photo.jpg` (ou `.png`) à la racine du projet et indique son nom dans `profile.json` → champ `"photo"`. Si absent, le CV affiche tes initiales à la place.

## Résultats

Chaque offre génère un dossier `generated/<nom_poste>/` contenant :

```
generated/
└── Developpeur_Kotlin_H_F/
    ├── cv.pdf          ← CV Typst (FR, sidebar, photo)
    ├── lettre.pdf      ← Lettre de motivation
    ├── cv_data.json    ← Données brutes du CV
    ├── letter_data.json
    └── lien.txt        ← URL de l'offre
```

## Structure du projet

```
auto-cv/
├── main.py
├── profile.json
├── modules/
│   ├── scraper_hellowork.py
│   ├── scraper_wttj.py
│   ├── scraper_indeed.py
│   ├── analyzer.py          ← extraction des compétences (Ollama)
│   ├── matcher.py           ← correspondance profil ↔ offre
│   ├── cv_generator.py      ← génération CV JSON (Ollama)
│   ├── cover_letter.py      ← génération lettre (Ollama)
│   ├── export_cv.py         ← compilation PDF via Typst
│   ├── export_letter.py     ← compilation PDF via Typst
│   ├── export_link.py
│   ├── cv_template.typ      ← template CV Typst
│   └── letter_template.typ  ← template lettre Typst
└── generated/               ← CVs générés (créé automatiquement)
```
