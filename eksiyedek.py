#!/usr/bin/env python3

import argparse
import logging
import sys
import xml.etree.ElementTree as ET
from datetime import datetime

from tqdm import tqdm

from eksisozluk.EksiSozluk import EksiApi


def build_xml(user_nick):
    root = ET.Element(
        "backup",
        attrib={
            "nick": user_nick,
            "backupdate": now.replace(microsecond=0).isoformat(),
        },
    )
    m = ET.Element(
        "entries",
        attrib={"count": str(api.get_user(user_nick).user_info.entry_counts.total)},
    )
    root.append(m)
    for i in tqdm(
        range(1, api.get_user_entries(user_nick).user_entries.page_count + 1)
    ):
        for entry in api.get_user_entries(user_nick, i).user_entries.entries:
            title = entry.topic_id.title
            id_ = entry.entry.id
            date = str(entry.entry.created)
            content = entry.entry.content
            b = ET.SubElement(
                m,
                "entry",
                attrib={
                    "title": title,
                    "id": str(id_),
                    "date": date,
                },
            )
            b.text = content
    return ET.ElementTree(root)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Ekşi Sözlük yazarlarının girdilerini XML formatında yedeklemeye yarar"
    )
    parser.add_argument("nick", help="Kullanıcı nicki")
    logging.disable(level=logging.DEBUG)
    args = parser.parse_args()
    nick = args.nick
    api = EksiApi()
    now = datetime.now()
    filename = "_".join(nick.split()) + "_" + now.strftime("%d-%m-%Y_%H-%M-%S") + ".xml"
    tree = build_xml(nick)
    with open(filename, "wb") as f:
        tree.write(f, encoding="UTF-8", xml_declaration=True)
