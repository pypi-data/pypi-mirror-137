import re
import json
from datetime import datetime as dt, time
from itertools import product
from typing import Dict, List, Optional, Tuple, Union

import pendulum
from pendulum.locales.en import locale

from .parser_exceptions import *
from .datetime_config import DatetimeConfig
from .utils import get_time_formats_for_long_date
from .tz_list import _all_abbreviated_tz_list


class DateTimeInfo:
    """This class performs two functions:
    1. If the datetime string passed is short, it tries to parse
    it using regex and `DatetimeConfig`. If parsing failed or it can not detect date and
    time with confidence, an Exception will be raised. The parsed `datetime` object can be
    accessed via `DatetimeInfo.datetime

    2. If the datetime string passed is a long, It will detect the formatting
    tokens and their relative position in order to build a list datetime format that can be used
    to parse the datetime string. eg for "Sunday, May 26th 2013 12:12:12 AM IST Asia/Kolkata",
    `_parse_long_date_formats()` will detect token used are `DDDD`, `MMM` and `Do` and also that
    day of the week comes first or not. Next, with help of `get_time_formats_for_long_date`, it will
    try to build a list of possible long datetime formats. This list will be used to parse the
    datetime string. `long_datetime_formats` property returns the list of possible formats.
    """

    def __init__(self, date_time_raw: str, config: DatetimeConfig):
        self.date_time_raw = date_time_raw

        self.am_or_pm: str = None
        self.iana_tz: str = None
        self.offset_: str = None
        self.abbreviated_tz: str = None
        self.day: str = None
        self.month: str = None
        self.year: str = None
        self.hour: str = None
        self.minutes: str = None
        self.seconds: str = None
        self.fractional_seconds: str = None

        self.token_day_of_week: str = None
        self.token_day: str = None
        self.token_month: str = None

        self.config: DatetimeConfig = config
        self._pre_process_datetime_string()
        self._parse_short_date_formats()

    def __str__(self):
        return json.dumps(self.__dict__, indent=2)

    def _parse(self, matchers):
        tokens = self.date_time_raw.split()
        for token in tokens:
            for var_name, func in matchers.items():
                if getattr(self, var_name) is None:
                    result = func(token)
                    if result and isinstance(result, dict):
                        # if the result is a dict, then resultant
                        # keys are the attributes that are
                        # needed to be set.
                        for key, value in result.items():
                            setattr(self, key, value)
                    elif result is not None:
                        setattr(self, var_name, result)

    def _parse_long_date_formats(self):
        long_date_matchers = self._get_matchers_map(long_date_formats=True)
        self._parse(long_date_matchers)
        if self.token_day is None:
            self.token_day = "DD"

    def _parse_short_date_formats(self):
        short_date_matcher = self._get_matchers_map()
        self._parse(short_date_matcher)

        # Add Validators here
        self._validate_meridiem()

    def _get_matchers_map(self, long_date_formats=False):
        """It returns a `dict` that maps parsing functions to instance
        variable that should store the result.
        """
        if not long_date_formats:
            methods_dict = {
                "iana_tz": self._match_iana_tz,
                "_time_str": self._match_time,
                "_date_str": self._match_short_date,
                "am_or_pm": self._match_am_or_pm,
                "offset_": self._match_offset,
                "abbreviated_tz": self._match_tz_abbreviation,
            }
        else:
            methods_dict = {
                "token_day_of_week": self._match_day_of_week_token,
                "token_month": self._match_month_token,
                "token_day": self._match_day_token,
            }
        return methods_dict

    def _match_iana_tz(self, token: str) -> str:
        """Match and store IANA timezone

        Args:
            token (str): A string value from `self.date_time_raw`
            when splitted by whitespace

        Returns:
            str : An IANA timezone string
        """
        if token in pendulum.timezones:
            return token

    def _match_time(self, token: str) -> Optional[dict]:
        """Use Regex to find any time string present in
        input token

        Args:
            token (str): A string value from `self.date_time_raw`
            when splitted by whitespace

        Raises:
            - MultipleTimesFoundError: When more than one time-string
            are matched
            - InvalidTimeError: When time like string is parsed, but the
            numeric value of hrs, minutes and seconds are out of bound.

        Returns:
            Optional[dict]: return a dict with `hour`, `minutes`, `seconds`
            and `milliseconds`, if any time string is found else return None
        """
        hh_mm_ss_pattern = r"\d{1,2}:\d{1,2}:\d{1,2}\.\d+|^\d{1,2}:\d{1,2}:\d{1,2}$|^\d{1,2}:\d{1,2}:\d{1,2}[+-]{1,1}"
        hh_mm_pattern = r"^(?![+-])\d{1,2}:\d{1,2}$|^(?![+-])\d{1,2}:\d{1,2}[+-]{1,1}"

        matches = re.findall(hh_mm_ss_pattern, token)
        if not matches:
            matches = re.findall(hh_mm_pattern, token)
            if not matches:
                return None

        if len(matches) > 1:
            raise MultipleTimesFoundError(f"Multiple Time values found: {matches}")

        time_ = matches[0].strip()
        if "+" in time_:
            time_ = time_.replace("+", "")
        if "-" in time_:
            time_ = time_.replace("-", "")
        time_ = time_.split(":")

        if len(time_) > 3:
            raise InvalidTimeError(matches[0])

        if len(time_) == 2:
            hour, minutes = time_
            seconds = "00"
        else:
            hour, minutes, seconds = time_

        if "." in seconds:
            seconds, fractional_seconds = seconds.split(".")
        else:
            fractional_seconds = None

        time_errors = []

        if not (0 <= int(hour) <= 24):
            time_errors.append(
                f"Invalid time : {hour}. Hours value must be between 0 and 24"
            )
        if not (0 <= int(minutes) <= 60):
            time_errors.append(
                f"Invalid time : {minutes}. Minutes value must be between 0 and 60"
            )
        if not (0 <= int(seconds) <= 60):
            time_errors.append(
                f"Invalid time : {seconds}. Seconds value must be between 0 and 60"
            )

        if time_errors:
            raise InvalidTimeError(
                f"Invalid time: {matches[0]}. {', '.join(time_errors)}"
            )

        return {
            "hour": f"{int(hour):02d}",
            "minutes": f"{int(minutes):02d}",
            "seconds": f"{int(seconds):02d}",
            "fractional_seconds": fractional_seconds,
        }

    def _match_short_date(self, token: str) -> Optional[Dict[str, str]]:
        """Use Regex to find any short date string present in
        input token

        If a valid, non-ambiguous match is found, then it also sets
        `self.day`, `self.month` and `self.year`

        Args:
            token (str): A string value from `self.date_time_raw`
            when splitted by whitespace

        Returns:
            Optional[Dict[str,str]]: returns a dict containing `year`,
            `month` and `day`
        """
        year_first_pattern = r"(\d{4,4})[-./\\](\d{1,2})[-./\\](\d{1,2})"
        year_last_pattern = r"(\d{1,2})[-./\\](\d{1,2})[-./\\](\d{4,4})"
        two_digit_date_pattern = r"^(\d{1,2})[-./\\](\d{1,2})[-./\\](\d{1,2})"
        # no_sep_date_pattern = r"\d{6,6}"

        # YYYY-XX-XX
        year_first_matches = re.match(year_first_pattern, token)
        if year_first_matches:
            day, month, year = self._process_year_first_or_last_matches(
                year_first_matches.groups(), True
            )

            return {"year": year, "month": month, "day": day}

        # XX-XX-YYYY
        year_last_matches = re.match(year_last_pattern, token)
        if year_last_matches:
            day, month, year = self._process_year_first_or_last_matches(
                year_last_matches.groups(), False
            )
            return {"year": year, "month": month, "day": day}

        # Cases = [XX-XX-XX, XX-X-X, X-X-XX, X-X-X]
        two_digit_date_pattern_matches = re.match(two_digit_date_pattern, token)
        if two_digit_date_pattern_matches:
            day, month, year = self._process_two_digit_date_pattern(
                two_digit_date_pattern_matches.groups()
            )

            return {"year": year, "month": month, "day": day}

        return None

    def _match_offset(self, token: str) -> Union[str, None]:
        """Use Regex to find if any utc offset value
        is present in input token

        Args:
            token (str): A string value from `self.date_time_raw`
            when splitted by whitespace

        Returns:
            Union[str, None]: +hh:mm or -hh:mm if a match is found
            else None
        """
        # Can't parse 12-23-1223T11:12:23.000-05:30
        # offset with - sign, confuses with date separator
        # that why we need space 12-23-1223T11:12:23.000 -05:30
        patterns = [
            r"[Uu][Tt][Cc][+-]\d+",
            r"[+-]\d{1,2}:\d{1,2}",
            # r"[+-]\d{1}:\d{1}", # match this and fail later
            r"[+-]\d+",
        ]

        # if the token matched short date
        # then it is a date don't match for offset
        try:
            short_date = self._match_short_date(token)
        except Exception as e:
            short_date = None

        if short_date:
            return None

        for pattern in patterns:
            matches = re.findall(pattern, token)
            if matches:
                if len(matches) != 1:
                    raise MultipleOffsetsError(f"Multiple offsets found: {matches}")
                match = matches[0].strip()
                if match.lower().startswith("utc"):
                    match = match[3:]
                sign, offset = match[0], match[1:]
                offset = self._pad_and_validate_offset_value(offset)
                if offset:
                    return f"{sign}{offset}"
        return None

    def _match_am_or_pm(self, token: str):
        """
        Use regex to check if input string contains
        AM or PM. Return the matched value
        """
        pattern = r"[ap][m]$"
        matches = re.findall(pattern, token, flags=re.IGNORECASE)
        if not matches or len(matches) != 1:
            return None
        return matches[0].upper()

    def _match_tz_abbreviation(self, token: str) -> Union[str, None]:
        """Check if the input token is an abbreviated timezone
        present in Datetime Config's tz_dict

        Args:
            token (str): A string value from `self.date_time_raw`
            when splitted by whitespace

        Returns:
            Union[str, None]: string like CST/EST etc if a
            match is found else None
        """
        if token.upper() in _all_abbreviated_tz_list:
            return token.upper()
        return None

    def _match_day_of_week_token(self, token: str):
        days = locale.locale["translations"]["days"]
        token_map = {
            "dddd": days["wide"].values(),
            "ddd": days["abbreviated"].values(),
            "dd": days["short"].values(),
        }
        return self._get_token(token, token_map)

    def _match_month_token(self, date_time_token: str):
        months = locale.locale["translations"]["months"]
        token_map = {
            "MMMM": months["wide"].values(),
            "MMM": months["abbreviated"].values(),
        }
        return self._get_token(date_time_token, token_map)

    def _match_day_token(self, date_time_token: str):
        ordinals = ["st", "nd", "rd", "th"]
        for val in ordinals:
            if date_time_token.endswith(val):
                return "Do"
            elif date_time_token.endswith(f"{val},"):
                return "Do,"

        return None

    def _get_token(self, token, token_map: dict):
        for key_, values in token_map.items():
            if token in values:
                return key_
            elif token.replace(",", "") in values:
                return f"{key_},"
        return None

    @property
    def _date_str(self):
        """Returns year-month-day"""
        if self.day and self.month and self.year:
            return f"{self.year}-{self.month}-{self.day}"

    @property
    def _time_str(self):
        """Returns:
        - Hours:Minutes:seconds
        - Hours:Minutes:seconds.Fraction
        """
        if not (self.hour and self.minutes and self.seconds):
            return None

        result = f"{self.year}-{self.month}-{self.day}"
        if self.fractional_seconds:
            result = f"{result}.{self.fractional_seconds}"

        return result

    @property
    def offset(self):
        """
        Return UTC offset that was found during parsing
        """
        if self.offset_:
            return self.offset_

        if self.abbreviated_tz:
            if self.abbreviated_tz not in self.config.tz_dict:
                raise OffsetNotKnownError(
                    f"Offset value not known for '{self.abbreviated_tz}'"
                )
            return self.config.tz_dict[self.abbreviated_tz]

        return None

    @property
    def dtstamp(self):
        """Created Datetime string from parsed raw input string.
        The format is DD-MM-YYYY hh:mm:ss and fractional seconds (upto 6 digit), AM/PM
        and utc offset are appended conditionally

        Returns:
            str/None: A datetime string
        """
        if (
            self.day
            and self.month
            and self.year
            and self.hour
            and self.minutes
            and self.seconds
        ):
            dt_str = f"{self.year}-{self.month}-{self.day}"
            dt_str += f" {self.hour}:{self.minutes}:{self.seconds}"
            if self.fractional_seconds:
                # This property along with dt_format is used to create
                # a datetime object. Since python datetime support 6 digits for
                # microseconds, therefore truncating fraction seconds to 6 digits
                dt_str += f".{self.fractional_seconds[:6]}"

            if self.am_or_pm and int(self.hour) <= 12:
                dt_str += f" {self.am_or_pm.upper()}"

            if self.offset:
                dt_str += f" {self.offset}"
            if self.iana_tz:
                dt_str += f" {self.iana_tz}"

            return dt_str

        return None

    @property
    def dt_format(self):
        """Build datetime format using pendulum tokens.
        This property along with `dtstamp` property can be used
        to parse date using `pendulum.from_format`.

        Returns:
            str: A datetime format build using pendulum formatting
            tokens. This string represent the datetime format for
            `dtstamp`
        """
        if not self.dtstamp:
            return None

        day = "D" if len(self.day) == 1 else "DD"
        month = "M" if len(self.month) == 1 else "MM"
        year = "YYYY"

        if self.am_or_pm and int(self.hour) <= 12:
            hrs = "h" if len(self.hour) == 1 else "hh"
        else:
            hrs = "H" if len(self.hour) == 1 else "HH"
        mins = "m" if len(self.minutes) == 1 else "mm"
        seconds = "s" if len(self.seconds) == 1 else "ss"
        fmt = f"{year}-{month}-{day} {hrs}:{mins}:{seconds}"

        if self.fractional_seconds:
            # Pendulum support upto 6 fractional seconds
            fmt += "." + ("S" * len(self.fractional_seconds[:6]))
        if self.am_or_pm and int(self.hour) <= 12:
            fmt += " A"
        if self.offset:
            fmt += " Z"
        if self.iana_tz:
            fmt += " z"
        return fmt

    @property
    def datetime(self):
        if not self.dt_format or not self.dtstamp:
            return None
        return pendulum.from_format(self.dtstamp, self.dt_format, tz=None)

    @property
    def long_date_format(self) -> str:
        """Parse the long date, return the Date format
        built using pendulum format tokens.


        Raises:
            InvalidDateError: Raised if parsing fails to
            detect tokens for month or day

        Returns:
            str: Return Date format built using pendulum
            formatting tokens
        """
        self._parse_long_date_formats()

        if not (self.token_month and self.token_day):
            raise InvalidDateError(f"{self.date_time_raw}")

        if self.token_day_of_week:
            date_fmt = (
                f"{self.token_day_of_week} "
                f"{self.token_month} "
                f"{self.token_day} "
                f"YYYY"
            )
        else:
            date_fmt = f"{self.token_month} {self.token_day} YYYY"
        return date_fmt

    @property
    def long_datetime_formats(self) -> Tuple[str]:
        """Returns a list of long datetime formats built
        using pendulum formatting tokens.
        """
        parts = [
            [self.long_date_format],
            get_time_formats_for_long_date(self.fractional_seconds),
        ]
        formats = (" ".join(values) for values in product(*parts))
        return formats

    def _pre_process_datetime_string(self):
        """This method is used to pre-process the input string
        if required, before the parsing starts. It performs following
        pre-processing:
        1. Repace a character if it is sandwiched between two integer
        """
        raw_dt = self.date_time_raw
        raw_dt = self._replace_single_characters(raw_dt)
        self.date_time_raw = raw_dt

    def _process_year_first_or_last_matches(self, date_parts, year_first):
        if year_first:
            year, others = date_parts[0], date_parts[1:]
        else:
            others, year = date_parts[:-1], date_parts[-1]

        if len(year) == 3:
            raise InvalidYearError(f"{date_parts} has invalid year.")

        if self.config.day_first is True:
            day, month = others
        elif self.config.day_first is False:
            month, day = others
        else:
            # if day_first is None
            if year_first:
                month, day = others[0], others[1]
                if int(month) > 12:
                    month, day = day, month
            else:
                day, month = self._process_day_and_month(others)

        # Validate day, year, month
        try:
            dt_date = dt(day=int(day), month=int(month), year=int(year))
        except Exception as e:
            msg = f"{str(e)}, date={date_parts}, config={self.config}"
            raise InvalidDateError(msg)

        day = f"{int(day):02d}"
        month = f"{int(month):02d}"

        return day, month, year

    def _process_two_digit_date_pattern(self, date_parts):
        if self.config.year_first is True:
            if self.config.day_first is True:
                # Input = YY-DD-MM
                year, day, month = date_parts
            elif self.config.day_first is False:
                # Input = YY-MM-DD
                year, month, day = date_parts
            else:
                # Input = YY-MM-DD
                year, month, day = date_parts
                if int(month) > 12:
                    month, day = day, month
                # At this point both month and day
                # could have improper values, eg day=42 and month=16
                # This is validated later below in this function.

        elif self.config.year_first is False:
            if self.config.day_first is True:
                # Input = DD-MM-YY
                day, month, year = date_parts
            elif self.config.day_first is False:
                # Input = MM-DD-YY
                month, day, year = date_parts
            else:
                # Input = XX-XX-YY
                date_str = "-".join([f"{int(token):02d}" for token in date_parts])
                day, month, year = self._try_formats(date_str, ("MM-DD-YY", "DD-MM-YY"))
        else:
            if self.config.day_first is True:
                # Input = DD-MM-YY
                day, month, year = date_parts
            elif self.config.day_first is False:
                # Could Be MM-DD-YY or YY-MM-DD
                date_str = "-".join([f"{int(token):02d}" for token in date_parts])
                day, month, year = self._try_formats(date_str, ("MM-DD-YY", "YY-MM-DD"))
            else:
                # Could Be MM-DD-YY or YY-MM-DD or DD-MM-YY
                date_str = "-".join([f"{int(token):02d}" for token in date_parts])
                day, month, year = self._try_formats(
                    date_str, ("MM-DD-YY", "YY-MM-DD", "DD-MM-YY")
                )

        if len(year) == 1:
            year = f"200{year}"
        elif len(year) == 2:
            year = f"20{year}"

        day = f"{int(day):02d}"
        month = f"{int(month):02d}"

        # Validate day, year, month
        try:
            dt_date = dt(day=int(day), month=int(month), year=int(year))
        except Exception as e:
            msg = f"{str(e)}, date={'-'.join(date_parts)}, {self.config}"
            raise InvalidDateError(msg)

        return day, month, year

    def _process_day_and_month(self, tokens: List[str]) -> tuple:
        """Given a list of two numeric tokens,
        try to decide which token is day and which
        is month.

        Args:
            tokens (List): a list containing two
            numeric tokens

        Raises:
            AmbiguousDateError: When we fail to decide between day and month


        Returns:
            tuple: (day, month)
        """

        first_token_is_month = int(tokens[0]) <= 12
        second_token_is_month = int(tokens[1]) <= 12
        if (first_token_is_month and second_token_is_month) and (
            tokens[0] == tokens[1]
        ):
            return tokens[0], tokens[1]

        if first_token_is_month and second_token_is_month:
            raise AmbiguousDateError(f"Can't decide day and month between: {tokens}")

        if not first_token_is_month and not second_token_is_month:
            raise AmbiguousDateError(f"Can't decide day and month between: {tokens}")

        day, month = (
            (tokens[0], tokens[1]) if second_token_is_month else (tokens[1], tokens[0])
        )
        return day, month

    def _pad_and_validate_offset_value(self, offset):
        if ":" in offset:
            # 5:30 --> 05:30
            # 05:30 --> 05:30
            if len(offset) == 4:
                return f"0{offset}"
            elif len(offset) == 5:
                return offset
            else:
                raise InvalidOffsetError(offset)
        else:
            # 2 --> 02:00 | 09 --> 09:00 | 12 --> 12:00
            # 530 --> 05:30
            # 0930 --> 09:30 | 1200 --> 12:00
            if len(offset) == 1:
                return f"0{offset}:00"
            elif len(offset) == 2:
                return f"{offset}:00"
            elif len(offset) == 3:
                return f"0{offset[0]}:{offset[1:]}"
            elif len(offset) == 4:
                return f"{offset[:2]}:{offset[2:]}"
            else:
                raise InvalidOffsetError(offset)

    def _replace_single_characters(self, string: str):
        # Input =  2018-13-09T11:12:23.000-05:30
        # output = 2018-13-09 11:12:23.000-05:30
        char_list = list(string)
        for i, current_char in enumerate(char_list[1:-1]):
            if (
                char_list[i - 1].isdigit()
                and char_list[i].isalpha()
                and char_list[i + 1].isdigit()
            ):
                char_list[i] = " "

        return "".join(char_list)

    def _is_format(self, date_str: str, format: str):
        """Given a date string and a format,
        try to parse the date.

        Args:
            date_str (str): date string
            format (str): date format built using
            tokens used in `pendulum` library

        Returns:
            tuple: If date is parsed successfully return
            (True, datetime object) else return (False, None)
        """
        try:
            parsed = pendulum.from_format(date_str, format)
            return parsed
        except Exception as e:
            return None

    def _try_formats(self, date_str: str, formats: Tuple[str, ...]):
        """Given a date string and a list for formats, make sure
        only one of the format successfully parses the date.
        If multiple or no format parses the date, raise AmbiguousDateError
        Args:
            date_str (str): date string
            formats (List[str]): list of date format built using
            tokens used in `pendulum` library

        Raises:
            AmbiguousDateError: If multiple or no format parses the date,
            raise `AmbiguousDateError`


        Returns:
            tuple[str]: (day, month, year)
        """
        parsed_results = [self._is_format(date_str, format_) for format_ in formats]

        parsed_results = list(filter(lambda x: x is not None, parsed_results))
        if len(parsed_results) != 1:
            raise AmbiguousDateError(
                f"Ambiguous date:{date_str}, possible formats: {formats}"
            )
        result = parsed_results[0]
        return (str(result.day), str(result.month), str(result.year))

    def _validate_meridiem(self):
        if self.hour is None or self.am_or_pm is None:
            # Nothing to check.
            return

        if self.am_or_pm.upper() == "AM":
            if int(self.hour) > 12:
                raise InvalidTimeError(
                    f"Hour is {self.hour} but meridiem is {self.am_or_pm}"
                )
