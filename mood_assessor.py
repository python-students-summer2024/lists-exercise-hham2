import datetime
from pathlib import Path

def assess_mood():
    """
    calls other functions which attempt to diagnose
    any mood disorders detected over a 7-day period
    """
    mood = input_mood()
    write_to_file(mood)
    diagnose_disorders()

def write_to_file(info):
    """
    @param Info what you want to append to the file
    """
    filepath = Path(r"data\mood_diary.txt")
    file = open(filepath, encoding = "utf-8", mode = "a")
    if responded_today() is False:
        file.write(f"{info} {date()}\n")
    else:
        print("Sorry, you have already entered your mood today.")
    file.close()

def input_mood():
    """
    Allows the user to enter their current mood, which is stored as an integer
    corresponding to the mood entered
    @return Returns either an integer corresponding to one's mood (2 = happy, 1 = relaxed, 0 = apathetic, -1 = sad, -2 = angry) 
    or None if one has already entered their mood today.
    """
    if responded_today() is False:
        response_needed = True
        while response_needed:
            response = input("Enter your current mood: ").strip().lower()
            mood_options = ["happy","relaxed","apathetic","sad","angry"]
            if response not in mood_options:
                print("Please enter a different mood.")
            else:
                response_needed = False
        for index, mood in enumerate(mood_options):
                mood_integer = 2 - index
                if mood == response:
                    break
        return mood_integer
    else:
         print("Sorry, you have already entered your mood today.")
         return False

def date():
    """
    Gets today's date.
    """
    date_today = datetime.date.today()
    return str(date_today)

def responded_today():
    """
    @return Returns boolean True if the user has already input a mood today, and boolean False if not.
    """
    lines = read_lines()
    new_lines = []
    for i in lines:
          i = i[2:12].strip()
          new_lines.append(i)
    return date() in new_lines #returns either True or False depending on whether or not the statement is true

def read_lines():
    """
    @return Returns a list, where each element corresponds to a line in the file being read
    """
    filepath = Path(r"data\mood_diary.txt")
    file = open(filepath, encoding = "utf-8", mode = "r")
    lines = file.readlines()[:-8:-1] #without the [:-8:-1] here specifically, the program sometimes won't take mood integers from only the last seven days; haven't figured out why
    return lines


def diagnose_disorders():
    """
    Diagnoses mood disorders based on moods input over the past seven days. If there are less than
    seven data points from the past seven days, the function ceases to run.
    """
    if len(read_lines()) < 7:
        return None
    lines = read_lines()
    new_lines = []
    for i in lines:
        i = i[0:2]
        new_lines.append(i[0:2])
        new_lines = new_lines[:-8:-1]
    formatted_lines = []
    for i in new_lines:
        i = str(i).strip()
        formatted_lines.append(i)
    average_mood = find_average_mood(formatted_lines)
    mood_integer_list = first_column_mood_diary()
    if mood_integer_list.count("2") >= 5:
        diagnosis = "manic"
    elif mood_integer_list.count("-1") >= 4:
        diagnosis = "depressive"
    elif mood_integer_list.count("0") >= 6:
        diagnosis = "schizoid"
    else:
        diagnosis = average_mood
    print(f"Your diagnosis: {diagnosis}!")

def find_average_mood(new_lines):
    """
    Reads the mood_diary.txt file and finds the average mood over the past seven days
    """
    total = 0
    for i in new_lines:
        total += int(i)
    average = int(total / 7)
    mood_options = ["happy","relaxed","apathetic","sad","angry"]
    formatted_mood_options = []
    for index, mood in enumerate(mood_options):
        mood_integer = 2 - index
        formatted_mood_options.append(mood_integer)
    average_mood_integer = formatted_mood_options.index(average)
    average_mood = mood_options[average_mood_integer]
    return average_mood

def first_column_mood_diary():
    """
    Returns the first column of the mood diary over the last seven days, which corresponds to the integer assigned to a mood
    """
    lines = read_lines()
    unformatted_first_column = []
    formatted_first_column = []
    for line in lines:
        unformatted_first_column.append(line[0:2])
        unformatted_first_column = unformatted_first_column[:-8:-1]
    for i in unformatted_first_column:
        i = str(i).strip()
        formatted_first_column.append(i)
    return formatted_first_column





    



