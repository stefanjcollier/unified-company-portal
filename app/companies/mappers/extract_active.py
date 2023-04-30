from datetime import date


def extract_active(start_date: date, end_date: date):
    if start_date is None and end_date is None:
        return None
    elif start_date is None:
        return end_date > date.today()
    elif end_date is None:
        return start_date < date.today()
    else:
        return start_date < date.today() < end_date
