from ast import keyword
from playwright.sync_api import sync_playwright
import json

def scroll_search_area(page):
    page.click("main")
    job_count, scroll_count = 0, 0
    while True:
        print("While")
        load_more_button = page.query_selector("button[class*='infinite-scroller__show-more-button']")
        if load_more_button.is_visible():
            load_more_button.click()

        page.keyboard.press(key="Space")
        page.wait_for_timeout(500)

        new_job_count = get_job_count(page)
        
        if job_count == new_job_count:
            if scroll_count > 10:
                break
        else:
            scroll_count = 0
        
        job_count = new_job_count
        scroll_count += 1
        
        
        

def collect_search_data(page
                        ):
    jobs = page.query_selector_all("ul.jobs-search__results-list li")
    for job in jobs:
        url = job.query_selector("a").get_attribute("href")
        job.click()
        page.wait_for_timeout(3000)
        show_more = page.query_selector("button[data-tracking-control-name=\"public_jobs_show-more-html-btn\"]")
        if show_more.is_visible():
            show_more.click()

        
        title = page.query_selector("section.two-pane-serp-page__detail-view h2.top-card-layout__title.topcard__title").inner_text()
        location = page.query_selector("a[data-tracking-control-name=\"public_jobs_topcard-org-name\"]")
        if location:
            location = location.inner_text()
        else:
            location = None
        post_date = page.query_selector("span.posted-time-ago__text.topcard__flavor--metadata").inner_text()
        number_of_applicants = page.query_selector("figcaption.num-applicants__caption")
        if number_of_applicants:
            number_of_applicants = number_of_applicants.inner_text()
        else:
            number_of_applicants = None
        job_desc = page.query_selector("div.show-more-less-html__markup").inner_text()
        criteria_list = page.query_selector_all("ul.description__job-criteria-list li")
        criterias = []
        for criteria in criteria_list:
            name = criteria.query_selector("h3").inner_text()
            value = criteria.query_selector("span").inner_text()
            criterias.append({"name": name, "value": value})


        with open("job_data.txt", "a") as f:
            f.write(json.dumps(
                {
                    "url": url,
                    "title": title,
                    "location": location, 
                    "post_date": post_date,
                    "number_of_applicants": number_of_applicants,
                    "job_desc": job_desc,
                    "criteria": criterias 
                }
            )+"\n")
    

def get_job_count(page):
    return len(page.query_selector_all("ul.jobs-search__results-list li a"))

    


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    kywrd =  "\"data engineer\""
    city = "San%20Francisco%2C%20California%2C%20United%20States"

    page.goto(f"https://www.linkedin.com/jobs/search?keywords={kywrd}"\
        f"&location={city}&geoId=&trk=public_jobs_jobs-search-bar_search-submit")
    
    scroll_search_area(page)

    collect_search_data(page)
    page.wait_for_timeout(500000)


    browser.close()