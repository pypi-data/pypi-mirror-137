#!/usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: © 2021 Massachusetts Institute of Technology.
# SPDX-FileCopyrightText: © 2021 Lee McCuller <mcculler@mit.edu>
# NOTICE: authors should document their contributions in concisely in NOTICE
# with details inline in source files, comments, and docstrings.
"""
"""
# make noarg a VERY unique value. Was using empty tuple, but python caches it, this should be quite unique
def unique_generator():
    def UNIQUE_CLOSURE():
        return UNIQUE_CLOSURE

    return (
        "<UNIQUE VALUE>",
        UNIQUE_CLOSURE,
    )


NOARG = unique_generator()
