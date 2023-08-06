"""This is the Norgate Data Python interface
"""


__author__ = "NorgateData Pty Ltd"

from .norgatehelper import *
import csv
from enum import Enum
import sys
import logbook
from datetime import datetime
from .version import __version__

__all__ = [
    "StockPriceAdjustmentType",
    "PaddingType",
    "assetid",
    "symbol",
    "base_type",
    "domicile",
    "currency",
    "exchange_name",
    "exchange_name_full",
    "security_name",
    "subtype1",
    "subtype2",
    "subtype3",
    "financial_summary",
    "business_summary",
    "last_quoted_date",
    "second_last_quoted_date",
    "first_quoted_date",
    "lowest_ever_tick_size",
    "margin",
    "point_value",
    "tick_size",
    "first_notice_date",
    "base_symbol",
    "futures_market_name",
    "futures_market_session_name",
    "futures_market_session_symbols",
    "futures_market_session_symbol",
    "futures_market_session_type",
    "futures_market_symbol",
    "futures_market_symbols",
    "futures_market_session_contracts",
    "price_timeseries",
    "capital_event_timeseries",
    "dividend_yield_timeseries",
    "index_constituent_timeseries",
    "major_exchange_listed_timeseries",
    "padding_status_timeseries",
    "unadjusted_close_timeseries",
    "last_database_update_time",
    "last_price_update_time",
    "status",
    "watchlist_symbols",
    "watchlist",
    "watchlists",
    "fundamental",
    "classification",
    "classification_at_level",
    "corresponding_industry_index",
    "databases",
    "database",
    "database_symbols",
    "session_type",
    "sharesoutstanding",
    "sharesfloat",
    "__version__",
    "__author__",
]

logbook.StreamHandler(sys.stdout).push_application()  # required for Jupyter to output
logger = logbook.Logger("Norgate Data")


class StockPriceAdjustmentType(Enum):
    NONE = 0
    CAPITAL = 1
    CAPITALSPECIAL = 2
    TOTALRETURN = 3


class PaddingType(Enum):
    NONE = 0
    ALLMARKETDAYS = 3
    ALLWEEKDAYS = 4
    ALLCALENDARDAYS = 5

checkstatus()
version_checker(__version__, "norgatedata")

#######################################################################################################
#                           SYMBOL METADATA
#######################################################################################################


def assetid(symbol: str):
    r = get_api_data("security", str(symbol) + "/assetid", None)
    validate_api_response(r, symbol)
    return int(bytes.decode(r.content))


def symbol(assetid: int):
    r = get_api_data("security", str(assetid) + "/symbol", None)
    validate_api_response(r, assetid)
    return bytes.decode(r.content)


def base_type(symbol):
    r = get_api_data("security", str(symbol) + "/basetype", None)
    validate_api_response(r, symbol)
    return bytes.decode(r.content)


def domicile(symbol):
    r = get_api_data("security", str(symbol) + "/domicile", None)
    validate_api_response(r, symbol)
    if len(r.content) == 0:
        return None
    return bytes.decode(r.content)


def exchange_name(symbol):
    r = get_api_data("security", str(symbol) + "/exchange", None)
    validate_api_response(r, symbol)
    if len(r.content) == 0:
        return None
    return bytes.decode(r.content)


def exchange_name_full(symbol):
    r = get_api_data("security", str(symbol) + "/exchangenamefull", None)
    validate_api_response(r, symbol)
    if len(r.content) == 0:
        return None
    return bytes.decode(r.content)


def currency(symbol):
    r = get_api_data("security", str(symbol) + "/currency", None)
    validate_api_response(r, symbol)
    if len(r.content) == 0:
        return None
    return bytes.decode(r.content)


def security_name(symbol):
    r = get_api_data("security", str(symbol) + "/name", None)
    validate_api_response(r, symbol)
    return bytes.decode(r.content)


def futures_market_name(symbol):
    r = get_api_data("futuresmarket", str(symbol) + "/name", None)
    validate_api_response(r, symbol)
    return bytes.decode(r.content)

def futures_market_session_type(sessionsymbol):
    return session_type(sessionsymbol)

def session_type(symbol):
    r = get_api_data("futuresmarketsession", str(symbol) + "/sessiontype", None)
    validate_api_response(r, symbol)
    return bytes.decode(r.content)

def futures_market_session_name(symbol):
    r = get_api_data("futuresmarketsession", str(symbol) + "/sessionname", None)
    validate_api_response(r, symbol)
    return bytes.decode(r.content)




def subtype1(symbol):
    r = get_api_data("security", str(symbol) + "/subtype1", None)
    validate_api_response(r, symbol)
    if len(r.content) == 0:
        return None
    return bytes.decode(r.content)


def subtype2(symbol):
    r = get_api_data("security", str(symbol) + "/subtype2", None)
    validate_api_response(r, symbol)
    if len(r.content) == 0:
        return None
    return bytes.decode(r.content)


def subtype3(symbol):
    r = get_api_data("security", str(symbol) + "/subtype3", None)
    validate_api_response(r, symbol)
    if len(r.content) == 0:
        return None
    return bytes.decode(r.content)


def financial_summary(symbol):
    # TODO: Output date at the same time ?
    r = get_api_data("security", str(symbol) + "/financialsummary", None)
    validate_api_response(r, symbol)
    if len(r.content) == 0:
        return None
    return bytes.decode(r.content)


def business_summary(symbol):
    # TODO: Output date at the same time ?
    r = get_api_data("security", str(symbol) + "/businesssummary", None)
    validate_api_response(r, symbol)
    if len(r.content) == 0:
        return None
    return bytes.decode(r.content)


def first_quoted_date(symbol, datetimeformat="iso", format=""):
    if format != '':
        datetimeformat = format # Hanlde previous calling style - to be deprecated
    r = get_api_data("security", str(symbol) + "/firstquoteddate", None)
    validate_api_response(r, symbol)
    if len(r.content) == 0:
        return None
    return decode_date(r.content, datetimeformat)


def last_quoted_date(symbol, datetimeformat="iso", format=""):
    if format != '':
        datetimeformat = format # Hanlde previous calling style - to be deprecated
    r = get_api_data("security", str(symbol) + "/lastquoteddate", None)
    validate_api_response(r, symbol)
    if len(r.content) == 0:
        return None
    return decode_date(r.content, datetimeformat)
    # return bytes.decode(r.content)


def second_last_quoted_date(symbol, datetimeformat="iso", format=""):
    if format != '':
        datetimeformat = format # Hanlde previous calling style - to be deprecated
    r = get_api_data("security", str(symbol) + "/secondlastquoteddate", None)
    validate_api_response(r, symbol)
    if len(r.content) == 0:
        return None
    return decode_date(r.content, datetimeformat)


def sharesoutstanding(symbol, datetimeformat="iso", format=""):
    if format != '':
        datetimeformat = format # Hanlde previous calling style - to be deprecated
    return fundamental(symbol, field='sharesoutstanding', datetimeformat=datetimeformat)

def sharesfloat(symbol, datetimeformat="iso", format=""):
    if format != '':
        datetimeformat = format # Hanlde previous calling style - to be deprecated
    return fundamental(symbol, field='sharesfloat', datetimeformat=datetimeformat)


#######################################################################################################
#                           FUTURES METADATA
#######################################################################################################
def lowest_ever_tick_size(symbol):
    r = get_api_data("security", str(symbol) + "/lowesteverticksize", None)
    validate_api_response(r, symbol)
    return float(r.content)


def margin(symbol):
    r = get_api_data("security", str(symbol) + "/margin", None)
    validate_api_response(r, symbol)
    return float(r.content)


def point_value(symbol):
    r = get_api_data("security", str(symbol) + "/pointvalue", None)
    validate_api_response(r, symbol)
    return float(r.content)


def tick_size(symbol):
    r = get_api_data("security", str(symbol) + "/ticksize", None)
    validate_api_response(r, symbol)
    return float(r.content)


def first_notice_date(symbol, datetimeformat="iso", format=""):
    if format != '':
        datetimeformat = format # Hanlde previous calling style - to be deprecated
    r = get_api_data("security", str(symbol) + "/firstnoticedate", None)
    validate_api_response(r, symbol)
    if len(r.content) == 0:
        return None
    return decode_date(r.content, datetimeformat)


def base_symbol(symbol):
    logger.warn("base_symbol deprecated, use futures_market_session_symbol instead")
    r = get_api_data("security", str(symbol) + "/basesymbol", None)
    validate_api_response(r, symbol)
    return bytes.decode(r.content)


def futures_market_session_symbol(symbol):
    r = get_api_data("security", str(symbol) + "/futuresmarketsessionsymbol", None)
    validate_api_response(r, symbol)
    return bytes.decode(r.content)


def futures_market_symbol(symbol):
    r = get_api_data("security", str(symbol) + "/futuresmarketsymbol", None)
    validate_api_response(r, symbol)
    return bytes.decode(r.content)

def futures_market_symbols():
    r = get_api_data("futuresmarket", "symbols", None)
    validate_api_response(r, "symbols")
    symbols = r.content.decode().splitlines()
    return symbols


def futures_market_session_symbols():
    r = get_api_data("futuresmarket", "sessionsymbols", None)
    validate_api_response(r, "sessionsymbols")
    symbols = r.content.decode().splitlines()
    return symbols


def futures_market_session_contracts(session_symbol):
    r = get_api_data(
        "futuresmarketsession", str(session_symbol) + "/sessioncontracts", None
    )
    validate_api_response(r, "session_symbol")
    symbols = r.content.decode().splitlines()
    return symbols


#######################################################################################################
#                           TIMESERIES
#######################################################################################################
def price_timeseries(
    symbol,
    stock_price_adjustment_setting=StockPriceAdjustmentType.TOTALRETURN,
    padding_setting=PaddingType.NONE,
    start_date: str = "1800-01-01",
    end_date: str = "2999-01-01",
    limit: int = -1,
    timeseriesformat: str = "numpy-recarray",
    fields=None,
    datetimeformat: str = "",
    timezone: str = "",
    interval: str = "D",
    format: str = "", # Old parameter name - replaced by timeseriesformat, but kept here for compatibility
):
    if format != '':
        timeseriesformat = format # Handle old parameter name style
    lowercase_columns = False
    if timeseriesformat == "pandas-dataframe-zipline":
        timeseriesformat = "pandas-dataframe"
        lowercase_columns = True
    parameters = {
        "start_date": encode_date_to_iso(start_date),
        "end_date": encode_date_to_iso(end_date),
        "limit": str(limit),
        "stock_price_adjustment_setting": stock_price_adjustment_setting.name,
        "padding_setting": padding_setting.name,
        "format": timeseriesformat,
        "datetimeformat": datetimeformat,
        "timezone": timezone,
        "interval": interval,
    }
    if fields is not None and type(fields) == list:
        parameters["fields"] = ",".join(fields)
    r = get_api_data("prices", str(symbol), parameters)
    validate_api_response(r, symbol)
    if timeseriesformat == "numpy-recarray":
        return create_numpy_recarray(
            r, None, datetimeformat=datetimeformat, timezone=timezone
        )
    if timeseriesformat == "pandas-dataframe":
        return create_pandas_dataframe(
            symbol,
            r,
            None,
            lowercase_columns=lowercase_columns,
            datetimeformat=datetimeformat,
            timezone=timezone,
        )
    if timeseriesformat == "numpy-ndarray":
        return create_numpy_ndarray(
            r, None, datetimeformat=datetimeformat, timezone=timezone
        )


###############
def capital_event_timeseries(
    symbol,
    padding_setting=PaddingType.NONE,
    start_date: str = "1800-01-01",
    end_date: str = "2999-01-01",
    limit: int = -1,
    timeseriesformat: str = "numpy-recarray",
    pandas_dataframe=None,
    numpy_ndarray=None,
    numpy_recarray=None,
    datetimeformat: str = "",
    timezone: str = "",
    format: str = "", # Old parameter name - replaced by timeseriesformat, but kept here for compatibility
):
    if format != '':
        timeseriesformat = format # Handle old parameter name style
    if (
        pandas_dataframe is not None
        or numpy_ndarray is not None
        or numpy_recarray is not None
    ):
        start_date, end_date, limit = validate_existing_array(
            pandas_dataframe, numpy_ndarray, numpy_recarray, timeseriesformat
        )
    parameters = {
        "start_date": encode_date_to_iso(start_date),
        "end_date": encode_date_to_iso(end_date),
        "limit": str(limit),
        "padding_setting": padding_setting.name,
        "format": timeseriesformat,
        "datetimeformat": datetimeformat,
        "timezone": timezone,
    }
    r = get_api_data("capitalevent", str(symbol), parameters)
    validate_api_response(r, symbol)
    if timeseriesformat == "numpy-recarray":
        return create_numpy_recarray(
            r, numpy_recarray, datetimeformat=datetimeformat, timezone=timezone
        )
    if timeseriesformat == "pandas-dataframe":
        return create_pandas_dataframe(
            symbol,
            r,
            pandas_dataframe,
            datetimeformat=datetimeformat,
            timezone=timezone,
        )
    if timeseriesformat == "numpy-ndarray":
        return create_numpy_ndarray(
            r, numpy_ndarray, datetimeformat=datetimeformat, timezone=timezone
        )


###############


def unadjusted_close_timeseries(
    symbol,
    padding_setting=PaddingType.NONE,
    start_date="1800-01-01",
    end_date: str = "2999-01-01",
    limit: int = -1,
    timeseriesformat: str = "numpy-recarray",
    pandas_dataframe=None,
    numpy_ndarray=None,
    numpy_recarray=None,
    datetimeformat: str = "",
    timezone: str = "",
    format: str = "", # Old parameter name - replaced by timeseriesformat, but kept here for compatibility
):
    if format != '':
        timeseriesformat = format # Handle old parameter name style
    if (
        pandas_dataframe is not None
        or numpy_ndarray is not None
        or numpy_recarray is not None
    ):
        start_date, end_date, limit = validate_existing_array(
            pandas_dataframe, numpy_ndarray, numpy_recarray, timeseriesformat
        )
    parameters = {
        "start_date": encode_date_to_iso(start_date),
        "end_date": encode_date_to_iso(end_date),
        "limit": str(limit),
        "padding_setting": padding_setting.name,
        "format": timeseriesformat,
        "datetimeformat": datetimeformat,
        "timezone": timezone,
    }
    r = get_api_data("unadjustedclose", str(symbol), parameters)
    validate_api_response(r, symbol)
    if timeseriesformat == "numpy-recarray":
        return create_numpy_recarray(
            r, numpy_recarray, datetimeformat=datetimeformat, timezone=timezone
        )
    if timeseriesformat == "pandas-dataframe":
        return create_pandas_dataframe(
            symbol,
            r,
            pandas_dataframe,
            datetimeformat=datetimeformat,
            timezone=timezone,
        )
    if timeseriesformat == "numpy-ndarray":
        return create_numpy_ndarray(
            r, numpy_ndarray, datetimeformat=datetimeformat, timezone=timezone
        )


#####


def dividend_yield_timeseries(
    symbol,
    padding_setting=PaddingType.NONE,
    start_date="1800-01-01",
    end_date: str = "2999-01-01",
    limit: int = -1,
    timeseriesformat="numpy-recarray",
    pandas_dataframe=None,
    numpy_ndarray=None,
    numpy_recarray=None,
    datetimeformat: str = "",
    timezone: str = "",
    format: str = "", # Old parameter name - replaced by timeseriesformat, but kept here for compatibility
):
    if format != '':
        timeseriesformat = format # Handle old parameter name style
    if (
        pandas_dataframe is not None
        or numpy_ndarray is not None
        or numpy_recarray is not None
    ):
        start_date, end_date, limit = validate_existing_array(
            pandas_dataframe, numpy_ndarray, numpy_recarray, timeseriesformat
        )
    parameters = {
        "start_date": encode_date_to_iso(start_date),
        "end_date": encode_date_to_iso(end_date),
        "limit": str(limit),
        "padding_setting": padding_setting.name,
        "format": timeseriesformat,
        "datetimeformat": datetimeformat,
        "timezone": timezone,
    }
    r = get_api_data("dividendyield", str(symbol), parameters)
    validate_api_response(r, symbol)
    if timeseriesformat == "numpy-recarray":
        return create_numpy_recarray(
            r, numpy_recarray, datetimeformat=datetimeformat, timezone=timezone
        )
    if timeseriesformat == "pandas-dataframe":
        return create_pandas_dataframe(
            symbol,
            r,
            pandas_dataframe,
            datetimeformat=datetimeformat,
            timezone=timezone,
        )
    if timeseriesformat == "numpy-ndarray":
        return create_numpy_ndarray(
            r, numpy_ndarray, datetimeformat=datetimeformat, timezone=timezone
        )


###############


def index_constituent_timeseries(
    symbol,
    indexname: str,
    padding_setting=PaddingType.NONE,
    start_date="1800-01-01",
    end_date: str = "2999-01-01",
    limit: int = -1,
    timeseriesformat: str = "numpy-recarray",
    pandas_dataframe=None,
    numpy_ndarray=None,
    numpy_recarray=None,
    datetimeformat: str = "",
    timezone: str = "",
    format: str = "", # Old parameter name - replaced by timeseriesformat, but kept here for compatibility
):
    if format != '':
        timeseriesformat = format # Handle old parameter name style
    if (
        pandas_dataframe is not None
        or numpy_ndarray is not None
        or numpy_recarray is not None
    ):
        start_date, end_date, limit = validate_existing_array(
            pandas_dataframe, numpy_ndarray, numpy_recarray, timeseriesformat
        )
    parameters = {
        "start_date": encode_date_to_iso(start_date),
        "end_date": encode_date_to_iso(end_date),
        "indexname": indexname,
        "limit": str(limit),
        "padding_setting": padding_setting.name,
        "format": timeseriesformat,
        "datetimeformat": datetimeformat,
        "timezone": timezone,
    }
    r = get_api_data("indexconstituent", str(symbol), parameters)
    validate_api_response(r, symbol)
    if timeseriesformat == "numpy-recarray":
        return create_numpy_recarray(
            r, numpy_recarray, datetimeformat=datetimeformat, timezone=timezone
        )
    if timeseriesformat == "pandas-dataframe":
        return create_pandas_dataframe(
            symbol,
            r,
            pandas_dataframe,
            datetimeformat=datetimeformat,
            timezone=timezone,
        )
    if timeseriesformat == "numpy-ndarray":
        return create_numpy_ndarray(
            r, numpy_ndarray, datetimeformat=datetimeformat, timezone=timezone
        )


###############
def major_exchange_listed_timeseries(
    symbol,
    padding_setting=PaddingType.NONE,
    start_date="1800-01-01",
    end_date="2999-01-01",
    limit: int = -1,
    timeseriesformat: str = "numpy-recarray",
    pandas_dataframe=None,
    numpy_ndarray=None,
    numpy_recarray=None,
    datetimeformat="",
    timezone="",
    format: str = "", # Old parameter name - replaced by timeseriesformat, but kept here for compatibility
):
    if format != '':
        timeseriesformat = format # Handle old parameter name style
    if (
        pandas_dataframe is not None
        or numpy_ndarray is not None
        or numpy_recarray is not None
    ):
        start_date, end_date, limit = validate_existing_array(
            pandas_dataframe, numpy_ndarray, numpy_recarray, timeseriesformat
        )
    parameters = {
        "start_date": encode_date_to_iso(start_date),
        "end_date": encode_date_to_iso(end_date),
        "limit": str(limit),
        "padding_setting": padding_setting.name,
        "format": timeseriesformat,
        "datetimeformat": datetimeformat,
        "timezone": timezone,
    }
    r = get_api_data("majorexchangelisted", str(symbol), parameters)
    validate_api_response(r, symbol)
    if timeseriesformat == "numpy-recarray":
        return create_numpy_recarray(
            r, numpy_recarray, datetimeformat=datetimeformat, timezone=timezone
        )
    if timeseriesformat == "pandas-dataframe":
        return create_pandas_dataframe(
            symbol,
            r,
            pandas_dataframe,
            datetimeformat=datetimeformat,
            timezone=timezone,
        )
    if timeseriesformat == "numpy-ndarray":
        return create_numpy_ndarray(
            r, numpy_ndarray, datetimeformat=datetimeformat, timezone=timezone
        )


###############
def padding_status_timeseries(
    symbol,
    padding_setting=PaddingType.NONE,
    start_date="1800-01-01",
    end_date="2999-01-01",
    limit: int = -1,
    timeseriesformat: str = "numpy-recarray",
    pandas_dataframe=None,
    numpy_ndarray=None,
    numpy_recarray=None,
    datetimeformat: str = "",
    timezone: str = "",
    format: str = "", # Old parameter name - replaced by timeseriesformat, but kept here for compatibility
):
    if format != '':
        timeseriesformat = format # Handle old parameter name style
    if (
        pandas_dataframe is not None
        or numpy_ndarray is not None
        or numpy_recarray is not None
    ):
        start_date, end_date, limit = validate_existing_array(
            pandas_dataframe, numpy_ndarray, numpy_recarray, timeseriesformat
        )
    parameters = {
        "start_date": encode_date_to_iso(start_date),
        "end_date": encode_date_to_iso(end_date),
        "limit": str(limit),
        "padding_setting": padding_setting.name,
        "format": timeseriesformat,
        "datetimeformat": datetimeformat,
        "timezone": timezone,
    }
    r = get_api_data("paddingstatus", str(symbol), parameters)
    validate_api_response(r, symbol)
    if timeseriesformat == "numpy-recarray":
        return create_numpy_recarray(
            r, numpy_recarray, datetimeformat=datetimeformat, timezone=timezone
        )
    if timeseriesformat == "pandas-dataframe":
        return create_pandas_dataframe(
            symbol,
            r,
            pandas_dataframe,
            datetimeformat=datetimeformat,
            timezone=timezone,
        )
    if timeseriesformat == "numpy-ndarray":
        return create_numpy_ndarray(
            r, numpy_ndarray, datetimeformat=datetimeformat, timezone=timezone
        )


#######################################################################################################
#                           INFORMATIONAL - UPDATE RELATED
#######################################################################################################


def last_database_update_time(databasename):
    r = get_api_data("database", databasename + "/lastupdatetime", None)
    validate_api_response(r, databasename)
    result = datetime.strptime(r.content.decode().replace(":", ""), "%Y-%m-%dT%H%M%S%z")
    return result


def last_price_update_time(symbol):
    r = get_api_data("security", str(symbol) + "/lastupdatetime", None)
    validate_api_response(r, symbol)
    result = datetime.strptime(r.content.decode().replace(":", ""), "%Y-%m-%dT%H%M%S%z")
    return result


def status():
    return checkstatus()


#######################################################################################################
#                           WATCHLIST
#######################################################################################################


def watchlist(watchlistname: str):
    parameters = {"format": "csv"}
    r = get_api_data("watchlist", watchlistname, parameters)
    validate_api_response(r, watchlistname)
    if len(r.content) == 0:
        return None
    txtlines = r.content.decode().splitlines()
    lines = csv.reader(txtlines, delimiter=",")
    symbols = []
    for line in lines:
        if line[0] == "Symbol":
            continue
        symbols.append(
            {"symbol": line[0], "assetid": int(line[1]), "securityname": line[2]}
        )
    return symbols


def watchlist_symbols(watchlistname: str):
    parameters = {"format": "symbolsonly"}
    r = get_api_data("watchlist", watchlistname, parameters)
    validate_api_response(r, watchlistname)
    if len(r.content) == 0:
        return None
    symbols = r.content.decode().splitlines()
    return symbols


def watchlists():
    r = get_api_data("watchlists", None, None)
    validate_api_response(r, "watchlists")
    if len(r.content) == 0:
        return None
    symbols = r.content.decode().splitlines()
    return symbols


#######################################################################################################
#                           DATABASE
#######################################################################################################


def database(databasename: str):
    parameters = {"format": "csv"}
    r = get_api_data("database", databasename, parameters)
    validate_api_response(r, databasename)
    txtlines = r.content.decode().splitlines()
    lines = csv.reader(txtlines, delimiter=",")
    symbols = []
    for line in lines:
        if line[0] == "Symbol":
            continue
        symbols.append(
            {"symbol": line[0], "assetid": int(line[1]), "securityname": line[2]}
        )
    return symbols


def database_symbols(databasename: str):
    parameters = {"format": "symbolsonly"}
    r = get_api_data("database", databasename, parameters)
    validate_api_response(r, databasename)
    if len(r.content) == 0:
        return None
    symbols = r.content.decode().splitlines()
    return symbols


def databases():
    r = get_api_data("databases", None, None)
    symbols = r.content.decode().splitlines()
    return symbols


#######################################################################################################
#                           FUNDAMENTALS
#######################################################################################################
def fundamental(symbol, field: str, datetimeformat: str = "iso", format: str = ""):
    if format != '':
        datetimeformat = format # Handle old parameter name style
    # Returns both the field value and date
    r = get_api_data("fundamental", str(symbol) + "/" + field, None)
    validate_api_response(r, symbol)
    if len(r.content) == 0:
        return None, None
    fundamentalresult, fundadate = r.content.decode().split(",")
    formats = r.headers["X-Norgate-Data-Field-Formats"].split(",")
    if formats[0] == "f8" and fundamentalresult != '':
        fundamentalresult = float(fundamentalresult)
    return fundamentalresult, decode_date(fundadate, datetimeformat)

#######################################################################################################
#                           CLASSIFICATION RELATED
#######################################################################################################
def classification(symbol, schemename: str, classificationresulttype: str):
    parameters = {
        "schemename": schemename,
        "classificationresulttype": classificationresulttype,
    }
    r = get_api_data("security", str(symbol) + "/classification", parameters)
    if len(r.content) == 0:
        return None
    validate_api_response(r, symbol)
    result = bytes.decode(r.content)
    return result


def classification_at_level(
    symbol, schemename: str, classificationresulttype: str, level: int
):
    parameters = {
        "schemename": schemename,
        "classificationresulttype": classificationresulttype,
        "level": level,
    }
    r = get_api_data("security", str(symbol) + "/classification", parameters)
    validate_api_response(r, symbol)
    if len(r.content) == 0:
        return None
    result = bytes.decode(r.content)
    return result


def corresponding_industry_index(
    symbol, indexfamilycode: str, level: int, indexreturntype: str
):
    parameters = {
        "indexfamilycode": indexfamilycode,
        "level": level,
        "indexreturntype": indexreturntype,
    }
    r = get_api_data(
        "security", str(symbol) + "/correspondingindustryindex", parameters
    )
    validate_api_response(r, symbol + " or " + indexfamilycode)
    if len(r.content) == 0:
        return None
    result = bytes.decode(r.content)
    return result


logger.info("NorgateData package v" + __version__ + ": Init complete")
