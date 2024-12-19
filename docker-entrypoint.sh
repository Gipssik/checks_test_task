#!/bin/bash
alembic upgrade head
gunicorn -k uvicorn.workers.UvicornWorker -c gunicorn-conf.py --timeout 1000 server:app
