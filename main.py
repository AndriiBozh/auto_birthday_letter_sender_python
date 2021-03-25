
import random
import os
import pandas
import datetime as dt
import smtplib

MY_MAIL = "sender's email"
MY_PASSW = "sender's email password"

now = dt.datetime.now()
current_date = {'month': now.month, 'day': now.day}

#letter_templates is a folder which contains all letter templates. One of these letters is to be randomly chosen
random_letter = random.choice(os.listdir('./letter_templates'))

with open(f'./letter_templates/{random_letter}', 'r') as letter_file:
    letter_to_edit = letter_file.read()

data_birthdays = pandas.read_csv('birthdays.csv')

data_dict = data_birthdays.to_dict(orient='records')

for obj in data_dict:
    try:
        # we have to convert year, month and day values to int to compare them with data from 'current_date
        # values from data_dict are floats: 'year': 2021.0, 'month': 3.0, 'day': 25.0
        if {k: current_date[k] for k in current_date if k in obj and current_date[k] == int(obj[k])}:
            with open('happy_birthday.txt', 'w') as new_letter:
                new_letter.write(letter_to_edit.replace('[NAME]', obj['name']))
            with open('happy_birthday.txt', 'r') as letter:
                letter_to_send = letter.read()
            recipient_email = obj['email']

            with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
                # for security
                connection.starttls()
                connection.login(user=MY_MAIL, password=MY_PASSW)
                connection.sendmail(from_addr=MY_MAIL, to_addrs=f"{recipient_email}", msg=f'Subject: Happy B!\n\n{letter_to_send}')

    except ValueError:
        print('error: cannot convert float NaN to integer')


