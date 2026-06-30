"""Render verdict results into a markdown report card (for TG / README / blog)."""
from __future__ import annotations
import json
from pathlib import Path

RESULTS = Path("/home/raphael/projects/lab/results")
REPORTS = Path("/home/raphael/projects/lab/reports")
REPORTS.mkdir(parents=True, exist_ok=True)

VERDICT_EMOJI = {
    True: "❌ Falsified by deflate",
    False: "✅ Survived deflate gauntlet",
}


def render_card(payload: dict) -> str:
    """Single-card format suitable for TG or GitHub release notes."""
    df = payload["deflate"]
    metrics = df["metrics"]
    dsr = metrics.get("dsr", {}).get("dsr", 0)
    pbo = metrics.get("pbo", {}).get("pbo", 0)
    wf = metrics.get("walk_forward", {}).get("fraction_positive", 0)
    boot_sr_p = metrics.get("bootstrap", {}).get("prob_sr_le_zero", 0)
    oos = payload["oos_sharpe"]
    is_sr = payload["is_sharpe"]

    return f"""## {payload['strategy']} on {payload['symbol']} ({payload['start']} → {payload['end']})

**Verdict:** {VERDICT_EMOJI[df['is_overfit']]} (deflate confidence {df['confidence']*100:.0f}%)

| Metric | Value | Read |
|---|---|---|
| In-sample Sharpe | {is_sr:.2f} | naive pick |
| Out-of-sample Sharpe | {oos:.2f} | the real test |
| **Deflated Sharpe (DSR)** | {dsr:.2f} | {'< 0.95 → not significant after multiple-testing correction' if dsr < 0.95 else '≥ 0.95 → survives selection bias'} |
| **PBO (CSCV)** | {pbo:.2f} | {'≥ 0.50 → in-sample best likely fails OOS' if pbo >= 0.50 else '< 0.50 → IS winner survives OOS'} |
| Walk-forward stability | {wf*100:.0f}% positive folds | |
| Bootstrap P(SR ≤ 0) | {boot_sr_p:.2f} | |
| Configs swept | {payload['n_configs']} | n_trials honest |
| Best params | `{payload['best_params']}` | |

### Why deflate said this

{chr(10).join('- ' + r for r in df['reasons'])}

---

🔬 **Reproduce:**
```bash
git clone https://github.com/raphael2025/experiment-encyclopedia
cd experiment-encyclopedia
python -m experiments.runner --strategy {payload['strategy']} --symbol {payload['symbol']}
```

📲 Discussion & weekly verdicts: [Telegram — Raphael交易系统](https://t.me/+E3UdPtwlISVhZDc1)
"""


def main():
    cards = []
    for f in sorted(RESULTS.glob("*_BTCUSDT.json")):
        if "_grid" in f.name or "_returns" in f.name:
            continue
        p = json.loads(f.read_text())
        card = render_card(p)
        (REPORTS / f"{p['strategy']}_card.md").write_text(card)
        cards.append(card)
        print(f"  ✓ {f.name} → {p['strategy']}_card.md")

    # 汇总卡
    summary = "# deflate 实验判决 — BTC 1d (2020-2026)\n\n"
    summary += "5 个策略，5 个 OVERFIT。**BTC 6 年日线无 alpha**（仅 funding carry 因现货腿保持弱正）。\n\n"
    for c in cards:
        # extract first table row
        first_line = c.split("\n")[2] if "\n" in c else c
        summary += f"- {first_line}\n"
    (REPORTS / "summary_BTC.md").write_text(summary)
    print(f"\n  ✓ summary → reports/summary_BTC.md")


if __name__ == "__main__":
    main()