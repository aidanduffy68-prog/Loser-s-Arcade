import random
import csv
import statistics
from datetime import datetime

# Simple FryCoin simulation engine (auto-played for data collection)
def simulate_run(start_balance=10000, max_rounds=15):
    balance = start_balance
    rounds_survived = 0
    total_trades = 0
    largest_loss = 0
    largest_win = 0

    regime = "NORMAL"
    regimes = ["NORMAL", "HIGH VOL", "CRASH"]

    while balance > 0 and rounds_survived < max_rounds:
        rounds_survived += 1
        trade_size = random.randint(100, 1000)
        action = random.choice(["YOLO", "REVENGE", "CALL"])

        # outcome bias: more likely to lose
        if action in ["YOLO", "REVENGE"]:
            pnl_pct = random.gauss(-0.4, 0.5)  # centered on -40% loss
        else:  # CALL
            pnl_pct = random.gauss(-0.1, 0.2)  # safer, still tends to lose

        pnl = int(trade_size * pnl_pct)
        balance += pnl
        total_trades += 1

        largest_loss = min(largest_loss, pnl)
        largest_win = max(largest_win, pnl)

        # update regime based on balance & chaos
        if balance < start_balance * 0.5:
            regime = random.choice(["HIGH VOL", "CRASH"])

    return {
        "final_balance": max(balance, 0),
        "rounds_survived": rounds_survived,
        "total_trades": total_trades,
        "largest_loss": largest_loss,
        "largest_win": largest_win,
        "ending_regime": regime
    }


def run_simulations(n=100, output_file="../simulations/auto_runs.csv"):
    results = []
    for i in range(n):
        run = simulate_run()
        run["run_id"] = i + 1
        results.append(run)

    # write to CSV
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "run_id", "final_balance", "rounds_survived", "total_trades",
                "largest_loss", "largest_win", "ending_regime"
            ]
        )
        writer.writeheader()
        writer.writerows(results)

    # print quick summary
    balances = [r["final_balance"] for r in results]
    print(f"Simulations complete: {n} runs")
    print(f"Average Final Balance: {statistics.mean(balances):.2f}")
    print(f"Median Final Balance: {statistics.median(balances):.2f}")
    print(f"Zeroed Accounts: {sum(b == 0 for b in balances)} / {n}")


if __name__ == "__main__":
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_simulations(100, f"../simulations/runs_{timestamp}.csv")
