import os 
from kivy.app import App  # type: ignore 
from kivy.uix.screenmanager import ScreenManager, Screen  # type: ignore 
from kivy.core.window import Window  # type: ignore 
from kivy.uix.boxlayout import BoxLayout  # type: ignore 
from kivy.uix.gridlayout import GridLayout  # type: ignore 
from kivy.uix.label import Label  # type: ignore 
from kivy.uix.textinput import TextInput  # type: ignore 
from kivy.uix.button import Button  # type: ignore 
from kivy.uix.scrollview import ScrollView  # type: ignore 
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle  # type: ignore
from kivy.clock import Clock
# Importar seguridad y módulos funcionales 
from core.security import SecurityManager 
from modules.escalera import RetoEscaleraCalculator 
from modules.bankroll import BankrollManager 
from modules.football import FootballPredictor 
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class MatchResult1X2Screen(BoxLayout):
    """Módulo de Análisis para Ganador / Empate (1X2)."""
    def __init__(self, **kwargs):
        super(MatchResult1X2Screen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 15
        self.spacing = 15

        # Título del módulo
        self.add_widget(Label(
            text="ANÁLISIS MÓDULO 1X2 (GANADOR / EMPATE)",
            font_size='16sp',
            bold=True,
            size_hint=(1, None),
            height=40,
            color=(0.0, 0.90, 1.0, 1)
        ))

        # Campos de entrada de ejemplo para cuotas
        form_layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(1, 0.6))
        
        form_layout.add_widget(Label(text="Cuota Local (1):", size_hint=(1, None), height=25))
        self.input_local = TextInput(text="1.85", multiline=False, size_hint=(1, None), height=40)
        form_layout.add_widget(self.input_local)

        form_layout.add_widget(Label(text="Cuota Empate (X):", size_hint=(1, None), height=25))
        self.input_empate = TextInput(text="3.40", multiline=False, size_hint=(1, None), height=40)
        form_layout.add_widget(self.input_empate)

        form_layout.add_widget(Label(text="Cuota Visitante (2):", size_hint=(1, None), height=25))
        self.input_visitante = TextInput(text="4.20", multiline=False, size_hint=(1, None), height=40)
        form_layout.add_widget(self.input_visitante)

        self.add_widget(form_layout)

        # Botón de cálculo
        btn_calcular = Button(
            text="Calcular Probabilidades 1X2",
            font_size='14sp',
            bold=True,
            size_hint=(1, None),
            height=50,
            background_color=(0.0, 0.7, 0.4, 1)
        )
        btn_calcular.bind(on_press=self.calcular_1x2)
        self.add_widget(btn_calcular)

        # Resultado
        self.lbl_resultado = Label(
            text="Ingrese cuotas y presione calcular.",
            font_size='14sp',
            size_hint=(1, None),
            height=60,
            color=(1, 1, 1, 1)
        )
        self.add_widget(self.lbl_resultado)

    def calcular_1x2(self, instance):
        try:
            q1 = float(self.input_local.text)
            qx = float(self.input_empate.text)
            q2 = float(self.input_visitante.text)
            
            # Cálculo básico de probabilidad implícita
            p1 = (1 / q1) * 100
            px = (1 / qx) * 100
            p2 = (1 / q2) * 100
            
            self.lbl_resultado.text = f"Probabilidades: Local: {p1:.1f}% | Empate: {px:.1f}% | Visitante: {p2:.1f}%"
        except ValueError:
            self.lbl_resultado.text = "Error: Ingrese valores numéricos válidos."

class ExactScoreCard(BoxLayout):
    """Tarjeta visual para mostrar un marcador exacto pronosticado."""

    def __init__(self, score_data, **kwargs):
        super(ExactScoreCard, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 12
        self.spacing = 6
        self.size_hint = (1, None)
        self.height = 120

        with self.canvas.before:
            Color(0.12, 0.16, 0.25, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[8])
        self.bind(pos=self.update_rect, size=self.update_rect)

        lbl_teams = Label(
            text=f"{score_data['home_team']} vs {score_data['away_team']}",
            font_size='15sp',
            bold=True,
            color=(0.063, 0.725, 0.506, 1)
        )
        lbl_score = Label(
            text=f"Marcador Pronosticado: {score_data['home_goals']} - {score_data['away_goals']}",
            font_size='14sp',
            bold=True,
            color=(0.9, 0.9, 0.9, 1)
        )
        lbl_odds = Label(
            text=f"Cuota Estimada: {score_data['odds']}",
            font_size='13sp',
            bold=True,
            color=(0.231, 0.510, 0.965, 1)
        )

        self.add_widget(lbl_teams)
        self.add_widget(lbl_score)
        self.add_widget(lbl_odds)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class FootballPredictor:
    def __init__(self, home_team, away_team,
                 hs, hc, hm, hf,
                 as_, ac, am, af):
        # ... tu inicialización existente ...
        self.home_team = home_team
        self.away_team = away_team
        # aquí guardas los datos y cálculos

    def calculate_prediction(self):
        # ... tu lógica actual que devuelve dict con home_xg, away_xg, probs, etc. ...
        pred = {
            "home_team": self.home_team,
            "away_team": self.away_team,
            "home_xg": 1.8,
            "away_xg": 1.2,
            "home_prob": 55,
            "draw_prob": 25,
            "away_prob": 20,
            "recommendation": "Victoria Local"
        }
        # añadimos marcador exacto
        pred.update(self.calculate_exact_score(pred["home_xg"], pred["away_xg"]))
        return pred

    def calculate_exact_score(self, home_xg, away_xg):
        """Genera marcador exacto basado en xG."""
        # Implementación simplificada - reemplazar con lógica real
        home_goals = max(0, int(home_xg))
        away_goals = max(0, int(away_xg))
        return {"home_goals": home_goals, "away_goals": away_goals}


# Configurar el color de fondo principal de la ventana (Negro Carbón Pro: #0B0F19)
Window.clearcolor = (0.043, 0.059, 0.098, 1)
 
class SecurityScreen(Screen): 
    """Pantalla inicial de seguridad y validación de acceso.""" 
    def __init__(self, **kwargs): 
        super(SecurityScreen, self).__init__(**kwargs) 
         
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20) 
         
        title_label = Label( 
            text="ANALYSIS SPORT", 
            font_size='24sp', 
            bold=True, 
            color=(0.063, 0.725, 0.506, 1) # Verde Neón 
        ) 
         
        device_id = SecurityManager.get_device_id() 
        self.id_label = Label( 
            text=f"ID Dispositivo: {device_id}", 
            font_size='14sp', 
            color=(0.231, 0.510, 0.965, 1) # Azul Eléctrico 
        ) 
         
        self.pass_input = TextInput( 
            text='', 
            hint_text='Ingrese Clave de Acceso (Ej: Milena1428)', 
            password=True, 
            multiline=False, 
            size_hint=(1, None), 
            height=50 
        ) 
         
        btn_login = Button( 
            text='ACCEDER AL SISTEMA', 
            size_hint=(1, None), 
            height=50, 
            background_color=(0.063, 0.725, 0.506, 1), 
            color=(1, 1, 1, 1) 
        ) 
        btn_login.bind(on_press=self.verify_access) 
         
        self.status_label = Label(text='', color=(1, 0.3, 0.3, 1)) 
 
        layout.add_widget(title_label) 
        layout.add_widget(self.id_label) 
        layout.add_widget(self.pass_input) 
        layout.add_widget(btn_login) 
        layout.add_widget(self.status_label) 
         
        self.add_widget(layout) 
 
    def verify_access(self, instance): 
        entered_code = self.pass_input.text 
        is_valid, role_or_msg = SecurityManager.validate_passcode(entered_code) 
        if is_valid: 
            self.status_label.text = "" 
            self.pass_input.text = "" 
            self.manager.current = 'dashboard' 
        else: 
            self.status_label.text = role_or_msg 
 

 
class EscaleraCard(BoxLayout): 
    """Componente visual de tarjeta individual para cada paso de la escalera.""" 
    def __init__(self, step_data, **kwargs): 
        super(EscaleraCard, self).__init__(**kwargs) 
        self.orientation = 'vertical' 
        self.padding = 10 
        self.spacing = 4 
        self.size_hint = (1, None) 
        self.height = 90 
         
        # Fondo y bordes redondeados para la tarjetica 
        with self.canvas.before: 
            # Color de fondo de la tarjeta (Azul oscuro / Grisáceo elegante) 
            Color(0.12, 0.16, 0.25, 1) 
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[8]) 
        self.bind(pos=self.update_rect, size=self.update_rect) 
         
        # Título del paso 
        lbl_step = Label( 
            text=f"PASO {step_data['step']}", 
            font_size='14sp', 
            bold=True, 
            color=(0.063, 0.725, 0.506, 1) # Verde Neón 
        ) 
         
        # Detalles de valores 
        stake = step_data.get('stake', 0) 
        retorno = step_data.get('return', step_data.get('gross_return', 0)) 
        bank_final = step_data.get('bank_after', step_data.get('new_bank', 0)) 
         
        lbl_details = Label( 
            text=f"Apuesta: ${stake:,.2f}  |  Retorno: ${retorno:,.2f}", 
            font_size='12sp', 
            color=(0.9, 0.9, 0.9, 1) 
        ) 
         
        lbl_bank = Label( 
            text=f"Bank Final: ${bank_final:,.2f}", 
            font_size='13sp', 
            bold=True, 
            color=(0.231, 0.510, 0.965, 1) # Azul Eléctrico 
        ) 
         
        self.add_widget(lbl_step) 
        self.add_widget(lbl_details) 
        self.add_widget(lbl_bank) 
 
    def update_rect(self, instance, value): 
        self.rect.pos = instance.pos 
        self.rect.size = instance.size 
 
class EscaleraScreen(Screen): 
    """Pantalla del módulo Reto Escalera con tarjetas individuales.""" 
    def __init__(self, **kwargs): 
        super(EscaleraScreen, self).__init__(**kwargs) 
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15) 
         
        layout.add_widget(Label(text="MÓDULO: RETO ESCALERA", font_size='18sp', 
bold=True, size_hint=(1, None), height=30, color=(0.063, 0.725, 0.506, 1))) 
         
        controls = BoxLayout(orientation='horizontal', size_hint=(1, None), height=45, 
spacing=10) 
        self.bank_input = TextInput(text='100000', multiline=False, input_filter='float', 
hint_text='Bank Inicial') 
        btn_calc = Button(text='CALCULAR', background_color=(0.231, 0.510, 0.965, 1), 
color=(1,1,1,1)) 
        btn_calc.bind(on_press=self.calcular) 
        controls.add_widget(self.bank_input) 
        controls.add_widget(btn_calc) 
        layout.add_widget(controls) 
         
        self.results_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10) 
        self.results_layout.bind(minimum_height=self.results_layout.setter('height')) 
         
        scroll = ScrollView(size_hint=(1, 1)) 
        scroll.add_widget(self.results_layout) 
        layout.add_widget(scroll) 
         
        btn_return = Button(text='VOLVER AL MENÚ', size_hint=(1, None), height=40, 
background_color=(0.3, 0.3, 0.3, 1), color=(1,1,1,1)) 
        btn_return.bind(on_press=lambda x: setattr(self.manager, 'current', 'dashboard')) 
        layout.add_widget(btn_return) 
         
        self.add_widget(layout) 
        self.calcular(None) 
 
    def calcular(self, instance): 
        self.results_layout.clear_widgets() 
        try: 
            bank = float(self.bank_input.text) 
        except ValueError: 
            bank = 100000.0 
             
        escalera = RetoEscaleraCalculator(initial_bank=bank, stake_percentage=0.60, 
fixed_odds=1.50) 
        for paso in escalera.calculate_ladder(): 
            card = EscaleraCard(paso) 
            self.results_layout.add_widget(card) 
 
class FootballCard(BoxLayout): 
    """Componente visual de tarjeta para mostrar el resumen de un partido/pronóstico de 
fútbol.""" 
    def __init__(self, match_data, **kwargs): 
        super(FootballCard, self).__init__(**kwargs) 
        self.orientation = 'vertical' 
        self.padding = 10 
        self.spacing = 4 
        self.size_hint = (1, None) 
        self.height = 100 
         
        with self.canvas.before: 
            Color(0.12, 0.16, 0.25, 1) 
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[8]) 
        self.bind(pos=self.update_rect, size=self.update_rect) 
         
        # Color dinámico según el resultado 
        res_color = (0.9, 0.9, 0.9, 1) 
        if match_data['result'] == 'win': 
            res_color = (0.063, 0.725, 0.506, 1) # Verde 
        elif match_data['result'] == 'loss': 
            res_color = (0.905, 0.298, 0.235, 1) # Rojo 
 
        lbl_teams = Label( 
            text=f"{match_data['home_team']} vs {match_data['away_team']}", 
            font_size='14sp', 
            bold=True, 
            color=(0.9, 0.9, 0.9, 1) 
        ) 
        lbl_details = Label( 
            text=f"Mercado: {match_data['market']} | Pronóstico: {match_data['prediction']}", 
            font_size='12sp', 
            color=(0.7, 0.7, 0.7, 1) 
        ) 
        lbl_status = Label( 
            text=f"Cuota: {match_data['odds']}  |  Estado: {match_data['result'].upper()}", 
            font_size='13sp', 
            bold=True, 
            color=res_color 
        ) 
         
        self.add_widget(lbl_teams) 
        self.add_widget(lbl_details) 
        self.add_widget(lbl_status) 
 
    def update_rect(self, instance, value): 
        self.rect.pos = instance.pos 
        self.rect.size = instance.size 
 
from modules.football import FootballPredictor 
 
class FootballCard(BoxLayout): 
    """Tarjeta visual con los resultados de la predicción de fútbol.""" 
    def __init__(self, data, **kwargs): 
        super(FootballCard, self).__init__(**kwargs) 
        self.orientation = 'vertical' 
        self.padding = 12 
        self.spacing = 6 
        self.size_hint = (1, None) 
        self.height = 120 
         
        with self.canvas.before: 
            Color(0.12, 0.16, 0.25, 1) 
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[8]) 
        self.bind(pos=self.update_rect, size=self.update_rect) 
         
        lbl_teams = Label( 
            text=f"{data['home_team']} vs {data['away_team']}", 
            font_size='15sp', 
            bold=True, 
            color=(0.063, 0.725, 0.506, 1) # Verde Neón 
        ) 
        lbl_probs = Label( 
            text=f"Probabilidades -> Local: {data['home_prob']}% | Empate: {data['draw_prob']}% | Visita: {data['away_prob']}%", 
            font_size='12sp', 
            color=(0.9, 0.9, 0.9, 1) 
        ) 
        lbl_rec = Label( 
            text=f"Pronóstico Sugerido: {data['recommendation']}", 
            font_size='13sp', 
            bold=True, 
            color=(0.231, 0.510, 0.965, 1) # Azul Eléctrico 
        ) 
         
        self.add_widget(lbl_teams) 
        self.add_widget(lbl_probs) 
        self.add_widget(lbl_rec) 
 
    def update_rect(self, instance, value): 
        self.rect.pos = instance.pos 
        self.rect.size = instance.size 
 
import re 
 
try: 
    from kivy.core.clipboard import Clipboard 
except ImportError:  # pragma: no cover - fallback para entornos sin soporte nativo 
    class Clipboard: 
        @staticmethod 
        def copy(text): 
            return text 
 
        @staticmethod 
        def get(*args, **kwargs): 
            return "" 
 
import re 
from kivy.core.clipboard import Clipboard 
 
class ExactScoreCard(BoxLayout):
    """Tarjeta visual para mostrar un marcador exacto pronosticado."""
    def __init__(self, score_data, **kwargs):
        super(ExactScoreCard, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 12
        self.spacing = 6
        self.size_hint = (1, None)
        self.height = 120
        with self.canvas.before:
            Color(0.12, 0.16, 0.25, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[8])
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        lbl_teams = Label(
            text=f"{score_data['home_team']} vs {score_data['away_team']}",
            font_size='15sp',
            bold=True,
            color=(0.063, 0.725, 0.506, 1)
        )
        lbl_score = Label(
            text=f"Marcador Pronosticado: {score_data['home_goals']} - {score_data['away_goals']}",
            font_size='14sp',
            bold=True,
            color=(0.9, 0.9, 0.9, 1)
        )
        lbl_odds = Label(
            text=f"Cuota Estimada: {score_data['odds']}",
            font_size='13sp',
            bold=True,
            color=(0.231, 0.510, 0.965, 1)
        )
        self.add_widget(lbl_teams)
        self.add_widget(lbl_score)
        self.add_widget(lbl_odds)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class FootballScreen(Screen):
    def __init__(self, **kwargs):
        super(FootballScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=8)
        
        layout.add_widget(Label(
            text="MÓDULO: PREDICCIÓN AVANZADA DE FÚTBOL",
            font_size='16sp', bold=True, size_hint=(1, None), height=30,
            color=(0.063, 0.725, 0.506, 1)
        ))
        
        # --- BARRA DE HERRAMIENTAS IA MEJORADA ---
        ai_bar = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height=35)
        btn_copy = Button(
            text='1. Copiar Prompt IA', background_color=(0.12, 0.53, 0.9, 1),
            color=(1, 1, 1, 1), font_size='12sp'
        )
        btn_copy.bind(on_press=self.copiar_prompt)
        ai_bar.add_widget(btn_copy)
        layout.add_widget(ai_bar)
        
        # --- CAJITA DE TEXTO PARA PEGAR DIRECTAMENTE ---
        paste_box_layout = BoxLayout(orientation='vertical', size_hint=(1, None), height=85, spacing=4)
        paste_box_layout.add_widget(Label(
            text="Pega aquí el texto con los datos de la IA (Ctrl+V):",
            font_size='11sp', color=(0.8, 0.8, 0.8, 1), size_hint=(1, None), height=18
        ))
        
        row_paste = BoxLayout(orientation='horizontal', spacing=8, size_hint=(1, None), height=55)
        self.text_paste_input = TextInput(
            text='', hint_text='Haz clic aquí, presiona Ctrl + V para pegar el texto...',
            multiline=True, font_size='11sp'
        )
        btn_process = Button(
            text='2. Rellenar Campos', size_hint=(None, 1), width=130,
            background_color=(0.1, 0.7, 0.3, 1), color=(1, 1, 1, 1), font_size='12sp'
        )
        btn_process.bind(on_press=self.procesar_texto_pegado)
        
        row_paste.add_widget(self.text_paste_input)
        row_paste.add_widget(btn_process)
        paste_box_layout.add_widget(row_paste)
        layout.add_widget(paste_box_layout)
        
        form = BoxLayout(orientation='vertical', size_hint=(1, None), height=230, spacing=6)
        
        # Nombres de equipos
        r_teams = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height=35)
        self.h_in = TextInput(text='Real Madrid', multiline=False, hint_text='Equipo Local')
        self.a_in = TextInput(text='Barcelona', multiline=False, hint_text='Equipo Visitante')
        r_teams.add_widget(self.h_in)
        r_teams.add_widget(self.a_in)
        form.add_widget(r_teams)
        
        # Datos del Local EN CASA
        form.add_widget(Label(
            text="Rendimiento Local (Jugando EN CASA)",
            font_size='11sp', color=(0.231, 0.510, 0.965, 1), size_hint=(1, None), height=18
        ))
        r_home = BoxLayout(orientation='horizontal', spacing=6, size_hint=(1, None), height=35)
        self.hs_in = TextInput(text='14', multiline=False, input_filter='float', hint_text='Goles Favor Casa')
        self.hc_in = TextInput(text='4', multiline=False, input_filter='float', hint_text='Goles Contra Casa')
        self.hm_in = TextInput(text='6', multiline=False, input_filter='float', hint_text='Partidos en Casa')
        self.hf_in = TextInput(text='12', multiline=False, input_filter='float', hint_text='Pts Últimos 5')
        r_home.add_widget(self.hs_in)
        r_home.add_widget(self.hc_in)
        r_home.add_widget(self.hm_in)
        r_home.add_widget(self.hf_in)
        form.add_widget(r_home)
        
        # Datos del Visitante FUERA DE CASA
        form.add_widget(Label(
            text="Rendimiento Visitante (Jugando FUERA)",
            font_size='11sp', color=(0.231, 0.510, 0.965, 1), size_hint=(1, None), height=18
        ))
        r_away = BoxLayout(orientation='horizontal', spacing=6, size_hint=(1, None), height=35)
        self.as_in = TextInput(text='10', multiline=False, input_filter='float', hint_text='Goles Favor Fuera')
        self.ac_in = TextInput(text='7', multiline=False, input_filter='float', hint_text='Goles Contra Fuera')
        self.am_in = TextInput(text='6', multiline=False, input_filter='float', hint_text='Partidos Fuera')
        self.af_in = TextInput(text='9', multiline=False, input_filter='float', hint_text='Pts Últimos 5')
        r_away.add_widget(self.as_in)
        r_away.add_widget(self.ac_in)
        r_away.add_widget(self.am_in)
        r_away.add_widget(self.af_in)
        form.add_widget(r_away)
        
        btn_calc = Button(
            text='CALCULAR PREDICCIÓN PROFESIONAL', size_hint=(1, None), height=40,
            background_color=(0.231, 0.510, 0.965, 1), color=(1, 1, 1, 1)
        )
        btn_calc.bind(on_press=self.calcular)
        form.add_widget(btn_calc)
        layout.add_widget(form)
        
        self.res_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        self.res_layout.bind(minimum_height=self.res_layout.setter('height'))
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.res_layout)
        layout.add_widget(scroll)
        
        btn_ret = Button(
            text='VOLVER AL MENÚ', size_hint=(1, None), height=40,
            background_color=(0.3, 0.3, 0.3, 1), color=(1, 1, 1, 1)
        )
        btn_ret.bind(on_press=lambda x: setattr(self.manager, 'current', 'dashboard'))
        layout.add_widget(btn_ret)
        self.add_widget(layout)
        
        self.calcular(None)

    def copiar_prompt(self, instance):
        local_team = self.h_in.text.strip() or "Equipo Local"
        away_team = self.a_in.text.strip() or "Equipo Visitante"
        prompt_text = (
            f"Actúa como un experto en estadísticas de fútbol. Necesito los datos para un modelo matemático del partido: "
            f"{local_team} (Local) vs {away_team} (Visitante).\n\n"
            f"Por favor, entrégame ÚNICAMENTE los 8 números exactos solicitados, separados por comas, en este orden estricto:\n"
            f"1. Goles a favor de {local_team} en casa\n"
            f"2. Goles en contra de {local_team} en casa\n"
            f"3. Partidos jugados en casa por {local_team}\n"
            f"4. Puntos últimos 5 en casa (máx 15)\n"
            f"5. Goles a favor de {away_team} fuera\n"
            f"6. Goles en contra de {away_team} fuera\n"
            f"7. Partidos jugados fuera por {away_team}\n"
            f"8. Puntos últimos 5 fuera (máx 15)\n\n"
            f"Formato obligatorio: 6, 6, 5, 7, 7, 5, 6, 9"
        )
        Clipboard.copy(prompt_text)
        self.text_paste_input.text = "¡Prompt copiado! Pega la respuesta de la IA aquí."

    def procesar_texto_pegado(self, instance):
        texto = self.text_paste_input.text
        if not texto:
            return
        numeros = re.findall(r'\b\d+(?:\.\d+)?\b', texto)
        if len(numeros) >= 8:
            self.hs_in.text = str(numeros[0])
            self.hc_in.text = str(numeros[1])
            self.hm_in.text = str(numeros[2])
            self.hf_in.text = str(numeros[3])
            self.as_in.text = str(numeros[4])
            self.ac_in.text = str(numeros[5])
            self.am_in.text = str(numeros[6])
            self.af_in.text = str(numeros[7])
            self.text_paste_input.text = "¡Datos rellenados con éxito!"

    def calcular(self, instance):
        self.res_layout.clear_widgets()
        try:
            pred = FootballPredictor(
                self.h_in.text, self.a_in.text,
                self.hs_in.text, self.hc_in.text, self.hm_in.text, self.hf_in.text,
                self.as_in.text, self.ac_in.text, self.am_in.text, self.af_in.text
            ).calculate_prediction()
        except ValueError:
            return
            
        card = BoxLayout(orientation='vertical', padding=12, spacing=6, size_hint=(1, None), height=130)
        with card.canvas.before:
            Color(0.12, 0.16, 0.25, 1)
            card.rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[8])
        card.bind(
            pos=lambda inst, val: setattr(inst.rect, 'pos', inst.pos),
            size=lambda inst, val: setattr(inst.rect, 'size', inst.size)
        )
        
        card.add_widget(Label(text=f"{pred['home_team']} vs {pred['away_team']}", font_size='15sp', bold=True, color=(0.063, 0.725, 0.506, 1)))
        card.add_widget(Label(text=f"xG Ajustado -> Local: {pred['home_xg']} | Visita: {pred['away_xg']}", font_size='12sp', color=(0.9,0.9,0.9,1)))
        card.add_widget(Label(text=f"Probabilidades -> Local: {pred['home_prob']}% | Empate: {pred['draw_prob']}% | Visita: {pred['away_prob']}%", font_size='12sp', color=(0.9,0.9,0.9,1)))
        card.add_widget(Label(text=f"Sugerencia: {pred['recommendation']}", font_size='13sp', bold=True, color=(0.231, 0.510, 0.965, 1)))
        
        exact_score_data = {
            'home_team': pred['home_team'],
            'away_team': pred['away_team'],
            'home_goals': 2,
            'away_goals': 1,
            'odds': 7.50
        }
        score_card = ExactScoreCard(exact_score_data)
        self.res_layout.add_widget(score_card)
        self.res_layout.add_widget(card)

import re

import re
from kivy.core.clipboard import Clipboard  # <-- Asegúrate de tener esta importación arriba si usas portapapeles

class BothTeamsScoreScreen(Screen):
    """Módulo optimizado de Ambos Marcan con Generador de Prompt y Extracción Automática."""
    def __init__(self, **kwargs):
        super(BothTeamsScoreScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=8)
        
        layout.add_widget(Label(
            text="MÓDULO: AMBOS EQUIPOS ANOTAN (ASISTIDO POR PROMPT)",
            font_size='14sp', bold=True, size_hint=(1, None), height=26,
            color=(0.231, 0.510, 0.965, 1)
        ))
        
        # --- SECCIÓN DEL PROMPT Y BOTONES DE AYUDA ---
        prompt_box = BoxLayout(orientation='vertical', size_hint=(1, None), height=135, spacing=4)
        prompt_box.add_widget(Label(
            text="1. Pega aquí el reporte de estadísticas que te dio la IA o la web:",
            font_size='10sp', color=(0.8, 0.8, 0.8, 1), size_hint=(1, None), height=15
        ))
        
        self.prompt_input = TextInput(
            text='', 
            multiline=True, 
            hint_text='Ej:\nPartido: Hyundai vs Gangwon\nLocal (Casa) - BTTS: 8/10, Goles Favor: 1.2, Goles Contra: 0.9\nVisitante (Fuera) - BTTS: 1/10, Goles Favor: 0.9, Goles Contra: 1.9',
            size_hint=(1, None), height=60
        )
        prompt_box.add_widget(self.prompt_input)
        
        # Botonera para el Prompt
        btn_row = BoxLayout(orientation='horizontal', size_hint=(1, None), height=32, spacing=8)
        
        btn_copiar_modelo = Button(
            text='COPIAR PROMPT PARA LA IA', font_size='10sp',
            background_color=(0.3, 0.4, 0.6, 1), color=(1, 1, 1, 1)
        )
        btn_copiar_modelo.bind(on_press=self.copiar_plantilla_prompt)
        
        btn_parse = Button(
            text='EXTRAER DATOS', font_size='10sp',
            background_color=(0.231, 0.510, 0.965, 1), color=(1, 1, 1, 1)
        )
        btn_parse.bind(on_press=self.rellenar_desde_prompt)
        
        btn_row.add_widget(btn_copiar_modelo)
        btn_row.add_widget(btn_parse)
        prompt_box.add_widget(btn_row)
        layout.add_widget(prompt_box)
        
        # --- FORMULARIO DE PARÁMETROS ---
        form = BoxLayout(orientation='vertical', size_hint=(1, None), height=195, spacing=5)
        
        r_teams = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height=32)
        self.h_in = TextInput(text='Hyundai', multiline=False, hint_text='Equipo Local')
        self.a_in = TextInput(text='Gangwon', multiline=False, hint_text='Equipo Visitante')
        r_teams.add_widget(self.h_in)
        r_teams.add_widget(self.a_in)
        form.add_widget(r_teams)
        
        form.add_widget(Label(text="Rendimiento Local (En Casa):", font_size='10sp', color=(0.063, 0.725, 0.506, 1), size_hint=(1, None), height=14))
        r_home = BoxLayout(orientation='horizontal', spacing=6, size_hint=(1, None), height=32)
        self.h_btts_matches = TextInput(text='8', multiline=False, input_filter='int', hint_text='BTTS (de 10)')
        self.h_scored_avg = TextInput(text='1.2', multiline=False, input_filter='float', hint_text='GF Casa')
        self.h_conceded_avg = TextInput(text='0.9', multiline=False, input_filter='float', hint_text='GC Casa')
        r_home.add_widget(self.h_btts_matches)
        r_home.add_widget(self.h_scored_avg)
        r_home.add_widget(self.h_conceded_avg)
        form.add_widget(r_home)
        
        form.add_widget(Label(text="Rendimiento Visitante (Fuera):", font_size='10sp', color=(0.063, 0.725, 0.506, 1), size_hint=(1, None), height=14))
        r_away = BoxLayout(orientation='horizontal', spacing=6, size_hint=(1, None), height=32)
        self.a_btts_matches = TextInput(text='1', multiline=False, input_filter='int', hint_text='BTTS (de 10)')
        self.a_scored_avg = TextInput(text='0.9', multiline=False, input_filter='float', hint_text='GF Fuera')
        self.a_conceded_avg = TextInput(text='1.9', multiline=False, input_filter='float', hint_text='GC Fuera')
        r_away.add_widget(self.a_btts_matches)
        r_away.add_widget(self.a_scored_avg)
        r_away.add_widget(self.a_conceded_avg)
        form.add_widget(r_away)
        
        btn_calc = Button(
            text='CALCULAR MODELO INTELIGENTE', size_hint=(1, None), height=35,
            background_color=(0.063, 0.725, 0.506, 1), color=(1, 1, 1, 1)
        )
        btn_calc.bind(on_press=self.calcular_btts_optimo)
        form.add_widget(btn_calc)
        layout.add_widget(form)
        
        # --- RESULTADOS ---
        self.res_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=8)
        self.res_layout.bind(minimum_height=self.res_layout.setter('height'))
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.res_layout)
        layout.add_widget(scroll)
        
        btn_ret = Button(
            text='VOLVER AL MENÚ', size_hint=(1, None), height=35,
            background_color=(0.3, 0.3, 0.3, 1), color=(1, 1, 1, 1)
        )
        btn_ret.bind(on_press=lambda x: setattr(self.manager, 'current', 'dashboard'))
        layout.add_widget(btn_ret)
        self.add_widget(layout)
        
        self.calcular_btts_optimo(None)

    def copiar_plantilla_prompt(self, instance):
        """Plantilla de texto plano estricta para lectura automática de goles."""
        plantilla = (
            "Analiza los últimos 10 partidos de cada equipo y responde ÚNICAMENTE con el siguiente formato de texto plano:\n\n"
            "Partido: [Local] vs [Visitante]\n"
            "Local (Casa) - Goles a Favor: [X.X], Goles en Contra: [X.X]\n"
            "Visitante (Fuera) - Goles a Favor: [X.X], Goles en Contra: [X.X]"
        )
        Clipboard.copy(plantilla)
        
        self.res_layout.clear_widgets()
        card = BoxLayout(orientation='vertical', padding=8, size_hint=(1, None), height=40)
        card.add_widget(Label(text="¡Prompt de Goles copiado al portapapeles!", font_size='11sp', color=(0.063, 0.725, 0.506, 1)))
        self.res_layout.add_widget(card)
    def rellenar_desde_prompt(self, instance):
        """Lee el texto pegado, extrae los datos numéricos y llena los inputs automáticamente."""
        texto = self.prompt_input.text
        if not texto:
            return
            
        try:
            match_partido = re.search(r'[:\-]\s*([a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+)\s+vs\s+([a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+)', texto, re.IGNORECASE)
            if match_partido:
                self.h_in.text = match_partido.group(1).strip()
                self.a_in.text = match_partido.group(2).strip()

            lineas = texto.split('\n')
            for linea in lineas:
                linea_lower = linea.lower()
                numeros = re.findall(r'\d+(?:\.\d+)?', linea)
                
                if 'local' in linea_lower and len(numeros) >= 3:
                    self.h_btts_matches.text = str(int(float(numeros[0])))
                    self.h_scored_avg.text = numeros[1]
                    self.h_conceded_avg.text = numeros[2]
                elif ('visitante' in linea_lower or 'fuera' in linea_lower) and len(numeros) >= 3:
                    self.a_btts_matches.text = str(int(float(numeros[0])))
                    self.a_scored_avg.text = numeros[1]
                    self.a_conceded_avg.text = numeros[2]

            self.calcular_btts_optimo(None)
        except Exception as e:
            print("Error al parsear:", e)

    def calcular_btts_optimo(self, instance):
        self.res_layout.clear_widgets()
        try:
            h_btts_ratio = float(self.h_btts_matches.text or 0) / 10.0
            a_btts_ratio = float(self.a_btts_matches.text or 0) / 10.0
            h_scored = float(self.h_scored_avg.text or 0)
            h_conceded = float(self.h_conceded_avg.text or 0)
            a_scored = float(self.a_scored_avg.text or 0)
            a_conceded = float(self.a_conceded_avg.text or 0)
        except ValueError:
            return
            
        factor_historico = ((h_btts_ratio + a_btts_ratio) / 2.0) * 100.0
        ataque_local_vs_defensa_visita = min(2.5, (h_scored + a_conceded) / 2.0)
        ataque_visita_vs_defensa_local = min(2.5, (a_scored + h_conceded) / 2.0)
        factor_goles = (((ataque_local_vs_defensa_visita + ataque_visita_vs_defensa_local) / 3.0)) * 100.0
        
        prob_btts = (factor_goles * 0.7) + (factor_historico * 0.3)
        prob_btts = min(100.0, max(0.0, prob_btts))
        
        if prob_btts >= 72.0:
            veredicto = "ALTA CONFIANZA (AMBOS MARCAN)"
            color_ver = (0.063, 0.725, 0.506, 1)
        elif prob_btts >= 58.0:
            veredicto = "ZONA MODERADA (STAKE BAJO)"
            color_ver = (1, 0.8, 0.2, 1)
        else:
            veredicto = "PARTIDO NO APTO"
            color_ver = (0.9, 0.3, 0.3, 1)
        
        card = BoxLayout(orientation='vertical', padding=10, spacing=4, size_hint=(1, None), height=110)
        with card.canvas.before:
            Color(0.12, 0.16, 0.25, 1)
            card.rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[8])
        card.bind(
            pos=lambda inst, val: setattr(inst.rect, 'pos', inst.pos),
            size=lambda inst, val: setattr(inst.rect, 'size', inst.size)
        )
        
        card.add_widget(Label(text=f"{self.h_in.text} vs {self.a_in.text}", font_size='13sp', bold=True, color=(0.063, 0.725, 0.506, 1)))
        card.add_widget(Label(text=f"Probabilidad Ponderada BTTS: {prob_btts:.1f}%", font_size='12sp', bold=True, color=(0.231, 0.510, 0.965, 1)))
        card.add_widget(Label(text=f"Veredicto: {veredicto}", font_size='11sp', bold=True, color=color_ver))
        
        self.res_layout.add_widget(card)
        import re
from kivy.core.clipboard import Clipboard
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle

class YellowCardsScreen(Screen):
    """Módulo optimizado de Tarjetas (Amarillas/Rojas) con Generador de Prompt y Cálculo Ponderado."""
    def __init__(self, **kwargs):
        super(YellowCardsScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=8)
        
        layout.add_widget(Label(
            text="MÓDULO: PRONÓSTICO DE TARJETAS (ASISTIDO POR PROMPT)",
            font_size='13sp', bold=True, size_hint=(1, None), height=26,
            color=(0.231, 0.510, 0.965, 1)
        ))
        
        # --- SECCIÓN DEL PROMPT Y BOTONES DE AYUDA ---
        prompt_box = BoxLayout(orientation='vertical', size_hint=(1, None), height=130, spacing=4)
        prompt_box.add_widget(Label(
            text="1. Pega aquí el reporte de tarjetas (Equipos y Árbitro):",
            font_size='10sp', color=(0.8, 0.8, 0.8, 1), size_hint=(1, None), height=15
        ))
        
        self.prompt_input = TextInput(
            text='', 
            multiline=True, 
            hint_text='Ej:\nPartido: Real Madrid vs Barcelona\nLocal (Casa) - Promedio Tarjetas: 2.4\nVisitante (Fuera) - Promedio Tarjetas: 2.8\nÁrbitro: Mateo Lahoz (Media: 5.5 tarjetas/partido)',
            size_hint=(1, None), height=58
        )
        prompt_box.add_widget(self.prompt_input)
        
        btn_row = BoxLayout(orientation='horizontal', size_hint=(1, None), height=32, spacing=8)
        
        btn_copiar_modelo = Button(
            text='COPIAR PROMPT PARA LA IA', font_size='10sp',
            background_color=(0.3, 0.4, 0.6, 1), color=(1, 1, 1, 1)
        )
        btn_copiar_modelo.bind(on_press=self.copiar_plantilla_prompt)
        
        btn_parse = Button(
            text='EXTRAER DATOS', font_size='10sp',
            background_color=(0.231, 0.510, 0.965, 1), color=(1, 1, 1, 1)
        )
        btn_parse.bind(on_press=self.rellenar_desde_prompt)
        
        btn_row.add_widget(btn_copiar_modelo)
        btn_row.add_widget(btn_parse)
        prompt_box.add_widget(btn_row)
        layout.add_widget(prompt_box)
        
        # --- FORMULARIO DE PARÁMETROS ---
        form = BoxLayout(orientation='vertical', size_hint=(1, None), height=210, spacing=5)
        
        r_teams = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height=32)
        self.h_in = TextInput(text='Local', multiline=False, hint_text='Equipo Local')
        self.a_in = TextInput(text='Visitante', multiline=False, hint_text='Equipo Visitante')
        r_teams.add_widget(self.h_in)
        r_teams.add_widget(self.a_in)
        form.add_widget(r_teams)
        
        form.add_widget(Label(text="Promedio Tarjetas por Equipo:", font_size='10sp', color=(0.063, 0.725, 0.506, 1), size_hint=(1, None), height=14))
        r_cards = BoxLayout(orientation='horizontal', spacing=6, size_hint=(1, None), height=32)
        self.h_cards_avg = TextInput(text='2.2', multiline=False, input_filter='float', hint_text='Tarjetas Local (Casa)')
        self.a_cards_avg = TextInput(text='2.6', multiline=False, input_filter='float', hint_text='Tarjetas Visita (Fuera)')
        r_cards.add_widget(self.h_cards_avg)
        r_cards.add_widget(self.a_cards_avg)
        form.add_widget(r_cards)
        
        form.add_widget(Label(text="Factor Árbitro y Línea de Mercado:", font_size='10sp', color=(0.063, 0.725, 0.506, 1), size_hint=(1, None), height=14))
        r_ref = BoxLayout(orientation='horizontal', spacing=6, size_hint=(1, None), height=32)
        self.ref_avg = TextInput(text='4.8', multiline=False, input_filter='float', hint_text='Media Árbitro')
        self.linea_over = TextInput(text='4.5', multiline=False, input_filter='float', hint_text='Línea de Apuesta (Ej: 4.5)')
        r_ref.add_widget(self.ref_avg)
        r_ref.add_widget(self.linea_over)
        form.add_widget(r_ref)
        
        btn_calc = Button(
            text='CALCULAR MODELO DE TARJETAS', size_hint=(1, None), height=35,
            background_color=(0.063, 0.725, 0.506, 1), color=(1, 1, 1, 1)
        )
        btn_calc.bind(on_press=self.calcular_tarjetas_optimo)
        form.add_widget(btn_calc)
        layout.add_widget(form)
        
        # --- RESULTADOS ---
        self.res_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=8)
        self.res_layout.bind(minimum_height=self.res_layout.setter('height'))
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.res_layout)
        layout.add_widget(scroll)
        
        btn_ret = Button(
            text='VOLVER AL MENÚ', size_hint=(1, None), height=35,
            background_color=(0.3, 0.3, 0.3, 1), color=(1, 1, 1, 1)
        )
        btn_ret.bind(on_press=lambda x: setattr(self.manager, 'current', 'dashboard'))
        layout.add_widget(btn_ret)
        self.add_widget(layout)
        
        self.calcular_tarjetas_optimo(None)

    def copiar_plantilla_prompt(self, instance):
        """Plantilla de texto plano estricta para lectura automática de tarjetas y árbitro en los últimos 10 partidos."""
        plantilla = (
            "Analiza los últimos 10 partidos de cada equipo y las estadísticas del árbitro asignado, y responde ÚNICAMENTE con el siguiente formato de texto plano:\n\n"
            "Partido: [Local] vs [Visitante]\n"
            "Árbitro - Promedio Tarjetas: [X.X]\n"
            "Local (Casa) - Tarjetas a Favor: [X.X], Tarjetas en Contra: [X.X]\n"
            "Visitante (Fuera) - Tarjetas a Favor: [X.X], Tarjetas en Contra: [X.X]"
        )
        Clipboard.copy(plantilla)
        
        self.res_layout.clear_widgets()
        card = BoxLayout(orientation='vertical', padding=8, size_hint=(1, None), height=40)
        card.add_widget(Label(text="¡Prompt de Tarjetas copiado al portapapeles!", font_size='11sp', color=(0.063, 0.725, 0.506, 1)))
        self.res_layout.add_widget(card)

    def rellenar_desde_prompt(self, instance):
        """Extrae automáticamente los promedios de tarjetas y del árbitro desde el texto."""
        texto = self.prompt_input.text
        if not texto:
            return
            
        try:
            match_partido = re.search(r'[:\-]\s*([a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+)\s+vs\s+([a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+)', texto, re.IGNORECASE)
            if match_partido:
                self.h_in.text = match_partido.group(1).strip()
                self.a_in.text = match_partido.group(2).strip()

            lineas = texto.split('\n')
            for linea in lineas:
                linea_lower = linea.lower()
                numeros = re.findall(r'\d+(?:\.\d+)?', linea)
                
                if 'local' in linea_lower and len(numeros) >= 1:
                    self.h_cards_avg.text = numeros[0]
                elif ('visitante' in linea_lower or 'fuera' in linea_lower) and len(numeros) >= 1:
                    self.a_cards_avg.text = numeros[0]
                elif 'árbitro' in linea_lower or 'arbitro' in linea_lower or 'media' in linea_lower:
                    if numeros:
                        self.ref_avg.text = numeros[-1] # Toma el último número que suele ser la media

            self.calcular_tarjetas_optimo(None)
        except Exception as e:
            print("Error al parsear tarjetas:", e)

    def calcular_tarjetas_optimo(self, instance):
        self.res_layout.clear_widgets()
        try:
            h_cards = float(self.h_cards_avg.text or 0)
            a_cards = float(self.a_cards_avg.text or 0)
            r_avg = float(self.ref_avg.text or 0)
            linea = float(self.linea_over.text or 4.5)
        except ValueError:
            return
            
        # Modelo Ponderado de Tarjetas:
        # Suma esperada basada en los equipos y ajustada con el peso estricto del árbitro (50% equipos, 50% árbitro)
        esperado_equipos = h_cards + a_cards
        esperado_total = (esperado_equipos * 0.5) + (r_avg * 0.5)
        
        # Cálculo de probabilidad orientativa frente a la línea de apuestas
            # Margen de diferencia respecto a la línea
        diferencia = esperado_total - linea
        prob_over = 50.0 + (diferencia * 18.0) # Escala de probabilidad
        prob_over = min(95.0, max(5.0, prob_over))
        
        if esperado_total >= (linea + 0.8) and prob_over >= 68.0:
            veredicto = f"ALTA CONFIANZA: OVER {linea} TARJETAS"
            color_ver = (0.063, 0.725, 0.506, 1)
        elif esperado_total <= (linea - 0.8):
            veredicto = f"ALTA CONFIANZA: UNDER {linea} TARJETAS"
            color_ver = (0.231, 0.510, 0.965, 1)
        else:
            veredicto = "ZONA NEUTRA / PARTIDO NO APTO"
            color_ver = (1, 0.8, 0.2, 1)
        
        card = BoxLayout(orientation='vertical', padding=10, spacing=4, size_hint=(1, None), height=120)
        with card.canvas.before:
            Color(0.12, 0.16, 0.25, 1)
            card.rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[8])
        card.bind(
            pos=lambda inst, val: setattr(inst.rect, 'pos', inst.pos),
            size=lambda inst, val: setattr(inst.rect, 'size', inst.size)
        )
        
        card.add_widget(Label(text=f"{self.h_in.text} vs {self.a_in.text}", font_size='13sp', bold=True, color=(0.063, 0.725, 0.506, 1)))
        card.add_widget(Label(text=f"Esperado Tarjetas: {esperado_total:.2f} | Prob. Over: {prob_over:.1f}%", font_size='12sp', bold=True, color=(0.231, 0.510, 0.965, 1)))
        card.add_widget(Label(text=f"Veredicto: {veredicto}", font_size='11sp', bold=True, color=color_ver))
        
        self.res_layout.add_widget(card)
import re
from kivy.core.clipboard import Clipboard
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle

class CornersScreen(Screen):
    """Módulo 9: Tiros de Esquina con Generador de Prompt y Cálculo Ponderado Cruzado."""
    def __init__(self, **kwargs):
        super(CornersScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=8)
        
        # Título del Módulo
        layout.add_widget(Label(
            text="MÓDULO: TIROS DE ESQUINA (ASISTIDO POR PROMPT)",
            font_size='13sp', bold=True, size_hint=(1, None), height=26,
            color=(0.231, 0.510, 0.965, 1)
        ))
        
        # --- SECCIÓN DEL PROMPT Y BOTONES DE AYUDA ---
        prompt_box = BoxLayout(orientation='vertical', size_hint=(1, None), height=130, spacing=4)
        prompt_box.add_widget(Label(
            text="1. Pega aquí el reporte de tiros de esquina:",
            font_size='10sp', color=(0.8, 0.8, 0.8, 1), size_hint=(1, None), height=15
        ))
        
        self.prompt_input = TextInput(
            text='', 
            multiline=True, 
            hint_text='Ej:\nPartido: Real Madrid vs Barcelona\nLocal (Casa) - Córneres a Favor: 5.5, Córneres en Contra: 3.8\nVisitante (Fuera) - Córneres a Favor: 4.5',
            size_hint=(1, None), height=58
        )
        prompt_box.add_widget(self.prompt_input)
        
        btn_row = BoxLayout(orientation='horizontal', size_hint=(1, None), height=32, spacing=8)
        
        btn_copiar_modelo = Button(
            text='COPIAR PROMPT PARA LA IA', font_size='10sp',
            background_color=(0.3, 0.4, 0.6, 1), color=(1, 1, 1, 1)
        )
        btn_copiar_modelo.bind(on_press=self.copiar_plantilla_prompt)
        
        btn_parse = Button(
            text='EXTRAER DATOS', font_size='10sp',
            background_color=(0.231, 0.510, 0.965, 1), color=(1, 1, 1, 1)
        )
        btn_parse.bind(on_press=self.rellenar_desde_prompt)
        
        btn_row.add_widget(btn_copiar_modelo)
        btn_row.add_widget(btn_parse)
        prompt_box.add_widget(btn_row)
        layout.add_widget(prompt_box)
        
        # --- FORMULARIO DE PARÁMETROS ---
        form = BoxLayout(orientation='vertical', size_hint=(1, None), height=210, spacing=5)
        
        r_teams = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height=32)
        self.h_in = TextInput(text='Local', multiline=False, hint_text='Equipo Local')
        self.a_in = TextInput(text='Visitante', multiline=False, hint_text='Equipo Visitante')
        r_teams.add_widget(self.h_in)
        r_teams.add_widget(self.a_in)
        form.add_widget(r_teams)
        
        form.add_widget(Label(text="Promedios Córneres Local (Casa):", font_size='10sp', color=(0.063, 0.725, 0.506, 1), size_hint=(1, None), height=14))
        r_home = BoxLayout(orientation='horizontal', spacing=6, size_hint=(1, None), height=32)
        self.h_corners_for = TextInput(text='5.5', multiline=False, input_filter='float', hint_text='A Favor (Casa)')
        self.h_corners_against = TextInput(text='3.8', multiline=False, input_filter='float', hint_text='En Contra (Casa)')
        r_home.add_widget(self.h_corners_for)
        r_home.add_widget(self.h_corners_against)
        form.add_widget(r_home)
        
        form.add_widget(Label(text="Promedios Córneres Visitante (Fuera) y Línea:", font_size='10sp', color=(0.063, 0.725, 0.506, 1), size_hint=(1, None), height=14))
        r_away = BoxLayout(orientation='horizontal', spacing=6, size_hint=(1, None), height=32)
        self.a_corners_for = TextInput(text='4.5', multiline=False, input_filter='float', hint_text='A Favor (Fuera)')
        self.linea_corners = TextInput(text='9.5', multiline=False, input_filter='float', hint_text='Línea Over/Under (Ej: 9.5)')
        r_away.add_widget(self.a_corners_for)
        r_away.add_widget(self.linea_corners)
        form.add_widget(r_away)
        
        btn_calc = Button(
            text='CALCULAR MODELO DE CÓRNERES', size_hint=(1, None), height=35,
            background_color=(0.063, 0.725, 0.506, 1), color=(1, 1, 1, 1)
        )
        btn_calc.bind(on_press=self.calcular_corners_optimo)
        form.add_widget(btn_calc)
        layout.add_widget(form)
        
        # --- SECCIÓN DE RESULTADOS ---
        self.res_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=8)
        self.res_layout.bind(minimum_height=self.res_layout.setter('height'))
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.res_layout)
        layout.add_widget(scroll)
        
        # Botón para volver al Menú Principal
        btn_ret = Button(
            text='VOLVER AL MENÚ', size_hint=(1, None), height=35,
            background_color=(0.3, 0.3, 0.3, 1), color=(1, 1, 1, 1)
        )
        btn_ret.bind(on_press=lambda x: setattr(self.manager, 'current', 'dashboard'))
        layout.add_widget(btn_ret)
        self.add_widget(layout)
        
        self.calcular_corners_optimo(None)

    def copiar_plantilla_prompt(self, instance):
        """Plantilla de texto plano estricta para lectura automática de córneres."""
        plantilla = (
            "Analiza los últimos 10 partidos de cada equipo y responde ÚNICAMENTE con el siguiente formato de texto plano:\n\n"
            "Partido: [Local] vs [Visitante]\n"
            "Local (Casa) - Córneres a Favor: [X.X], Córneres en Contra: [X.X]\n"
            "Visitante (Fuera) - Córneres a Favor: [X.X]"
        )
        Clipboard.copy(plantilla)
        
        self.res_layout.clear_widgets()
        card = BoxLayout(orientation='vertical', padding=8, size_hint=(1, None), height=40)
        card.add_widget(Label(text="¡Prompt de Córneres copiado al portapapeles!", font_size='11sp', color=(0.063, 0.725, 0.506, 1)))
        self.res_layout.add_widget(card)
    def rellenar_desde_prompt(self, instance):
        """Extrae automáticamente los promedios de saques de esquina y nombres desde el texto pegado."""
        texto = self.prompt_input.text
        if not texto:
            return
            
        try:
            match_partido = re.search(r'[:\-]\s*([a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+)\s+vs\s+([a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+)', texto, re.IGNORECASE)
            if match_partido:
                self.h_in.text = match_partido.group(1).strip()
                self.a_in.text = match_partido.group(2).strip()

            lineas = texto.split('\n')
            for linea in lineas:
                linea_lower = linea.lower()
                numeros = re.findall(r'\d+(?:\.\d+)?', linea)
                
                if 'local' in linea_lower and len(numeros) >= 2:
                    self.h_corners_for.text = numeros[0]
                    self.h_corners_against.text = numeros[1]
                elif ('visitante' in linea_lower or 'fuera' in linea_lower) and numeros:
                    self.a_corners_for.text = numeros[0]

            self.calcular_corners_optimo(None)
        except Exception as e:
            print("Error al parsear córneres:", e)

    def calcular_corners_optimo(self, instance):
        """Modelo matemático corregido de Córneres (Cruza volumen ofensivo local y foráneo frente a concesiones)."""
        self.res_layout.clear_widgets()
        try:
            hf = float(self.h_corners_for.text or 0)
            hc = float(self.h_corners_against.text or 0)
            af = float(self.a_corners_for.text or 0)
            linea = float(self.linea_corners.text or 9.5)
        except ValueError:
            return
            
        # Modelo cruzado real de saques de esquina
        total_esperado = ((hf + af) + (hc * 0.8)) / 1.5
        
        diferencia = total_esperado - linea
        prob_over = min(95.0, max(5.0, 50.0 + (diferencia * 16.0)))
        
        if total_esperado >= (linea + 1.0) and prob_over >= 66.0:
            veredicto = f"ALTA CONFIANZA: OVER {linea} CÓRNERES"
            color_ver = (0.063, 0.725, 0.506, 1)
        elif total_esperado <= (linea - 1.0) and prob_over <= 34.0:
            veredicto = f"ALTA CONFIANZA: UNDER {linea} CÓRNERES"
            color_ver = (0.231, 0.510, 0.965, 1)
        else:
            veredicto = "ZONA NEUTRA / PARTIDO NO APTO"
            color_ver = (1, 0.8, 0.2, 1)
        
        # Tarjeta visual de resultado
        card = BoxLayout(orientation='vertical', padding=10, spacing=4, size_hint=(1, None), height=110)
        with card.canvas.before:
            Color(0.12, 0.16, 0.25, 1)
            card.rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[8])
        card.bind(
            pos=lambda inst, val: setattr(inst.rect, 'pos', inst.pos),
            size=lambda inst, val: setattr(inst.rect, 'size', inst.size)
        )
        
        card.add_widget(Label(text=f"{self.h_in.text} vs {self.a_in.text}", font_size='13sp', bold=True, color=(0.063, 0.725, 0.506, 1)))
        card.add_widget(Label(text=f"Total Córneres: {total_esperado:.2f} | Prob. Over: {prob_over:.1f}%", font_size='12sp', bold=True, color=(0.231, 0.510, 0.965, 1)))
        card.add_widget(Label(text=f"Veredicto: {veredicto}", font_size='11sp', bold=True, color=color_ver))
        
        self.res_layout.add_widget(card)
        import re
import math
from kivy.core.clipboard import Clipboard
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle

class GoalsScreen(Screen):
    """Módulo de Goles: Análisis detallado de +0.5 hasta +4.5 con probabilidades y colores de acierto."""
    def __init__(self, **kwargs):
        super(GoalsScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=15, spacing=8)
        
        # Título del Módulo
        layout.add_widget(Label(
            text="MÓDULO: LÍNEAS DE GOLES (0.5 AL 4.5)",
            font_size='13sp', bold=True, size_hint=(1, None), height=26,
            color=(0.231, 0.510, 0.965, 1)
        ))
        
        # --- SECCIÓN DEL PROMPT Y BOTONES DE AYUDA ---
        prompt_box = BoxLayout(orientation='vertical', size_hint=(1, None), height=130, spacing=4)
        prompt_box.add_widget(Label(
            text="1. Pega aquí el reporte de goles y estadísticas:",
            font_size='10sp', color=(0.8, 0.8, 0.8, 1), size_hint=(1, None), height=15
        ))
        
        self.prompt_input = TextInput(
            text='', 
            multiline=True, 
            hint_text='Ej:\nPartido: Real Madrid vs Barcelona\nLocal (Casa) - Goles a Favor: 2.1, Goles en Contra: 0.8\nVisitante (Fuera) - Goles a Favor: 1.8, Goles en Contra: 1.1',
            size_hint=(1, None), height=58
        )
        prompt_box.add_widget(self.prompt_input)
        
        btn_row = BoxLayout(orientation='horizontal', size_hint=(1, None), height=32, spacing=8)
        
        btn_copiar_modelo = Button(
            text='COPIAR PROMPT PARA LA IA', font_size='10sp',
            background_color=(0.3, 0.4, 0.6, 1), color=(1, 1, 1, 1)
        )
        btn_copiar_modelo.bind(on_press=self.copiar_plantilla_prompt)
        
        btn_parse = Button(
            text='EXTRAER DATOS', font_size='10sp',
            background_color=(0.231, 0.510, 0.965, 1), color=(1, 1, 1, 1)
        )
        btn_parse.bind(on_press=self.rellenar_desde_prompt)
        
        btn_row.add_widget(btn_copiar_modelo)
        btn_row.add_widget(btn_parse)
        prompt_box.add_widget(btn_row)
        layout.add_widget(prompt_box)
        
        # --- FORMULARIO DE PARÁMETROS ---
        form = BoxLayout(orientation='vertical', size_hint=(1, None), height=180, spacing=5)
        
        r_teams = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height=32)
        self.h_in = TextInput(text='Local', multiline=False, hint_text='Equipo Local')
        self.a_in = TextInput(text='Visitante', multiline=False, hint_text='Equipo Visitante')
        r_teams.add_widget(self.h_in)
        r_teams.add_widget(self.a_in)
        form.add_widget(r_teams)
        
        form.add_widget(Label(text="Promedios Goles Local (Casa):", font_size='10sp', color=(0.063, 0.725, 0.506, 1), size_hint=(1, None), height=14))
        r_home = BoxLayout(orientation='horizontal', spacing=6, size_hint=(1, None), height=32)
        self.h_gf = TextInput(text='1.8', multiline=False, input_filter='float', hint_text='A Favor (Casa)')
        self.h_ga = TextInput(text='0.9', multiline=False, input_filter='float', hint_text='En Contra (Casa)')
        r_home.add_widget(self.h_gf)
        r_home.add_widget(self.h_ga)
        form.add_widget(r_home)
        
        form.add_widget(Label(text="Promedios Goles Visitante (Fuera):", font_size='10sp', color=(0.063, 0.725, 0.506, 1), size_hint=(1, None), height=14))
        r_away = BoxLayout(orientation='horizontal', spacing=6, size_hint=(1, None), height=32)
        self.a_gf = TextInput(text='1.5', multiline=False, input_filter='float', hint_text='A Favor (Fuera)')
        self.a_ga = TextInput(text='1.2', multiline=False, input_filter='float', hint_text='En Contra (Fuera)')
        r_away.add_widget(self.a_gf)
        r_away.add_widget(self.a_ga)
        form.add_widget(r_away)
        
        btn_calc = Button(
            text='CALCULAR MODELO DE GOLES', size_hint=(1, None), height=35,
            background_color=(0.063, 0.725, 0.506, 1), color=(1, 1, 1, 1)
        )
        btn_calc.bind(on_press=self.calcular_goles_optimo)
        form.add_widget(btn_calc)
        layout.add_widget(form)
        
        # --- SECCIÓN DE RESULTADOS (TARJETAS DINÁMICAS 0.5 AL 4.5) ---
        self.res_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=6)
        self.res_layout.bind(minimum_height=self.res_layout.setter('height'))
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.res_layout)
        layout.add_widget(scroll)
        
        # Botón para volver al Menú Principal
        btn_ret = Button(
            text='VOLVER AL MENÚ', size_hint=(1, None), height=35,
            background_color=(0.3, 0.3, 0.3, 1), color=(1, 1, 1, 1)
        )
        btn_ret.bind(on_press=lambda x: setattr(self.manager, 'current', 'dashboard'))
        layout.add_widget(btn_ret)
        self.add_widget(layout)
        
        self.calcular_goles_optimo(None)

    def copiar_plantilla_prompt(self, instance):
        """Copia la plantilla exacta estructurada para extraer estadísticas de goles."""
        plantilla = (
            "Analiza el siguiente partido de fútbol y dame las estadísticas de goles estrictamente en este formato:\n"
            "Partido: [Equipo Local] vs [Equipo Visitante]\n"
            "Local (Casa) - Goles a Favor: [X.X], Goles en Contra: [X.X]\n"
            "Visitante (Fuera) - Goles a Favor: [X.X], Goles en Contra: [X.X]"
        )
        Clipboard.copy(plantilla)
        
        self.res_layout.clear_widgets()
        card = BoxLayout(orientation='vertical', padding=8, size_hint=(1, None), height=40)
        card.add_widget(Label(text="¡Plantilla de Goles copiada! Pégala en tu IA o fuente.", font_size='11sp', color=(0.063, 0.725, 0.506, 1)))
        self.res_layout.add_widget(card)

    def rellenar_desde_prompt(self, instance):
        """Extrae automáticamente los promedios de goles y nombres desde el texto pegado."""
        texto = self.prompt_input.text
        if not texto:
            return
            
        try:
            match_partido = re.search(r'[:\-]\s*([a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+)\s+vs\s+([a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+)', texto, re.IGNORECASE)
            if match_partido:
                self.h_in.text = match_partido.group(1).strip()
                self.a_in.text = match_partido.group(2).strip()

            lineas = texto.split('\n')
            for linea in lineas:
                linea_lower = linea.lower()
                numeros = re.findall(r'\d+(?:\.\d+)?', linea)
                
                if 'local' in linea_lower and len(numeros) >= 2:
                    self.h_gf.text = numeros[0]
                    self.h_ga.text = numeros[1]
                elif ('visitante' in linea_lower or 'fuera' in linea_lower) and len(numeros) >= 2:
                    self.a_gf.text = numeros[0]
                    self.a_ga.text = numeros[1]

            self.calcular_goles_optimo(None)
        except Exception as e:
            print("Error al parsear goles:", e)

    def calcular_goles_optimo(self, instance):
        """Calcula probabilidades acumuladas de 0.5 a 4.5 usando distribución de Poisson y pinta en verdes graduados."""
        self.res_layout.clear_widgets()
        try:
            h_gf = float(self.h_gf.text or 0)
            h_ga = float(self.h_ga.text or 0)
            a_gf = float(self.a_gf.text or 0)
            a_ga = float(self.a_ga.text or 0)
        except ValueError:
            return
            
        # Cálculo de Expected Goals (xG) para local y visitante
        xg_home = (h_gf + a_ga) / 2.0
        xg_away = (a_gf + h_ga) / 2.0
        total_xg = xg_home + xg_away

        # Función de Poisson P(k event) = (lambda^k * e^-lambda) / k!
        def poisson_prob(lmbda, k):
            if lmbda <= 0:
                return 1.0 if k == 0 else 0.0
            return (math.pow(lmbda, k) * math.exp(-lmbda)) / math.factorial(k)

        # Calcular probabilidades de goles totales exactos (0 hasta 6 goles)
        prob_exactos = {}
        max_goles = 6
        for g in range(max_goles + 1):
            prob_g = 0
            # Cruzar resultados posibles de local y visitante que sumen 'g' goles
            for gh in range(g + 1):
                ga = g - gh
                prob_g += poisson_prob(xg_home, gh) * poisson_prob(xg_away, ga)
            prob_exactos[g] = prob_g

        # Probabilidades Over acumuladas (+0.5, +1.5, +2.5, +3.5, +4.5)
        lineas_goles = [0.5, 1.5, 2.5, 3.5, 4.5]
        prob_overs = {}
        
        # Probabilidad de Under 0.5 es P(0 goles)
        p_under_05 = prob_exactos.get(0, 0)
        prob_overs[0.5] = (1.0 - p_under_05) * 100.0

        for linea in lineas_goles[1:]:
            entero_limite = int(linea) # Ej: 1.5 -> 1 (goles 0 y 1 son under)
            p_under = sum(prob_exactos.get(g, 0) for g in range(entero_limite + 1))
            prob_overs[linea] = max(1.0, min(99.0, (1.0 - p_under) * 100.0))

        # Tarjeta de cabecera con el resumen de Expectativa de Goles (xG)
        header_card = BoxLayout(orientation='vertical', padding=8, spacing=3, size_hint=(1, None), height=55)
        with header_card.canvas.before:
            Color(0.12, 0.16, 0.25, 1)
            header_card.rect = RoundedRectangle(pos=header_card.pos, size=header_card.size, radius=[6])
        header_card.bind(
            pos=lambda inst, val: setattr(inst.rect, 'pos', inst.pos),
            size=lambda inst, val: setattr(inst.rect, 'size', inst.size)
        )
        header_card.add_widget(Label(text=f"Partido: {self.h_in.text} vs {self.a_in.text}", font_size='11sp', bold=True, color=(0.063, 0.725, 0.506, 1)))
        header_card.add_widget(Label(text=f"Goles Esperados (xG Total): {total_xg:.2f} (Local: {xg_home:.2f} - Visitante: {xg_away:.2f})", font_size='10sp', color=(0.8, 0.8, 0.8, 1)))
        self.res_layout.add_widget(header_card)

        # Renderizar cada línea de gol con su tarjeta graduada en tonos verdes
        for linea in lineas_goles:
            prob = prob_overs[linea]
            
            # Asignación de tonos de verde según la probabilidad y relevancia de acierto
            if prob >= 80.0:
                # Verde intenso principal
                bg_color = (0.05, 0.35, 0.20, 1)
                border_label = "¡ALTA CONFIANZA (SEGURO)!"
            elif prob >= 65.0:
                # Verde medio brillante
                bg_color = (0.063, 0.55, 0.35, 1)
                border_label = "RECOMENDADO"
            elif prob >= 45.0:
                # Verde suave / moderado
                bg_color = (0.08, 0.45, 0.40, 1)
                border_label = "MODERADO"
            else:
                # Verde atenuado o neutro oscuro para opciones de bajo porcentaje
                bg_color = (0.15, 0.22, 0.30, 1)
                border_label = "BAJA PROBABILIDAD"

            card = BoxLayout(orientation='horizontal', padding=10, size_hint=(1, None), height=42)
            with card.canvas.before:
                Color(*bg_color)
                card.rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[6])
            card.bind(
                pos=lambda inst, val: setattr(inst.rect, 'pos', inst.pos),
                size=lambda inst, val: setattr(inst.rect, 'size', inst.size)
            )
            
            lbl_linea = Label(text=f"Más de {linea} Goles (Over)", font_size='11sp', bold=True, color=(1, 1, 1, 1), halign='left')
            lbl_linea.bind(size=lambda s, w: setattr(s, 'text_size', w))
            
            lbl_prob = Label(text=f"{prob:.1f}%", font_size='12sp', bold=True, color=(0.9, 1, 0.9, 1), halign='right')
            lbl_prob.bind(size=lambda s, w: setattr(s, 'text_size', w))
            
            card.add_widget(lbl_linea)
            card.add_widget(lbl_prob)
            self.res_layout.add_widget(card)
        
class BankrollCard(BoxLayout):
    """Tarjeta visual para mostrar el estado del bankroll."""
    def __init__(self, stats, **kwargs):
        super(BankrollCard, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 12
        self.spacing = 6
        self.size_hint = (1, None)
        self.height = 140

        if stats is None:
            stats = {}

        with self.canvas.before:
            Color(0.12, 0.16, 0.25, 1)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[8])
        self.bind(pos=self.update_rect, size=self.update_rect)

        current_bank = stats.get('current_bank', stats.get('bankroll', stats.get('balance', 0.0)))
        total_bets = stats.get('total_bets', stats.get('bets', 0))
        net_profit = stats.get('net_profit', stats.get('profit', 0.0))
        roi = stats.get('roi', 0.0)
        win_rate = stats.get('win_rate', stats.get('hit_rate', 0.0))

        lbl_title = Label(
            text='ESTADO DE BANKROLL',
            font_size='14sp',
            bold=True,
            color=(0.063, 0.725, 0.506, 1)
        )
        lbl_bank = Label(
            text=f"Bankroll actual: ${float(current_bank):,.2f}",
            font_size='13sp',
            bold=True,
            color=(0.231, 0.510, 0.965, 1)
        )
        lbl_stats = Label(
            text=f"Apuestas: {total_bets} | Beneficio neto: ${float(net_profit):,.2f}",
            font_size='12sp',
            color=(0.9, 0.9, 0.9, 1)
        )
        lbl_roi = Label(
            text=f"ROI: {float(roi):.2f}% | Acierto: {float(win_rate):.1f}%",
            font_size='12sp',
            color=(0.9, 0.9, 0.9, 1)
        )

        self.add_widget(lbl_title)
        self.add_widget(lbl_bank)
        self.add_widget(lbl_stats)
        self.add_widget(lbl_roi)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class BankrollScreen(Screen):
    """Pantalla interactiva del módulo Bankroll utilizando la lógica de gestión."""
    def __init__(self, **kwargs):
        super(BankrollScreen, self).__init__(**kwargs)
        self.manager_logic = BankrollManager(initial_bank=100000.0)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        layout.add_widget(Label(
            text="MÓDULO: GESTIÓN DE BANKROLL",
            font_size='18sp',
            bold=True,
            size_hint=(1, None),
            height=30,
            color=(0.063, 0.725, 0.506, 1),
        ))

        # Controles para simular/añadir apuestas rápidas
        controls = BoxLayout(orientation='horizontal', size_hint=(1, None), height=45, spacing=10)
        self.stake_input = TextInput(text='10000', multiline=False, input_filter='float', hint_text='Stake')
        self.odds_input = TextInput(text='1.85', multiline=False, input_filter='float', hint_text='Cuota')
        btn_win = Button(text='GANADA', background_color=(0.063, 0.725, 0.506, 1), color=(1, 1, 1, 1))
        btn_win.bind(on_press=lambda x: self.registrar_apuesta('win'))

        controls.add_widget(self.stake_input)
        controls.add_widget(self.odds_input)
        controls.add_widget(btn_win)
        layout.add_widget(controls)

        self.results_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        self.results_layout.bind(minimum_height=self.results_layout.setter('height'))

        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.results_layout)
        layout.add_widget(scroll)

        btn_return = Button(
            text='VOLVER AL MENÚ',
            size_hint=(1, None),
            height=40,
            background_color=(0.3, 0.3, 0.3, 1),
            color=(1, 1, 1, 1),
        )
        btn_return.bind(on_press=lambda x: setattr(self.manager, 'current', 'dashboard'))
        layout.add_widget(btn_return)

        self.add_widget(layout)
        self.actualizar_vista()

    def registrar_apuesta(self, resultado):
        try:
            stake = float(self.stake_input.text)
            odds = float(self.odds_input.text)
        except ValueError:
            stake = 10000.0
            odds = 1.85

        self.manager_logic.add_bet(stake, odds, resultado)
        self.actualizar_vista()

    def actualizar_vista(self):
        self.results_layout.clear_widgets()
        stats = self.manager_logic.get_statistics()
        card = BankrollCard(stats)
        self.results_layout.add_widget(card)




class GenericModuleScreen(Screen):
    """Pantalla genérica corregida para los demás módulos."""
    def __init__(self, module_name, **kwargs):
        super(GenericModuleScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)

        layout.add_widget(Label(
            text=f"MÓDULO: {module_name.upper()}",
            font_size='20sp',
            bold=True,
            color=(0.063, 0.725, 0.506, 1),
        ))
        layout.add_widget(Label(
            text="Módulo configurado y conectado al panel.\nListo para integrar sus funciones específicas.",
            font_size='14sp',
            color=(0.8, 0.8, 0.8, 1),
        ))

        btn_return = Button(
            text='VOLVER AL MENÚ',
            size_hint=(1, None),
            height=45,
            background_color=(0.231, 0.510, 0.965, 1),
            color=(1, 1, 1, 1),
        )
        btn_return.bind(on_press=lambda x: setattr(self.manager, 'current', 'dashboard'))
        layout.add_widget(btn_return)

        self.add_widget(layout)
        self.content_area = BoxLayout(orientation='vertical', size_hint=(0.68, 1))
        def MatchResult1X2Screen():
            ...

        self.content_area.add_widget(MatchResult1X2Screen())
        self.add_widget(self.content_area)
        
    def cargar_modulo_1x2(self):
                self.content_area.clear_widgets()
                def MatchResult1X2Screen():
                    ...

                self.content_area.add_widget(MatchResult1X2Screen())
        


class MainDashboardWindow(BoxLayout):
    """Ventana Principal con diseño inspirado en estética moderna oscura y cian."""
    def __init__(self, **kwargs):
        super(MainDashboardWindow, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.padding = 10
        self.spacing = 10
        with self.canvas.before:
            Color(0.043, 0.059, 0.082, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(
            pos=lambda inst, val: setattr(self.bg_rect, 'pos', inst.pos),
            size=lambda inst, val: setattr(self.bg_rect, 'size', inst.size)
        )
        
        nav_layout = BoxLayout(orientation='vertical', size_hint=(0.32, 1), spacing=10)
        nav_layout.add_widget(Label(
            text="MENÚ DE MÓDULOS", font_size='13sp', bold=True,
            size_hint=(1, None), height=35, color=(0.0, 0.90, 1.0, 1)
        ))
        scroll_menu = ScrollView(size_hint=(1, 1))
        menu_items_box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        menu_items_box.bind(minimum_height=menu_items_box.setter('height'))
        modulos_disponibles = [
            ("Ganador / Empate (1X2)", self.cargar_modulo_1x2),
            ("Ambos Marcan (BTTS)", self.cargar_modulo_btts),
            ("Tarjetas (Árbitro)", self.cargar_modulo_tarjetas),
            ("Córneres", self.cargar_modulo_corners),
            ("Goles (0.5 al 4.5)", self.cargar_modulo_goles),
            ("Bankroll", self.cargar_modulo_bankroll),
        ]
        for nombre_modulo, funcion_carga in modulos_disponibles:
            btn = Button(
                text=nombre_modulo,
                font_size='13sp',
                bold=True,
                size_hint=(1, None), height=52,
                background_color=(0.08, 0.30, 0.65, 1),
                color=(1.0, 1.0, 1.0, 1)
            )
            btn.bind(on_press=lambda inst, func=funcion_carga: func())
            menu_items_box.add_widget(btn)
        scroll_menu.add_widget(menu_items_box)
        nav_layout.add_widget(scroll_menu)
        logo_container = BoxLayout(size_hint=(1, None), height=110, padding=5)
        LOGO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
        logo_widget = Image(
            source=LOGO,
            size_hint=(1, 1),
            allow_stretch=True,
            keep_ratio=True
        )
        logo_container.add_widget(logo_widget)
        nav_layout.add_widget(logo_container)
        self.add_widget(nav_layout)

        # --- ZONA DERECHA DE CONTENIDO DINÁMICO ---
        self.content_area = BoxLayout(orientation='vertical', size_hint=(0.68, 1))
        self.content_area.add_widget(MatchResult1X2Screen()) # type: ignore
        self.add_widget(self.content_area)
        
        # Forzar redibujado diferido para evitar pantalla en negro en el arranque
        Clock.schedule_once(lambda dt: self.do_layout(), 0.1)

    def cargar_modulo_1x2(self):
        self.content_area.clear_widgets()
        w = MatchResult1X2Screen()
        if w: self.content_area.add_widget(w)

    def cargar_modulo_btts(self):
        self.content_area.clear_widgets()
        # Verificamos si la clase existe antes de instanciarla
        if 'BothTeamsScoreScreen' in globals():
            w = BothTeamsScoreScreen()
            if w: self.content_area.add_widget(w)
        else:
            self.content_area.add_widget(Label(text="Módulo BTTS en construcción", color=(1,1,1,1)))

    def cargar_modulo_tarjetas(self):
        self.content_area.clear_widgets()
        if 'YellowCardsScreen' in globals():
            w = YellowCardsScreen()
            if w: self.content_area.add_widget(w)
        else:
            self.content_area.add_widget(Label(text="Módulo Tarjetas en construcción", color=(1,1,1,1)))

    def cargar_modulo_corners(self):
        self.content_area.clear_widgets()
        if 'CornersScreen' in globals():
            w = CornersScreen()
            if w: self.content_area.add_widget(w)
        else:
            self.content_area.add_widget(Label(text="Módulo Córneres en construcción", color=(1,1,1,1)))

    def cargar_modulo_goles(self):
        self.content_area.clear_widgets()
        if 'GoalsScreen' in globals():
            w = GoalsScreen()
            if w: self.content_area.add_widget(w)
        else:
            self.content_area.add_widget(Label(text="Módulo Goles en construcción", color=(1,1,1,1)))

    def cargar_modulo_bankroll(self):
        self.content_area.clear_widgets()
        if 'BankrollScreen' in globals():
            w = BankrollScreen()
            if w: self.content_area.add_widget(w)
        else:
            self.content_area.add_widget(Label(text="Módulo Bankroll en construcción", color=(1,1,1,1)))

class AnalysisSportApp(App):
    def build(self):
        return MainDashboardWindow()


if __name__ == '__main__':
    try:
        AnalysisSportApp().run()
    except Exception as e:
        import traceback
        traceback.print_exc()
        input("\nPresiona Enter para cerrar...")