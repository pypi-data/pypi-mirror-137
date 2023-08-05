"Parse TimeTracker time worksheets and add start and endtime to each task"

from __future__ import annotations

from datetime import date, datetime, time, timedelta
from collections import namedtuple
import enum
import locale
import pathlib

__version__ = '1.0.0'


_LOCALE = locale.getlocale(locale.LC_TIME)
TITRAX_PATH = '~/.TimeTracker'
DAYFILE_PREFIX = '# TIMETRACKER log saved at '
# Date format ex.: "Mon Jan  3 15:50:30 2022"
DATE_FORMAT = '%a %b %d %H:%M:%S %Y'
# Row format ex.: " 0:30 Lunsj"
TIME_FORMAT = '%H:%M'
ROUNDING_INTERVALS = (5, 10, 15, 20, 30)

Hours = namedtuple('Hours', ('hours', 'start', 'end'))


class SortHoursBy(str, enum.Enum):
    PROJECT = 'project'
    MIN = 'timemin'
    MAX = 'timemax'

    def __str__(self):
        return self.value


def set_safe_locale():
    locale.setlocale(locale.LC_TIME, "C")


def undo_set_safe_locale():
    locale.setlocale(locale.LC_TIME, _LOCALE)


def timedelta_to_time(td):
    dt = datetime.min + td
    return dt.time()


def isoweeknumber_to_days(weeknumber: int):
    this_year = date.today().year
    days = [date.fromisocalendar(this_year, weeknumber, daynumber).isoformat()
            for daynumber in range(1, 7+1)]
    return days


class TitraxDayfileParser:

    @staticmethod
    def get_dayfile_path(day) -> pathlib.Path:
        filename = str(day)
        path = pathlib.Path(TITRAX_PATH) / filename
        return path.expanduser()

    @classmethod
    def get_day_contents(cls, day) -> list:
        path = cls.get_dayfile_path(day)
        try:
            with open(path) as F:
                contents = F.readlines()
        except FileNotFoundError:
            raise ValueError(f'File for day {day} not found')
        return contents

    @staticmethod
    def parse_dateline(dateline: str) -> datetime:
        set_safe_locale()
        end_time_string = dateline[len(DAYFILE_PREFIX):].strip()
        end_time = datetime.strptime(end_time_string, DATE_FORMAT)
        undo_set_safe_locale()
        return end_time

    @classmethod
    def parse_day_contents(cls, contents: list, sort_by: SortHoursBy = None):
        if not contents:
            raise ValueError('Not a titrax dayfile, empty')
        dateline = contents[0]
        if not dateline.startswith(DAYFILE_PREFIX):
            raise ValueError('Not a titrax dayfile, first line is wrong')
        rows = [row for row in contents[1:] if not row.startswith('#')]
        if not rows:
            raise ValueError('No hours registered')

        end_datetime = cls.parse_dateline(dateline)
        hours = cls.parse_rows(rows)
        return end_datetime, hours

    @staticmethod
    def parse_rows(rows: list) -> dict:
        set_safe_locale()
        hours_list = []
        for row in rows:
            time_spent_string, project = row.strip().split(maxsplit=1)
            if len(time_spent_string) < len('HH:MM'):
                time_spent_string = '0' + time_spent_string
            timeobj = time.fromisoformat(time_spent_string)
            time_spent = timedelta(hours=timeobj.hour, minutes=timeobj.minute)
            hours_list.append((project, time_spent))
        undo_set_safe_locale()
        hours = dict(hours_list)
        return hours


class Worksheet:
    day: str
    start: datetime
    end: datetime
    hours: dict
    projects: str
    dayfile: str
    _hours_per_project: dict

    def __eq__(self, other):
        for attr in ('day', 'start', 'end', 'hours_per_project'):
            if getattr(self, attr) != getattr(other, attr):
                return False
        return True

    def __init__(self, hours, start=None, end=None):
        if start and end:
            raise ValueError("Either start or end must be set but not both")
        self._hours_per_project = hours
        self.sum = self._sum_hours()
        if start:
            self.start = start
            self.end = start + self.sum
        else:
            self.end = end
            self.start = self.end - self.sum

        self.day = self.end.date().isoformat()
        self.projects = tuple(hours.keys())
        self.hours = self._hours_with_start_end()

    @classmethod
    def from_titrax_day(cls, day):
        "Create new worksheet from titrax dayfile"
        parser = TitraxDayfileParser
        contents = parser.get_day_contents(str(day))
        dayfile = '\n'.join(contents)
        end_datetime, hours = parser.parse_day_contents(contents)
        obj = cls(hours, end=end_datetime)
        obj.dayfile = dayfile
        return obj

    def _sum_hours(self):
        seconds = sum(td.seconds for td in self._hours_per_project.values())
        return timedelta(seconds=seconds)

    def _hours_with_start_end(self):
        start = self.start
        startend_dict = {}
        for project, hours in self._hours_per_project.items():
            end = start + hours
            startend_dict[project] = Hours(hours, start, end)
            start = end
        return startend_dict

    def round(self, round_to: int):
        assert round_to in ROUNDING_INTERVALS
        hours_per_project = {}
        interval = round_to * 60
        for project, hours in self._hours_per_project.items():
            seconds = round(hours.seconds/interval)*interval
            hours_per_project[project] = timedelta(seconds=seconds)
        obj = self.__class__(hours_per_project, start=self.start)
        return obj

    def sort(self, sort_by: SortHoursBy):
        hours_tuple = self._hours_per_project.items()
        if sort_by == SortHoursBy.PROJECT:
            hours_list = sorted(hours_tuple)
        elif sort_by == SortHoursBy.MIN:
            hours_list = [(k, v)
                          for v, k in sorted((v, k)
                          for k, v in hours_tuple)]
        elif sort_by == SortHoursBy.MAX:
            hours_list = [(k, v)
                          for v, k in reversed(sorted(
                                  (v, k) for k, v in hours_tuple))
                          ]
        hours_per_project = dict(hours_list)
        obj = self.__class__(hours_per_project, start=self.start)
        return obj

    def reset_starttime(self, starttime):
        day = date.fromisoformat(self.day)
        starttime = datetime.combine(day, timedelta_to_time(starttime))
        obj = self.__class__(self._hours_per_project, start=starttime)
        return obj

    def pprint_titrax(self):
        out = []
        out.append(DAYFILE_PREFIX + str(self.end))
        out.append('#')
        for project, hours in self.hours.items():
            out.append(f' {hours.hour} {project}')
        print('\n'.join(out))

    def pprint(self, round_to: int = None) -> str:
        out = []
        pp_sum = timedelta_to_time(self.sum).strftime('%H:%M')
        out.append(f'{self.day} ({pp_sum}):')
        project_width = max(map(len, self.hours.keys()))
        for project, hours in self.hours.items():
            start = hours.start.time().strftime('%H:%M')
            end = hours.end.time().strftime('%H:%M')
            padding = project_width - len(project)
            project = project + ' ' * padding
            hours_string = timedelta_to_time(hours.hours).strftime('%H:%M')
            out.append(f'  {project} {start} – {end} {hours_string}')
        print('\n'.join(out))

    def __str__(self):
        return f'{self.day}: {self.start} - {self.end} ({self.sum})'


def main():
    import argparse

    def sorttype(string):
        try:
            return SortHoursBy[string.upper()]
        except KeyError:
            raise argparse.ArgumentError()

    def timetype(string):
        timeobj = type=time.fromisoformat(string)
        return timedelta(hours=timeobj.hour, seconds=timeobj.second)

    parser = argparse.ArgumentParser(
        description='Convert and pretty-print titrax worksheets'
    )
    dateparser = parser.add_mutually_exclusive_group(required=True)
    dateparser.add_argument('days', type=str, nargs='*', default=[],
                            help='One or more days, in iso8601')
    dateparser.add_argument('-w', '--isoweek', type=int,
                            help='ISO week number in the current year')
    parser.add_argument('--start', type=timetype,
                        help='When the day starts, in 24h format')
    parser.add_argument('-r', '--round', type=int, choices=ROUNDING_INTERVALS)
    parser.add_argument('-s', '--sort', dest='sortkey', type=sorttype,
                        default=None, choices=list(SortHoursBy))
    parser.add_argument('--project', dest='sortkey', action='store_const',
                        const=SortHoursBy.PROJECT)
    parser.add_argument('--min', dest='sortkey', action='store_const',
                        const=SortHoursBy.MIN)
    parser.add_argument('--max', dest='sortkey', action='store_const',
                        const=SortHoursBy.MAX)

    args = parser.parse_args()

    if args.isoweek:
        days = isoweeknumber_to_days(args.isoweek)
    else:
        days = args.days

    for day in days:
        print()
        try:
            w = Worksheet.from_titrax_day(day)
        except ValueError as e:
            print(day, ':', e)
            continue
        if args.round:
            w = w.round(args.round)
        if args.start:
            w = w.reset_starttime(args.start)
        if args.sortkey:
            w = w.sort(args.sortkey)
        w.pprint()
    print()


if __name__ == '__main__':
    main()
