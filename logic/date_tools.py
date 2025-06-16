from datetime import datetime, date, timedelta

# megakapja: start_date, duration, weekend_meal_enabled az adatbazisbol
# visszaadja az end_date-t stringkent pl: -> "2025-06-10"
def calc_end_date(start_date, duration, weekend_meal_enabled):

    start_date = datetime.strptime(start_date,"%Y-%m-%d")
    meals_counted = 0
    current_date = start_date

    while meals_counted < int(duration):
        weekday = current_date.weekday()

        if weekday in [6, 0, 1, 2]:
            meals_counted += 1
        elif weekday == 3:
            if weekend_meal_enabled:
                meals_counted += 2
            else:
                meals_counted += 1

        current_date += timedelta(days=1)

    return (current_date - timedelta(days=1)).strftime("%Y-%m-%d")

# megkapja: start_date, end_date, weekend_meal_enabled
# visszaadja egy dictionary-ket tartalmazo listat az osszes datummal a kezdo es vege datum kozott
# PL: [{'date': '2025-06-15', 'type': 'normal'}, {'date': '2025-06-16', 'type': 'normal'}]
def generate_meal_days(start_date, end_date, weekend_meal_enabled):

    current = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    meal_days = []

    while current <= end:
        weekday = current.weekday()
        date_str = current.strftime("%Y-%m-%d")

        if weekday in [6, 0, 1, 2]:
            meal_days.append({"date": date_str, "type": "normal"})
        elif weekday == 3:
            meal_days.append({"date": date_str, "type": "normal"})
            if weekend_meal_enabled:
                meal_days.append({"date": date_str, "type": "weekend"})
        current += timedelta(days=1)

    return meal_days


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


print(generate_meal_days("2025-06-15", "2025-06-29", 1))