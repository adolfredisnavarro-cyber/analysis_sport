class FootballPredictor:
    """Motor profesional de predicción de fútbol con splits de local/visitante y rachas."""

    def __init__(self, home_team, away_team, 
                 h_scored_home, h_conceded_home, h_matches_home, h_recent_points,
                 a_scored_away, a_conceded_away, a_matches_away, a_recent_points):
        self.home_team = home_team
        self.away_team = away_team
        
        # Estadísticas del Local jugando EXCLUSIVAMENTE en casa
        self.h_scored = float(h_scored_home)
        self.h_conceded = float(h_conceded_home)
        self.h_matches = max(float(h_matches_home), 1.0)
        self.h_form = float(h_recent_points) # Puntos en últimos 5 partidos (max 15)
        
        # Estadísticas del Visitante jugando EXCLUSIVAMENTE fuera
        self.a_scored = float(a_scored_away)
        self.a_conceded = float(a_conceded_away)
        self.a_matches = max(float(a_matches_away), 1.0)
        self.a_form = float(a_recent_points) # Puntos en últimos 5 partidos (max 15)

    def calculate_prediction(self):
        # 1. Promedios puros de local y visitante
        h_avg_scored = self.h_scored / self.h_matches
        h_avg_conceded = self.h_conceded / self.h_matches
        
        a_avg_scored = self.a_scored / self.a_matches
        a_avg_conceded = self.a_conceded / self.a_matches

        # 2. Goles esperados (xG cruzando el ataque local vs defensa visitante y viceversa)
        home_xg = (h_avg_scored + a_avg_conceded) / 2
        away_xg = (a_avg_scored + h_avg_conceded) / 2

        # 3. Ajuste por estado de forma reciente (normalizado sobre 15 puntos posibles)
        form_multiplier_home = 1.0 + ((self.h_form - 7.5) / 30.0) # Ajuste sutil por racha
        form_multiplier_away = 1.0 + ((self.a_form - 7.5) / 30.0)

        home_power = home_xg * 1.10 * max(0.8, form_multiplier_home)
        away_power = away_xg * max(0.8, form_multiplier_away)

        diff = home_power - away_power

        # 4. Determinación de probabilidades y recomendación
        if diff > 0.30:
            home_prob, draw_prob, away_prob = 54.0, 26.0, 20.0
            recommendation = f"Gana {self.home_team} (1)"
        elif diff < -0.30:
            home_prob, draw_prob, away_prob = 20.0, 26.0, 54.0
            recommendation = f"Gana {self.away_team} (2)"
        else:
            home_prob, draw_prob, away_prob = 37.0, 35.0, 28.0
            recommendation = f"Doble Oportunidad: {self.home_team} o Empate (1X)"

        return {
            "home_team": self.home_team,
            "away_team": self.away_team,
            "home_xg": round(home_power, 2),
            "away_xg": round(away_power, 2),
            "home_prob": home_prob,
            "draw_prob": draw_prob,
            "away_prob": away_prob,
            "recommendation": recommendation
        }