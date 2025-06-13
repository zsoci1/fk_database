from datetime import datetime, date, timedelta

# megakapja: start_date, duration az adatbazisbol
# visszaadja az end_date-t stringkent pl: -> "2025-06-10"
def calc_end_date(start_date, duration):

    start_date = datetime.strptime(start_date,"%Y-%m-%d")
    working_days = 0
    current_date = start_date

    while working_days < int(duration):
        if current_date.weekday() in [6, 0, 1, 2, 3]: # vasarnap - csut
            working_days += 1
        current_date += timedelta(days=1)

    return (current_date - timedelta(days=1)).strftime("%Y-%m-%d")

# megkapja: start_date, end_date
# visszaadja egy listat az osszes munkanappal (vas-csut) az elofiztes kezdete es vege kozott
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


# visszaadja egy listat az aktualis munkahet 5 napjaval pl: datetime.date(2025, 6, 8), ...
def get_current_work_week(today=None):
    if today is None:
        today = date.today()
    
    shifted_weekday = (today.weekday() + 1) % 7

    start_of_week = today - timedelta(days=shifted_weekday)

    work_week = [start_of_week + timedelta(days=i) for i in range(5)]

    return work_week

# visszaad egy listat ket string-el: az aktualis munkahet elso es utolso napja
# ilyen formaban ('2025-06-15', '2025-06-19')
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
    start_str = sunday.strftime("%Y-%m-%d") # vasarnap 
    end_srt = thursday.strftime("%Y-%m-%d")  # csutortok

    return (start_str, end_srt)


