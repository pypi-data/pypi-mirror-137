#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
"""Flask configuration for LetterBomb's web-service."""

# Where to save log file, can be an absolute or relative path
# Leave as blank string to not generate a log file
# Default: ""
LOG_FILE: str = ""

# 10 - debug, 20 - info, 30 - warn, 40 - error, 50 - critical
# Default: 20
LOG_LEVEL: int = 20

# Show version of LetterBomb module in bottom-left corner of webpage
# Might be a small vulnerability if an old version has a security issue and you aren't updated yet
# Default: False
SHOW_VERSION: bool = False

# Show sublinks below the LetterBomb image
# Default: True
SHOW_SUBLINKS: bool = True

# Show a ribbon advertising forking at the top-right corner of webpage
# Default: True
SHOW_RIBBON: bool = True

# Fill these in if you intend on having a Captcha
# Leave *BOTH* of these blank if you do not want to include a Captcha
# Default: ""
RECAPTCHA_PUBLICKEY: str = ""
RECAPTCHA_PRIVATEKEY: str = ""

# Don't enable unless you know what you are doing
# If enabled, overrides LOG_LEVEL to 10 (DEBUG)
# Default: False
DEBUG: bool = False
