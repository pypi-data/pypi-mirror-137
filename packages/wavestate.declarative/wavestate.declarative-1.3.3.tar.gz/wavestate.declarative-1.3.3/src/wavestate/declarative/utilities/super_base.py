#!/usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: © 2021 Massachusetts Institute of Technology.
# SPDX-FileCopyrightText: © 2021 Lee McCuller <mcculler@mit.edu>
# NOTICE: authors should document their contributions in concisely in NOTICE
# with details inline in source files, comments, and docstrings.
"""
"""


class SuperBase(object):
    """ """

    def __new__(cls, *args, **kwargs):
        return super(SuperBase, cls).__new__(cls)

    def __init__(self, **kwargs):
        super(SuperBase, self).__init__()
        if kwargs:
            raise RuntimeError(
                ("kwargs has extra items for class {0}, contains: {1}").format(
                    self.__class__, kwargs
                )
            )
        return
