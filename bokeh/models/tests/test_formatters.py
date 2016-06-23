import pytest
from unittest import skipIf

try:
    from flexx import pyscript
    is_flexx = True
except ImportError as e:
    is_flexx = False

from bokeh.models import FuncTickFormatter, Slider

@skipIf(not is_flexx, "flexx not installed")
def test_functickformatter_from_py_func_no_args():

    def convert_to_minutes(seconds):
        return seconds * 60

    formatter = FuncTickFormatter.from_py_func(convert_to_minutes)
    js_code = pyscript.py2js(convert_to_minutes, 'formatter')

    function_wrapper = formatter.code.replace(js_code, '')

    assert function_wrapper == "function (seconds) {return formatter(seconds)};"
    assert formatter.lang == "javascript"

@skipIf(not is_flexx, "flexx not installed")
def test_functickformatter_from_py_func_with_args():

    slider = Slider()

    def convert_to_minutes(seconds, x=slider):
        return seconds * 60

    formatter = FuncTickFormatter.from_py_func(convert_to_minutes)
    js_code = pyscript.py2js(convert_to_minutes, 'formatter')

    function_wrapper = formatter.code.replace(js_code, '')

    assert function_wrapper == "function (seconds) {return formatter(seconds)};"
    assert formatter.args['x'] is slider
    assert formatter.lang == "javascript"

@skipIf(not is_flexx, "flexx not installed")
def test_functickformatter_bad_pyfunc_formats():
    def missing_positional_arg():
        return None
    with pytest.raises(ValueError):
        FuncTickFormatter.from_py_func(missing_positional_arg)

    def missing_positional_arg_with_kwargs(x=5):
        return None
    with pytest.raises(ValueError):
        FuncTickFormatter.from_py_func(missing_positional_arg_with_kwargs)

    def too_many_positional_arguments(x, y):
        return None
    with pytest.raises(ValueError):
        FuncTickFormatter.from_py_func(missing_positional_arg)