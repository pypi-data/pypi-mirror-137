# Copyright 2004-2022 Bright Computing Holding BV
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

import csv
import yaml
from datetime import datetime
from functools import total_ordering

import prettytable
from six import StringIO
from six.moves import zip

from .datetimefunctions import format_datetime, get_datetime_ago


@total_ordering
class NoneWrapper:
    """
    Object of any data type can be compared to the instance of this class.
    No error is raised with any comparison operators.
    Needed to convert None into its instance to sort table with unexpected, mixed data types.
    """
    def __init__(self):
        pass

    def __eq__(self, other):
        if isinstance(other, NoneWrapper):
            return True
        else:
            return False

    def __gt__(self, other):
        if isinstance(other, NoneWrapper):
            return False
        else:
            return True

    def __str__(self):
        return "?"

    def __repr__(self):
        return "?"


@total_ordering
class SSHAlias:
    """
    Small helper class for our SSH alias column.

    We sort the SSH aliases based on the index of the alias, not on the prefix. E.g. os1 and os2
    are sorted as 1 and 2. For some clusters there won't be an SSH alias, for example while the
    cluster is being created (there are other cases as well). We want to display those as "?",
    but we also need to be able to sort on the column. So for sorting we treat "?" as 0.
    """
    def __init__(self, alias, prefix=""):
        self._alias = alias

        if isinstance(alias, str):
            self._index = alias.replace(prefix, "")
        elif isinstance(alias, int):
            self._index = alias
        else:
            raise TypeError(f"alias of type {type(alias)} not supported")

    @staticmethod
    def _index_to_int(index):
        try:
            return int(index)
        except ValueError:
            return 0

    def __eq__(self, other):
        return self._index_to_int(self._index) == self._index_to_int(other._index)

    def __gt__(self, other):
        return self._index_to_int(self._index) > self._index_to_int(other._index)

    def __str__(self):
        return str(self._alias)

    def __repr__(self):
        return str(self._alias)


class SortableData(object):
    """
    Utility class for dealing with sortable data.

    :param all_headers: Headers of all columns in following format
        [
            (column_id, column_name),
            ....
        ]
    :param requested_headers: a list of ids of the columns to be displayed.
        If empty. All columns are displayed.
    :param rows: Rows of data
    """

    def __init__(self, all_headers, requested_headers, rows):
        self.all_headers = all_headers
        self.requested_headers = [
            col_data for col_data in self.all_headers
            if not requested_headers or col_data[0] in requested_headers
        ]
        self.rows = rows

    def sort(self, *sorting_columns):
        columns = [header[0] for header in self.all_headers]
        filtered_sorting_columns = [s for s in sorting_columns if s in columns]

        # pick first one by default
        if not filtered_sorting_columns:
            filtered_sorting_columns = [columns[0]]

        column_ids = [elt[0] for elt in self.all_headers]

        self.column_indices = [
            column_ids.index(sorting_column) for sorting_column in filtered_sorting_columns
        ]

        self.rows = [[NoneWrapper() if col is None else col for col in row] for row in self.rows]

        self.sorted_rows = sorted(
            self.rows, key=lambda x: [
                x[column_index] for column_index in self.column_indices
            ]
        )

        self.filter(self.sorted_rows)
        self.sorted_rows = self._format_datetime(self.sorted_rows)

    def filter(self, all_rows):
        requested_indices = []
        filtered_rows = []
        filtered_columns = []

        for column_data in self.all_headers:
            if column_data in self.requested_headers and column_data not in filtered_columns:
                filtered_columns.append(column_data)
                requested_indices += [self.all_headers.index(column_data)]

        for row in all_rows:
            filtered_rows.append([row[x] for x in requested_indices])

        self.filtered_columns_data, self.sorted_rows = filtered_columns, filtered_rows

    def output(self, output_format):
        if output_format == "table":
            return self.make_pretty_table(self.filtered_columns_data, self.sorted_rows)
        elif output_format == "csv":
            return self.make_csv_table(self.filtered_columns_data, self.sorted_rows)
        elif output_format == "value":
            return self.make_value_output(self.filtered_columns_data, self.sorted_rows)
        elif output_format == "yaml":
            return self.make_yaml_output(self.filtered_columns_data, self.sorted_rows)
        assert False, "output_format was of unrecognized format: %s" % (output_format)

    @staticmethod
    def make_pretty_table(columns, data):
        columns_names = [column[1] for column in columns]
        table = prettytable.PrettyTable(columns_names)
        table.align = "l"
        for row in data:
            table.add_row(row)
        return table

    @staticmethod
    def make_csv_table(columns, data):
        columns_names = [column[1] for column in columns]
        csv_output = StringIO()
        csv_writer = csv.writer(csv_output)
        csv_writer.writerow(columns_names)
        csv_writer.writerows(data)

        return csv_output.getvalue()

    @staticmethod
    def make_value_output(columns, data):
        def escape(cell):
            cell = str(cell)
            if " " in cell:
                cell = '"' + cell.replace('"', '\\"') + '"'
            elif cell == "":
                cell = '""'
            return cell

        def make_line(row):
            return " ".join([escape(cell) for cell in row])

        lines = [make_line(row) for row in data]
        return "\n".join(lines)

    @staticmethod
    def make_yaml_output(columns, data):
        results = []

        for row in data:
            results.append({col[0]: str(cell) for col, cell in zip(columns, row)})

        output = {"results": results}
        return yaml.safe_dump(output, default_flow_style=False)

    @staticmethod
    def _format_datetime(rows):
        for i, row in enumerate(rows):
            for j, cell in enumerate(row):
                if isinstance(cell, datetime):
                    rows[i][j] = "{created} ({ago})".format(
                        created=format_datetime(rows[i][j]),
                        ago=get_datetime_ago(rows[i][j])
                    )
        return rows
