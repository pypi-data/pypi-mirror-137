# Auxiliary modules
from os.path import join, dirname
import sys

# Module to be tested
sys.path.append(join(dirname(__file__), '..'))
import heppy
from heppy.heatmap import _make_text



#
# Set up
#
_values_for_some_bin = {
	'nominal' : 11.1,
	'uncert_up' : 0.5,
	'uncert_down' : -0.7,
	'stat_up' : 0.2,
	'stat_down' : -0.1,
	'syst_up' : 0.3,
	'syst_down' : -0.4,
}





def test_to_str():
	'''
	Test formatting a single float value to a string with a given precision
	'''
	from heppy import TextFormatter
	test_value = 1234.345
	assert TextFormatter._to_str(test_value) == '1230'
	assert TextFormatter._to_str(test_value, significants=1) == '1000'
	assert TextFormatter._to_str(test_value, significants=2) == '1200'
	assert TextFormatter._to_str(test_value, significants=3) == '1230'
	assert TextFormatter._to_str(test_value, significants=4) == '1234'
	assert TextFormatter._to_str(test_value, significants=5) == '1234.3'
	assert TextFormatter._to_str(test_value, significants=6) == '1234.35'
	assert TextFormatter._to_str(test_value, significants=7) == '1234.345'
	assert TextFormatter._to_str(test_value, significants=8) == '1234.345'
	assert TextFormatter._to_str(test_value, fixedprec=4) == '1234.345'
	assert TextFormatter._to_str(test_value, fixedprec=3) == '1234.345'
	assert TextFormatter._to_str(test_value, fixedprec=2) == '1234.35'
	assert TextFormatter._to_str(test_value, fixedprec=1) == '1234.3'
	assert TextFormatter._to_str(test_value, fixedprec=0) == '1234'
	assert TextFormatter._to_str(test_value, fixedprec=-1) == '1230'
	assert TextFormatter._to_str(test_value, fixedprec=-2) == '1200'
	assert TextFormatter._to_str(test_value, fixedprec=-3) == '1000'
	assert TextFormatter._to_str(test_value, fixedprec=-4) == '0'



def test_make_text_with_string_template():
	'''
	Test formatting of heatmap bin content text with a string template
	'''
	template = '{nominal} {uncert_up} {uncert_down} {stat_up} {stat_down} {syst_up} {syst_down}'
	text = _make_text(template, _values_for_some_bin)
	assert text == '11.1 0.5 -0.7 0.2 -0.1 0.3 -0.4'



def test_make_text_with_named_formatting_function():
	'''
	Test formatting of heatmap bin content text with a named formatting function
	'''
	def template_function(nominal=None, uncert_up=None, uncert_down=None, stat_up=None, stat_down=None, syst_up=None, syst_down=None):
		return '_'.join([str(arg) for arg in [nominal, uncert_up, uncert_down, stat_up, stat_down, syst_up, syst_down]])
	text = _make_text(template_function, _values_for_some_bin)
	assert text == '11.1_0.5_-0.7_0.2_-0.1_0.3_-0.4'



def test_make_text_with_lambda_formatting_function():
	'''
	Test formatting of heatmap bin content text with an unnamed formatting function (lambda)
	'''
	template_lambda = lambda nominal, uncert_up, uncert_down, stat_up, stat_down, syst_up, syst_down : ':'.join([str(arg) for arg in [nominal, uncert_up, uncert_down, stat_up, stat_down, syst_up, syst_down]])
	text = _make_text(template_lambda, _values_for_some_bin)
	assert text == '11.1:0.5:-0.7:0.2:-0.1:0.3:-0.4'
