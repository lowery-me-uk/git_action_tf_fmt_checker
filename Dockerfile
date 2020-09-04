FROM python:3-slim AS builder
ADD . /app
WORKDIR /app

COPY --from=builder /src /app
RUN pip install --target=/app -r /src/requirements.txt

FROM gcr.io/distroless/python3-debian10
COPY --from=builder /src /app
WORKDIR /app
ENV PYTHONPATH /app
CMD ["/app/main.py"]