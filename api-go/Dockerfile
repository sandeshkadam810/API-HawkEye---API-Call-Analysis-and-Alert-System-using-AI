FROM golang:latest
WORKDIR /app
COPY . .
RUN go mod tidy
RUN go build -o api-go main.go
CMD ["./api-go"]
