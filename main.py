import re, threading, requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock

ID = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"

class Ana(BoxLayout):
    def __init__(self, **kw):
        super().__init__(orientation="vertical", padding=20, spacing=15, **kw)
        self.girdi = TextInput(hint_text="Suno linkini yapıştır",
                               multiline=False, size_hint_y=None, height=120)
        self.btn = Button(text="İndir", size_hint_y=None, height=140)
        self.btn.bind(on_press=self.baslat)
        self.durum = Label(text="")
        for w in (self.girdi, self.btn, self.durum):
            self.add_widget(w)

    def yaz(self, t):
        Clock.schedule_once(lambda dt: setattr(self.durum, "text", t))

    def baslat(self, *_):
        threading.Thread(target=self.indir, daemon=True).start()

    def indir(self):
        m = re.search(ID, self.girdi.text)
        if not m:
            return self.yaz("Geçersiz link")
        sid = m.group(0)
        self.yaz("İndiriliyor...")
        try:
            r = requests.get(f"https://cdn1.suno.ai/{sid}.mp3", timeout=60)
            r.raise_for_status()
            yol = f"/storage/emulated/0/Download/suno_{sid[:8]}.mp3"
            open(yol, "wb").write(r.content)
            self.yaz("İndirildi: Download/suno_" + sid[:8] + ".mp3")
        except Exception as e:
            self.yaz("Hata: " + str(e))

class SunoApp(App):
    def build(self):
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE])
        except ImportError:
            pass
        return Ana()

SunoApp().run()
