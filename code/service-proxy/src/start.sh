#!/bin/sh

cd /app/app
pip install pydantic-settings

echo "############## RUN PROXY SERVICE ###################"
uvicorn main:app --host 0.0.0.0 --port 8079