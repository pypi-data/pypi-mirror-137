import json
import time
from flask import request
from .loggers.logger import Logger

logger = Logger('microgue')


class Timer:
    class __Singleton:
        last_timer_name = 'default'
        timers = {}

        def get(self, timer_name):
            return self.timers.get(timer_name, None)

        def set(self, timer_name, timer_time):
            self.last_timer_name = timer_name
            self.timers[timer_name] = timer_time

    instance = None

    @staticmethod
    def singleton():
        if not Timer.instance:
            Timer.instance = Timer.__Singleton()

    @staticmethod
    def set(timer_name='default'):
        Timer.singleton()
        Timer.instance.set(timer_name, time.time())

    @staticmethod
    def check(timer_name=None, timer_limit=0):
        Timer.singleton()
        timer_name = timer_name if timer_name else Timer.instance.last_timer_name

        try:
            timer_duration = time.time() - Timer.instance.get(timer_name)
        except TypeError:
            logger.debug(f'Timer | {timer_name} | Not Set', priority=2)
            return

        if timer_duration > timer_limit:
            logger.debug(f'Timer | {timer_name} | duration: {timer_duration}', priority=2)


def get_request_method():
    return request.method


def get_request_headers(key=None, default=''):
    if key:
        if request.headers:
            return request.headers.get(key, default)
        else:
            return default
    else:
        if request.headers:
            return dict(request.headers)
        else:
            if default != '':
                return default
            else:
                return {}


def get_request_data(key=None, default=''):
    if key:
        if request.data:
            return json.loads(request.data).get(key, default)
        else:
            return default
    else:
        if request.data:
            return json.loads(request.data)
        else:
            if default != '':
                return default
            else:
                return {}


def get_request_form(key=None, default=[]):
    if key:
        if request.form:
            return request.form.getlist(key)
        else:
            return default
    else:
        if request.form:
            form = {}
            keys = request.form.keys()
            for key in keys:
                form[key] = request.form.getlist(key)
            return form
        else:
            if default != []:
                return default
            else:
                return {}


def get_request_files(key=None, default=''):
    if key:
        if request.files:
            return request.files.get(key, default)
        else:
            return default
    else:
        if request.files:
            return dict(request.files)
        else:
            if default != '':
                return default
            else:
                return {}


def get_request_args(key=None, default=''):
    if key:
        if request.args:
            return request.args.get(key, default)
        else:
            return default
    else:
        if request.args:
            return dict(request.args)
        else:
            if default != '':
                return default
            else:
                return {}


def get_request_url():
    return request.url


def mask_fields_in_data(data, fields, mask='*****'):
    data = data.copy()
    for field in fields:
        if field in data:
            data[field] = mask
    return data
