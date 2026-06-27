import csv
import os
from datetime import datetime, timezone

import requests

URL = "https://openapi.twse.com.tw/v1/exchangeReport/MI_INDEX"
TARGET_INDEX = "發行量加權股價指數"  # 加權指數（TAIEX）


def main():
    resp = requests.get(URL, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    row = next((d for d in data if d.get("指數") == TARGET_INDEX), None)
    if row is None:
        raise RuntimeError(f"找不到「{TARGET_INDEX}」，TWSE 回應格式可能變了，要去檢查 API")

    os.makedirs("data", exist_ok=True)
    path = "data/taiex_daily.csv"
    is_new = not os.path.exists(path)

    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["日期", "收盤指數", "漲跌", "漲跌點數", "漲跌百分比", "fetch_at_utc"])
        writer.writerow(
            [
                row["日期"],
                row["收盤指數"],
                row["漲跌"],
                row["漲跌點數"],
                row["漲跌百分比"],
                datetime.now(timezone.utc).isoformat(timespec="seconds"),
            ]
        )

    print(f"寫入完成：{row['日期']} 收盤指數 {row['收盤指數']}")


if __name__ == "__main__":
    main()
