#!/usr/bin/env bash

gunicorn src.app:app --bind 0.0.0.0:5000 --log-level=debug --workers=4