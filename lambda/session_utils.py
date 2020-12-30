def save_start_of_day(handler_input, time):
    save_attribute('start_of_day', handler_input, time)


def save_start_of_break(handler_input, time):
    save_attribute('start_of_break', handler_input, time)


def save_end_of_break(handler_input, time):
    save_attribute('end_of_break', handler_input, time)


def save_attribute(attribute_name, handler_input, time):
    attr = handler_input.attributes_manager.persistent_attributes
    attr[attribute_name] = time;

    handler_input.attributes_manager.session_attributes = attr

    handler_input.attributes_manager.save_persistent_attributes()