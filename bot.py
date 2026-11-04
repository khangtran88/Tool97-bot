"""Bot Telegram báo Parabolic SAR đảo chiều (crypto, dữ liệu OKX, miễn phí)."""
import json
import os
import requests

# ======================= CHỈNH Ở ĐÂY =======================
# Danh sách cặp tiền (định dạng OKX: COIN-USDT)
PAIRS = ["BTC-USDT", "ETH-USDT", "SOL-USDT"]

# Khung thời gian: "1H" và "4H"
# Thông số SAR cho từng khung: (bắt đầu, bước tăng, tối đa)
# Mặc định chuẩn TradingView là (0.02, 0.02, 0.2)
SAR_SETTINGS = {
    "1H": (0.02, 0.02, 0.2),
    "4H": (0.02, 0.02, 0.2),
}
# ===========================================================

STATE_FILE = "state.json"


def get_candles(pair, bar):
    """Lấy tối đa 300 nến ĐÃ ĐÓNG, cũ -> mới. Mỗi nến: (ts, high, low, close)."""
    url = "https://www.okx.com/api/v5/market/candles"
    r = requests.get(url, params={"instId": pair, "bar": bar, "limit": 300}, timeout=20)
    r.raise_for_status()
    rows = r.json()["data"]  # mới -> cũ
    out = []
    for row in reversed(rows):
        if row[8] != "1":  # bỏ nến đang chạy
            continue
        out.append((int(row[0]), float(row[2]), float(row[3]), float(row[4])))
    return out


def psar(highs, lows, start, inc, maxaf):
    """Trả về (danh sách xu hướng True=tăng, danh sách giá trị SAR)."""
    n = len(highs)
    up = highs[1] >= highs[0] if n > 1 else True
    sar = lows[0] if up else highs[0]
    ep = highs[0] if up else lows[0]
    af = start
    trends, sars = [up], [sar]
    for i in range(1, n):
        sar = sar + af * (ep - sar)
        if up:
            sar = min(sar, lows[i - 1], lows[i - 2] if i >= 2 else lows[i - 1])
            if lows[i] < sar:  # đảo chiều sang giảm
                up, sar, ep, af = False, ep, lows[i], start
            elif highs[i] > ep:
                ep, af = highs[i], min(af + inc, maxaf)
        else:
            sar = max(sar, highs[i - 1], highs[i - 2] if i >= 2 else highs[i - 1])
            if highs[i] > sar:  # đảo chiều sang tăng
                up, sar, ep, af = True, ep, highs[i], start
            elif lows[i] < ep:
                ep, af = lows[i], min(af + inc, maxaf)
        trends.append(up)
        sars.append(sar)
    return trends, sars


def find_flips(candles, params, last_ts):
    """Tìm các lần đảo chiều ở nến mới hơn last_ts."""
    highs = [c[1] for c in candles]
    lows = [c[2] for c in candles]
    trends, sars = psar(highs, lows, *params)
    flips = []
    for i in range(1, len(candles)):
        if trends[i] != trends[i - 1]:
            ts = candles[i][0]
            if last_ts is None:
                if i == len(candles) - 1:  # lần chạy đầu: chỉ xét nến mới nhất
                    flips.append((ts, trends[i], candles[i][3], sars[i]))
            elif ts > last_ts:
                flips.append((ts, trends[i], candles[i][3], sars[i]))
    return flips


def send_telegram(text):
    token = os.environ["TELEGRAM_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    r = requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": text},
        timeout=20,
    )
    r.raise_for_status()


def main():
    state = {}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            state = json.load(f)

    for pair in PAIRS:
        for bar, params in SAR_SETTINGS.items():
            key = f"{pair}_{bar}"
            try:
                candles = get_candles(pair, bar)
                if len(candles) < 20:
                    continue
                for ts, is_up, close, sar_val in find_flips(candles, params, state.get(key)):
                    if is_up:
                        msg = f"🟢 {pair} {bar}: SAR đảo sang TĂNG (MUA)"
                    else:
                        msg = f"🔴 {pair} {bar}: SAR đảo sang GIẢM (BÁN)"
                    msg += f"\nGiá đóng nến: {close}\nSAR: {sar_val:.6g}"
                    send_telegram(msg)
                state[key] = candles[-1][0]
            except Exception as e:
                print(f"Lỗi {key}: {e}")

    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


if __name__ == "__main__":
    main()
