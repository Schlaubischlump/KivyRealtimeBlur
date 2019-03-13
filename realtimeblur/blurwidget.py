from kivy.lang import Builder
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.effectwidget import EffectWidget

from .blureffect import BlurEffect
from .saturationeffect import SaturationEffect
from .luminancerangeeffect import LuminanceRangeEffect

Builder.load_string('''
<RealtimeBlurWidget>:
    tint_color: 1, 1, 1, 0

    canvas.after:
        Color:
            rgba: self.tint_color
        Rectangle:
            pos: self.effect_region[:2]
            size: self.effect_region[2:]
''')


class RealtimeBlurWidget(EffectWidget):
    effect_region = ListProperty([0, 0, 0, 0])

    blur_radius = NumericProperty(14.0)

    saturation = NumericProperty(0.8)

    range_reduction = NumericProperty(1.0)

    tint_color = ListProperty([0, 0, 0, 0])

    def __init__(self, *args, **kwargs):
        super(RealtimeBlurWidget, self).__init__(*args, **kwargs)
        self.saturate_effect = SaturationEffect(saturation=self.saturation)
        self.luminance_effect = LuminanceRangeEffect(range_reduction=self.range_reduction)
        self.blur_effect = BlurEffect(blur_radius=self.blur_radius)
        self.effects = [self.saturate_effect, self.blur_effect, self.luminance_effect]
        self.update()

    def update(self):
        self.blur_effect.blur_radius = int(self.blur_radius)
        self.saturate_effect.saturation = float(self.saturation)
        self.luminance_effect.range_reduction = float(self.range_reduction)

    def on_blur_radius(self, instance, radius):
        self.blur_effect.blur_radius = int(radius)

    def on_saturation(self, instance, saturation):
        self.saturate_effect.saturation = float(saturation)

    def on_range_reduction(self, instance, reduction):
        self.luminance_effect.range_reduction = float(reduction)

    def on_effect_region(self, instance, region):
        self.saturate_effect.effect_region = map(float, region)
        self.luminance_effect.effect_region = map(float, region)
        self.blur_effect.effect_region = map(float, region)