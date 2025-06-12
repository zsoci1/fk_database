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


# visszaadja az osszes munkanapot (vas-csut) egy listaban a start es end date kozott
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


# meghatarozza az aktualis munkahetet

def get_current_work_week(today=None):
    if today is None:
        today = date.today()
    
    # weekday(): Monday=0, Sunday=6
    # Let's shift it so Sunday=0, Monday=1, ..., Saturday=6
    shifted_weekday = (today.weekday() + 1) % 7

    # Find the most recent Sunday (start of work week)
    start_of_week = today - timedelta(days=shifted_weekday)

    # Get Sunday to Thursday
    work_week = [start_of_week + timedelta(days=i) for i in range(5)]

    return work_week
