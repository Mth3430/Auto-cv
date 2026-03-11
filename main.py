import argparse
import os
import re

from modules.scraper_indeed import scrape_indeed
from modules.scraper_wttj import scrape_wttj
from modules.scraper_hellowork import scrape_hellowork
from modules.analyzer import extract_skills
from modules.matcher import match_skills
from modules.cv_generator import generate_cv
from modules.cover_letter import generate_cover_letter
from modules.export_cv import export_cv
from modules.export_letter import export_letter
from modules.export_link import export_link

def clean_name(text):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', text)[:50]

parser = argparse.ArgumentParser(description="Auto CV generator")
parser.add_argument("site", type=str, help="Site: indeed, wttj, hellowork")
parser.add_argument("count", type=int, help="Max number of jobs")
parser.add_argument("keyword", type=str, help="Job keyword")
args = parser.parse_args()

site = args.site.lower()
count = args.count
keyword = args.keyword

print(f"[1/3] Scraping {site} for '{keyword}' (max {count}, Montpellier)...")

if site == "indeed":
    jobs = scrape_indeed(keyword, max_jobs=count)
elif site == "wttj":
    jobs = scrape_wttj(keyword, max_jobs=count)
elif site == "hellowork":
    jobs = scrape_hellowork(keyword, max_jobs=count)
else:
    print("Site inconnu. Choisis parmi: indeed, wttj, hellowork")
    exit()

print(f"[2/3] Found {len(jobs)} job(s).")

if not jobs:
    print("Aucun poste trouvé. Vérifie le mot-clé ou le site.")
    exit()

print(f"[3/3] Generating documents...")

for i, job in enumerate(jobs, 1):
    print(f"\n[{i}/{len(jobs)}] {job['title']} @ {job['company']}")
    print(f"  Description ({len(job['description'])} chars): {job['description'][:120]}...")

    job_skills_text = extract_skills(job["description"])
    matched_skills = match_skills(job_skills_text)
    print(f"  Matched skills: {matched_skills}")

    cv_data = generate_cv(job, matched_skills)
    letter_data = generate_cover_letter(job, matched_skills, cv_data)

    folder_name = clean_name(job["title"])
    folder_path = f"generated/{folder_name}"
    os.makedirs(folder_path, exist_ok=True)

    export_cv(cv_data, f"{folder_path}/cv.pdf")
    export_letter(letter_data, f"{folder_path}/lettre.pdf")
    export_link(job, f"{folder_path}/lien.txt")

    print(f"  Saved to: {folder_path}/")

print("\nDone.")
