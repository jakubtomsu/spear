#
# Copyright (c) 2025 The SPEAR Development Team. Licensed under the MIT License <http://opensource.org/licenses/MIT>.
# Copyright (c) 2022 Intel. Licensed under the MIT License <http://opensource.org/licenses/MIT>.
#

#
# Helper for coloring terminal output using ANSI escape codes.
#

import os
import sys

_RESET = "\033[0m"

_COLORS = {
    "black":   "30",
    "red":     "31",
    "green":   "32",
    "yellow":  "33",
    "blue":    "34",
    "magenta": "35",
    "cyan":    "36",
    "white":   "37"}

# supports_color() follows the NO_COLOR/FORCE_COLOR conventions (https://no-color.org/) on top of the standard
# library's own notion of whether stdout is a terminal.

_supports_color_cached = None
def supports_color():
    global _supports_color_cached
    if _supports_color_cached is not None:
        return _supports_color_cached
    _supports_color_cached = _supports_color()
    return _supports_color_cached

def _supports_color():
    if os.environ.get("NO_COLOR") is not None:
        return False
    if os.environ.get("FORCE_COLOR") is not None:
        return True
    return sys.stdout.isatty()

def colorize(text, color, bold=False):
    if not supports_color():
        return text
    prefix = "1;" if bold else ""
    return f"\033[{prefix}{_COLORS[color]}m{text}{_RESET}"

#
# A log func can be registered via spear.register_log_func(func=...). Since the default printing behavior in
# spear.log(...) is independent of registered log funcs, disable it first via spear.set_default_log_enabled(
# enabled=False) to avoid printing each message twice.
#

def log_func(message):
    message_lower = message.lower()
    if "error" in message_lower or "exception" in message_lower:
        print(colorize(text=message, color="red", bold=True))
    elif "warning" in message_lower:
        print(colorize(text=message, color="yellow"))
    else:
        print(message)
