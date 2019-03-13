from kivy.properties import ListProperty, NumericProperty
from kivy.uix.effectwidget import AdvancedEffectBase

effect_string = '''
uniform vec2 effectAreaPos;
uniform vec2 effectAreaSize;
uniform float saturation;

// Values from "Graphics Shaders: Theory and Practice" by Bailey and Cunningham
const vec3 luminanceWeighting = vec3(0.2125, 0.7154, 0.0721);

float insideBox(vec2 v, vec2 bottomLeft, vec2 topRight) {
    vec2 s = step(bottomLeft, v) - step(topRight, v);
    return s.x * s.y;   
}

vec4 effect(vec4 color, sampler2D texture, vec2 tex_coords, vec2 coords) {
    vec2 uv = vec2(4.0*coords / resolution);
    float t = insideBox(coords, effectAreaPos, effectAreaPos+effectAreaSize);
    float luminance = dot(color.rgb, luminanceWeighting);
    vec3 greyScaleColor = vec3(luminance);
    return t*vec4(mix(greyScaleColor, color.rgb, saturation), color.w)+(1.0-t)*color;
}
'''


class SaturationEffect(AdvancedEffectBase):
    effect_region = ListProperty([0.0, 0.0, 0.0, 0.0])

    saturation = NumericProperty(1.0)

    def __init__(self, *args, **kwargs):
        super(SaturationEffect, self).__init__(*args, **kwargs)

        self.uniforms = {'effectAreaPos': [0.0, 0.0],
                         'effectAreaSize': [0.0, 0.0],
                         'saturation': 1.0}

        self.glsl = effect_string

    def on_effect_region(self, instance, region):
        if len(region) == 4:
            self.uniforms['effectAreaPos'] = region[:2]
            self.uniforms['effectAreaSize'] = region[2:]

    def on_saturation(self, instance, saturation):
        self.uniforms['saturation'] = saturation