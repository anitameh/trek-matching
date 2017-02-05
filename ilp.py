import pulp
from transformData import read_in_csv_to_list, write_list_to_csv, csv_to_dict


student_choice_data = read_in_csv_to_list('/Users/anita/Downloads/student_choices.csv',
                                          headers=True)
COMPANIES_LIST = ['100ChartPicture', 'BubbleMania', 'Closeto20', 'Measuring', 'MysteryNumber',
                  'PicoPhonyZilch', 'PuzzleinaBag', 'RacetoaFlat', 'Salute', 'ShapeCodes',
                  'SteppingStones']
NUMBER_OF_COMPANIES = len(COMPANIES_LIST)
NUMBER_OF_PERIODS = 4  # there are four slots per day that students can attend
NUMBER_OF_STUDENTS = len(student_choice_data)
MIN_NUMBER_AT_COMPANY = 5  # this will be a list
MAX_NUMBER_AT_COMPANY = 9  # this will be a list


def main():
    # read in the data
    student_info_dicts, companies_dict, companies_dict_reverse = csv_to_dict(COMPANIES_LIST,
                                                                             student_choice_data)

    # define the problem type as an optimization problem to maximize the objective function
    prob = pulp.LpProblem('WesTrek', pulp.LpMaximize)

    # set up decision variables
    decision_var_matrix = []
    decision_vars_list = []

    for i in xrange(NUMBER_OF_STUDENTS):
        for j in xrange(NUMBER_OF_COMPANIES):
            decision_var_matrix.append((i,j))

    for each_period in range(NUMBER_OF_PERIODS):
        variable_type_name = 'period_%s_decision_variable' % (i+1)
        decision_vars_list.append(pulp.LpVariable.dicts(name=variable_type_name,
                                                        indexs=decision_var_matrix,
                                                        lowBound=0,
                                                        upBound=1,
                                                        cat=pulp.LpInteger))

    # set up constraints
    # Constraint 1: each student must be in one & only one company per pd
    for i in xrange(NUMBER_OF_STUDENTS):
        for k in xrange(NUMBER_OF_PERIODS):
            vars_to_sum = [decision_vars_list[k][(i, j)] for j in range(NUMBER_OF_COMPANIES)]
            prob += pulp.lpSum(vars_to_sum) == 1

    # Constraint 2: each company must have a minimum number of students
    # WE DON'T NEED THIS
    for i in xrange(NUMBER_OF_STUDENTS):
        for j in xrange(NUMBER_OF_COMPANIES):
            vars_to_sum = [decision_vars_list[k][(i, j)] for k in range(NUMBER_OF_PERIODS)]
            prob += pulp.lpSum(vars_to_sum) <= 1

    # Constraint 3: each company must have a minimum number of students
    for j in xrange(NUMBER_OF_COMPANIES):
        for k in xrange(NUMBER_OF_PERIODS):
            vars_to_sum = [decision_vars_list[k][(i, j)] for i in range(NUMBER_OF_STUDENTS)]
            prob += pulp.lpSum(vars_to_sum) >= MIN_NUMBER_AT_COMPANY

    # Constraint 4: each company can only have up to a maximum # of students
    for j in xrange(NUMBER_OF_COMPANIES):
        for k in xrange(NUMBER_OF_PERIODS):
            vars_to_sum = [decision_vars_list[k][(i, j)] for i in range(NUMBER_OF_STUDENTS)]
            prob += pulp.lpSum(vars_to_sum) <= MAX_NUMBER_AT_COMPANY

    # Constraint 5: each student must get 3 of their 4 choices
    # THIS WILL BE A PARAMETER THAT CAN BE TUNED
    for i in xrange(NUMBER_OF_STUDENTS):
        vars_to_sum = [decision_vars_list[k][(i, j)] for j in student_info_dicts[i]['choices']
                       for k in range(NUMBER_OF_PERIODS)]
        prob += pulp.lpSum(vars_to_sum) == 3

    # set up objective function

    # solve linear program