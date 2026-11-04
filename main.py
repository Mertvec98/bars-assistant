from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class BarsAssistant(BoxLayout):
    def __init__(self, **kwargs):
        super(BarsAssistant, self).__init__(**kwargs)
        self.orientation = 'vertical'
        
        self.lbl = Label(text="[БАРС ИИ]\nСистема успешно скомпилирована!", font_size='24sp', halign='center')
        self.add_widget(self.lbl)
        
        self.btn = Button(text="Активировать офлайн-мозг", size_hint=(1, 0.2))
        self.btn.bind(on_press=self.test_ai)
        self.add_widget(self.btn)

    def test_ai(self, instance):
        self.lbl.text = "Барс: Я запущен прямо из твоего личного APK!"

class BarsApp(App):
    def build(self):
        return BarsAssistant()

if __name__ == '__main__':
    BarsApp().run()
