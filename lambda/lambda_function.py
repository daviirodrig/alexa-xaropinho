# -*- coding: utf-8 -*-

# This is a simple Hello World Alexa Skill, built using
# the decorators approach in skill builder.
import logging

from utils import create_presigned_url
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    #"""Handler for Skill Launch."""
    # type: (HandlerInput) -> Response
    audio_url = create_presigned_url(
        "Media/rapaz_normal_estourado.mp3").replace("&", '&amp;')
    speech_text = f'<audio src="{audio_url}"/>'
    # return handler_input.response_builder.speak(speech_text).response
    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Xaropinho", "Rapaaaaiz")).set_should_end_session(True).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    #"""Handler for Help Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "Você pode pedir para que eu imite o xaropinho"

    return handler_input.response_builder.speak(speech_text).ask(
        speech_text).set_card(SimpleCard(
            "Xaropinho", speech_text)).response


@sb.request_handler(
    can_handle_func=lambda handler_input:
        is_intent_name("AMAZON.CancelIntent")(handler_input) or
        is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    #"""Single handler for Cancel and Stop Intent."""
    # type: (HandlerInput) -> Response
    speech_text = '<say-as interpret-as="interjection">adeus</say-as>.'

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Xaropinho", speech_text)).response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    #"""Handler for Session End."""
    # type: (HandlerInput) -> Response
    return handler_input.response_builder.response


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    # """Catch all exception handler, log exception and
    # respond with custom message.
    # """
    # type: (HandlerInput, Exception) -> Response
    logger.error(exception, exc_info=True)

    speech = "Desculpa, ocorreu um erro. Por favor tente novamente."
    handler_input.response_builder.speak(speech).ask(speech)

    return handler_input.response_builder.response


lambda_handler = sb.lambda_handler()
