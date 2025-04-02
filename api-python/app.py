from flask import Flask, jsonify
import time, random
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

# Configure OpenTelemetry
tracer_provider = TracerProvider()
trace.set_tracer_provider(tracer_provider)  # ✅ Set as global provider
span_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://otel-collector:4317"))
tracer_provider.add_span_processor(span_processor)

tracer = trace.get_tracer(__name__)  # ✅ Get a tracer instance

@app.route('/')
def api_python():
    with tracer.start_as_current_span("api-python-span") as span:  # ✅ Create a span
        response_time = random.randint(50, 500)
        time.sleep(response_time / 1000)
        
        span.set_attribute("response_time", response_time)  # ✅ Add metadata to trace

        if random.random() < 0.2:
            span.set_status(trace.Status(trace.StatusCode.ERROR, "Internal Server Error"))  # ✅ Mark as error
            return jsonify({"message": "Error from api-python"}), 500

        span.set_status(trace.Status(trace.StatusCode.OK))  # ✅ Mark as success
        return jsonify({"message": "Hello from api-python", "response_time": response_time})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
