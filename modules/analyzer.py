import ollama

def extract_skills(description):
    prompt = f"""
Extract the technical skills from this job description.
Return a simple list.

Job:
{description}
"""
    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['message']['content']