from playwright.sync_api import sync_playwright

WTTJ_LOCATION = "Montpellier%2C%20H%C3%A9rault%2C%20Occitanie%2C%20France"
WTTJ_LATLNG = "43.61093%2C3.87635"

def scrape_wttj(keyword, max_jobs=50):
    jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        page = context.new_page()

        url = (
            f"https://www.welcometothejungle.com/fr/jobs"
            f"?query={keyword}"
            f"&aroundQuery={WTTJ_LOCATION}"
            f"&refinementList%5Boffices.country_code%5D%5B%5D=FR"
            f"&aroundLatLng={WTTJ_LATLNG}"
            f"&aroundRadius=20"
        )
        print(f"  [WTTJ] Loading: {url}")
        page.goto(url)
        page.wait_for_timeout(5000)

        links = page.query_selector_all('a[href*="/jobs/"]')
        print(f"  [WTTJ] Found {len(links)} raw job links")
        seen = set()
        candidates = []

        for link in links:
            href = link.get_attribute("href")
            title_tag = link.query_selector("h3") or link.query_selector("h2")
            company_tag = link.query_selector("p[data-test='job-card-company-name']")

            title = title_tag.inner_text().strip() if title_tag else ""
            company = company_tag.inner_text().strip() if company_tag else "Unknown"

            if href and title and href not in seen:
                seen.add(href)
                candidates.append({
                    "title": title,
                    "company": company,
                    "url": "https://www.welcometothejungle.com" + href
                })
                if len(candidates) >= max_jobs:
                    break

        print(f"  [WTTJ] {len(candidates)} candidate(s) collected")

        for i, candidate in enumerate(candidates, 1):
            print(f"  [WTTJ] Fetching {i}/{len(candidates)}: {candidate['title']}")
            try:
                job_page = context.new_page()
                job_page.goto(candidate["url"])
                job_page.wait_for_timeout(3000)

                description = ""
                for selector in [
                    "[data-testid='job-section-description']",
                    "section[id='description']",
                    ".sc-job-section",
                    "div[class*='jobDescription']",
                    "div[class*='job-description']",
                ]:
                    el = job_page.query_selector(selector)
                    if el:
                        description = el.inner_text().strip()
                        print(f"  [WTTJ] Got description ({len(description)} chars)")
                        break

                if not description:
                    el = job_page.query_selector("main")
                    if el:
                        description = el.inner_text().strip()[:3000]
                        print(f"  [WTTJ] Got description via fallback ({len(description)} chars)")

                jobs.append({
                    "title": candidate["title"],
                    "company": candidate["company"],
                    "description": description or candidate["title"],
                    "url": candidate["url"]
                })
                job_page.close()
            except Exception as e:
                print(f"  [WTTJ] ERROR: {e}")
                jobs.append({
                    "title": candidate["title"],
                    "company": candidate["company"],
                    "description": candidate["title"],
                    "url": candidate["url"]
                })

        browser.close()
    return jobs