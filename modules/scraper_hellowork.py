from playwright.sync_api import sync_playwright

LOCATION = "Montpellier"

def scrape_hellowork(keyword, max_jobs=20):
    jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        page = context.new_page()

        url = f"https://www.hellowork.com/fr-fr/emploi/recherche.html?k={keyword}&k_autocomplete=&l=Montpellier+34000&l_autocomplete=http%3A%2F%2Fwww.rj.com%2Fcommun%2Flocalite%2Fcommune%2F34172"
        print(f"  [HelloWork] Loading: {url}")
        page.goto(url)

        page.wait_for_timeout(3000)

        # Dismiss cookie consent
        for btn_selector in [
            "button[data-testid='button-deny']",
            "button[class*='continue-without']",
            "button[title*='continuer']",
            "button[title*='Continuer']",
            "a[class*='continue-without-accepting']",
        ]:
            try:
                btn = page.query_selector(btn_selector)
                if btn:
                    btn.click()
                    print(f"  [HelloWork] Dismissed cookies via '{btn_selector}'")
                    page.wait_for_timeout(2000)
                    break
            except Exception:
                pass

        # Wait for job content to load (Turbo frames)
        page.wait_for_timeout(5000)


        cards = page.query_selector_all("[data-cy='serpCard']")
        print(f"  [HelloWork] Found {len(cards)} cards with [data-cy='serpCard']")
        candidates = []

        for card in cards[:max_jobs]:
            try:
                link_tag = card.query_selector("[data-cy='offerTitle']")
                if not link_tag:
                    continue

                title = link_tag.get_attribute("title") or link_tag.inner_text().strip()
                # Extract clean title (remove location/company suffix after " - ")
                if " - " in title:
                    title = title.split(" - ")[0].strip()

                href = link_tag.get_attribute("href") or ""
                full_url = href if href.startswith("http") else "https://www.hellowork.com" + href

                # Company name from aria-label: "Voir offre de <title> à <loc>, chez <company>"
                aria = link_tag.get_attribute("aria-label") or ""
                company = "Unknown"
                if " chez " in aria:
                    company = aria.split(" chez ")[-1].split(",")[0].strip()

                candidates.append({
                    "title": title,
                    "company": company,
                    "url": full_url
                })
            except Exception:
                continue

        print(f"  [HelloWork] {len(candidates)} candidate(s) collected")

        for i, candidate in enumerate(candidates, 1):
            print(f"  [HelloWork] Fetching {i}/{len(candidates)}: {candidate['title']}")
            try:
                job_page = context.new_page()
                job_page.goto(candidate["url"])
                job_page.wait_for_timeout(3000)

                description = ""
                for selector in [
                    "[data-cy='job-description']",
                    ".job-description",
                    "[class*='jobDescription']",
                    "[class*='job-detail']",
                    "section[class*='description']",
                ]:
                    el = job_page.query_selector(selector)
                    if el:
                        description = el.inner_text().strip()
                        print(f"  [HelloWork] Got description ({len(description)} chars)")
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
                print(f"  [HelloWork] ERROR: {e}")
                jobs.append({
                    "title": candidate["title"],
                    "company": candidate["company"],
                    "description": candidate["title"],
                    "url": candidate["url"]
                })

        browser.close()
    return jobs
