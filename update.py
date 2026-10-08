import json
import os
import sys
from datetime import datetime, timezone

import requests


SOURCE_URL = (
    "https://studentbooks.moe.gov.eg/"
    "Performance_Assessments/books.json"
)

OUTPUT_FILE = "books.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/140.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "application/json,text/plain,*/*"
    ),
    "Accept-Language": "ar,en-US;q=0.9,en;q=0.8",
    "Referer": "https://studentbooks.moe.gov.eg/",
}


def download_json():
    print("Downloading:")
    print(SOURCE_URL)

    response = requests.get(
        SOURCE_URL,
        headers=HEADERS,
        timeout=60,
    )

    print("HTTP:", response.status_code)

    response.raise_for_status()

    data = response.json()

    if not isinstance(data, (dict, list)):
        raise ValueError(
            "The response is not a valid JSON object/list."
        )

    return data


def save_json(data):
    temp_file = OUTPUT_FILE + ".tmp"

    with open(
        temp_file,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2,
        )

    os.replace(
        temp_file,
        OUTPUT_FILE,
    )


def main():
    try:
        data = download_json()

        save_json(data)

        now = datetime.now(
            timezone.utc
        ).isoformat()

        print("SUCCESS")
        print("Updated:", now)
        print("Saved:", OUTPUT_FILE)

    except Exception as error:
        print()
        print("FAILED")
        print(type(error).__name__)
        print(error)

        # مهم:
        # لا نحذف books.json القديم إذا فشل السحب.
        if os.path.exists(OUTPUT_FILE):
            print(
                "Old books.json was kept."
            )
        else:
            print(
                "No previous books.json exists."
            )

        sys.exit(1)


if __name__ == "__main__":
    main()
