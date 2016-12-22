#!/usr/bin/env python
# encoding: utf-8


import xlwt
import MySQLdb

class MysqlExport(object):
    def __init__(self):
        self.wbk = xlwt.Workbook()
        self.sheet = self.wbk.add_sheet('sheet 1')
        self.__table = ''
        self.__fields = []

    @property
    def table(self):
        return self.__table

    @table.setter
    def table(self, table):
        self.__table = table

    @property
    def fields(self):
        return self.__fields

    @fields.setter
    def fields(self, fields):
        if not isinstance(fields, list):
            raise TypeError('fields is not a list')
        self.__fields = fields

   def export_heads(self):
        for index, head in enumerate(self.fields):
            self.sheet.write(0, index, head)

    def execute_hql(self, hql):
        try:
            conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='', db='mydb1', charset='utf8')
            cursor = conn.cursor()
            cursor.execute(hql)

            row = 0
            for self.fields in cursor.fetchall():
                for index, field in enumerate(self.fields):
                    self.sheet.write(row, index, field.decode('utf8'))
                row += 1
        finally:
            self.wbk.save(u'examples.xls')
            cursor.close()
            conn.close()

    def export_data(self):
        try:
            hql = 'select %s from %s' % (','.join(self.fields), self.table)
            self.execute_hql(hql)
        except Exception, e:
            print e
            raise e
