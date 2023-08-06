# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashWordcloud(Component):
    """A DashWordcloud component.
This is a Dash wrapper for wordcloud2.js.

See https://github.com/timdream/wordcloud2.js

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- backgroundColor (string; optional):
    The color of the background.

- className (string; default "wc-canvas"):
    Often used with CSS to style elements with common properties.

- classes (string; optional):
    For DOM clouds, allows the user to define the class of the span
    elements. Can be a normal class string.

- clearCanvas (boolean; optional):
    Paint the entire canvas with background color and consider it
    empty before start.

- click (list; optional):
    Captures word onClick event and returns the cloud item that was
    clicked.

- color (string | dict; optional):
    Color of the text, can be any CSS color.

- dppx (number; default 1):
    The device pixel density.

- drawMask (number; optional):
    Visualize the grid by draw squares to mask the drawn areas.

- drawOutOfBound (boolean; optional):
    Set to True to allow word being draw partly outside of the canvas.
    Allow word bigger than the size of the canvas to be drawn.

- ellipticity (number; optional):
    The degree of \"flatness\" of the shape wordcloud2.js should draw.

- fontFamily (string; optional):
    The font to use.

- fontWeight (string; optional):
    The font weight to use, can be, as an example, 'normal', 'bold' or
    '600'.

- gridSize (number; optional):
    The size of the grid in pixels for marking the availability of the
    canvas — the larger the grid size, the bigger the gap between
    words.

- height (number; required):
    The canvas height.

- hover (boolean; default False):
    Set True to enable hover and tooltips.

- list (list; required):
    List of words/text to paint on the canvas in a 2-d array, in the
    form of [word, size].  eg. [['foo', 12], ['bar', 6]]  Optionally,
    you can send additional data as array elements, in the form of
    '[word, size, data1, data2, ... ]' which can then be used in the
    callback functions of 'click', 'hover' interactions and
    fontWeight, color and classes callbacks.

- maskColor (string; optional):
    Color of the mask squares.

- maskGapWidth (number; optional):
    Width of the gaps between mask squares.

- maxRotation (number; optional):
    If the word should rotate, the maximum rotation (in rad) the text
    should rotate. Set the two value equal to keep all text in one
    angle.

- minRotation (number; optional):
    If the word should rotate, the minimum rotation (in rad) the text
    should rotate.

- minSize (number; optional):
    The minimum font size to draw on the canvas.

- origin (list of numbers; optional):
    The origin of the “cloud” in [x, y].

- rotateRatio (number; optional):
    Probability for the word to rotate. Set the number to 1 to always
    rotate.

- rotationSteps (number; optional):
    Force the use of a defined number of angles. Set the value equal
    to 2 in a -90°/90° range means just -90, 0 or 90 will be used.

- shape (a value equal to: 'circle', 'cardioid', 'diamond', 'square', 'triangle', 'triangle-forward', 'triangle-upright', 'pentagon', 'star'; optional):
    The shape of the \"cloud\" to draw. Available presents are:.

- shrinkToFit (boolean; optional):
    Set to 'True' to shrink the word so it will fit into canvas. Best
    if 'drawOutOfBound' is set to 'False'. :warning: This word will
    now have lower 'weight'.

- shuffle (boolean; optional):
    Shuffle the points to draw so the result will be different each
    time for the same list and settings.

- style (dict; optional):
    Canvas style.

- weightFactor (number; optional):
    Number to multiply for 'size' of each word in the list.

- width (number; required):
    The canvas width."""
    @_explicitize_args
    def __init__(self, dppx=Component.UNDEFINED, width=Component.REQUIRED, height=Component.REQUIRED, list=Component.REQUIRED, fontFamily=Component.UNDEFINED, fontWeight=Component.UNDEFINED, color=Component.UNDEFINED, classes=Component.UNDEFINED, minSize=Component.UNDEFINED, weightFactor=Component.UNDEFINED, clearCanvas=Component.UNDEFINED, backgroundColor=Component.UNDEFINED, gridSize=Component.UNDEFINED, origin=Component.UNDEFINED, drawOutOfBound=Component.UNDEFINED, shrinkToFit=Component.UNDEFINED, drawMask=Component.UNDEFINED, maskColor=Component.UNDEFINED, maskGapWidth=Component.UNDEFINED, minRotation=Component.UNDEFINED, maxRotation=Component.UNDEFINED, rotationSteps=Component.UNDEFINED, shuffle=Component.UNDEFINED, rotateRatio=Component.UNDEFINED, shape=Component.UNDEFINED, ellipticity=Component.UNDEFINED, hover=Component.UNDEFINED, click=Component.UNDEFINED, style=Component.UNDEFINED, id=Component.UNDEFINED, className=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'backgroundColor', 'className', 'classes', 'clearCanvas', 'click', 'color', 'dppx', 'drawMask', 'drawOutOfBound', 'ellipticity', 'fontFamily', 'fontWeight', 'gridSize', 'height', 'hover', 'list', 'maskColor', 'maskGapWidth', 'maxRotation', 'minRotation', 'minSize', 'origin', 'rotateRatio', 'rotationSteps', 'shape', 'shrinkToFit', 'shuffle', 'style', 'weightFactor', 'width']
        self._type = 'DashWordcloud'
        self._namespace = 'dash_wordcloud'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'backgroundColor', 'className', 'classes', 'clearCanvas', 'click', 'color', 'dppx', 'drawMask', 'drawOutOfBound', 'ellipticity', 'fontFamily', 'fontWeight', 'gridSize', 'height', 'hover', 'list', 'maskColor', 'maskGapWidth', 'maxRotation', 'minRotation', 'minSize', 'origin', 'rotateRatio', 'rotationSteps', 'shape', 'shrinkToFit', 'shuffle', 'style', 'weightFactor', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in ['width', 'height', 'list']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DashWordcloud, self).__init__(**args)
