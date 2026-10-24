"""Download the week 9 sources into data/. Run: python -m src.get_data"""
from pathlib import Path   # Path lets us build file paths like data/map_ucr.csv
import pandas as pd        # pandas = the DataFrame library (this week's tool)
import requests            # requests downloads files from a URL

DATA = Path("data")            # the folder where raw files live
DATA.mkdir(exist_ok=True)      # make the folder; no error if it already exists

# MAP's FBI archive (Dropbox link from the supplement)
MAP_URL = ("https://www.dropbox.com/scl/fi/4y2a6yy0pv4lxffm7sa4v/UCR65_25.csv"
           "?rlkey=jhs7ktqhb9h3dnml1wety4nhb&st=7rxppnar&dl=1")
# Washington Post's 50-city file on GitHub
WAPO_URL = ("https://raw.githubusercontent.com/washingtonpost/"
            "data-homicides/master/homicide-data.csv")


def fetch(url: str, dest: Path) -> None:
    if dest.exists():                    # already downloaded?
        print(f"cached: {dest}")         # say so
        return                           # and skip the download
    r = requests.get(url, timeout=120)   # download the file (wait up to 120 s)
    r.raise_for_status()                 # crash loudly if the download failed
    dest.write_bytes(r.content)          # save the raw bytes to disk
    print(f"saved: {dest} ({dest.stat().st_size:,} bytes)")   # report the file size


def main() -> None:
    fetch(MAP_URL, DATA / "map_ucr.csv")     # file 1 -> data/map_ucr.csv
    fetch(WAPO_URL, DATA / "wapo_all.csv")   # file 2 -> data/wapo_all.csv

    # the Post's file is Latin-1, not UTF-8; without this pandas raises UnicodeDecodeError
    wapo = pd.read_csv(DATA / "wapo_all.csv", encoding="latin-1")
    dallas = wapo[wapo["city"] == "Dallas"].drop(        # keep only Dallas rows
        columns=["victim_last", "victim_first"])         # and drop victim names
    dallas.to_csv(DATA / "wapo_dallas.csv", index=False)  # save the Dallas subset
    print(f"wapo_dallas.csv: {len(dallas)} rows (expect 1567)")   # check the count


if __name__ == "__main__":   # only run main() when this file is run directly
    main()
