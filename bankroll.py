class BankrollManager:
    """Gestiona el registro de apuestas, control de caja, ganancias y rendimiento (Yield)."""

    def __init__(self, initial_bank=50000.0):
        self.initial_bank = initial_bank
        self.bets_history = []

    def add_bet(self, stake, odds, result):
        """
        Añade una apuesta al historial.
        :param stake: Cantidad apostada
        :param odds: Cuota de la apuesta
        :param result: 'win' (ganada), 'loss' (perdida), 'void' (nula)
        """
        profit = 0.0
        if result == 'win':
            profit = (stake * odds) - stake
        elif result == 'loss':
            profit = -stake
        elif result == 'void':
            profit = 0.0

        bet_record = {
            "stake": stake,
            "odds": odds,
            "result": result,
            "profit": round(profit, 2)
        }
        self.bets_history.append(bet_record)

    def get_statistics(self):
        """Calcula el balance total, el profit neto y el Yield de la sesión/historial."""
        total_staked = sum(b["stake"] for b in self.bets_history)
        total_profit = sum(b["profit"] for b in self.bets_history)
        current_bank = self.initial_bank + total_profit

        yield_percentage = 0.0
        if total_staked > 0:
            yield_percentage = round((total_profit / total_staked) * 100, 2)

        return {
            "initial_bank": self.initial_bank,
            "current_bank": round(current_bank, 2),
            "total_profit": round(total_profit, 2),
            "total_staked": round(total_staked, 2),
            "yield": yield_percentage,
            "total_bets": len(self.bets_history)
        }