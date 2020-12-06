import logging

from niftypet.ninst import cudasetup as cs


def test_find_cuda(caplog):
    with caplog.at_level(logging.WARNING):
        cuda = cs.find_cuda()
    assert cuda or caplog.record_tuples


def test_dev_setup(caplog):
    with caplog.at_level(logging.WARNING):
        ccstr = cs.dev_setup()
    assert ccstr


def test_resources_setup(caplog):
    with caplog.at_level(logging.WARNING):
        gpu = cs.resources_setup()
    assert gpu or caplog.record_tuples
