import json

def match_skills(job_skills):
    with open("profile.json") as f:
        profile = json.load(f)

    user_skills = profile["skills"]
    matches = [skill for skill in user_skills if skill.lower() in job_skills.lower()]
    return matches