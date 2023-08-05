# Copyright 2018 QuantRocket LLC - All Rights Reserved
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

import numpy as np
import pandas as pd
from quantrocket.moonshot import read_moonshot_csv
from .tears import create_full_tear_sheet
from .quantrocket_utils import pad_initial


def intraday_to_daily(results, how=None):
    """
    This is taken from quantrocket-moonchart / linechart to remove a cyclical dependency.

    Roll up a DataFrame of intraday performance results to daily, dropping
    the "Time" level from the multi-index.

    The following aggregation methods are supported:

    extreme: min or max of day, whichever is of greater absolute magnitude
    last: last value of day
    max: max of day
    mean: mean of day
    sum: sum of day

    By default, supported fields are aggregated as follows:

    AbsExposure: max
    AbsWeight: max
    Benchmark: last
    Commission: sum
    CommissionAmount: sum
    NetExposure: extreme
    NetLiquidation: mean
    Pnl: sum
    PositionQuantity: extreme
    PositionValue: extreme
    Price: last
    Return: sum
    Slippage: sum
    TotalHoldings: max
    Turnover: sum
    Weight: extreme

    This can be overridden with the `how` parameter.

    Parameters
    ----------
    results : DataFrame, required
         a DataFrame of intraday Moonshot backtest results or PNL results, with
         a "Time" level in the index

    how : dict, optional
        a dict of {fieldname: aggregation method} specifying how to aggregate
        fields. This is combined with and overrides the default methods.

    Returns
    -------
    DataFrame
        a DataFrame of daily results, without a "Time" level in the index

    Examples
    --------
    Convert intraday Moonshot results to daily:

    >>> intraday_results = read_moonshot_csv("moonshot_intraday_backtest.csv")
    >>> daily_results = intraday_to_daily(intraday_results)
    """
    if "Time" not in results.index.names:
        raise Exception("results DataFrame must have 'Time' level in index")

    fields_in_results = results.index.get_level_values("Field").unique()

    daily_results = {}

    # how to aggregate by field
    field_hows = {
        'AbsExposure': 'max',
        'AbsWeight': 'max',
        'Benchmark': 'last',
        'Commission': 'sum',
        'CommissionAmount': 'sum',
        'NetExposure': 'extreme',
        'NetLiquidation': 'mean',
        'Pnl': 'sum',
        'PositionQuantity': 'extreme',
        'PositionValue': 'extreme',
        'Price': 'last',
        'Return': 'sum',
        'Slippage': 'sum',
        'TotalHoldings': 'max',
        'Turnover': 'sum',
        'Weight': 'extreme',
    }

    if how:
        field_hows.update(how)

    for field in fields_in_results:
        if field not in field_hows:
            continue

        field_how = field_hows[field]

        field_results = results.loc[field].astype(np.float64)
        grouped = field_results.groupby(field_results.index.get_level_values("Date"))

        if field_how == "extreme":
            mins = field_results.groupby(field_results.index.get_level_values("Date")).min()
            maxes = field_results.groupby(field_results.index.get_level_values("Date")).max()
            daily_results[field] = mins.where(mins.abs() > maxes.abs(), maxes)
        else:
            daily_results[field] = getattr(grouped, field_how)()

    daily_results = pd.concat(daily_results, names=["Field", "Date"])
    return daily_results


def _get_benchmark_returns(benchmark_prices):
    """
    Returns a Series of benchmark prices, if any. If more than one column has
    benchmark prices, uses the first.
    """
    have_benchmarks = benchmark_prices.notnull().any(axis=0)
    have_benchmarks = have_benchmarks[have_benchmarks]
    if have_benchmarks.empty:
        return None

    col = have_benchmarks.index[0]
    if len(have_benchmarks.index) > 1:
        import warnings
        warnings.warn("Multiple benchmarks found, only using first ({0})".format(col))

    benchmark_prices = benchmark_prices[col]
    benchmark_prices.name = "benchmark"
    return benchmark_prices.pct_change()


def from_moonshot(results, **kwargs):
    """
    Creates a full tear sheet from a moonshot backtest results DataFrame.

    Additional kwargs are passed to create_full_tear_sheet.

    Parameters
    ----------
    results : DataFrame
        multiindex (Field, Date) DataFrame of backtest results

    Returns
    -------
    None
    """
    if "Time" in results.index.names:
        results = intraday_to_daily(results)

    # pandas DatetimeIndexes are serialized with UTC offsets, and pandas
    # parses them back to UTC but doesn't set the tz; pyfolio needs tz-aware
    if not results.index.get_level_values("Date").tz:
        results = results.tz_localize("UTC", level="Date")

    returns = results.loc["Return"].sum(axis=1)
    positions = results.loc["NetExposure"]
    positions["cash"] = 1 - positions.abs().sum(axis=1)

    returns.name = "returns"
    returns = pad_initial(returns)

    fields = results.index.get_level_values("Field").unique()
    if "Benchmark" in fields:
        benchmark_rets = _get_benchmark_returns(
            results.loc["Benchmark"].astype(np.float64))
        benchmark_rets.name = "benchmark_returns"
        benchmark_rets = pad_initial(benchmark_rets)
        kwargs["benchmark_rets"] = benchmark_rets

    return create_full_tear_sheet(
        returns,
        positions=positions,
        **kwargs
    )


def from_moonshot_csv(filepath_or_buffer, **kwargs):
    """
    Creates a full tear sheet from a moonshot backtest results CSV.

    Additional kwargs are passed to :class:`pyfolio.create_full_tear_sheet`.

    Parameters
    ----------
    filepath_or_buffer : str or file-like object
        filepath or file-like object of the CSV

    Returns
    -------
    None
    """
    results = read_moonshot_csv(filepath_or_buffer)
    return from_moonshot(results, **kwargs)
