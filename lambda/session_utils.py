def save_start_of_day(handler_input, time):
    attr = handler_input.attributes_manager.persistent_attributes
    if not attr:
        attr['start_of_day'] = time;

    handler_input.attributes_manager.session_attributes = attr

    handler_input.attributes_manager.save_persistent_attributes()
