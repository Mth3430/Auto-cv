from playwright.sync_api import sync_playwright

LOCATION = "Montpellier"

def scrape_indeed(keyword, max_jobs=20):
    jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        url = f"https://fr.indeed.com/jobs?q={keyword}&l={LOCATION}"
        print(f"  [Indeed] Loading: {url}")
        page.goto(url)
        page.wait_for_timeout(4000)

        try:
            page.click("button[id*='accept'], button[class*='accept']", timeout=2000)
        except Exception:
            pass

        cards = page.query_selector_all(".job_seen_beacon, .resultWithShelf")
        print(f"  [Indeed] Found {len(cards)} cards")
        candidates = []

        for card in cards[:max_jobs]:
            try:
                title_tag = card.query_selector("h2 span[title], h2 span")
                company_tag = card.query_selector("[data-testid='company-name'], .companyName")
                link_tag = card.query_selector("a[id^='job_']")

                if not title_tag or not link_tag:
                    continue

                href = link_tag.get_attribute("href") or ""
                full_url = href if href.startswith("http") else "https://fr.indeed.com" + href

                candidates.append({
                    "title": title_tag.get_attribute("title") or title_tag.inner_text().strip(),
                    "company": company_tag.inner_text().strip() if company_tag else "Unknown",
                    "url": full_url
                })
            except Exception:
                continue

        print(f"  [Indeed] {len(candidates)} candidate(s) collected")

        for i, candidate in enumerate(candidates, 1):
            print(f"  [Indeed] Fetching {i}/{len(candidates)}: {candidate['title']}")
            try:
                job_page = context.new_page()
                job_page.goto(candidate["url"])
                job_page.wait_for_timeout(3000)

                description = ""
                for selector in [
                    "#jobDescriptionText",
                    "[data-testid='jobsearch-JobComponent-description']",
                    ".jobsearch-jobDescriptionText",
                    "[class*='jobDescription']",
                ]:
                    el = job_page.query_selector(selector)
                    if el:
                        description = el.inner_text().strip()
                        print(f"  [Indeed] Got description ({len(description)} chars)")
                        break

                if not description:
                    el = job_page.query_selector("main")
                    if el:
                        description = el.inner_text().strip()[:3000]

                jobs.append({
                    "title": candidate["title"],
                    "company": candidate["company"],
                    "description": description or candidate["title"],
                    "url": candidate["url"]
                })
                job_page.close()
            except Exception as e:
                print(f"  [Indeed] ERROR: {e}")
                jobs.append({
                    "title": candidate["title"],
                    "company": candidate["company"],
                    "description": candidate["title"],
                    "url": candidate["url"]
                })

        browser.close()
    return jobs
