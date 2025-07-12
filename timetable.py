from datetime import datetime, timedelta
from ics import Calendar, Event

# Create a weekday timetable
timetable = [
    ("07:00", "07:30", "Wake up & freshen up"),
    ("07:30", "08:00", "Breakfast"),
    ("08:00", "18:00", "Institute"),
    ("18:00", "18:30", "Light snack / Relax"),
    ("18:30", "19:30", "Gym"),
    ("19:30", "20:00", "Dinner"),
    ("20:00", "21:00", "Study (focused subject)"),
    ("21:00", "22:00", "Coding"),
    ("22:00", "23:00", "Study (revision/practice)"),
    ("23:00", "23:30", "Chill / Free time"),
    ("23:30", "00:00", "Wind down / Prepare for bed"),
]

# Generate a calendar for a sample weekday (e.g., starting from next Monday)
start_date = datetime.now()
# Shift to next Monday
days_ahead = 0 - start_date.weekday() + 7 if start_date.weekday() > 0 else 0
monday = start_date + timedelta(days=days_ahead)
calendar = Calendar()

for day_offset in range(5):  # Monday to Friday
    current_day = monday + timedelta(days=day_offset)
    for start, end, activity in timetable:
        start_time = datetime.strptime(start, "%H:%M").time()
        end_time = datetime.strptime(end, "%H:%M").time()
        event = Event()
        event.name = activity
        event.begin = datetime.combine(current_day.date(), start_time)
        # Handle wrap-around past midnight
        if end_time < start_time:
            event.end = datetime.combine((current_day + timedelta(days=1)).date(), end_time)
        else:
            event.end = datetime.combine(current_day.date(), end_time)
        calendar.events.add(event)

# Save calendar to .ics file and also prepare a printable version
calendar_path = "/mnt/data/Weekday_Timetable.ics"
with open(calendar_path, "w") as f:
    f.writelines(calendar.serialize())

# Generate printable version
printable_text = "WEEKDAY TIMETABLE (Monday to Friday)\n\n"
printable_text += "{:<12} {:<12} {}\n".format("Start", "End", "Activity")
printable_text += "-"*40 + "\n"
for start, end, activity in timetable:
    printable_text += "{:<12} {:<12} {}\n".format(start, end, activity)

printable_path = "/mnt/data/Weekday_Timetable_Printable.txt"
with open(printable_path, "w") as f:
    f.write(printable_text)

calendar_path, printable_path
