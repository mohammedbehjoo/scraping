# importing libraries
import numpy as np
from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
import logging
import json
from random import randint
from time import sleep
from tqdm import tqdm


def data_extraction(job):
    result = {}
    # getting the title
    title = job.find("h2")
    result["title"] = title.get_text()
    # getting the url
    result["url"] = "https://quera.org/"+title.find("a").get("href")
    # getting the date
    date = job.select(".css-nm8t2j span")
    result["date"] = date[0].get("title")
    # getting the company
    result["company"] = job.find(class_="css-1m52y4d").text
    # getting location
    try:
        result["location"] = job.select(".css-5ngv18 span")[0].text
    except IndexError:
        result["location"] = np.nan
    # getting technologies and sub techs
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

    return result


def scrape(url, logger):
    logger.info(" start scraping the page {}".format(url))

    results = []

    # getting the page
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except HTTPError as http_err:
        logger.error("HTTP error occurred: {}".format(http_err))
        return results
    except ConnectionError as conn_err:
        logger.error("Connection error occurred: {}".format(conn_err))
        return results
    except Timeout as timeout_err:
        logger.error("Timeout error occurred: {}".format(timeout_err))
        return results
    except RequestException as req_err:
        logger.error("Request error occurred: {}".format(req_err))
        return results

    # parsing the page
    soup = BeautifulSoup(response.content, "html.parser")

    # find each job
    jobs = soup.select(".css-1g5o4an")

    for count, job in enumerate(jobs):
        try:
            results.append(data_extraction(job))
        except:
            logger.warning("failed to extract job # {}".format(count))

    logger.info("this page was scraped successfully.")

    return results

    return


if __name__ == "__main__":
    # set up logging
    logging.basicConfig(filename="quera_jobs.log", filemode="w",
                        format="%(asctime)s %(levelname)s: %(message)s")
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # set up the range of the pages to scrape
    # TODO: in the furture: make this part to get the page number automatically from the webpage.

    # start_page and end_page number
    start_page = 1
    end_page = 8

    # scrape the pages and initialize a list for that
    all_results = []
    # # loop over the pages
    for page in tqdm(range(start_page, end_page+1)):
        print("page: ", page)
        url = f"https://quera.org/magnet/jobs?page={page}"
        all_results.extend(scrape(url, logger))
        time_milliseconds = randint(100, 1000)
        time_second = time_milliseconds*0.001
        logger.info("sleeping for {} seconds".format(time_second))
        sleep(time_second)
        logger.info("just woke up")

    print(all_results)

    # save the results into a JSON file
    with open("quera_jobs.json", "w") as file:
        json.dump(all_results, file)