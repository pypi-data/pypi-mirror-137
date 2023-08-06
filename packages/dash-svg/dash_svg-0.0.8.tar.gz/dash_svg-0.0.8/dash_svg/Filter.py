# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Filter(Component):
    """A Filter component.
Filter is a wrapper for the <filter> SVG element.
For detailed attribute info see:
https://developer.mozilla.org/en-US/docs/Web/SVG/Element/filter

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The children of this component.

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- aria-* (string; optional):
    A wildcard aria attribute.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- data-* (string; optional):
    A wildcard data attribute.

- filterRes (string | number; optional):
    Deprecated: This feature is no longer recommended. Though some
    browsers might still support it, it may have already been  removed
    from the relevant web standards, may be in the  process of being
    dropped, or may only be kept for compatibility  purposes. Avoid
    using it, and update existing code if  possible; see the
    compatibility table at the bottom of  this page to guide your
    decision. Be aware that this feature  may cease to work at any
    time.The filterRes attribute  indicates the width and height of
    the intermediate images  in pixels of a filter primitive.Take care
    when assigning  a non-default value to this attribute. Too small
    of a  value may result in unwanted pixelation in the result.  Too
    large of a value may result in slow processing and  large memory
    usage.Note that negative values or zero values  disable the
    rendering of the element which referenced  the filter.You can use
    this attribute with the following  SVG elements:This value takes
    one or two values, the first  one outlining the resolution in
    horizontal direction,  the second one in vertical direction. If
    only one value  is specified, it is used for both directions.BCD
    tables  only load in the browser.

- filterUnits (string | number; optional):
    The filterUnits attribute defines the coordinate system for the
    attributes x, y, width and height.You can use this attribute  with
    the following SVG elements:x, y, width and height  represent
    values in the current coordinate system that  results from taking
    the current user coordinate system  in place at the time when the
    <filter> element is referenced  (i.e., the user coordinate system
    for the element referencing  the <filter> element via a filter
    attribute).In that case,  x, y, width and height represent
    fractions or percentages  of the bounding box on the referencing
    element.BCD tables  only load in the browser.

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

- primitiveUnits (string | number; optional):
    The primitiveUnits attribute specifies the coordinate system  for
    the various length values within the filter primitives  and for
    the attributes that define the filter primitive  subregion.You can
    use this attribute with the following  SVG elements:This value
    indicates that any length values  within the filter definitions
    represent values in the  current user coordinate system in place
    at the time when  the <filter> element is referenced (i.e., the
    user coordinate  system for the element referencing the <filter>
    element  via a filter attribute).This value indicates that any
    length values within the filter definitions represent  fractions
    or percentages of the bounding box on the referencing  element.BCD
    tables only load in the browser.

- role (string; optional):
    The ARIA role attribute.

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
    def __init__(self, children=None, id=Component.UNDEFINED, n_clicks=Component.UNDEFINED, n_clicks_timestamp=Component.UNDEFINED, key=Component.UNDEFINED, role=Component.UNDEFINED, filterRes=Component.UNDEFINED, filterUnits=Component.UNDEFINED, primitiveUnits=Component.UNDEFINED, x=Component.UNDEFINED, y=Component.UNDEFINED, className=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'aria-*', 'className', 'data-*', 'filterRes', 'filterUnits', 'key', 'loading_state', 'n_clicks', 'n_clicks_timestamp', 'primitiveUnits', 'role', 'x', 'y']
        self._type = 'Filter'
        self._namespace = 'dash_svg'
        self._valid_wildcard_attributes =            ['data-', 'aria-']
        self.available_properties = ['children', 'id', 'aria-*', 'className', 'data-*', 'filterRes', 'filterUnits', 'key', 'loading_state', 'n_clicks', 'n_clicks_timestamp', 'primitiveUnits', 'role', 'x', 'y']
        self.available_wildcard_properties =            ['data-', 'aria-']
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Filter, self).__init__(children=children, **args)
