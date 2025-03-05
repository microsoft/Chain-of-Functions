import argparse
from typing import Optional
import json

TASK_TYPE = ['NQA', 'Text', 'Binary']

def object_function_description():
    '''
    Return a dictionary of function descriptions
    '''
    return {
        'max_one_object': 'Return the data with the maximum value {value}.',
        'min_one_object': 'Return the data with the minimum value {value}.',
        'max_two_objects': 'Return the two data with the maximum values {value}.',
        'min_two_objects': 'Return the two data with the minimum values {value}.',
        'max_three_objects': 'Return the three data with the maximum three values {value}.',
        'min_three_objects': 'Return the three data with the minimum three values {value}.',
        'second_max_object': 'Return the data with the second maximum value {value}.',
        'second_min_object': 'Return the data with the second minimum value {value}.',
        'value_of_objects': 'Return the values of data.',
        'color_of_objects': 'Return the color of data.',
        'arguments_of_object': 'Return the arguments of data.',
        'legends_of_object': 'Return the legend of data.',
        'if_object_that_equal_to_value': 'Return if the data\'s value is equal to {value}.',
        'if_object_that_larger_than_value': 'Return if the data\'s value is larger/more than {value}.',
        'if_object_that_smaller_than_value': 'Return if the data\'s value is smaller/less than {value}.',
        'objects_that_larger_than_value': 'Return data whose values are larger/more than {value}, satisfited values: {satisfied_values}.',
        'objects_that_smaller_than_value': 'Return data whose value are smaller/less than {value}, satisfited values: {satisfied_values}.',
        'count_of_objects': 'Return the number of data, with values {value}.',
        'num_of_legends': 'Return the number of legends used among the data, with legends {value}.',
        'num_of_colors': 'Return the number of colors used among the data, with colors {value}.',
        'num_of_arguments': 'Return the number of arguments used among the data, with arguments {value}.',
        'exclude_objects_with_arguments': 'Exclude the data with the arguments {value} and return the data without the arguments.',
        'exclude_objects_with_legends': 'Exclude the data with the legends {value} and return the data without the legends.',
        'objects_with_same_value': 'Return one group of data with the same value {value}.',
        'if_objects_consistently_increase': 'Return if the values of the data consistently increase.',
        'if_objects_consistently_decrease': 'Return if the values of the data consistently decrease.',
        'if_same_values': 'Return if the values of the data are the same.',
        'if_same_colors': 'Return if the colors of the data are the same.',
        'if_same_arguments': 'Return if the arguments of the data are the same.',
        'if_same_legends': 'Return if the legends of the data are the same.',
        'upper_one_bar': 'Return the upper-position bar in the chart, with values {value}.',
        'upper_two_bars': 'Return the upper two-position bars in the chart, with values {value}.',
        'upper_three_bars': 'Return the upper three-position bars in the chart, with values {value}.',
        'bottom_one_bar': 'Return the bottom bar in the chart, with values {value}.',
        'bottom_two_bars': 'Return the two bottom-position bars in the chart, with values {value}.',
        'bottom_three_bars': 'Return the three bottomposition bars in the chart, with values {value}.',
        'leftmost_object': 'Return the leftmost bars in the chart, with values {value}.',
        'left_two_objects': 'Return the two leftmost bars in the chart, with values {value}.',
        'left_three_objects': 'Return the three leftmost bars in the chart, with values {value}.',
        'rightmost_object': 'Return the rightmost bars in the chart, with values {value}.',
        'right_two_objects': 'Return the two rightmost bars in the chart, with values {value}.',
        'right_three_objects': 'Return the three rightmost bars in the chart, with values {value}.',
        'upper_rightmost_object': 'Return the upper-rightmost bar in the chart, with values {value}.',
        'upper_leftmost_object': 'Return the upper-leftmost bar in the chart, with values {value}.',
        'lower_rightmost_object': 'Return the bottom-rightmost bar in the chart, with values {value}.',
        'lower_leftmost_object': 'Return the bottom-leftmost bar in the chart, with values {value}.',
        'upper_line_of_objects': 'Return the objects in the upper-position line of the chart, with legend {value}.',
        'lower_line_of_objects': 'Return the objects in the bottom-position line of the chart, with legend {value}.',
        'maximum_difference_between_two_group_of_data': 'Return the maximum difference between the two legends of data: max(|A1-A2|, |B1-B2|, |C1-C2|), with the argument {value}.',
        'minimum_difference_between_two_group_of_data': 'Return the minimum difference between the two legends of data: min(|A1-A2|, |B1-B2|, |C1-C2|), with the argument {value}.',
        'the_argument_that_has_maximum_difference': 'Return the argument B that has the maximum difference between the two legends of data, with value = max(|A1-A2|, |B1-B2|, |C1-C2|) = {value}.',
        'the_argument_that_has_minimum_difference': 'Return the argument B that has the minimum difference between the two legends of data, with value = min(|A1-A2|, |B1-B2|, |C1-C2|) = {value}.',
        'legend_of_one_object_value': 'Return the legend of the specific data with value {value}.',
        'argument_of_one_object_value': 'Return the argument of the specific data with value {value}.',
    }

def value_function_description():
    '''
    Return a dictionary of function descriptions
    '''
    return {
        'sum_of_values': 'Return the sum of the values of data: A + B + C.',
        'mean_of_values': 'Return the mean of the values of data: (A + B + C) / len = D / len.',
        'median_of_values': 'Return the median value of data.',
        'A_minus_B': 'Return A - B.',
        'difference_between_A_and_B': 'Return the difference between two data: | A - B |.',
        'A_multiply_B': 'Return the product of two data: A * B.',
        'A_divided_by_B': 'Return the division of two data: A / B.',
        'A_is_larger_than_B': 'Return True if the value of the first data is larger than the value of the second data: A > B.',
        'A_is_smaller_than_B': 'Return True if the value of the first data is smaller than the value of the second data: A < B.',
        'multiply_constant': 'Return the value multiplied by a constant {value}: A * constant.',
    }

SELECT_FUNCTION_DICT = {
    "all_object_selection": 'object_selection',
    "argument_selection": 'object_selection',
    "legend_selection": 'object_selection',
    "color_selection": 'object_selection',
    "one_object_selection": 'object_selection',
    "color_argument_selection": 'object_selection'
}


OBJECT_GROUP_DICT = {
    'max_one_object': 'min_max',
    'min_one_object': 'min_max',
    'max_two_objects': 'min_max',
    'min_two_objects': 'min_max',
    'max_three_objects': 'min_max',
    'min_three_objects': 'min_max',
    'second_max_object': 'min_max',
    'second_min_object': 'min_max',
    'value_of_objects': 'value',
    'color_of_objects': 'text_information',
    'arguments_of_object': 'text_information',
    'legends_of_object': 'text_information',
    'legend_of_objects': 'text_information',
    'if_object_that_equal_to_value': 'if_match_condition',
    'if_object_that_larger_than_value': 'if_match_condition',
    'if_object_that_smaller_than_value': 'if_match_condition',
    'objects_that_larger_than_value': 'filter',
    'objects_that_smaller_than_value': 'filter',
    'count_of_objects': 'count',
    'num_of_legends': 'count',
    'num_of_colors': 'count',
    'num_of_arguments': 'count',
    'exclude_objects_with_arguments': 'exclude_objects',
    'exclude_objects_with_legends': 'exclude_objects',
    'objects_with_same_value': 'filter',
    'if_objects_consistently_increase': 'if_match_condition',
    'if_objects_consistently_decrease': 'if_match_condition',
    'if_same_values': 'if_match_condition',
    'if_same_colors': 'if_match_condition',
    'if_same_arguments': 'if_match_condition',
    'if_same_legends': 'if_match_condition',
    'upper_one_bar': 'position',
    'upper_two_bars': 'position',
    'upper_three_bars': 'position',
    'bottom_one_bar': 'position',
    'bottom_two_bars': 'position',
    'bottom_three_bars': 'position',
    'leftmost_object': 'position',
    'left_two_objects': 'position',
    'left_three_objects': 'position',
    'rightmost_object': 'position',
    'right_two_objects': 'position',
    'right_three_objects': 'position',
    'upper_rightmost_object': 'position',
    'upper_leftmost_object': 'position',
    'lower_rightmost_object': 'position',
    'lower_leftmost_object': 'position',
    'upper_line_of_objects': 'position',
    'lower_line_of_objects': 'position',
    'maximum_difference_between_two_group_of_data': 'min_max_diff',
    'minimum_difference_between_two_group_of_data': 'min_max_diff',
    'the_argument_that_has_maximum_difference': 'min_max_diff_arg',
    'the_argument_that_has_minimum_difference': 'min_max_diff_arg',
    'legend_of_one_object_value': 'text_information',
    'argument_of_one_object_value': 'text_information',
}

VALUE_GROUP_DICT = {
    'sum_of_values': 'stat',
    'mean_of_values': 'stat',
    'median_of_values': 'stat',
    'A_minus_B': 'arithmetical_operation',
    'difference_between_A_and_B': 'arithmetical_operation',
    'A_multiply_B': 'arithmetical_operation',
    'A_divided_by_B': 'arithmetical_operation',
    'A_is_larger_than_B': 'compare',
    'A_is_smaller_than_B': 'compare',
    'multiply_constant': 'arithmetical_operation',
}

GROUP_DICT = OBJECT_GROUP_DICT | VALUE_GROUP_DICT | SELECT_FUNCTION_DICT


def sort_dict_by_value(d):
    return {k: v for k, v in sorted(d.items(), key=lambda item: item[1], reverse=True)}

def update_step_num_stat(response, step_number_stat):
    function_list = response['function_list']
    key = len(function_list.split('/')) - 1

    if key not in step_number_stat:
        step_number_stat[key] = 1
    else:
        step_number_stat[key] += 1

    return step_number_stat

def update_step_num_stat_correctness(response, step_number_stat_correctness):
    if response['step_num'] not in step_number_stat_correctness:
        step_number_stat_correctness[response['step_num']] = 1
    else:
        step_number_stat_correctness[response['step_num']] += 1

    return step_number_stat_correctness

def update_function_stat(function_list, function_stat):
    for i, function in enumerate(function_list):
        if function not in GROUP_DICT:
            continue
        group = GROUP_DICT[function]
        if i not in function_stat:
            function_stat[i] = {}
        if group not in function_stat[i]:
            function_stat[i][group] = 1
        else:
            function_stat[i][group] += 1

            ### sort by value
            function_stat[i] = sort_dict_by_value(function_stat[i])

    return function_stat

def update_reasoning_path(function_list, reasoning_path_stat):
    '''
    Group the function for each step
    '''
    new_function_combination = ''
    for i, function in enumerate(function_list):
        if function not in GROUP_DICT:
            return reasoning_path_stat
        group = GROUP_DICT[function]
        new_function_combination += group + '/'
    if new_function_combination not in reasoning_path_stat:
        reasoning_path_stat[new_function_combination] = 1
    else:
        reasoning_path_stat[new_function_combination] += 1

    return reasoning_path_stat

def update_reasoning_path_wrt_step(function_list, reasoning_path_wrt_step_stat):
    '''
    Group the function for each step
    '''
    for i, function in enumerate(function_list):
        if i not in reasoning_path_wrt_step_stat:
            reasoning_path_wrt_step_stat[i] = {}
        if function not in reasoning_path_wrt_step_stat[i]:
            reasoning_path_wrt_step_stat[i][function] = 1
        else:
            reasoning_path_wrt_step_stat[i][function] += 1

    return reasoning_path_wrt_step_stat

def update_group_combination_wrt_step_num(function_list, group_combination_stat):
    '''
    get the number of Short function chains for each step
    {
    'object_selection/value'{1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
    'object_selection/filter'{1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
    }
    '''

    selected_group_combination = ['object_selection/value', 'object_selection/filter', 'object_selection/min_max', 'object_selection/count', 'object_selection/position']

    group_combination = ''
    for i, function in enumerate(function_list):
        if function not in GROUP_DICT:
            return group_combination_stat
        group = GROUP_DICT[function]
        group_combination += group + '/'
    
    step_num = len(function_list)


    for group in selected_group_combination:
        if group in group_combination:
            if group not in group_combination_stat:
                group_combination_stat[group] = {}

            if step_num not in group_combination_stat[group]:
                group_combination_stat[group][step_num] = 1
            else:
                group_combination_stat[group][step_num] += 1

    return group_combination_stat

def get_stat(score_path, task_type=['NQA']):
    '''
    '''

    output_path = score_path.replace(".jsonl", "_stat_analysis_ada.txt")

    score_list = []
    with open(score_path, 'r') as f:
        for line in f:
            data = json.loads(line)
            score_list.append(data)

    step_number_stat = {}
    step_number_stat_correctness = {}
    function_stat = {}
    function_stat_correctness = {}
    reasoning_path_stat = {}
    reasoning_path_stat_correctness = {}
    reasoning_path_stat_wrt_step = {}
    reasoning_path_stat_wrt_step_correctness = {}
    group_combination_stat = {}
    group_combination_stat_correctness = {}
    start_if_stat = {}

    for i, response in enumerate(score_list):
        if response['task_type'] not in task_type:
            continue

        if 'bar' not in response['chart_type'] and 'line' not in response['chart_type'] and 'pie' not in response['chart_type']:
            continue

        function_list = response['function_list']
        function_list = function_list.split('/')[:-1]

        step_number_stat = update_step_num_stat(response, step_number_stat)
        function_stat = update_function_stat(function_list, function_stat)
        reasoning_path_stat = update_reasoning_path(function_list, reasoning_path_stat)
        reasoning_path_stat_wrt_step = update_reasoning_path_wrt_step(function_list, reasoning_path_stat_wrt_step)
        group_combination_stat = update_group_combination_wrt_step_num(function_list, group_combination_stat)
        if response['score']:
            step_number_stat_correctness = update_step_num_stat(response, step_number_stat_correctness)
            function_stat_correctness = update_function_stat(function_list, function_stat_correctness)
            reasoning_path_stat_correctness = update_reasoning_path(function_list, reasoning_path_stat_correctness)
            reasoning_path_stat_wrt_step_correctness = update_reasoning_path_wrt_step(function_list, reasoning_path_stat_wrt_step_correctness)
            group_combination_stat_correctness = update_group_combination_wrt_step_num(function_list, group_combination_stat_correctness)


    ### compute accuracy for each step number
    step_number_acc = {}
    for key in step_number_stat:
        if key not in step_number_stat_correctness:
            step_number_stat_correctness[key] = 0
        print(f'step number: {key}, total: {step_number_stat[key]}, correct: {step_number_stat_correctness[key]}')
        step_number_acc[key] = step_number_stat_correctness[key] / step_number_stat[key]

    ## compute accuracy for each combination of function
    group_combination_stat_acc = {}
    for key in group_combination_stat:
        if key not in group_combination_stat_correctness:
            group_combination_stat_correctness[key] = 0
        if key not in group_combination_stat_acc:
            group_combination_stat_acc[key] = {}
        for group in group_combination_stat[key]:
            if group not in group_combination_stat_correctness[key]:
                group_combination_stat_correctness[key][group] = 0
            print(f'step number: {key}, group: {group}, total: {group_combination_stat[key][group]}, correct: {group_combination_stat_correctness[key][group]}')
            group_combination_stat_acc[key][group] = group_combination_stat_correctness[key][group] / group_combination_stat[key][group]
    
    reasoning_path_acc = {}
    for key in reasoning_path_stat:
        if reasoning_path_stat[key] < 10:
            continue
        if key not in reasoning_path_stat_correctness:
            reasoning_path_stat_correctness[key] = 0
        print(f'Function chains: {key}, total: {reasoning_path_stat[key]}, correct: {reasoning_path_stat_correctness[key]}')
        reasoning_path_acc[key] = reasoning_path_stat_correctness[key] / reasoning_path_stat[key]

    print(reasoning_path_acc)

    with open(output_path, 'w') as f:
        f.write(f'Step Number:\n')
        for k in step_number_stat:
            f.write(f'{k}: Total {step_number_stat[k]}, Correct number {step_number_stat_correctness[k]}, Accuracy {step_number_acc[k]}\n')
        f.write(f'===========================================================================')
        f.write(f'\nFunction chains:\n')
        for k in reasoning_path_stat:
            if k not in reasoning_path_acc:
                continue
            f.write(f'{k}: Total {reasoning_path_stat[k]}, Correct number {reasoning_path_stat_correctness[k]}, Accuracy {reasoning_path_acc[k]}\n')
        f.write(f'===========================================================================')
        f.write(f'\nShort function chains:\n')
        
        for k in group_combination_stat:
            if k not in group_combination_stat_acc:
                continue
            f.write(f'{k}: Total {group_combination_stat[k]}, Correct number {group_combination_stat_correctness[k]}, Accuracy {group_combination_stat_acc[k]}\n')
            ### overall accuracy
            total_acc_num = 0
            total_acc_den = 0
            for group in group_combination_stat[k]:
                total_acc_num += group_combination_stat_correctness[k][group]
                total_acc_den += group_combination_stat[k][group]
            f.write(f'key: {k}, total: {total_acc_den}, correct: {total_acc_num}, accuracy: {total_acc_num / total_acc_den}\n')

        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--score_path', type=str, help='Path to the score jsonl file', required=True)
    args = parser.parse_args()

    get_stat(args.score_path)
