import datetime

def last_day_of_month(date):
    # Guaranteed to get the next month. Force any_date to 28th and then add 4 days.
    next_month = date.replace(day=28) + datetime.timedelta(days=4)
    
    # Subtract all days that are over since the start of the month.
    day = next_month - datetime.timedelta(days=next_month.day)
    return day