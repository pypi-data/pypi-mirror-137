# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class FeFuncG(Component):
    """A FeFuncG component.
FeFuncG is a wrapper for the <feFuncG> SVG element.
For detailed attribute info see:
https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feFuncG

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The children of this component.

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- amplitude (string | number; optional):
    The amplitude attribute controls the amplitude of the gamma
    function  of a component transfer element when its type attribute
    is gamma.You can use this attribute with the following  SVG
    elements:.

- aria-* (string; optional):
    A wildcard aria attribute.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- data-* (string; optional):
    A wildcard data attribute.

- exponent (string | number; optional):
    The exponent attribute defines the exponent of the gamma
    function.You  can use this attribute with the following SVG
    elements:If  the type attribute of the component element is set to
    gamma, this value specifies the exponent of the gamma  function.

- intercept (string | number; optional):
    The intercept attribute defines the intercept of the linear
    function  of color component transfers when the type attribute is
    set to linear.You can use this attribute with the following  SVG
    elements:.

- key (string; optional):
    A unique identifier for the component, used to improve performance
    by React.js while rendering components See
    https://reactjs.org/docs/lists-and-keys.html for more info.

- loading_state (dict; optional):
    Object that holds the loading state object coming from
    dash-renderer.

    `loading_state` is a dict with keys:

    - component_name (string; optional):
        Holds the name of the component that is loading.

    - is_loading (boolean; optional):
        Determines if the component is loading or not.

    - prop_name (string; optional):
        Holds which property is loading.

- n_clicks (number; default 0):
    An integer that represents the number of times that this element
    has been clicked on.

- n_clicks_timestamp (number; default -1):
    An integer that represents the time (in ms since 1970) at which
    n_clicks changed. This can be used to tell which button was
    changed most recently.

- role (string; optional):
    The ARIA role attribute.

- tableValues (string | number; optional):
    The tableValues attribute defines a list of numbers defining  a
    lookup table of values for a for a color component transfer
    function.You can use this attribute with the following  SVG
    elements:This value holds a comma- and/or space-separated  list of
    <number>s, which define a lookup table for the  color component
    transfer function. Each number can be  between 0 and 1.An empty
    list results in an identity transfer  function.

- x (string | number; optional):
    The x attribute defines a x-axis coordinate in the user coordinate
    system.You can use this attribute with the following SVG
    elements:Warning: As of SVG2 <altGlyph> is deprecated  and
    shouldn't be used.For <altGlyph>, x defines the x-axis  coordinate
    of the alternate glyph.For <feBlend>, x defines  the minimum x
    coordinate for the rendering area of the  primitive.For
    <feColorMatrix>, x defines the minimum x  coordinate for the
    rendering area of the primitive.For  <feComponentTransfer>, x
    defines the minimum x coordinate  for the rendering area of the
    primitive.For <feComposite>,  x defines the minimum x coordinate
    for the rendering area  of the primitive.For <feConvolveMatrix>, x
    defines the  minimum x coordinate for the rendering area of the
    primitive.For  <feDiffuseLighting>, x defines the minimum x
    coordinate  for the rendering area of the primitive.For
    <feDisplacementMap>,  x defines the minimum x coordinate for the
    rendering area  of the primitive.For <feDropShadow>, x defines the
    minimum  x coordinate for the rendering area of the primitive.For
    <feFlood>, x defines the minimum x coordinate for the  rendering
    area of the primitive.For <feFuncA>, x defines  the minimum x
    coordinate for the rendering area of the  primitive.For <feFuncB>,
    x defines the minimum x coordinate  for the rendering area of the
    primitive.For <feFuncG>,  x defines the minimum x coordinate for
    the rendering area  of the primitive.For <feFuncR>, x defines the
    minimum  x coordinate for the rendering area of the primitive.For
    <feGaussianBlur>, x defines the minimum x coordinate for  the
    rendering area of the primitive.For <feImage>, x defines  the
    minimum x coordinate for the rendering area of the  primitive.For
    <feMerge>, x defines the minimum x coordinate  for the rendering
    area of the primitive.For <feMergeNode>,  x defines the minimum x
    coordinate for the rendering area  of the primitive.For
    <feMorphology>, x defines the minimum  x coordinate for the
    rendering area of the primitive.For  <feOffset>, x defines the
    minimum x coordinate for the  rendering area of the primitive.For
    <fePointLight>, x  defines the x location for the light source in
    the coordinate  system defined by the primitiveUnits attribute on
    the  <filter> element.For <feSpecularLighting>, x defines the
    minimum x coordinate for the rendering area of the primitive.For
    <feSpotLight>, x defines the x location for the light  source in
    the coordinate system defined by the primitiveUnits  attribute on
    the <filter> element.For <feTile>, x defines  the minimum x
    coordinate for the rendering area of the  primitive.For
    <feTurbulence>, x defines the minimum x  coordinate for the
    rendering area of the primitive.For  <filter>, x defines the x
    coordinate of the upper left  corner for the rendering area of the
    filter.For <foreignObject>,  x defines the  x coordinate of the
    upper left corner of  its viewport.Note: Starting with SVG2, x is
    a Geometry  Property meaning this attribute can also be used as a
    CSS property for <foreignObject>.Warning: As of SVG2 <glyphRef>
    is deprecated and shouldn't be used.For <glyphRef>, x  defines the
    x-axis coordinate of the glyph.For <image>,  x defines the  x
    coordinate of the upper left corner of  the image.Note: Starting
    with SVG2, x is a Geometry Property  meaning this attribute can
    also be used as a CSS property  for images.For <mask>, x defines
    the  x coordinate of  the upper left corner of its area of effect.
    The exact  effect of this attribute is influenced by the maskUnits
    attribute.For <pattern>, x defines the  x coordinate of  the upper
    left corner of the tile pattern. The exact effect  of this
    attribute is influenced by the patternUnits and  patternTransform
    attributes.For <rect>, x defines the   x coordinate of the upper
    left corner of the shape.Note:  Starting with SVG2, x is a
    Geometry Property meaning this  attribute can also be used as a
    CSS property for rectangles.For  <svg>, x defines the  x
    coordinate of the upper left corner  of its viewport.Note:
    Starting with SVG2, x is a Geometry  Property meaning this
    attribute can also be used as a  CSS property for <svg>.For
    <text>, if it contain a single  value, x defines the x coordinate
    on where the content  text position must be placed. The content
    text position  is usually a point on the baseline of the first
    line of  text. The exact content text position is influenced by
    some properties like text-anchor, or direction.If there  are
    multiple values, x defines the x coordinate of each  individual
    glyph from the text. If there are less values  than glyphs, the
    remaining glyphs are placed in the continuity  of the last
    positioned glyph. If there are more values  than glyphs, extra
    values are ignored.Warning: As of SVG2  <tref> is deprecated and
    shouldn't be used.For <tref>,  if it contain a single value, x
    defines the x coordinate  on where the content text position must
    be placed. The  content text position is usually a point on the
    baseline  of the first line of text. The exact content text
    position  is influenced by some properties like text-anchor, or
    direction.If there are multiple values, x defines the  x
    coordinate of each individual glyph from the text. If  there are
    less values than glyphs, the remaining glyphs  are placed in the
    continuity of the last positioned glyph.  If there are more values
    than glyphs, extra values are  ignored.For <tspan>, if it contain
    a single value, x defines  the x coordinate on where the content
    text position must  be placed. The content text position is
    usually a point  on the baseline of the first line of text. The
    exact content  text position is influenced by some properties like
    text-anchor,  or direction.If there are multiple values, x defines
    the  x coordinate of each individual glyph from the text. If
    there are less values than glyphs, the remaining glyphs  are
    placed in the continuity of the last positioned glyph.  If there
    are more values than glyphs, extra values are  ignored.For <use>,
    x defines the  x coordinate of the  upper left corner of the
    referenced element.Note: Starting  with SVG2, x is a Geometry
    Property meaning this attribute  can also be used as a CSS
    property for used elements.

- y (string | number; optional):
    The y attribute defines a y-axis coordinate in the user coordinate
    system.You can use this attribute with the following SVG
    elements:Warning: As of SVG2 <altGlyph> is deprecated  and
    shouldn't be used.For <altGlyph>, y defines the y-axis  coordinate
    of the alternate glyph.For <feBlend>, y defines  the minimum y
    coordinate for the rendering area of the  primitive.For
    <feColorMatrix>, y defines the minimum y  coordinate for the
    rendering area of the primitive.For  <feComponentTransfer>, y
    defines the minimum y coordinate  for the rendering area of the
    primitive.For <feComposite>,  y defines the minimum y coordinate
    for the rendering area  of the primitive.For <feConvolveMatrix>, y
    defines the  minimum y coordinate for the rendering area of the
    primitive.For  <feDiffuseLighting>, y defines the minimum y
    coordinate  for the rendering area of the primitive.For
    <feDisplacementMap>,  y defines the minimum y coordinate for the
    rendering area  of the primitive.For <feDropShadow>, y defines the
    minimum  y coordinate for the rendering area of the primitive.For
    <feFlood>, y defines the minimum y coordinate for the  rendering
    area of the primitive.For <feFuncA>, y defines  the minimum y
    coordinate for the rendering area of the  primitive.For <feFuncB>,
    y defines the minimum y coordinate  for the rendering area of the
    primitive.For <feFuncG>,  y defines the minimum y coordinate for
    the rendering area  of the primitive.For <feFuncR>, y defines the
    minimum  y coordinate for the rendering area of the primitive.For
    <feGaussianBlur>, y defines the minimum y coordinate for  the
    rendering area of the primitive.For <feImage>, y defines  the
    minimum y coordinate for the rendering area of the  primitive.For
    <feMerge>, y defines the minimum y coordinate  for the rendering
    area of the primitive.For <feMergeNode>,  y defines the minimum y
    coordinate for the rendering area  of the primitive.For
    <feMorphology>, y defines the minimum  y coordinate for the
    rendering area of the primitive.For  <feOffset>, y defines the
    minimum y coordinate for the  rendering area of the primitive.For
    <fePointLight>, y  defines the y location for the light source in
    the coordinate  system defined by the primitiveUnits attribute on
    the  <filter> element.For <feSpecularLighting>, y defines the
    minimum y coordinate for the rendering area of the primitive.For
    <feSpotLight>, y defines the y location for the light  source in
    the coordinate system defined by the primitiveUnits  attribute on
    the <filter> element.For <feTile>, y defines  the minimum y
    coordinate for the rendering area of the  primitive.For
    <feTurbulence>, y defines the minimum y  coordinate for the
    rendering area of the primitive.For  <filter>, y defines the y
    coordinate of the upper left  corner for the rendering area of the
    filter.For <foreignObject>,  y defines the y coordinate of the
    upper left corner of  its viewport.Note: Starting with SVG2, y is
    a Geometry  Property meaning this attribute can also be used as a
    CSS property for <foreignObject>.Warning: As of SVG2 <glyphRef>
    is deprecated and shouldn't be used.For <glyphRef>, y  defines the
    y-axis coordinate of the glyph.For <image>,  y defines the y
    coordinate of the upper left corner of  the image.Note: Starting
    with SVG2, y is a Geometry Property  meaning this attribute can
    also be used as a CSS property  for images.For <mask>, y defines
    the y coordinate of the  upper left corner of its area of effect.
    The exact effect  of this attribute is influenced by the maskUnits
    attribute.For  <pattern>, y defines the y coordinate of the upper
    left  corner of the tile pattern. The exact effect of this
    attribute  is influenced by the patternUnits and patternTransform
    attributes.For <rect>, y defines the y coordinate of the  upper
    left corner of the shape.Note: Starting with SVG2,  y is a
    Geometry Property meaning this attribute can also  be used as a
    CSS property for rectangles.For <svg>, y  defines the y coordinate
    of the upper left corner of its  viewport.Note: Starting with
    SVG2, y is a Geometry Property  meaning this attribute can also be
    used as a CSS property  for <svg>.For <text>, if it contain a
    single value, y  defines the y coordinate on where the content
    text position  must be placed. The content text position is
    usually a  point on the baseline of the first line of text. The
    exact  content text position is influenced by some properties
    like text-anchor, or direction.If there are multiple values,  y
    defines the y coordinate of each individual glyph from  the text.
    If there are less values than glyphs, the remaining  glyphs are
    placed in the continuity of the last positioned  glyph. If there
    are more values than glyphs, extra values  are ignored.Warning: As
    of SVG2 <tref> is deprecated and  shouldn't be used.For <tref>, if
    it contain a single value,  y defines the y coordinate on where
    the content text position  must be placed. The content text
    position is usually a  point on the baseline of the first line of
    text. The exact  content text position is influenced by some
    properties  like text-anchor, or direction.If there are multiple
    values,  y defines the y coordinate of each individual glyph from
    the text. If there are less values than glyphs, the remaining
    glyphs are placed in the continuity of the last positioned  glyph.
    If there are more values than glyphs, extra values  are
    ignored.For <tspan>, if it contain a single value,  y defines the
    y coordinate on where the content text position  must be placed.
    The content text position is usually a  point on the baseline of
    the first line of text. The exact  content text position is
    influenced by some properties  like text-anchor, or direction.If
    there are multiple values,  y defines the y coordinate of each
    individual glyph from  the text. If there are less values than
    glyphs, the remaining  glyphs are placed in the continuity of the
    last positioned  glyph. If there are more values than glyphs,
    extra values  are ignored.For <use>, y defines the y coordinate of
    the  upper left corner of the referenced element.Note: Starting
    with SVG2, y is a Geometry Property meaning this attribute  can
    also be used as a CSS property for used elements."""
    @_explicitize_args
    def __init__(self, children=None, id=Component.UNDEFINED, n_clicks=Component.UNDEFINED, n_clicks_timestamp=Component.UNDEFINED, key=Component.UNDEFINED, role=Component.UNDEFINED, amplitude=Component.UNDEFINED, exponent=Component.UNDEFINED, intercept=Component.UNDEFINED, tableValues=Component.UNDEFINED, x=Component.UNDEFINED, y=Component.UNDEFINED, className=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'amplitude', 'aria-*', 'className', 'data-*', 'exponent', 'intercept', 'key', 'loading_state', 'n_clicks', 'n_clicks_timestamp', 'role', 'tableValues', 'x', 'y']
        self._type = 'FeFuncG'
        self._namespace = 'dash_svg'
        self._valid_wildcard_attributes =            ['data-', 'aria-']
        self.available_properties = ['children', 'id', 'amplitude', 'aria-*', 'className', 'data-*', 'exponent', 'intercept', 'key', 'loading_state', 'n_clicks', 'n_clicks_timestamp', 'role', 'tableValues', 'x', 'y']
        self.available_wildcard_properties =            ['data-', 'aria-']
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(FeFuncG, self).__init__(children=children, **args)
