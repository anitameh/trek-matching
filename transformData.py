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


def csv_to_dict(list_of_companies, student_choice_data):
    """
    :param list list_of_companies:
    :param student_choice_data:

    :rtype:
    :return:
    """
    student_info_dicts = {}

    # assign each company a number i.e. an id
    companies_dict = {company: number for number, company in enumerate(list_of_companies)}
    companies_dict_reverse = {number: company for number, company in enumerate(list_of_companies)}

    for index, row in enumerate(student_choice_data):
        first_name, last_name, choice1, choice2, choice3, choice4 = row
        full_name = last_name + ', ' + first_name
        choices = [choice1, choice2, choice3, choice4]
        student_info_dicts[index] = {'choices': [companies_dict[each_choice] for each_choice in choices],
                                     'choices_full_names': choices,
                                     'name': full_name,
                                     'assignments': []}

    return student_info_dicts, companies_dict, companies_dict_reverse
