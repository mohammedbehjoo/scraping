import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import numpy as np
import json

url = "https://quera.org/magnet/jobs?page=1"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

# page number
start_page = 1
end_page = soup.select(".css-g3korc")[-2].text

# selecting jobs
collected_jobs=[]
jobs = soup.select(".css-1g5o4an")
for count, job in enumerate(jobs):
    result = {}

    result["title"] = job.find("h2").text

    result["url"] = "https://quera.org/" + job.find("h2").find("a").get("href")

    result["company"] = job.find(class_="css-1m52y4d").text

    try:
        result["location"] = job.select(".css-5ngv18 span")[0].text
    except IndexError:
        result["location"] = np.nan

    result["date"] = job.select(".css-nm8t2j span")[0].get("title")

    technologies = job.select(".css-h1qgq")[:]
    result["technologies"] = [tech.text for tech in technologies]
    sub_technologies = job.select(".css-1qy3adt")[:]
    result["sub_technologies"] = [tech.text for tech in sub_technologies]

    details = job.select(".css-1iyteef span")
    result["level"] = details[0].text
    result["type"] = details[1].text
    result["remote"] = np.nan
    result["salary"] = np.nan
    if len(details) > 2:
        if "دورکاری" in details[2].text:
            result["remote"] = details[2].text
        else:
            result["salary"] = details[2].text
    if len(details) > 3:
        result["salary"] = details[3].text

    collected_jobs.append(result)


with open("quera_jobs.json","w") as file:
    json.dump(collected_jobs,file)