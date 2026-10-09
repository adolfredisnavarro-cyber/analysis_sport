class RetoEscaleraCalculator:
    """Calcula la progresión matemática de los 10 pasos con interés compuesto y base del 60%."""

    def __init__(self, initial_bank=50000.0, stake_percentage=0.60, fixed_odds=1.50, total_steps=10):
        self.initial_bank = initial_bank
        self.stake_percentage = stake_percentage
        self.fixed_odds = fixed_odds
        self.total_steps = total_steps

    def calculate_ladder(self):
        """Genera la tabla completa de los 10 pasos de la escalera."""
        ladder_steps = []
        current_bank = self.initial_bank

        for step in range(1, self.total_steps + 1):
            # El monto a apostar es el porcentaje (60%) del bank disponible actual
            stake = round(current_bank * self.stake_percentage, 2)
            gross_return = round(stake * self.fixed_odds, 2)
            net_profit = round(gross_return - stake, 2)
            
            # El nuevo bank total se actualiza sumando la ganancia neta al bank anterior
            next_bank = round((current_bank - stake) + gross_return, 2)

            ladder_steps.append({
                "step": step,
                "bank_before": current_bank,
                "stake": stake,
                "odds": self.fixed_odds,
                "gross_return": gross_return,
                "net_profit": net_profit,
                "bank_after": next_bank
            })

            current_bank = next_bank

        return ladder_steps