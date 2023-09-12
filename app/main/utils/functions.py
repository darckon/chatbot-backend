from flask import current_app as app
import requests
import datetime

from sqlalchemy import true


def get_currency_money(money):

    response = requests.get(
                f"{app.config['CURRENCY_MONEY']}/{money}",
                headers={"content-type": "application/json"}
            )
    value = response.json()
    return value['serie'][0]['valor']


def is_actual_week(search_date):
    actual_date = datetime.date.today()
    actual_year, actual_week_num, actual_day_of_week = actual_date.isocalendar()  # noqa

    year, week_num, day_of_week = search_date.isocalendar()
    if actual_week_num == week_num:
        return True
    else:
        return False
