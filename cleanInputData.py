import csv


def read_in_csv_to_list(filename, headers=False):
    """
    :param Str filename: path to file
    :param bool headers: True if first row contains headers

    :rtype: list
    :return: [row1, row2, etc]
    """
    start_row = 0
    if headers:
        start_row = 1

    with open(filename, 'r') as inputfile:
        data = [row for row in csv.reader(inputfile.read().splitlines())]
        return data[start_row:]


def write_list_to_csv(filename, data, headers=False):
    """
    :param Str filename: path to file
    :param list data: a list of lists to write to a .csv file
    :param bool headers: True if first row of csv should contain headers

    :rtype: csv
    :return: csv
    """
    with open(filename, 'wb') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        if headers:
            csv_writer.writerow(headers)
        for row in data:
            csv_writer.writerow(row)
