def export_link(job, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Job title: {job['title']}\n")
        f.write(f"Company: {job['company']}\n")
        f.write(f"Link: {job['url']}\n")