import pronotepy
import requests
from getpass import getpass
import sys
from time import sleep
from datetime import datetime

PRONOTEPY_USERNAME = getpass("Ponote Username: ")
PRONOTEPY_PASSWORD = getpass("Pronote Password: ")
TELEGRAM_BOT_TOKEN = getpass("Telegram Bot Token: ")
TELEGRAM_CHAT_ID = getpass("Telegram Chat ID: ")

last_grade_subject_name = None
last_grade_date = None
last_grade_average = None
DEFAULT_SLEEP_TIME = 3600

def say(type, message):
    current_date = datetime.now().strftime('%H:%M:%S %d/%m/%y')

    if type == "error":
        print(f"[{current_date}] Error: {message}", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"[{current_date}] {message}")

def connect_pronotepy_client():
    client = pronotepy.Client(
        'https://0560026z.index-education.net/pronote/eleve.html', # change this
        username=PRONOTEPY_USERNAME,
        password=PRONOTEPY_PASSWORD
    )

    if not client.logged_in:
        say("error", "Failed to connect to Pronote")

    return client

def get_last_grade(client):
    try:
        last_grade = client.current_period.grades[len(client.current_period.grades) - 1]
    except IndexError:
        return None
    except Exception as e:
        say("error", f"Failed to get grades: {e}")

    return last_grade

def is_new_grade(grade):
    global last_grade_subject_name
    global last_grade_date
    global last_grade_average

    if grade.subject.name != last_grade_subject_name and grade.date != last_grade_date and grade.average != last_grade_average: # i know it's shit but `grade.id` is reseted after `session_check()`
        last_grade_subject_name = grade.subject.name
        last_grade_date = grade.date
        last_grade_average = grade.average

        return True
    
    return False

def get_subject_emoji(subject_name):
    match subject_name:
        case "MATHEMATIQUES":
            return "📐"
        case "FRANCAIS":
            return "📖"
        case "NUMERIQUE SC.INFORM.":
            return "💻"
        case "SCIENCES INGENIEUR":
            return "🔧"
        case "ANGLAIS LV1":
            return "🇬🇧"
        case "ESPAGNOL LV2":
            return "🇪🇸"
        case "HISTOIRE-GÉOGRAPHIE":
            return "🌍"
        case "EDUCATION MORALE & CIVIQUE":
            return "🧑‍⚖️"
        case "ENSEIGN.SCIENTIFIQUE":
            return "🔬"
        case "ED.PHYSIQUE & SPORT.":
            return "⚽"
        case _:
            return "❓"

def format_message(grade):
    grade_emoji = get_subject_emoji(grade.subject.name)

    if grade.is_bonus:
        grade_count_text = " (bonus)"
    elif grade.is_optionnal:
        grade_count_text = " (optionnel)"
    else:
        grade_count_text = ""

    if grade.grade == "Abs":
        grade_value = "Absence"
    else:
        grade_value = grade.grade + "/" + grade.out_of + grade_count_text

    return f"{grade_emoji} <u><b>Nouvelle note: {grade.comment}</b></u>\n\
Date: <b>{grade.date.strftime('%d/%m/%y')}</b>\n\
Note: <b>{grade_value}</b>\n\
Moyenne de classe: <b>{grade.average}</b>\n\
Coefficient: <b>{grade.coefficient}</b>\n\
Matière: <b>{grade.subject.name.title()}</b>"

def send_message(message):
    data = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }

    r = requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", data=data)
    
    if r.status_code != 200:
        say("error", f"Failed to send message: {r.status_code} {r.json()['description']}")

if __name__ == "__main__":
    client = connect_pronotepy_client()
    say("info", "Launched!")

    while True:
        if client.session_check():
            say("info", "Session reloaded")

        current_grade = get_last_grade(client)
        if current_grade is None:
            sleep(DEFAULT_SLEEP_TIME)
            continue

        if is_new_grade(current_grade):
            message = format_message(current_grade)
            send_message(message)

        sleep(DEFAULT_SLEEP_TIME)

