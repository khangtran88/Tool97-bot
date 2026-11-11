"""Bot Telegram: AlgoAlpha Trend Targets khung M15, chỉ báo khi M15, H1, H4 đồng thuận (Binance Futures)."""
import json
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

import requests

# Danh sách cặp tiền giữ nguyên trong file bot.py cũ (không xóa file bot.py)
from bot import PAIRS, rma_atr, wma, ema, supertrend_bands

# ======================= CHỈNH Ở ĐÂY =======================
# Chỉ báo trên khung M15: (Factor, ATR period, WMA, EMA)
M15_PARAMS = (8.0, 90, 40, 14)
# Chỉ báo dùng để xác định xu hướng khung H1 và H4
HTF_PARAMS = (8.0, 30, 40, 14)

REQUIRE_H1 = True          # bắt buộc H1 cùng xu hướng
REQUIRE_H4 = True          # bắt buộc H4 cùng xu hướng
USE_EMA_FILTER = True      # bắt buộc giá M15 cùng phía với EMA
EMA_FILTER_LEN = 100       # độ dài EMA (khung M15)

ATR_PERIOD = 14            # ATR dùng để tính SL (khung M15)
SL_MULT = 5.0              # SL = x lần ATR dưới đáy (trên đỉnh) nến tín hiệu
TP_R = (1.0, 2.0, 3.0)     # TP1, TP2, TP3 tính theo bội số khoảng cách SL
MAX_HOLD_HOURS = 120       # nhắc đóng lệnh sau 5 ngày
# ===========================================================

STATE_FILE = "state_m15.json"
M15_CANDLES = 1000         # số nến M15 tải mỗi lần (đủ để chỉ báo ổn định)
HTF_CANDLES = 1000         # số nến H1, H4 tải khi cần (chỉ tải khi có tín hiệu M15 mới)
WORKERS = 6                # số luồng tải song song
MIN_INTERVAL = 0.16        # giây giữa 2 lần gọi Binance (giữ dưới giới hạn tốc độ)
IV_MS = {"15m": 900000, "1h": 3600000, "4h": 14400000}

SOURCES = [  # (địa chỉ, tiền tố): Futures trước, Spot dự phòng nếu Futures bị chặn
    ("https://fapi.binance.com", "/fapi/v1"),
    ("https://data-api.binance.vision", "/api/v3"),
    ("https://api.binance.com", "/api/v3"),
    ("https://api1.binance.com", "/api/v3"),
    ("https://api2.binance.com", "/api/v3"),
    ("https://api3.binance.com", "/api/v3"),
]
_fut_blocked = False
_seen = set()
_lock = threading.Lock()
_next_call = 0.0
_offset = None


def _throttle():
    global _next_call
    with _lock:
        now = time.monotonic()
        wait = max(0.0, _next_call - now)
        _next_call = max(now, _next_call) + MIN_INTERVAL
    if wait:
        time.sleep(wait)


def _request(url, params):
    """Gọi 1 địa chỉ, tự chờ và thử lại khi Binance báo quá tốc độ (429/418)."""
    r = None
    for attempt in range(3):
        _throttle()
        r = requests.get(url, params=params, timeout=20)
        if r.status_code in (429, 418):
            try:
                wait = float(r.headers.get("Retry-After", 5))
            except Exception:
                wait = 5
            time.sleep(min(wait, 30))
            continue
        break
    return r


def _get(kind, params):
    """Gọi Binance (kind: 'klines' hoặc 'time'). Thử Futures trước, dự phòng Spot."""
    global _fut_blocked
    saw400, other, last = False, False, "không rõ"
    for host, prefix in SOURCES:
        if prefix == "/fapi/v1" and _fut_blocked:
            continue
        try:
            r = _request(host + prefix + "/" + kind, params)
        except requests.RequestException as e:
            other, last = True, f"{host}: {e}"
            if prefix == "/fapi/v1":
                _fut_blocked = True
            continue
        if r.status_code == 200:
            if host not in _seen:
                _seen.add(host)
                print(f"Nguồn dữ liệu đang dùng: {host}")
            return r.json()
        if r.status_code == 400:
            saw400 = True
            continue
        other, last = True, f"{host}: HTTP {r.status_code}"
        if prefix == "/fapi/v1":
            _fut_blocked = True
    if saw400 and not other:
        raise ValueError(f"Cặp tiền không hợp lệ: {params.get('symbol')}")
    raise RuntimeError(last)


def now_ms():
    """Giờ theo máy chủ Binance (tránh lệch đồng hồ máy chạy bot)."""
    global _offset
    if _offset is None:
        try:
            _offset = int(_get("time", {})["serverTime"]) - int(time.time() * 1000)
        except Exception:
            _offset = 0
    return int(time.time() * 1000) + _offset


def fetch(symbol, interval, limit):
    """Nến ĐÃ ĐÓNG HẲN (đóng ít nhất 3 giây), cũ -> mới: (ts, high, low, close)."""
    cur = now_ms()
    iv = IV_MS[interval]
    rows = _get("klines", {"symbol": symbol, "interval": interval, "limit": limit})
    out = []
    for r in rows:
        if r[0] + iv > cur - 3000 or r[6] >= cur - 3000:
            continue
        out.append((int(r[0]), float(r[2]), float(r[3]), float(r[4])))
    return out


def trend_series(candles, params):
    """Trạng thái xu hướng của chỉ báo (1 tăng, -1 giảm, 0 chưa có) cho từng nến."""
    f, ap, w, e = params
    h = [x[1] for x in candles]
    l = [x[2] for x in candles]
    c = [x[3] for x in candles]
    lo, up = supertrend_bands(h, l, c, f, ap)
    mid = [(a + b) / 2 if a is not None and b is not None else None for a, b in zip(lo, up)]
    tl = ema(wma(mid, w), e)
    trend, cur = [0] * len(c), 0
    for i in range(len(c)):
        if i >= 2 and tl[i] is not None and tl[i - 1] is not None and tl[i - 2] is not None:
            if tl[i] > tl[i - 1] and tl[i - 1] <= tl[i - 2]:
                cur = 1
            if tl[i] < tl[i - 1] and tl[i - 1] >= tl[i - 2]:
                cur = -1
        trend[i] = cur
    return trend


def htf_trend_at(candles, interval, t_close):
    """Xu hướng H1/H4 tại thời điểm t_close, chỉ dùng nến HTF đã đóng trước thời điểm đó."""
    trend = trend_series(candles, HTF_PARAMS)
    iv = IV_MS[interval]
    j = None
    for k in range(len(candles) - 1, -1, -1):
        if candles[k][0] + iv <= t_close:
            j = k
            break
    return trend[j] if j is not None else 0


def fmt(x):
    return f"{x:.8g}"


def vn_time(ms):
    return datetime.fromtimestamp(ms / 1000, timezone(timedelta(hours=7))).strftime("%H:%M %d/%m")


def side_txt(s):
    return "tăng" if s == 1 else "giảm"


def process(pair, st):
    """Xử lý 1 cặp. Trả về dict: ts (nến M15 cuối đã xử lý), open (lệnh đang mở), msgs (tin cần gửi)."""
    candles = fetch(pair, "15m", M15_CANDLES)
    if len(candles) < 300:
        return {"skip": f"không đủ dữ liệu ({len(candles)} nến)"}
    n = len(candles)
    h = [x[1] for x in candles]
    l = [x[2] for x in candles]
    c = [x[3] for x in candles]
    trend = trend_series(candles, M15_PARAMS)
    atr = rma_atr(h, l, c, ATR_PERIOD)
    ema_f = ema(c, EMA_FILTER_LEN) if USE_EMA_FILTER else None

    last, op = st.get("ts"), st.get("open")
    flips = [(i, trend[i]) for i in range(1, n) if trend[i] != trend[i - 1] and trend[i] != 0 and atr[i] is not None]
    if last is None:   # lần chạy đầu: chỉ xét nến mới nhất
        new = [f for f in flips if f[0] == n - 1]
    else:
        new = [f for f in flips if candles[f[0]][0] > last]

    msgs = []
    for i, side in new:
        ts = candles[i][0]
        t_close = ts + IV_MS["15m"]
        if op and op["side"] != side:
            msgs.append(f"⚪ {pair} M15: THOÁT lệnh {'MUA' if op['side'] == 1 else 'BÁN'} (M15 đảo chiều)\n"
                        f"Nến đóng lúc {vn_time(t_close)} (giờ VN), giá {fmt(c[i])}")
            op = None
        why = None
        if USE_EMA_FILTER:
            e = ema_f[i]
            if e is None or (c[i] - e) * side <= 0:
                why = "EMA"
        h1 = h4 = None
        if why is None and REQUIRE_H1:
            h1 = htf_trend_at(fetch(pair, "1h", HTF_CANDLES), "1h", t_close)
            if h1 != side:
                why = "H1"
        if why is None and REQUIRE_H4:
            h4 = htf_trend_at(fetch(pair, "4h", HTF_CANDLES), "4h", t_close)
            if h4 != side:
                why = "H4"
        if why is not None:
            continue
        if side == 1:
            sl = l[i] - atr[i] * SL_MULT
        else:
            sl = h[i] + atr[i] * SL_MULT
        d = abs(c[i] - sl)
        tps = [c[i] + side * d * k for k in TP_R]
        head = (f"🟢 {pair} M15: MUA" if side == 1 else f"🔴 {pair} M15: BÁN") + " (đồng thuận M15 + H1 + H4)"
        lines = [head, f"Nến M15 đóng lúc {vn_time(t_close)} (giờ VN)",
                 f"Entry: {fmt(c[i])}", f"SL: {fmt(sl)} ({SL_MULT:g}xATR)"]
        for k, tp in zip(TP_R, tps):
            lines.append(f"TP{TP_R.index(k) + 1} ({k:g}R): {fmt(tp)}")
        if REQUIRE_H1:
            lines.append(f"H1: {side_txt(h1)} | H4: {side_txt(h4)}" if REQUIRE_H4 else f"H1: {side_txt(h1)}")
        if USE_EMA_FILTER:
            lines.append(f"Giá {'trên' if side == 1 else 'dưới'} EMA{EMA_FILTER_LEN} (M15)")
        lines.append(f"Thoát khi bot báo M15 đảo chiều, hoặc sau {MAX_HOLD_HOURS // 24} ngày")
        msgs.append("\n".join(lines))
        op = {"side": side, "ts": ts}

    if op and (candles[-1][0] + IV_MS["15m"] - op["ts"]) >= MAX_HOLD_HOURS * 3600000:
        msgs.append(f"⏰ {pair} M15: lệnh {'MUA' if op['side'] == 1 else 'BÁN'} đã giữ quá {MAX_HOLD_HOURS // 24} ngày, nên đóng")
        op = None
    return {"ts": candles[-1][0], "open": op, "msgs": msgs}


def send_telegram(text):
    token = os.environ["TELEGRAM_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                      json={"chat_id": chat_id, "text": text}, timeout=20)
    r.raise_for_status()


def main():
    state = {}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            state = json.load(f)
    pairs_state = state.setdefault("pairs", {})
    started = time.time()

    def work(pair):
        try:
            return pair, process(pair, pairs_state.get(pair, {})), None
        except Exception as e:
            return pair, None, str(e)

    ok = fail = sent = 0
    last_err = ""
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        for pair, res, err in ex.map(work, PAIRS):
            if err is not None:
                fail += 1
                last_err = err
                print(f"Lỗi {pair}: {err}")
                continue
            if "skip" in res:
                print(f"Bỏ qua {pair}: {res['skip']}")
                continue
            try:
                for m in res["msgs"]:
                    send_telegram(m)
                    sent += 1
                    time.sleep(0.3)
            except Exception as e:
                fail += 1
                last_err = str(e)
                print(f"Lỗi gửi Telegram {pair}: {e}")
                continue
            pairs_state[pair] = {"ts": res["ts"], "open": res["open"]}
            ok += 1

    if ok == 0 and fail > 0:
        if not state.get("_err"):
            try:
                send_telegram(f"⚠️ Bot không lấy được dữ liệu Binance.\n{last_err}")
                state["_err"] = True
            except Exception as e:
                print(f"Lỗi gửi cảnh báo: {e}")
    elif ok > 0:
        state["_err"] = False

    with open(STATE_FILE, "w") as f:
        json.dump(state, f)
    print(f"Xong: {ok} cặp OK, {fail} lỗi, {sent} tin, {time.time() - started:.0f} giây")


if __name__ == "__main__":
    main()
