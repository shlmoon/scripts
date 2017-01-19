import re
import os

import codecs


def get_results():
    def _get_result(x):
        data = rex.search(x).groupdict()
        g = lambda x: x.decode('utf-8') if isinstance(x, str) else x
        return {g(k): g(v) for k, v in data.items()}

    current_file = os.getcwd()
    filepath = '%s/region.txt' % current_file
    reg = r'(?P<code>.*?): (?P<city>.*)'
    rex = re.compile(reg)
    with open(filepath) as fg:
        return [_get_result(x) for x in fg.readlines()]


try:
    result_list = get_results()
    fg = codecs.open('region.py', 'w', 'utf-8')
    fg.write('# coding: utf-8\n\n')
    fg.write('result_list = [\n')
    for x in result_list:
        sts = "    {u'%s': u'%s', u'%s': u'%s'},\n" % (
            u'code', x.get('code'), u'city', x.get('city')
        )
        print sts
        print type(sts)
        fg.write(sts)
    fg.write(']')

finally:
    fg.close()

    # fg.write('\nresult_list = {lst}'.format(lst=result_list))