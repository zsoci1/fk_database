from datetime import datetime, timedelta

# fuggveny ami kiszamolja az elofizetes lejarati datumat a start_date
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
    