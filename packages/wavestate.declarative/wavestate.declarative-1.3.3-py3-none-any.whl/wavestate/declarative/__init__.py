#!/usr/bin/env python
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: © 2021 Massachusetts Institute of Technology.
# SPDX-FileCopyrightText: © 2021 Lee McCuller <mcculler@mit.edu>
# NOTICE: authors should document their contributions in concisely in NOTICE
# with details inline in source files, comments, and docstrings.
"""
"""
from .properties import (
    HasDeclaritiveAttributes,
    mproperty,
    dproperty,
    mproperty_fns,
    dproperty_fns,
    mproperty_plain,
    dproperty_plain,
    mfunction,
    PropertyTransforming,
    PropertyAttributeError,
    group_dproperty,
    group_mproperty,
    mproperty_adv,
    dproperty_adv,
    mproperty_adv_group,
    dproperty_adv_group,
)

from .callbacks import (
    callbackmethod,
    Callback,
    RelayBool,
    RelayBoolAny,
    RelayBoolAll,
    RelayBoolNotAny,
    RelayBoolNotAll,
    RelayBoolNot,
    RelayValue,
    RelayValueRejected,
    RelayValueCoerced,
    min_max_validator,
    min_max_validator_int,
)


from .overridable_object import (
    OverridableObject,
)

from .metaclass import (
    AutodecorateMeta,
    Autodecorate,
    AttrExpandingObject,
    GetSetAttrExpandingObject,
)

from .utilities.unique import (
    NOARG,
    unique_generator,
)

from ._version import (
    version,
    __version__,
)


def first_non_none(*args):
    for a in args:
        if a is not None:
            return a
    return None


FNN = first_non_none

PropertyAttributeError.__module__ == __name__
