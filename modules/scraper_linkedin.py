from playwright.sync_api import sync_playwright

def scrape_linkedin(keyword, location):
    jobs = []
    url = f"https://www.linkedin.com/jobs/search/?keywords={keyword}&location={location}"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_selector(".jobs-search-results__list-item", timeout=10000)

        cards = page.query_selector_all(".jobs-search-results__list-item")
        for card in cards[:20]:  # Limite par défaut à 20 pour tester
            title = card.query_selector("h3") 
            company = card.query_selector("h4") 
            link_tag = card.query_selector("a")
            if title and link_tag:
                jobs.append({
                    "title": title.inner_text().strip(),
                    "company": company.inner_text().strip() if company else "Unknown",
                    "description": title.inner_text().strip(),
                    "url": link_tag.get_attribute("href")
                })
        browser.close()
    return jobs