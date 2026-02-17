import pytest

import graphloom
import graphloom.builder as builder_mod
import graphloom.elkjs as elkjs_mod


def test_lazy_builder_exports_are_available_via_module_getattr():
    assert graphloom.MinimalGraphIn is builder_mod.MinimalGraphIn
    assert graphloom.MinimalNodeIn is builder_mod.MinimalNodeIn
    assert graphloom.MinimalEdgeIn is builder_mod.MinimalEdgeIn
    assert graphloom.build_canvas is builder_mod.build_canvas
    assert graphloom.sanitize_id is builder_mod.sanitize_id


def test_lazy_elkjs_export_is_available_via_module_getattr():
    assert graphloom.layout_with_elkjs is elkjs_mod.layout_with_elkjs


def test_unknown_graphloom_attribute_raises_attribute_error():
    with pytest.raises(AttributeError, match="module 'graphloom' has no attribute 'not_real'"):
        getattr(graphloom, "not_real")
