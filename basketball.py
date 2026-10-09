class BasketballAnalyzer:
    """Calcula las métricas de puntos y rendimiento por cuartos en baloncesto."""

    @staticmethod
    def analyze_points(datos):
        """Calcula la proyección de puntos totales para el partido."""
        if not datos or any(v is None for v in datos.values()):
            return {"error": "Faltan datos reales o están incompletos."}

        puntos_local = datos.get("DATO_1", 0)
        puntos_visita = datos.get("DATO_2", 0)
        media_liga = datos.get("DATO_3", 0)

        proyeccion_total = round((puntos_local + puntos_visita + media_liga) / 3, 1)

        return {
            "proyeccion_puntos_totales": proyeccion_total,
            "analisis": "Ritmo ofensivo alto" if proyeccion_total > 150 else "Ritmo defensivo / Bajo anotador"
        }