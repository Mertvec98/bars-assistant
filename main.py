
import os
import math
import sqlite3
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse
from kivy.clock import Clock
from kivy.core.window import Window

# Проверяем, запущено ли приложение как реальный APK на Android
try:
    from jnius import autoclass
    from android.permissions import request_permissions, Permission
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
    Locale = autoclass('java.util.Locale')
    android_ready = True
except:
    android_ready = False

# Защищенная папка БАРСА в памяти телефона
BART_DIR = "/storage/emulated/0/Download/Bars_Data"
if not os.path.exists(BART_DIR):
    os.makedirs(BART_DIR)

db_path = os.path.join(BART_DIR, "bars_memory.db")
tts_engine = None

def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS conversation (id INTEGER PRIMARY KEY AUTOINCREMENT, role TEXT, message TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS creator_info (key TEXT PRIMARY KEY, value TEXT)')
    cursor.execute("INSERT OR IGNORE INTO creator_info (key, value) VALUES ('name', 'Адам')")
    conn.commit()
    conn.close()

class BarsBrain(RelativeLayout):
    def __init__(self, **kwargs):
        super(BarsBrain, self).__init__(**kwargs)
        Window.clearcolor = (0.04, 0.06, 0.11, 1)
        
        # Когда этот код соберется в APK, он сам принудительно откроет микрофон!
        if android_ready:
            request_permissions([Permission.RECORD_AUDIO, Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])
            
        self.angle = 0
        self.base_size = 300  
        self.current_size = self.base_size
        
        # Наш футуристичный статус
        self.status_label = Label(
            text="БАРС: Офлайн-ядро запущено\nНажми на сферу для вызова ИИ",
            font_size='20sp',
            bold=True,
            halign='center',
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.23}
        )
        self.add_widget(self.status_label)
        
        # Пульсирующий эквалайзер
        with self.canvas:
            self.neon_color = Color(0, 1, 0.8, 1) 
            self.ellipse = Ellipse(pos=(0, 0), size=(self.current_size, self.current_size))
            
        self.bind(size=self.update_ellipse_position)
        Clock.schedule_interval(self.animate_pulse, 1.0 / 60.0)
        
        # Кнопка на сфере
        self.btn = Button(background_color=(0,0,0,0), size_hint=(None, None), size=(300, 300), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.btn.bind(on_press=self.activate_bars)
        self.add_widget(self.btn)
        
        Clock.schedule_once(self.say_hello, 1.5)

    def update_ellipse_position(self, *args):
        self.ellipse.pos = (self.center_x - self.current_size / 2, self.center_y - self.current_size / 2)

    def animate_pulse(self, dt):
        self.angle += 0.05
        pulse_factor = math.sin(self.angle) * 15 
        self.current_size = self.base_size + pulse_factor
        self.ellipse.size = (self.current_size, self.current_size)
        self.ellipse.pos = (self.center_x - self.current_size / 2, self.center_y - self.current_size / 2)

    def say_hello(self, dt):
        self.speak("Слушаю тебя, Создатель Адам. Система полностью автономна.")

    def speak(self, text):
        global tts_engine
        # Используем встроенный системный мужской голос телефона!
        if android_ready and tts_engine:
            tts_engine.speak(text, TextToSpeech.QUEUE_FLUSH, None, None)
        print(f"[БАРС]: {text}")

    def activate_bars(self, instance):
        self.status_label.text = "БАРС: Слушаю приказ..."
        self.speak("Приказ принят")

class BartApp(App):
    def build(self):
        global tts_engine
        init_db()
        if android_ready:
            activity = PythonActivity.mActivity
            tts_engine = TextToSpeech(activity, None)
            # Насильно ставим русский язык (телефон автоматически выберет твой системный мужской голос)
            tts_engine.setLanguage(Locale("ru"))
        return BarsBrain()

if __name__ == '__main__':
    BartApp().run()
