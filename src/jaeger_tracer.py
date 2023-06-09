from functools import wraps

from flask import request
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

from src.core.config import config

DEBUG = config.debug


def configure_tracer() -> None:
    trace.set_tracer_provider(TracerProvider())
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name="jaeger",
                agent_port=6831,
            )
        )
    )
    # Чтобы видеть трейсы в консоли
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(ConsoleSpanExporter())
    )


tracer = trace.get_tracer(__name__)


if DEBUG:
    def jaeger_trace(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)
        return wrapper
else:
    def jaeger_trace(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            name = f.__name__
            with tracer.start_as_current_span(name) as span:
                request_id = request.headers.get("X-Request-Id")
                span.set_attribute("http.request_id", request_id)
                return f(*args, **kwargs)

        return wrapper
