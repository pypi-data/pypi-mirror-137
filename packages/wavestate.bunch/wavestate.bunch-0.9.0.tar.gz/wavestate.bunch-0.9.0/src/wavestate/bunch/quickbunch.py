#!/usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: © 2021 Massachusetts Institute of Technology.
# SPDX-FileCopyrightText: © 2021 Lee McCuller <mcculler@mit.edu>
# NOTICE: authors should document their contributions in concisely in NOTICE
# with details inline in source files, comments, and docstrings.
"""
"""
from collections.abc import Mapping


class QuickBunch(dict):
    def __getattr__(self, name):
        return self[name]

    def __setattr__(self, name, val):
        self[name] = val
        return

    def __dir__(self):
        dir_lst = list(super(QuickBunch, self).__dir__())
        dir_lst = dir_lst + list(k for k in self.keys() if isinstance(k, str))
        dir_lst.sort()
        return dir_lst

    def __getstate__(self):
        return self.__dict__.copy()

    def __setstate__(self, state):
        self.__dict__.update(state)

    def get(self, name, *default):
        return super(QuickBunch, self).get(name, *default)


Mapping.register(QuickBunch)
