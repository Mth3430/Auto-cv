import ollama
import json
from datetime import datetime

def generate_cover_letter(job, skills, cv_data=None):
    with open("profile.json") as f:
        profile = json.load(f)

    prompt = f"""Tu es un expert en recrutement. Rédige une lettre de motivation professionnelle en français.

Offre :
- Poste : {job['title']}
- Entreprise : {job['company']}
- Description : {job['description'][:1500]}

Profil : {json.dumps(profile, ensure_ascii=False)}
Compétences pertinentes : {', '.join(skills) if skills else 'voir profil'}

Réponds UNIQUEMENT avec un objet JSON valide (pas de markdown) :
{{
  "corps": "3 paragraphes de lettre de motivation en français, sans formule d'appel ni formule de politesse finale"
}}
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response['message']['content'].strip()
    if "```" in raw:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        raw = raw[start:end]

    try:
        parsed = json.loads(raw)
        corps = parsed.get("corps", raw)
    except Exception:
        corps = raw

    nom = cv_data.get("nom", profile.get("name", "")) if cv_data else profile.get("name", "")
    titre = cv_data.get("titre", job["title"]) if cv_data else job["title"]

    return {
        "nom": nom,
        "titre": titre,
        "email": profile.get("email", ""),
        "telephone": profile.get("phone", ""),
        "ville": "Montpellier",
        "date": datetime.now().strftime("%d/%m/%Y"),
        "poste_vise": job["title"],
        "entreprise": job["company"],
        "corps": corps,
    }
