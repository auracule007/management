import datetime


def get_days_in_month(month, year):
    if month in (4, 6, 9, 11):
        return 30
    elif month == 2:
        if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
            return 29
        else:
            return 28
    else:
        return 31

def calculate_expiration_date(start_date, interval):
  
    if interval == 'Weekly':
        return start_date + datetime.timedelta(days=7)
    elif interval == 'Monthly':
        year = start_date.year
        month = start_date.month
        days_in_month = get_days_in_month(month, year)
        next_month = (month % 12) + 1
        next_year = year if next_month <= 12 else year + 1
        next_month_days = get_days_in_month(next_month, next_year)
        if start_date.day <= min(days_in_month, next_month_days):
            return start_date + datetime.timedelta(days=max(days_in_month - start_date.day, 0) + next_month_days)
        else:
            return start_date.replace(day=min(days_in_month, next_month_days)) + datetime.timedelta(days=max(days_in_month - start_date.day, 0))
    elif interval == 'Yearly':
        return start_date + datetime.timedelta(days=365)
    else:
        raise ValueError("Invalid  interval:", interval)
    
    