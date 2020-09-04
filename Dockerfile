FROM python:3-slim AS builder
ADD . /app
WORKDIR /app

FROM gcr.io/distroless/python3-debian10
COPY --from=builder /src /app
RUN pip install --target=/app -r /app/requirements.txt
WORKDIR /app
ENV PYTHONPATH /app
CMD ["/app/main.py"]