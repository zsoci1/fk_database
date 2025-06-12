from datetime import datetime, date, timedelta

# kiszamolja az elofizetes lejarati datumat a start_date
# es a duration alapjan, csak a munkanapokat (vas-csut) szamolja
def calc_end_date(start_date, duration):

    start_date = datetime.strptime(start_date,"%Y-%m-%d")
    working_days = 0
    current_date = start_date

    while working_days < duration:
        if current_date.weekday() in [6, 0, 1, 2, 3]: # vasarnap - csut
            working_days += 1
        current_date += timedelta(days=1)

    return (current_date - timedelta(days=1)).strftime("%Y-%m-%d")


# visszaadja az osszes munkanapot (vas-csut) egy listaban az elofiztes kezdete es vege kozott
def generate_working_day(start_date, end_date):

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    current_date = start_date
    dates = []

    while current_date <= end_date:
        if current_date.weekday() in [6, 0, 1, 2, 3]:
            dates.append(current_date.strftime("%Y-%m-%d"))
        current_date += timedelta(days=1)

    return dates


# visszaadja az aktualis munkahet 5 napjat datummal
def get_current_work_week(today=None):
    if today is None:
        today = date.today()
    
    shifted_weekday = (today.weekday() + 1) % 7

    start_of_week = today - timedelta(days=shifted_weekday)

    work_week = [start_of_week + timedelta(days=i) for i in range(5)]

    return work_week


# visszadadja az aktualis munkahet elso es utolso napjat (start_date_srt, end_date_str)
# vas csut
def get_current_week_range():

    today = datetime.today()
    weekday = today.weekday()

    if weekday in [4, 5]:
        days_until_sunday = (6 - weekday + 7) % 7 or 7
        sunday = today + timedelta(days=days_until_sunday)
    else:
        days_since_sunday = (weekday - 6) % 7
        sunday = today - timedelta(days=days_since_sunday)
    
    thursday = sunday + timedelta(days=4)
    start_str = sunday.strftime("%Y.%m.%d") # vasarnap EV.HONAP.NAP
    end_srt = thursday.strftime("%m.%d") # csutortok HONAP.NAP

    return (start_str, end_srt)

