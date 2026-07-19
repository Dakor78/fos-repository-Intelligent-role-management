"""
Подготовка датасетов для примеров Модуля II.

Запуск (из папки examples/data):  python prepare_data.py

Скачивает исходные датасеты и формирует компактные производные файлы.
Итоговый объём папки — около 5 МБ (лимит курса — не более 5 ГБ).

Датасеты:
  1. products.csv               — каталог товаров (Тема 4, инструменты).
       Источник: UCI Online Retail II (реальные транзакции интернет-магазина).
       Из транзакций выделяются 500 самых продаваемых товаров: sku, name, price, sold.
  2. squad_dev.json             — корпус для RAG (Тема 6).
       Источник: SQuAD v1.1 dev — 2067 абзацев из статей Википедии (реальный текст).
  3. prompt_injections.parquet  — размеченные примеры инъекций (Тема 7).
       Источник: deepset/prompt-injections (546 примеров, label: 0=безопасный, 1=инъекция).
"""
import io
import json
import zipfile
from pathlib import Path

import requests

HERE = Path(__file__).parent

SQUAD_URL = "https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v1.1.json"
PI_URL = ("https://huggingface.co/datasets/deepset/prompt-injections/"
          "resolve/main/data/train-00000-of-00001-9564e8b05b4757ab.parquet")
RETAIL_URL = "https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip"


def download(url: str, dst: Path) -> None:
    if dst.exists():
        print(f"[skip] {dst.name} уже есть")
        return
    print(f"[get ] {dst.name} <- {url}")
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    dst.write_bytes(r.content)


def build_products() -> None:
    """Из сырых транзакций Online Retail II строит компактный каталог товаров."""
    import pandas as pd

    out = HERE / "products.csv"
    if out.exists():
        print("[skip] products.csv уже есть")
        return
    print("[get ] online_retail_II.zip (~44 МБ, временно)")
    r = requests.get(RETAIL_URL, timeout=300)
    r.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        name = [n for n in z.namelist() if n.endswith(".xlsx")][0]
        df = pd.read_excel(io.BytesIO(z.read(name)), sheet_name=0)

    df = df.dropna(subset=["Description", "Price", "StockCode"])
    df = df[(df["Price"] > 0) & (df["Quantity"] > 0)]
    cat = (df.groupby(["StockCode", "Description"])
             .agg(price=("Price", "median"), sold=("Quantity", "sum"))
             .reset_index())
    cat = cat[cat["Description"].str.len() > 5]
    cat = cat.sort_values("sold", ascending=False).head(500).reset_index(drop=True)
    cat["Description"] = cat["Description"].str.strip().str.title()
    cat = cat.rename(columns={"StockCode": "sku", "Description": "name"})
    cat[["sku", "name", "price", "sold"]].to_csv(out, index=False)
    print(f"[ok  ] products.csv: {len(cat)} товаров")


if __name__ == "__main__":
    download(SQUAD_URL, HERE / "squad_dev.json")
    download(PI_URL, HERE / "prompt_injections.parquet")
    build_products()
    print("Готово.")
