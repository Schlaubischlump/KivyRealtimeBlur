from math import sqrt, pi, exp
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.effectwidget import AdvancedEffectBase

effect_string = '''
uniform vec2 effectAreaPos;
uniform vec2 effectAreaSize;

vec4 blur(sampler2D inputImageTexture, vec2 inputTextureCoordinate, vec2 res) {{
	vec2 singleStepOffset = 1.0 / res;
	{0}
	vec4 sum = vec4(0.0);
	{1}
	return sum;
}}

float insideBox(vec2 v, vec2 bottomLeft, vec2 topRight) {{
    vec2 s = step(bottomLeft, v) - step(topRight, v);
    return s.x * s.y;   
}}

vec4 effect(vec4 color, sampler2D texture, vec2 tex_coords, vec2 coords)
{{
    vec2 uv = vec2(coords / resolution);
    float t = insideBox(coords, effectAreaPos, effectAreaPos+effectAreaSize);
    return t*blur(texture, uv, resolution) + (1.0-t)*color;
}}
'''



class BlurEffect(AdvancedEffectBase):
    effect_region = ListProperty()

    blur_radius = NumericProperty(5)

    def __init__(self, *args, **kwargs):
        super(BlurEffect, self).__init__(*args, **kwargs)
        self.uniforms = {'effectAreaPos': [0.0, 0.0],
                         'effectAreaSize': [0.0, 0.0]}
        self.glsl = self.create_glsl(int(self.blur_radius))

    def create_glsl(self, radius, sigma=10.0):

        def normal_gaussian_weights():
            # generate the normal Gaussian weights for a given sigma
            standard_gaussian_weights = []
            sum_of_weights = 0.0
            for current_gaussian_weight_index in range(radius + 1):
                standard_gaussian_weights.append((1.0 / sqrt(2.0 * pi * pow(sigma, 2.0))) * exp(
                    -(current_gaussian_weight_index * current_gaussian_weight_index) / (2.0 * (sigma * sigma))))

                if current_gaussian_weight_index == 0:
                    sum_of_weights += standard_gaussian_weights[current_gaussian_weight_index];
                else:
                    sum_of_weights += 2.0 * standard_gaussian_weights[current_gaussian_weight_index];

            # return the normalize weights
            return list(map(lambda x: x/sum_of_weights, standard_gaussian_weights))

        weights = normal_gaussian_weights()

        shader_str_first = ""
        shader_str_second = ""

        for current_blur_coordinate_index in range(radius*2+1):
            offset_from_center = current_blur_coordinate_index - radius
            if offset_from_center < 0:
                shader_str_first += "vec2 off{0} = inputTextureCoordinate.xy - singleStepOffset * {1};\n".format(
                    current_blur_coordinate_index, -float(offset_from_center)
                )
                shader_str_second += "sum += texture2D(inputImageTexture, off{0}) * {1};\n".format(
                    current_blur_coordinate_index, weights[-offset_from_center]
                )
            elif offset_from_center > 0:
                shader_str_first += "vec2 off{0} = inputTextureCoordinate.xy - singleStepOffset * {1};\n".format(
                    current_blur_coordinate_index, float(offset_from_center)
                )
                shader_str_second += "sum += texture2D(inputImageTexture, off{0}) * {1};\n".format(
                    current_blur_coordinate_index, weights[offset_from_center]
                )
            else:
                shader_str_first += "vec2 off{0} = inputTextureCoordinate.xy;\n".format(current_blur_coordinate_index)
                shader_str_second += "sum += texture2D(inputImageTexture, off{0}) * {1};\n".format(
                    current_blur_coordinate_index, weights[offset_from_center]
                )
        return effect_string.format(shader_str_first, shader_str_second)

    def on_fbo(self, instance, fbo):
        tex = fbo.texture
        tex.mag_filter = "linear"
        tex.min_filter = "linear"
        tex.wrap = "repeat"

    def on_effect_region(self, instance, region):
        if len(region) == 4:
            self.uniforms['effectAreaPos'] = region[:2]
            self.uniforms['effectAreaSize'] = region[2:]

    def on_blur_radius(self, instance, radius):
        self.glsl = self.create_glsl(int(radius))