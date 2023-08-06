# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class FeTurbulence(Component):
    """A FeTurbulence component.
FeTurbulence is a wrapper for the <feTurbulence> SVG element.
For detailed attribute info see:
https://developer.mozilla.org/en-US/docs/Web/SVG/Element/feTurbulence

Keyword arguments:

- children (a list of or a singular dash component, string or number; optional):
    The children of this component.

- id (string; optional):
    The ID of this component, used to identify dash components in
    callbacks. The ID needs to be unique across all of the components
    in an app.

- aria-* (string; optional):
    A wildcard aria attribute.

- baseFrequency (string | number; optional):
    The baseFrequency attribute represents the base frequency
    parameter  for the noise function of the <feTurbulence> filter
    primitive.You  can use this attribute with the following SVG
    elements:If  two numbers are provided, the first one represents
    the  base frequency in the horizontal direction and the second
    one the base frequency in the vertical direction. If one  number
    is provided, then that value is used for both x  and y.Negative
    values are forbidden.BCD tables only load  in the browser.

- className (string; optional):
    Often used with CSS to style elements with common properties.

- colorInterpolationFilters (a value equal to: '"auto"|"inherit"|"linearRGB"|"sRGB"' | boolean; optional):
    The color-interpolation-filters attribute specifies the color
    space for imaging operations performed via filter effects.Note:
    This property just has an affect on filter operations.  Therefore,
    it has no effect on filter primitives like  <feOffset>, <feImage>,
    <feTile> or <feFlood>.color-interpolation-filters  has a different
    initial value than color-interpolation.
    color-interpolation-filters has an initial value of linearRGB,
    whereas color-interpolation has an initial value of sRGB.  Thus,
    in the default case, filter effects operations occur  in the
    linearRGB color space, whereas all other color  interpolations
    occur by default in the sRGB color space.It  has no affect on
    filter functions, which operate in the  sRGB color space.Note: As
    a presentation attribute, color-interpolation-filters  can be used
    as a CSS property.You can use this attribute  with the following
    SVG elements:Indicates that the user  agent can choose either the
    sRGB or linearRGB spaces for  color interpolation. This option
    indicates that the author  doesn't require that color
    interpolation occur in a particular  color space.Indicates that
    color interpolation should  occur in the sRGB color
    space.Indicates that color interpolation  should occur in the
    linearized RGB color space as described  in the sRGB
    specification.BCD tables only load in the  browser.

- data-* (string; optional):
    A wildcard data attribute.

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

- numOctaves (string | number; optional):
    The numOctaves attribute defines the number of octaves for the
    noise function of the <feTurbulence> primitive.   An octave  is a
    noise function defined by its frequency and amplitude.  A
    turbulence is built by accumulating several octaves  with
    increasing frequencies and decreasing amplitudes.    The higher
    the number of octaves, the more natural the  noise looks. Though
    more octaves also require more calculations,  resulting in a
    negative impact on performance. You can  use this attribute with
    the following SVG elements:Defines  the number of octaves.
    Negative values are forbidden.BCD  tables only load in the
    browser.

- result (string; optional):
    The result attribute defines the assigned name for this filter
    primitive. If supplied, then graphics that result from  processing
    this filter primitive can be referenced by  an in attribute on a
    subsequent filter primitive within  the same <filter> element. If
    no value is provided, the  output will only be available for
    re-use as the implicit  input into the next filter primitive if
    that filter primitive  provides no value for its in attribute.You
    can use this  attribute with the following SVG elements:This value
    is  a <custom-ident> and defines the name for the filter
    primitive.  It is only meaningful within a given <filter> element
    and thus has only local scope. It is legal for the same
    <filter-primitive-reference> to appear multiple times  within the
    same <filter> element. When referenced, this  value will use the
    closest preceding filter primitive  with the given result.

- role (string; optional):
    The ARIA role attribute.

- seed (string | number; optional):
    The seed attribute represents the starting number for the pseudo
    random number generator of the <feTurbulence> filter primitive.You
    can use this attribute with the following SVG elements:BCD  tables
    only load in the browser.

- stitchTiles (string | number; optional):
    The stitchTiles attribute defines how the Perlin Noise tiles
    behave at the border.You can use this attribute with the
    following SVG elements:This value indicates that no attempt  is
    made to achieve smooth transitions at the border of  tiles which
    contain a turbulence function. Sometimes the  result will show
    clear discontinuities at the tile borders.This  value indicates
    that the user agent will automatically  adjust the x and y values
    of the base frequency such that  the <feTurbulence> node’s width
    and height (i.e., the  width and height of the current subregion)
    contain an  integral number of the tile width and height for the
    first  octave.BCD tables only load in the browser.

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
    def __init__(self, children=None, id=Component.UNDEFINED, n_clicks=Component.UNDEFINED, n_clicks_timestamp=Component.UNDEFINED, key=Component.UNDEFINED, role=Component.UNDEFINED, baseFrequency=Component.UNDEFINED, colorInterpolationFilters=Component.UNDEFINED, numOctaves=Component.UNDEFINED, result=Component.UNDEFINED, seed=Component.UNDEFINED, stitchTiles=Component.UNDEFINED, x=Component.UNDEFINED, y=Component.UNDEFINED, className=Component.UNDEFINED, loading_state=Component.UNDEFINED, **kwargs):
        self._prop_names = ['children', 'id', 'aria-*', 'baseFrequency', 'className', 'colorInterpolationFilters', 'data-*', 'key', 'loading_state', 'n_clicks', 'n_clicks_timestamp', 'numOctaves', 'result', 'role', 'seed', 'stitchTiles', 'x', 'y']
        self._type = 'FeTurbulence'
        self._namespace = 'dash_svg'
        self._valid_wildcard_attributes =            ['data-', 'aria-']
        self.available_properties = ['children', 'id', 'aria-*', 'baseFrequency', 'className', 'colorInterpolationFilters', 'data-*', 'key', 'loading_state', 'n_clicks', 'n_clicks_timestamp', 'numOctaves', 'result', 'role', 'seed', 'stitchTiles', 'x', 'y']
        self.available_wildcard_properties =            ['data-', 'aria-']
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(FeTurbulence, self).__init__(children=children, **args)
