# Quera Jobs Scraping
This is a simple web scraper that crawl the [quera](https://quera.org/magnet/jobs) website and save the job offers into a single file.

## Requirements
- Python 3.7+
- `BeautifulSoup` library
- `Requests` library
- `logging` library
- `json` library
---
---
## How Does It Get the Job Done?
The scraper Utilizes `BeautifulSoup` scarping library to crawl and parse each html page and get the details of each job offer like: Title, Company, Link to the job, and etc. It then saves the info in a JSON file.

---
---
## Sample Output
```json
{
    "jobs": [
        {
            "title": "استخدام Senior Back-end Developer (Python)",
            "url": "https://quera.org//magnet/jobs/69rqj",
            "date": "۵ دی ۱۴۰۱،‏ ۹:۲۷",
            "company": "Raika Research",
            "location": "تهران",
            "level": "Senior",
            "type": "تمام وقت",
            "salary": "حقوق ۳۵,۰۰۰,۰۰۰ تا ۴۰,۰۰۰,۰۰۰",
            "remote": "امکان دورکاری",
            "technologies": ["Python", "Django"],
            "sub_technologies": ["Linux"]

        },
        {
            "title": "استخدام تحلیلگر داده",
            "url": "https://quera.org//magnet/jobs/6xqj",
            "date": "۱۸ آذر ۱۴۰۱،‏ ۲۰:۳۷",
            "company": "Quera",
            "location": "تهران",
            "level": "Junior",
            "type": "پروژه‌ای",
            "salary": "حقوق ۱۵,۰۰۰,۰۰۰ تا ۲۰,۰۰۰,۰۰۰",
            "remote": "امکان دورکاری",
            "technologies": ["Python", "Data Analysis"],
            "sub_technologies": ["SQL"]
        }
    ]
}
```
