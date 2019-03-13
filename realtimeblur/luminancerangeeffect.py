from kivy.properties import NumericProperty, ListProperty
from kivy.uix.effectwidget import AdvancedEffectBase

effect_string = '''
uniform vec2 effectAreaPos;
uniform vec2 effectAreaSize;
uniform float rangeReduction;

// Values from "Graphics Shaders: Theory and Practice" by Bailey and Cunningham
const vec3 luminanceWeighting = vec3(0.2125, 0.7154, 0.0721);

float insideBox(vec2 v, vec2 bottomLeft, vec2 topRight) {
    vec2 s = step(bottomLeft, v) - step(topRight, v);
    return s.x * s.y;   
}

vec4 effect(vec4 color, sampler2D texture, vec2 tex_coords, vec2 coords) {
    vec2 uv = vec2(coords / resolution);
    float t = insideBox(coords, effectAreaPos, effectAreaPos+effectAreaSize);
    float luminance = dot(color.rgb, luminanceWeighting);
    float luminanceRatio = ((0.5 - luminance) * rangeReduction);
    return t*vec4((color.rgb) + (luminanceRatio), color.w)+(1.0-t)*color;
}
'''

class LuminanceRangeEffect(AdvancedEffectBase):
    effect_region = ListProperty([0.0, 0.0, 0.0, 0.0])

    range_reduction = NumericProperty(0.6)

    def __init__(self, *args, **kwargs):
        super(LuminanceRangeEffect, self).__init__(*args, **kwargs)

        self.uniforms = {'effectAreaPos': [0.0, 0.0],
                         'effectAreaSize': [0.0, 0.0],
                         'rangeReduction': 1.0}

        self.glsl = effect_string

    def on_effect_region(self, instance, region):
        if len(region) == 4:
            self.uniforms['effectAreaPos'] = region[:2]
            self.uniforms['effectAreaSize'] = region[2:]

    def on_range_reduction(self, instance, reduction):
        self.uniforms['rangeReduction'] = reduction