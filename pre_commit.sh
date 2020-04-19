#!/bin/sh
yapf . --recursive -i -p
python -m isort -rc -y -up -l 79 -m 4
