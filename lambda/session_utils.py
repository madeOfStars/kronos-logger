from utils import calculate_diff_between_start_time_and_end_time

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
    worked_hours = calculate_diff_between_start_time_and_end_time(start_time, time)
    save_attribute('break_length', handler_input, time)

    return worked_hours


def save_attribute(attribute_name, handler_input, time):
    attr = handler_input.attributes_manager.persistent_attributes
    attr[attribute_name] = time;

    handler_input.attributes_manager.session_attributes = attr

    handler_input.attributes_manager.save_persistent_attributes()