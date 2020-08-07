#!/usr/bin/env python3
""" Tests for the autosysloguru wrapper for Loguru. """
from __future__ import annotations
from autosysloguru import logger

from typing import List, Dict

logger.info('This is a logger info message.')


def good_sink(message: loguru.Message):
    print('My name is', message.record['name'])


def bad_filter(record: loguru.Record):
    return record['invalid']

    logger.add(good_sink, filter=bad_filter)
