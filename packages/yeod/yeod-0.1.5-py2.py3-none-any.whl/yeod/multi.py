#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Yahoo! Finance market data downloader (+fix for Pandas Datareader)
# https://github.com/ranaroussi/yeod
#
# Copyright 2017-2019 Ran Aroussi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from __future__ import print_function

import time as _time
import multitasking as _multitasking
import pandas as _pd
import requests
import json
import os.path
import os

from . import Ticker, utils
from . import shared


def download(tickers, start=None, end=None, actions=False, threads=True,
             group_by='column', auto_adjust=False, back_adjust=False,
             progress=True, period="max", interval="1d", prepost=False,
             proxy=None, rounding=False,api_token="",usecache=False,**kwargs):
    """Download yahoo tickers
    :Parameters:
        tickers : str, list
            List of tickers to download
        period : str
            Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            Either Use period parameter or use start and end
        interval : str
            Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            Intraday data cannot extend last 60 days
        start: str
            Download start date string (YYYY-MM-DD) or _datetime.
            Default is 1900-01-01
        end: str
            Download end date string (YYYY-MM-DD) or _datetime.
            Default is now
        group_by : str
            Group by 'ticker' or 'column' (default)
        prepost : bool
            Include Pre and Post market data in results?
            Default is False
        auto_adjust: bool
            Adjust all OHLC automatically? Default is False
        actions: bool
            Download dividend + stock splits data. Default is False
        threads: bool / int
            How many threads to use for mass downloading. Default is True
        proxy: str
            Optional. Proxy server URL scheme. Default is None
        rounding: bool
            Optional. Round values to 2 decimal places?
    """

    # create ticker list
    tickers = tickers if isinstance(
        tickers, (list, set, tuple)) else tickers.replace(',', ' ').split()

    tickers = list(set([ticker.upper() for ticker in tickers]))

    if progress:
        shared._PROGRESS_BAR = utils.ProgressBar(len(tickers), 'completed')

    # reset shared._DFS
    shared._DFS = {}
    shared._ERRORS = {}

    # download using threads
    if threads:
        if threads is True:
            threads = min([len(tickers), _multitasking.cpu_count() * 2])
        _multitasking.set_max_threads(threads)
        for i, ticker in enumerate(tickers):
            _download_one_threaded(ticker, period=period, interval=interval,
                                   start=start, end=end, prepost=prepost,
                                   actions=actions, auto_adjust=auto_adjust,
                                   back_adjust=back_adjust,
                                   progress=(progress and i > 0), proxy=proxy,
                                   rounding=rounding,api_token=api_token,usecache=usecache)
        while len(shared._DFS) < len(tickers):
            _time.sleep(0.01)

    # download synchronously
    else:
        for i, ticker in enumerate(tickers):
            data = _download_one(ticker, period=period, interval=interval,
                                 start=start, end=end, prepost=prepost,
                                 actions=actions, auto_adjust=auto_adjust,
                                 back_adjust=back_adjust, rounding=rounding,api_token=api_token)
            shared._DFS[ticker.upper()] = data
            if progress:
                shared._PROGRESS_BAR.animate()

    if progress:
        shared._PROGRESS_BAR.completed()

    if shared._ERRORS:
        print('\n%.f Failed download%s:' % (
            len(shared._ERRORS), 's' if len(shared._ERRORS) > 1 else ''))
        # print(shared._ERRORS)
        print("\n".join(['- %s: %s' %
                         v for v in list(shared._ERRORS.items())]))

    if len(tickers) == 1:
        return shared._DFS[tickers[0]]

    try:
        data = _pd.concat(shared._DFS.values(), axis=1,
                          keys=shared._DFS.keys())
    except Exception:
        _realign_dfs()
        data = _pd.concat(shared._DFS.values(), axis=1,
                          keys=shared._DFS.keys())

    if group_by == 'column':
        data.columns = data.columns.swaplevel(0, 1)
        data.sort_index(level=0, axis=1, inplace=True)

    return data


def _realign_dfs():
    idx_len = 0
    idx = None

    for df in shared._DFS.values():
        if len(df) > idx_len:
            idx_len = len(df)
            idx = df.index

    for key in shared._DFS.keys():
        try:
            shared._DFS[key] = _pd.DataFrame(
                index=idx, data=shared._DFS[key]).drop_duplicates()
        except Exception:
            shared._DFS[key] = _pd.concat([
                utils.empty_df(idx), shared._DFS[key].dropna()
            ], axis=0, sort=True)

        # remove duplicate index
        shared._DFS[key] = shared._DFS[key].loc[
            ~shared._DFS[key].index.duplicated(keep='last')]


@_multitasking.task
def _download_one_threaded(ticker, start=None, end=None,
                           auto_adjust=False, back_adjust=False,
                           actions=False, progress=True, period="max",
                           interval="1d", prepost=False, proxy=None,
                           rounding=False,api_token="",usecache=False):

    data = _download_one(ticker, start, end, auto_adjust, back_adjust,
                         actions, period, interval, prepost, proxy, rounding,api_token,usecache)
    shared._DFS[ticker.upper()] = data
    if progress:
        shared._PROGRESS_BAR.animate()


def _download_one(ticker, start=None, end=None,
                  auto_adjust=False, back_adjust=False,
                  actions=False, period="max", interval="1d",
                  prepost=False, proxy=None, rounding=False,api_token="",usecache=False):


    return onetickerx(ticker,fromx=start,to=end,api_token=api_token,usecache=usecache)

    # return Ticker(ticker).history(period=period, interval=interval,
    #                               start=start, end=end, prepost=prepost,
    #                               actions=actions, auto_adjust=auto_adjust,
    #                               back_adjust=back_adjust, proxy=proxy,
    #                               rounding=rounding, many=True)

def mcreate(paths):
    for path in paths:
        if os.path.exists(path) == False:
            os.mkdir(path)
 
def onetickerx(ticker,fromx="2019-01-01",to="2122-01-01",api_token="",usecache=False):    
    filepath=f"data/ticker/{fromx}_{to}/{ticker}.json"

    if os.path.exists(filepath) and usecache: 
        print(f"Loading from cache {filepath}")
        with open(filepath) as jsonfile:      
            jx=json.load(jsonfile)
        dx=_pd.read_json(json.dumps(jx))
        if len(dx.index.values) == 0:
                print(f"{ticker} has no data {url}")
                shared._ERRORS[ticker]="Empty"
                return utils.empty_df()
                
        if "date" not in list(dx.columns):
                print(f"{ticker} has no data {url}")
                shared._ERRORS[ticker]="Empty"
                return utils.empty_df()
        dx=dx.rename(columns={"date":"Date","open":"Open","high":"High","low":"Low","close":"Close","adjusted_close":"Adjusted_Close","volume":"Volume"})
        dx.set_index("Date",inplace=True)
        return dx
    else:
        url=f"https://eodhistoricaldata.com/api/eod/{ticker}?from={fromx}&to={to}&fmt=json&period=d&api_token={api_token}"
        response=requests.get(url)

        if response.status_code != 200 or response.status_code >= 400:
            print(f"Could not retrieve {ticker}")
            shared._ERRORS[ticker]="Empty"
            return utils.empty_df()
        else:
            mcreate([f"data",f"data/ticker",f"data/ticker/{fromx}_{to}"])
            with open(filepath,"w") as jsonfile:
                json.dump(response.json(),jsonfile)
            jx=json.dumps(response.json())

            dx=_pd.read_json(jx)
            if len(dx.index.values) == 0:
                print(f"{ticker} has no data {url}")
                shared._ERRORS[ticker]="Empty"
                return utils.empty_df()

            if "date" not in list(dx.columns):
                print(f"{ticker} has no data {url}")
                shared._ERRORS[ticker]="Empty"
                return utils.empty_df()


            dx=dx.rename(columns={"date":"Date","open":"Open","high":"High","low":"Low","close":"Close","adjusted_close":"Adjusted_Close","volume":"Volume"})




            dx.set_index("Date",inplace=True)

            return dx.fillna(method='ffill').interpolate(method='linear')

