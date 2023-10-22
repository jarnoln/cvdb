import datetime


def calculate_duration(start_date, end_date=None):
    """ Calculate how many years and months have passed between start and end dates """
    # If end date not defined, use current date
    if not end_date:
        end_date = datetime.date.today()
    years = end_date.year - start_date.year
    months = end_date.month - start_date.month
    if months < 0:
        years = years - 1
        months = months + 12
    return years, months


def duration_as_string(years, months):
    """ Return duration as printable string """
    duration_y = ''
    duration_m = ''
    if years > 1:
        duration_y = '{} years'.format(years)
    elif years == 1:
        duration_y = '1 year'
    if months > 1:
        duration_m = '{} months'.format(months)
    elif months == 1:
        duration_m = '1 month'
    elif years == 0 and months == 0:
        duration_m = 'less than a month'
    if duration_y and duration_m:
        return '{}, {}'.format(duration_y, duration_m)

    return duration_y + duration_m
