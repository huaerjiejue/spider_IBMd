import pytest
from operate import IBMD

def test_get_quote():
    ibmd = IBMD('tt2194499')
    ibmd.get_quote()
    assert ibmd.quotes[0] != ''

def test_get_one_picture():
    ibmd = IBMD('tt2194499')
    ibmd.get_one_picture()
    assert ibmd.one_picture != ''
