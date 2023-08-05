#!/usr/bin/env python

"""Tests for `ftl_module_utils` package."""

import pytest
import sys

def test_ftl_module_utils():
    import ftl_module_utils.load
    ftl_module_utils.load.patch()
    import ansible

def test_module_utils_basic():
    import ftl_module_utils.module_utils.basic
