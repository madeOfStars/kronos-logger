from utils import format_time
from session_utils import save_start_of_day
from session_utils import save_start_of_break

class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello World!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class LogStartingDayIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("LogStartingDayIntent")(handler_input)
        
    def handle(self, handler_input):
        start_time_input = get_slot_value(handler_input, "start_time")
        
        time_output = start_time_input
        if start_time_input is None:
            time_output = format_time()

        save_start_of_day(handler_input, time_output)

        speak_output = "You started your day at {starting_time}. Have a great day!".format(starting_time = time_output)
        
        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )


class LogStartOfBreakIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("LogStartOfBreakIntent")(handler_input)
        
    def handle(self, handler_input):
        start_time_input = get_slot_value(handler_input, "break_start_time")
        
        time_output = start_time_input
        if start_time_input is None:
            time_output = format_time()

        save_start_of_break(handler_input, time_output)

        speak_output = "You started your break at {starting_time}. Have a great day!".format(starting_time = time_output)
        
        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )