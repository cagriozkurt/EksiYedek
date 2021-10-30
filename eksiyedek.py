import datetime
import re
import types
import xml.etree.ElementTree as ET

import requests
from bs4 import BeautifulSoup

backupdate = datetime.datetime.now().replace(microsecond=0).isoformat()

nick = "ssg"
fileName = "_".join(nick.split()) + ".xml"
headers = {
    "Host": "eksisozluk.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "X-Requested-With": "XMLHttpRequest",
    "Alt-Used": "eksisozluk.com",
    "Connection": "keep-alive",
    "Referer": f"https://eksisozluk.com/biri/{nick}",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "TE": "trailers",
}
url = f"https://eksisozluk.com/son-entryleri?nick={nick}"
r = requests.get(url, headers=headers)
r.raise_for_status()
soup = BeautifulSoup(r.text, "html.parser")
try:
    entries_count_text = soup.find("small").get_text()
except AttributeError:
    print("Yazar kayıp.")
else:
    entries_count = re.findall(r"\d+", entries_count_text)[0]
    if int(entries_count[-1]) < 5:
        number_of_pages = round(int(entries_count) / 10) + 1
    else:
        number_of_pages = round(int(entries_count) / 10)
    print(str(number_of_pages) + " sayfa entry indirilecek...")
    root = ET.Element("backup", attrib={"nick": nick, "backupdate": backupdate})
    m1 = ET.Element("entries", attrib={"count": entries_count})
    root.append(m1)
    n = 1
    while True:
        print(f"{n} / {number_of_pages} - % {round(n/number_of_pages*100, 2)}")
        page_url = url + f"&p={n}"
        page_r = requests.get(page_url, headers=headers)
        page_r.raise_for_status()
        if "no-more-data" in page_r.text:
            break
        else:
            page_soup = BeautifulSoup(page_r.text, "html.parser")
            entries = page_soup.findAll("div", {"class": "topic-item"})
            for entry in entries:
                entry_id = entry.find("li")["data-id"]
                entry_title = entry.find("h1")["data-title"]
                entry_date = entry.find(
                    "a", {"class": "entry-date permalink"}
                ).get_text()
                date_regex = re.findall(
                    r"(\d{2})\.(\d{2})\.(\d{4})\s?(\d{2}:\d{2})?", entry_date
                )[0]
                if date_regex[3]:
                    new_date_format = (
                        date_regex[2]
                        + "-"
                        + date_regex[1]
                        + "-"
                        + date_regex[0]
                        + "T"
                        + date_regex[3]
                        + ":00"
                    )
                else:
                    new_date_format = (
                        date_regex[2]
                        + "-"
                        + date_regex[1]
                        + "-"
                        + date_regex[0]
                        + "T00:00:00"
                    )
                entry_content = entry.find("div", {"class": "content"})
                for br in entry_content.findAll("br"):
                    br.replace_with("\n")
                b = ET.SubElement(
                    m1,
                    "entry",
                    attrib={
                        "title": entry_title,
                        "id": entry_id,
                        "date": new_date_format,
                    },
                )
                b.text = entry_content.get_text()
            n += 1

    tree = ET.ElementTree(root)
    with open(fileName, "wb") as f:
        tree.write(f, encoding="UTF-8", xml_declaration=True)
