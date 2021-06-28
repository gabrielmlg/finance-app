from datetime import date, timedelta, datetime
import pandas as pd

def last_day_of_month(date):
    # Guaranteed to get the next month. Force any_date to 28th and then add 4 days.
    next_month = date.replace(day=28) + timedelta(days=4)
    
    # Subtract all days that are over since the start of the month.
    day = next_month - timedelta(days=next_month.day)
    return day


def rangeDateList(start, end):
    dates = pd.date_range(start=date(2020, 1, 1), end=datetime.today())
    dates = dates.date
    return dates