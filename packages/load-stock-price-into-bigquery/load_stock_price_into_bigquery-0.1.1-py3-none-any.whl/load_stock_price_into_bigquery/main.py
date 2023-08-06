#!/usr/bin/env python3

import argparse
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from datetime import date, timedelta
from typing import List

import numpy as np
import pandas as pd
import pandas_datareader as pdr
from google.cloud.bigquery import Client

from .sp500_symbols import sp500_symbols

PROJECT_ID = "stock-scraping-316514"
TABLE_ID = "stock.daily-stock-price"


@dataclass
class StockPrice:
    symbol: str
    date: str
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: int


class StockPriceWriter(ABC):

    @abstractmethod
    def write(self, stock_prices: List[StockPrice]) -> None:
        pass


class BigQueryWriter(StockPriceWriter):

    def __init__(self, project_id: str, table_id: str) -> None:
        self.project_id = project_id
        self.table_id = table_id
        self.client = Client(project=project_id)

    def write(self, stock_prices: List[StockPrice]) -> None:
        job = self.client.load_table_from_json(
            [asdict(stock_price) for stock_price in stock_prices],
            self.table_id)
        job.result()


def get_daily_stock_price(symbols: List[str], start: str, end: str) -> List[StockPrice]:
    df = pdr.get_data_yahoo(symbols, start=start, end=end)
    df = df[np.logical_and(df.index >= start, df.index <= end)]

    stock_prices = []
    for symbol in symbols:
        for row in df.loc[:, pd.IndexSlice[:, symbol]].iterrows():
            stock_price = StockPrice(
                symbol=symbol,
                date=str(row[0].date()),
                open=row[1]["Open"][0],
                high=row[1]["High"][0],
                low=row[1]["Low"][0],
                close=row[1]["Close"][0],
                adj_close=row[1]["Adj Close"][0],
                volume=row[1]["Volume"][0],
            )

            stock_prices.append(stock_price)

    return stock_prices


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_date", type=str)
    parser.add_argument("--end_date", type=str)
    args = parser.parse_args()

    start = args.start_date
    if start is None:
        start = str(date.today() - timedelta(days=6))

    end = args.end_date
    if end is None:
        end = str(date.today() - timedelta(days=6))

    stock_prices = get_daily_stock_price(sp500_symbols, start=start, end=end)

    writer = BigQueryWriter(
        project_id=PROJECT_ID,
        table_id=TABLE_ID,
    )

    writer.write(stock_prices)


if __name__ == "__main__":
    main()
