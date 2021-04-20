import ask_sdk_core.utils as ask_utils
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils.request_util import get_slot_value

from utils import format_time
from utils import make_difference_readable
from utils import get_formatted_current_date
from session_utils import save_start_of_day
from session_utils import save_start_of_break_and_calculate_worked_hours
from session_utils import save_end_of_break
from session_utils import save_end_of_day_and_total_hours

from db_utils import DbUtils
from aws_dynamo_db import AwsDynamo

du = DbUtils()

aws = AwsDynamo()


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

        worked_hours = save_start_of_break_and_calculate_worked_hours(handler_input, time_output)
        worked_hours_message = make_difference_readable(worked_hours)

        speak_output = "You started your break at {starting_time}. ".format(starting_time = time_output) + worked_hours_message + " so far. Have a great day!"
        
        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )


class LogEndOfBreakIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("LogEndOfBreakIntent")(handler_input)
        
    def handle(self, handler_input):
        break_end_input = get_slot_value(handler_input, "break_end_time")
        
        time_output = break_end_input
        if break_end_input is None:
            time_output = format_time()

        save_end_of_break(handler_input, time_output)

        speak_output = "You ended your break at {ending_time}. Have a great day!".format(ending_time = time_output)
        
        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )


class LogEndOfDayIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("LogEndOfDayIntent")(handler_input)
        
    def handle(self, handler_input):
        end_input = get_slot_value(handler_input, "end_time")
        
        time_output = end_input
        if end_input is None:
            time_output = format_time()

        start_of_day, break_length, end_of_day, total_worked_hours, formatted_worked_hours = save_end_of_day_and_total_hours(handler_input, time_output)

        worked_hours_message = make_difference_readable(total_worked_hours)

        current_date = get_formatted_current_date()

        du.save_day(current_date, start_of_day, break_length, end_of_day, formatted_worked_hours)

        speak_output = "You ended your day at {ending_time}. ".format(ending_time = time_output) +  worked_hours_message + " so far. Have a great day!"
        
        return (
            handler_input.response_builder
            .speak(speak_output)
            .response
        )