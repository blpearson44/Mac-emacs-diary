#!/usr/bin/env python3

import subprocess
import re
from datetime import date, timedelta
import pandas as pd

try:
    process = subprocess.run(
        [
            "/usr/local/bin/icalBuddy",
            "-sd",
            "-b",
            "CAL ",
            "-df",
            "%m/%d/%Y",
            "-tf",
            "%H:%M",
            "-nrd",
            "-nc",
            "eventsToday+60",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=True,
    )
except subprocess.CalledProcessError:
    print(
        "Error: icalBuddy failed to run. This is likely due to an issue with permissions on the application the script is being run from."
    )
    quit()


events_string = process.stdout.decode()
dates = re.split("\d\d/\d\d/\d\d\d\d", events_string)
dates.pop(0)
today = date.today()
with open("/Users/ben/Org/diary", "w") as diary:
    for i in range(len(dates)):
        day = today + timedelta(days=i)
        diary.write(day.strftime("%m/%d/%Y"))
        this_day = dates[i].split("CAL")
        for event in this_day:
            event = event.replace("\n", " ")
            event = event.replace(": ------------------------", "")
            time = re.search("\d\d:\d\d - \d\d:\d\d", event)
            try:
                time = time.group(0)
                event = event.replace(time, "")
                time = time.replace(" ", "")
                event = time + " " + event
            except TypeError:
                pass
            except AttributeError:
                pass
            diary.write("\t")
            diary.write(event.strip())
            diary.write("\n")
