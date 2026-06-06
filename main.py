from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFillRoundFlatButton
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
import time

try:
    from kivymd.uix.appbar import MDTopAppBar
except ImportError:
    from kivymd.uix.toolbar import MDTopAppBar


class InterfazMacro(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.coordenadas = {
            "agacharse": None,
            "pared": None,
            "disparo_izq": None
        }

        self.paso_calibracion = 0

        layout = MDBoxLayout(orientation='vertical')

        toolbar = MDTopAppBar(title="FF Macro - Sistema de Doble Combo")
        layout.add_widget(toolbar)

        contenido = MDBoxLayout(orientation='vertical', padding=20, spacing=15)

        self.label_estado = MDLabel(
            text="Presiona el botón gris para iniciar el mapeo de tu HUD.",
            halign="center",
            theme_text_color="Secondary",
            font_style="Body1"
        )
        contenido.add_widget(self.label_estado)

        self.btn_capturar = MDFillRoundFlatButton(
            text="INICIAR CONFIGURACIÓN HUD",
            pos_hint={"center_x": 0.5},
            md_bg_color=(0.3, 0.3, 0.3, 1),
            on_release=self.iniciar_mapeo
        )
        contenido.add_widget(self.btn_capturar)

        self.btn_combo1 = MDRaisedButton(
            text="PROBAR COMBO PARED AGACHADO",
            pos_hint={"center_x": 0.5},
            md_bg_color=(0.9, 0.1, 0.1, 1),
            on_release=self.ejecutar_combo_pared
        )
        contenido.add_widget(self.btn_combo1)

        self.btn_combo2 = MDRaisedButton(
            text="PROBAR COMBO RESET DE PRECISIÓN (B)",
            pos_hint={"center_x": 0.5},
            md_bg_color=(0.1, 0.5, 0.9, 1),
            on_release=self.ejecutar_combo_reset_precision
        )
        contenido.add_widget(self.btn_combo2)

        layout.add_widget(contenido)
        self.add_widget(layout)

    def iniciar_mapeo(self, instance):
        self.paso_calibracion = 1
        self.btn_capturar.md_bg_color = (1, 0.5, 0, 1)
        self.label_estado.text = "🎯 PASO 1: Haz clic donde tienes el botón de AGACHARSE"

    def on_touch_down(self, touch):
        if super().on_touch_down(touch):
            return True

        if self.paso_calibracion == 1:
            self.coordenadas["agacharse"] = (round(touch.x, 1), round(touch.y, 1))
            self.paso_calibracion = 2
            self.label_estado.text = "🎯 PASO 2: Haz clic donde tienes el botón de la PARED GLOO"
            return True

        elif self.paso_calibracion == 2:
            self.coordenadas["pared"] = (round(touch.x, 1), round(touch.y, 1))
            self.paso_calibracion = 3
            self.label_estado.text = "🎯 PASO 3: Haz clic donde tienes el botón de DISPARO"
            return True

        elif self.paso_calibracion == 3:
            self.coordenadas["disparo_izq"] = (round(touch.x, 1), round(touch.y, 1))
            self.paso_calibracion = 0
            self.btn_capturar.md_bg_color = (0, 0.6, 0, 1)
            self.label_estado.text = "✅ ¡HUD Calibrado con éxito! Ya puedes probar ambos combos abajo."
            return True

    def simular_toque(self, x, y):
        """Simula un toque real en la pantalla usando el sistema de eventos de Kivy."""
        from kivy.input.providers.mouse import MouseMotionEvent
        touch = MouseMotionEvent(None, "macro_touch", (x, y))
        touch.x = x
        touch.y = y
        touch.pos = (x, y)
        self.dispatch("on_touch_down", touch)
        time.sleep(0.05)
        self.dispatch("on_touch_up", touch)

    def ejecutar_combo_pared(self, instance):
        if not self.coordenadas["agacharse"] or not self.coordenadas["pared"] or not self.coordenadas["disparo_izq"]:
            self.label_estado.text = "⚠️ Configura los 3 botones primero."
            return

        self.label_estado.text = "🔥 Ejecutando: Pared Agachado..."

        def _ejecutar(dt):
            ax, ay = self.coordenadas["agacharse"]
            px, py = self.coordenadas["pared"]
            dx, dy = self.coordenadas["disparo_izq"]

            self.simular_toque(ax, ay)   # 1. Agacharse
            time.sleep(0.02)
            self.simular_toque(px, py)   # 2. Pared Gloo
            time.sleep(0.02)
            self.simular_toque(dx, dy)   # 3. Disparo

            self.label_estado.text = "✅ Combo Pared ejecutado: Agacharse → Pared → Disparo"

        Clock.schedule_once(_ejecutar, 0.1)

    def ejecutar_combo_reset_precision(self, instance):
        if not self.coordenadas["agacharse"] or not self.coordenadas["disparo_izq"]:
            self.label_estado.text = "⚠️ Configura los botones primero (requiere Disparo y Agacharse)."
            return

        self.label_estado.text = "⚡ Ejecutando: Reset de Precisión..."

        def _ejecutar(dt):
            ax, ay = self.coordenadas["agacharse"]
            dx, dy = self.coordenadas["disparo_izq"]

            self.simular_toque(dx, dy)   # 1. Disparo (inicia ráfaga)
            time.sleep(0.05)
            self.simular_toque(ax, ay)   # 2. Agacharse (baja retícula)
            time.sleep(0.03)
            self.simular_toque(ax, ay)   # 3. Levantarse (mira cerrada)

            self.label_estado.text = "✅ Combo Reset B ejecutado: Disparo → Agachar → Levantar"

        Clock.schedule_once(_ejecutar, 0.1)


class MacroApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return InterfazMacro()


if __name__ == "__main__":
    MacroApp().run()
