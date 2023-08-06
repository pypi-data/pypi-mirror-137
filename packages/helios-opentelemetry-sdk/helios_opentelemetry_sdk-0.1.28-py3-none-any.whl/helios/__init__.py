from opentelemetry.propagators import textmap

from helios.base import HeliosBase, HeliosTags  # noqa: F401 (ignore lint error: imported but not used)
from helios.helios import Helios
from helios.helios_test_trace import HeliosTestTrace
from typing import Optional, Union, Dict, Callable
from opentelemetry.util import types
from opentelemetry.propagate import inject, extract
from opentelemetry.context import get_current
from logging import getLogger

_LOG = getLogger(__name__)


def initialize(api_token: str,
               service_name: str,
               enabled: bool = False,
               collector_endpoint: Optional[str] = None,
               test_collector_endpoint: Optional[str] = None,
               sampling_ratio: Optional[Union[float, int, str]] = 1.0,
               environment: Optional[str] = None,
               resource_tags: Optional[Dict[str, Union[bool, float, int, str]]] = None,
               debug: Optional[bool] = False,
               **kwargs) -> Helios:

    return Helios.get_instance(
        api_token=api_token,
        service_name=service_name,
        enabled=enabled,
        collector_endpoint=collector_endpoint,
        test_collector_endpoint=test_collector_endpoint,
        sampling_ratio=sampling_ratio,
        environment=environment,
        resource_tags=resource_tags,
        debug=debug,
        **kwargs
    )


def create_custom_span(name: str,
                       attributes: types.Attributes = None,
                       wrapped_fn: Optional[Callable[[], any]] = None,
                       set_as_current_context: bool = False):
    if not Helios.has_instance():
        _LOG.debug('Cannot create custom span before initializing Helios')
        return

    hs = Helios.get_instance()
    return hs.create_custom_span(name, attributes, wrapped_fn, set_as_current_context)


def validate(spans, validations_callback, expected_number_of_spans=1):
    if len(spans) <= expected_number_of_spans:
        for s in spans:
            validations_callback(s)
    else:
        validated_spans_count = 0
        for s in spans:
            try:
                validations_callback(s)
                validated_spans_count += 1
            except AssertionError:
                continue
        assert validated_spans_count == expected_number_of_spans


def inject_current_context(carrier, setter: textmap.Setter = None):
    carrier = carrier if carrier is not None else {}
    current_context = get_current()
    if setter is not None:
        inject(carrier, context=current_context, setter=setter)
    else:
        inject(carrier, context=current_context)
    return carrier


def extract_context(carrier):
    carrier = carrier if carrier else {}
    context = extract(carrier)
    return context


def initialize_test(api_token=None):
    return HeliosTestTrace(api_token)
