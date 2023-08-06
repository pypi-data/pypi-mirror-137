# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashChartist(Component):
    """A DashChartist component.
Wrapper for react-chartist library. For API and
examples see:

https://github.com/fraserxu/react-chartist

https://gionkunz.github.io/chartist-js/index.html

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- data (dict; required):
    Chart data.

- options (dict; optional):
    The options object with options that override the default options.
    Check the examples for a detailed list.

- responsiveOptions (list; optional):
    Specify an array of responsive option arrays which are a media
    query and options object pair => [[mediaQueryString,
    optionsObject],[more...]].

- style (dict; optional):
    Defines CSS styles which will override styles previously set.

- tooltips (boolean; optional):
    Set True to enable tooltips.

- type (a value equal to: 'Line', 'Bar', 'Pie'; required):
    The chart type."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, type=Component.REQUIRED, data=Component.REQUIRED, className=Component.UNDEFINED, options=Component.UNDEFINED, tooltips=Component.UNDEFINED, responsiveOptions=Component.UNDEFINED, style=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'className', 'data', 'options', 'responsiveOptions', 'style', 'tooltips', 'type']
        self._type = 'DashChartist'
        self._namespace = 'dash_chartist'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'className', 'data', 'options', 'responsiveOptions', 'style', 'tooltips', 'type']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in ['type', 'data']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DashChartist, self).__init__(**args)
