# Zewen Lin
import requests
from bs4 import BeautifulSoup


class WebScraper:
    def __init__(self, url, category):
        self.url = url
        self.category = category

    def url_add_category(self):
        if self.url == "https://www.timesjobs.com/":
            return self.url + "candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=" \
                   + self.category + "&txtLocation="

    def run(self):
        company_name = []
        skills = []
        new_url = self.url_add_category()
        html_text = requests.get(new_url).text
        soup = BeautifulSoup(html_text, 'lxml')
        jobs = soup.find_all("li", class_="clearfix job-bx wht-shd-bx")
        for job in jobs:
            published_date = job.find('span', class_='sim-posted').span.text
            if 'few' in published_date:
                company_name.append(job.find('h3', class_='joblist-comp-name').text.replace('  ', '').strip())
                skills.append(job.find('span', class_='srp-skills').text.replace('  ', '').strip())
        return company_name, skills
