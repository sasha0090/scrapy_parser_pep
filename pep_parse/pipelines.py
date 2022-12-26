import csv
import datetime as dt
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).parents[1]


def write_status_summary(status_summary):
    now = dt.datetime.now()
    now_formatted = now.strftime("%Y-%m-%d_%H-%M-%S")

    results_dir = BASE_DIR / "results"
    results_dir.mkdir(exist_ok=True)

    file_name = f"status_summary_{now_formatted}.csv"
    file_path = results_dir / file_name

    # Сделал так потому что правила W503 и W504 flake8 противоречат друг другу,
    # а тесты не игнорируют W503 или W504.
    result = [("Статус", "Количество")] + status_summary.most_common()
    result += [("Total", sum(status_summary.values()))]

    with open(file_path, "w", encoding="utf-8") as f:
        writer = csv.writer(f, dialect="unix")
        writer.writerows(result)


class PepParsePipeline:
    def open_spider(self, spider):
        self.status_summary = Counter()

    def close_spider(self, spider):
        write_status_summary(self.status_summary)

    def process_item(self, item, spider):
        self.status_summary[item["status"]] += 1
        return item
