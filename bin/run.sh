#!/usr/bin/env bash

gunicorn src.main:app --bind 0.0.0.0:5000 --log-level=debug