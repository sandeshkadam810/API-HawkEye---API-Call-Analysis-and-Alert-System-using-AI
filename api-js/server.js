const express = require("express");
const { NodeSDK } = require("@opentelemetry/sdk-node");
const { OTLPTraceExporter } = require("@opentelemetry/exporter-trace-otlp-grpc");
const { BatchSpanProcessor } = require("@opentelemetry/sdk-trace-base");
const { trace } = require("@opentelemetry/api");

// Initialize OpenTelemetry
const exporter = new OTLPTraceExporter({
  url: "http://otel:4317", // Ensure OpenTelemetry Collector is running
});

const sdk = new NodeSDK({
  traceExporter: exporter,
  spanProcessor: new BatchSpanProcessor(exporter),
});

sdk.start();
console.log("✅ OpenTelemetry tracing initialized");

const tracer = trace.getTracer("api-js");

const app = express();

app.get("/", (req, res) => {
  tracer.startActiveSpan("GET /api-js", (span) => {
    let responseTime = Math.floor(Math.random() * 450) + 50;

    setTimeout(() => {
      span.setAttribute("response_time", responseTime);

      if (Math.random() < 0.2) {
        span.setAttribute("error", true);
        span.setStatus({ code: 2, message: "Internal Server Error" });
        res.status(500).json({ message: "Error from api-js", traceId: span.spanContext().traceId });
      } else {
        span.setStatus({ code: 1 });
        res.json({ message: "Hello from api-js", response_time: responseTime, traceId: span.spanContext().traceId });
      }
      span.end();
    }, responseTime);
  });
});

app.listen(5002, () => console.log("🚀 api-js running on port 5002"));
