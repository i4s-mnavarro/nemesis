# -*- coding: utf-8 -*-

import pytz
import logging
import argparse
import datetime

from mongoengine import connect

from nemesis.common.config import options


def load_options():

    parser = argparse.ArgumentParser(description='VATS Scripting executor and parser')
    parser.add_argument('--conf', action='store', required=True, help='path to config file')
    args = parser.parse_args()

    options.load(args.conf)


def set_logger():
    log_file = options.nemesis_log_file
    fmt = '[%(asctime)s] nemesis %(name)s (%(levelname)s): %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(filename=log_file, format=fmt, datefmt=date_format, level=logging.DEBUG)


def mongo_connect():
    connect(
        db=options.mongodb_db,
        username=options.mongodb_username,
        password=options.mongodb_password,
        host=options.mongodb_host,
        port=int(options.mongodb_port),
        authentication_source=options.mongodb_auth_database
    )


def get_utc_from_str(dt_str):
    dt = datetime.datetime.strptime(dt_str, '%d-%m-%Y')
    current_tz = pytz.timezone(options.nemesis_timezone)
    return current_tz.localize(dt)


def get_all_dates(start_date, end_date):
    delta_date = end_date - start_date
    labels = []
    for i in range(delta_date.days + 1):
        labels.append(start_date + datetime.timedelta(days=i))
    return labels


def get_labels(all_dates, timezone=options.nemesis_timezone):
    current_tz = pytz.timezone(timezone)
    labels = []
    for day in all_dates:
        label = day.replace(tzinfo=pytz.utc).astimezone(current_tz)
        labels.append('{datetime:%d-%m-%Y}'.format(datetime=label))
    return labels
