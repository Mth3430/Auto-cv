import ollama
import json

def generate_cv(job, skills):
    with open("profile.json") as f:
        profile = json.load(f)

    prompt = f"""Tu es un expert en recrutement. Génère un CV professionnel en français adapté à l'offre suivante.

Offre d'emploi :
- Titre : {job['title']}
- Entreprise : {job['company']}
- Description : {job['description'][:2000]}

Profil du candidat :
{json.dumps(profile, ensure_ascii=False, indent=2)}

Compétences pertinentes identifiées : {', '.join(skills) if skills else 'voir profil'}

Réponds UNIQUEMENT avec un objet JSON valide (pas de markdown, pas d'explication) ayant cette structure exacte :
{{
  "nom": "prénom nom du candidat",
  "titre": "intitulé du poste visé",
  "email": "email",
  "telephone": "numéro",
  "ville": "Montpellier",
  "linkedin": "",
  "github": "",
  "photo": "",
  "accroche": "2-3 phrases percutantes adaptées à l'offre",
  "competences": ["compétence1", "compétence2"],
  "langues": [
    {{"langue": "Français", "niveau": "Natif"}},
    {{"langue": "Anglais", "niveau": "B2"}}
  ],
  "experiences": [
    {{
      "poste": "titre du poste",
      "entreprise": "nom entreprise",
      "dates": "Mois AAAA – Mois AAAA",
      "description": "description courte des missions"
    }}
  ],
  "projets": [
    {{
      "nom": "nom du projet",
      "technologies": ["tech1", "tech2"],
      "description": "description courte"
    }}
  ],
  "formation": [
    {{
      "diplome": "intitulé du diplôme",
      "etablissement": "nom établissement",
      "dates": "AAAA – AAAA"
    }}
  ]
}}
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response['message']['content'].strip()

    # Extract JSON if wrapped in markdown code block
    if "```" in raw:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        raw = raw[start:end]

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Fallback: return basic structure from profile
        return {
            "nom": profile.get("name", "John Doe"),
            "titre": job["title"],
            "email": profile.get("email", ""),
            "telephone": profile.get("phone", ""),
            "ville": "Montpellier",
            "linkedin": profile.get("linkedin", ""),
            "github": profile.get("github", ""),
            "photo": "",
            "accroche": f"Candidature pour le poste de {job['title']} chez {job['company']}.",
            "competences": skills if skills else profile.get("skills", []),
            "langues": [{"langue": "Français", "niveau": "Natif"}],
            "experiences": [],
            "projets": [
                {
                    "nom": p["name"],
                    "technologies": p.get("tech", []),
                    "description": p.get("description", "")
                }
                for p in profile.get("projects", [])
            ],
            "formation": []
        }
