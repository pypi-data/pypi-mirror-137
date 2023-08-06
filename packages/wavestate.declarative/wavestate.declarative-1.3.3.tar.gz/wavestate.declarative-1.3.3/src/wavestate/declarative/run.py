#!/usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: © 2021 Massachusetts Institute of Technology.
# SPDX-FileCopyrightText: © 2021 Lee McCuller <mcculler@mit.edu>
# NOTICE: authors should document their contributions in concisely in NOTICE
# with details inline in source files, comments, and docstrings.
"""
"""

import sys
import importlib

if __name__ == "__main__":
    script = sys.argv[1]
    args = sys.argv[2:]

    split_idx = script.rfind(".")
    mod = script[:split_idx]
    t_obj = script[split_idx + 1 :]
    print("Importing module: ", mod)
    module = importlib.import_module(mod)
    print("Getting Class: ", t_obj)

    cls = getattr(module, t_obj)

    cls.__cls_argparse__(
        args,
        __usage_prog__="python -m declarative.run {0}".format(script),
    )
