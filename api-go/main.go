package main

import (
	"context"
	"log"

	"github.com/gin-gonic/gin"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/exporters/otlp/otlptrace"
	"go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
	"go.opentelemetry.io/otel/sdk/trace"
)

func main() {
	r := gin.Default()

	// Set up OpenTelemetry
	ctx := context.Background()

	// Create an OTLP gRPC client
	client := otlptracegrpc.NewClient(
		otlptracegrpc.WithEndpoint("otel-collector:4317"),
		otlptracegrpc.WithInsecure(), // Use this if you're not using TLS
	)

	// Create an OTLP trace exporter
	exporter, err := otlptrace.New(ctx, client)
	if err != nil {
		log.Fatalf("failed to initialize OTLP exporter: %v", err)
	}

	// Create a TracerProvider and set it as the global provider
	tp := trace.NewTracerProvider(trace.WithBatcher(exporter))
	otel.SetTracerProvider(tp)

	// Ensure proper shutdown of tracer provider
	defer func() {
		if err := tp.Shutdown(ctx); err != nil {
			log.Fatalf("failed to shutdown TracerProvider: %v", err)
		}
	}()

	log.Println("OpenTelemetry tracing initialized")

	r.GET("/", func(c *gin.Context) {
		c.String(200, "Hello, OpenTelemetry!")
	})

	r.Run(":8080") // Start the Gin server
}
