# -*- coding: utf-8 -*-
from itertools import zip_longest
from datetime import datetime

# https://akiyoko.hatenablog.jp/entry/2014/06/21/095039
class SimpleTable(object):

    def __init__(self, header=None, rows=None):
        self.header = header or ()
        self.rows = rows or []

    def set_header(self, header):
        self.header = header

    def add_row(self, row):
        self.rows.append(row)

    def _calc_maxes(self):
        array = [self.header] + self.rows
        return [max(len(str(s)) for s in ss) for ss in zip_longest(*array, fillvalue='')]

    def _get_printable_row(self, row):
        maxes = self._calc_maxes()
        return '| ' + ' | '.join([('{0: <%d}' % m).format(r) for r, m in zip_longest(row, maxes, fillvalue='')]) + ' |'

    def _get_printable_header(self):
        return self._get_printable_row(self.header)

    def _get_printable_border(self):
        maxes = self._calc_maxes()
        return '+-' + '-+-'.join(['-' * m for m in maxes]) + '-+'

    def get_table(self):
        lines = []
        if self.header:
            lines.append(self._get_printable_border())
            lines.append(self._get_printable_header())
        lines.append(self._get_printable_border())
        for row in self.rows:
            lines.append(self._get_printable_row(row))
        lines.append(self._get_printable_border())
        return lines

    def print_table(self):
        lines = self.get_table()
        for line in lines:
            print(line)

def print_result(result):
    print("")
    print(str(result["job_id"]) + ".json")
    print(datetime.fromtimestamp(result["play_time"]))
    print("")
    table = SimpleTable()
    table.set_header(("", "WAVE 1", "WAVE 2", "WAVE 3"))
    while len(result["wave_details"]) < 3:
        result["wave_details"].append({
            "golden_ikura_pop_num": "-",
            "event_type": {
                "key": "-",
                "name": "-"
            },
            "ikura_num": "-",
            "golden_ikura_num": "-",
            "quota_num": "-",
            "water_level": {
                "name": "-",
                "key": "-"
            }
        })
    table.add_row((
        "Golden Egg",
        str(result["wave_details"][0]["golden_ikura_num"]) + "/" + str(result["wave_details"][0]["quota_num"]),
        str(result["wave_details"][1]["golden_ikura_num"]) + "/" + str(result["wave_details"][1]["quota_num"]),
        str(result["wave_details"][2]["golden_ikura_num"]) + "/" + str(result["wave_details"][2]["quota_num"])
    ))
    table.add_row((
        "Power Egg",
        str(result["wave_details"][0]["ikura_num"]),
        str(result["wave_details"][1]["ikura_num"]),
        str(result["wave_details"][2]["ikura_num"])
    ))
    table.add_row((
        "Water Level",
        str(result["wave_details"][0]["water_level"]["key"]),
        str(result["wave_details"][1]["water_level"]["key"]),
        str(result["wave_details"][2]["water_level"]["key"])
    ))
    table.add_row((
        "Event Type",
        str(result["wave_details"][0]["event_type"]["key"]) if result["wave_details"][0]["event_type"]["key"] != "water-levels" else "-",
        str(result["wave_details"][1]["event_type"]["key"]) if result["wave_details"][1]["event_type"]["key"] != "water-levels" else "-",
        str(result["wave_details"][2]["event_type"]["key"]) if result["wave_details"][2]["event_type"]["key"] != "water-levels" else "-"
    ))
    table.print_table()
    print("")