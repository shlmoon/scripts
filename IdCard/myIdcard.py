# coding: utf-8

from functools import reduce
import re
import os
import datetime
import inspect


def get_results():
    current_file = os.getcwd()
    filepath = '%s/region.txt' % current_file
    reg = r'(?P<code>.*?): (?P<city>.*)'
    rex = re.compile(reg)
    with open(filepath) as fg:
        return [rex.search(x).groupdict() for x in fg.readlines()]


result_list = get_results()


class IdCardCheck(object):

    def __init__(self, idCard='', ignore_region=False):
        self.result = None
        self.region = ''
        self.ignore_region = ignore_region
        self.IdCard = idCard

    @property
    def IdCard(self):
        return self._IdCard

    @IdCard.setter
    def IdCard(self, id_card):
        self.validate(id_card)
        self._IdCard = id_card

    def validate(self, id_card):
        self.validate_idcard(id_card)
        method_lists = inspect.getmembers(self, predicate=inspect.ismethod)
        for k, method in method_lists:
            if k.startswith('validate_') and not k == 'validate_idcard':
                method(id_card)

    def validate_idcard(self, id_card):
        reg = r'(?P<region>\d{6})(?P<date>\d{8})\d{2}(?P<sex>\d)(?P<checkcode>\w)$'
        rex = re.compile(reg)
        data = rex.search(id_card)
        if data is None:
            raise ValueError('IdCard is invalid')
        self.result = data.groupdict()

    def _valid_checkcode(self, id_card):
        CountValue = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        checkvals = reduce(
            lambda x, y: x + y,
            map(
                lambda x, y: x * y,
                [int(x) for x in id_card],
                CountValue
            )
        )
        checkvals = checkvals % 11
        count_rule = {
            '0': '1',
            '1': '0',
            '2': 'X',
            '3': '9',
            '4': '8',
            '5': '7',
            '6': '6',
            '7': '5',
            '8': '4',
            '9': '3',
            '10': '2'
        }
        return count_rule.get(str(checkvals))

    def validate_checkcode(self, id_card):
        validate_code = self._valid_checkcode(id_card[:-1])
        if not validate_code == id_card[-1]:
            raise ValueError(
                'IdCard {idn} checkcode Error.IdCard maybe {_idn}'.format(
                    idn=id_card,
                    _idn=id_card[:-1] + validate_code
                )
            )

    def _get_region(self):
        assert self.ignore_region is False
        region_num = self.result.get('region')
        self.region = filter(
            lambda x: x.get('code') == region_num, result_list
        )
        return self.region

    def validate_region(self, id_card):
        try:
            data = self._get_region()
            if not data:
                raise ValueError(
                    'IdCard {idn} region Error.'.format(idn=id_card)
                )
        except AssertionError:
            return

    def validate_date(self, id_card):
        date = datetime.datetime.strptime(self.result.get('date'), '%Y%m%d')
        today = datetime.datetime.today()
        min_date = today - datetime.timedelta(days=100 * 365)
        if date < min_date or date > today:
            raise ValueError(
                'IdCard {idn} birthday Error.'.format(idn=id_card)
            )

    def get_regioninfo(self):
        try:
            data = self._get_region()
            return data[0].get('city')
        except AssertionError:
            raise ValueError('if you want  to get region info.you must set param ignore_region is False')

    def get_birthdayinfo(self):
        birthday = self.result.get('date')
        reg = r'(?P<year>\d{4})(?P<mouth>\d{2})(?P<day>\d{2})$'
        rex = re.compile(reg)
        return rex.search(birthday).groupdict()

    def get_sexinfo(self):
        sex = self.result.get('sex')
        valus = int(sex) % 2
        if valus == 1:
            return 'Female'
        return 'Male'
