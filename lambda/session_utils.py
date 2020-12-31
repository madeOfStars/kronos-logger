from utils import calculate_diff_between_start_time_and_end_time
from utils import format_timedelta_to_hours_and_minutes
from utils import format_timedelta


def save_start_of_day(handler_input, time):
    save_attribute('start_of_day', handler_input, time)


def save_start_of_break_and_calculate_worked_hours(handler_input, time):
    save_attribute('start_of_break', handler_input, time)

    attr = handler_input.attributes_manager.persistent_attributes
    start_time = attr['start_of_day']

    return calculate_diff_between_start_time_and_end_time(start_time, time)


def save_end_of_break(handler_input, time):
    attr = handler_input.attributes_manager.persistent_attributes
    start_time = attr['start_of_break']
    break_length = calculate_diff_between_start_time_and_end_time(start_time, time)
    hours, minutes = format_timedelta_to_hours_and_minutes(break_length)
    attribute_value = "{:02}:{:02}".format(hours, minutes)
    save_attribute('break_length', handler_input, attribute_value)


def save_end_of_day_and_total_hours(handler_input, time):
    save_attribute('end_of_day', handler_input, time)
    
    attr = handler_input.attributes_manager.persistent_attributes
    start_of_day = attr['start_of_day']
    start_of_break = attr['start_of_break']
    break_length = attr['break_length']

    all_hours = calculate_diff_between_start_time_and_end_time(start_of_day, time)
    all_hours_minus_break = calculate_diff_between_start_time_and_end_time("00:00", break_length)
    total_hours = all_hours - all_hours_minus_break

    formatted_worked_hours = format_timedelta(total_hours)
    save_attribute('total_hours', handler_input, formatted_worked_hours)

    return start_of_day, break_length, time, total_hours, formatted_worked_hours


def save_attribute(attribute_name, handler_input, time):
    attr = handler_input.attributes_manager.persistent_attributes
    attr[attribute_name] = time;

    handler_input.attributes_manager.session_attributes = attr

    handler_input.attributes_manager.save_persistent_attributes()