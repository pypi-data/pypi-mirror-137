#!/usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: © 2021 Massachusetts Institute of Technology.
# SPDX-FileCopyrightText: © 2021 Lee McCuller <mcculler@mit.edu>
# NOTICE: authors should document their contributions in concisely in NOTICE
# with details inline in source files, comments, and docstrings.
"""
"""

from ._version import version, __version__, version_info

from .bunch import Bunch, FrozenBunch

from .deep_bunch import DeepBunch


__all__ = [
    "Bunch",
    "FrozenBunch",
    "DeepBunch",
    "version",
    "__version__",
    "version_info",
]
