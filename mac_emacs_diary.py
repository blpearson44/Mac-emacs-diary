#!/usr/bin/env python3
"""Copy events from Mac calendar to Emacs Diary."""

import subprocess
import re
from datetime import date, timedelta

# Paths to diary and icalBuddy, change them if they differ
DIARY_PATH = "/Users/ben/Org/diary"
ICALBUDDY_PATH = "/usr/local/bin/icalBuddy"
NUM_DAYS = 60

if __name__ == "__main__":
    try:
        process = subprocess.run(
            [
                ICALBUDDY_PATH,
                "-sd",
                "-b",
                "CAL ",
                "-df",
                "%m/%d/%Y",
                "-tf",
                "%H:%M",
                "-nrd",
                "-nc",
                "eventsToday+" + str(NUM_DAYS),
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

    # and now for annoying regex
    events_string = process.stdout.decode()
    dates = re.findall("\d\d/\d\d/\d\d\d\d", events_string)
    events = re.split("\d\d/\d\d/\d\d\d\d", events_string)
    events.pop(0)
    today = date.today()
    with open(DIARY_PATH, "w") as diary:
        for i in range(len(events)):
            diary.write(dates[i])
            this_day = events[i].split("CAL")
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
