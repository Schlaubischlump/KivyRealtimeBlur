from kivy.app import App
from kivy.lang import Builder
from realtimeblur import RealtimeBlurWidget

kv = '''
<DragLabel@DragBehavior+Label>:
    canvas.before:
        Color:
            rgb: 1, 0, 0, 1
        Rectangle:
            pos: self.pos
            size: self.size

    drag_rectangle: self.x, self.y, self.width, self.height
    drag_timeout: 10000000
    drag_distance: 0
    color: 0, 0, 0, 1
    pos: 0, 100
    
<DragImage@DragBehavior+AsyncImage>:
    canvas.before:
        Color:
            rgb: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
    drag_rectangle: self.x, self.y, self.width, self.height
    drag_timeout: 10000000
    drag_distance: 0
    pos: 400, 400
    

FloatLayout:
    blur_widget: effect_widget

    canvas.before:
        Color:
            rgb: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
    
    BoxLayout:
        size_hint: 1, 0.1
        
        Slider: 
            min: 0
            max: 5
            value: root.blur_widget.saturation
            on_value:
                root.blur_widget.saturation = self.value
        
        Slider: 
            min: 0
            max: 25
            value: root.blur_widget.blur_radius
            on_value:
                root.blur_widget.blur_radius = self.value
        
        Slider: 
            size_hint_y: 1
            min: 0
            max: 1
            value: root.blur_widget.range_reduction
            on_value:
                root.blur_widget.range_reduction = self.value
    
    
    RealtimeBlurWidget:
        id: effect_widget
        
        effect_region: self.x, self.height-500, self.width, 500
        
        tint_color: 1, 1, 1, .0
                
        DragLabel:
            size_hint: 0.25, 0.2
            text: 'Drag me'
            
        DragImage:
            size_hint: 0.4, 0.5
            keep_ratio: False
            allow_stretch: True
            source: "https://archive.org/download/PublicDomainImages/Bubbles.jpg"
'''


class TestApp(App):
    def build(self):
        return Builder.load_string(kv)

TestApp().run()
