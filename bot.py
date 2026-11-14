"""Bot Telegram báo AlgoAlpha Trend Targets đổi chiều xu hướng (Binance, miễn phí)."""
import json
import os
import time
import requests

# ======================= CHỈNH Ở ĐÂY =======================
# Danh sách cặp tiền Binance (viết liền, không có dấu gạch): BTCUSDT, ETHUSDT...
PAIRS = [
    "JCTUSDT",
    "SOLUSDT",
    "ZECUSDT",
    "XRPUSDT",
    "HYPEUSDT",
    "1000PEPEUSDT",
    "NEARUSDT",
    "DOGEUSDT",
    "ENAUSDT",
    "ONUSDT",
    "SUIUSDT",
    "UNIUSDT",
    "AIOTUSDT",
    "HOTUSDT",
    "AVAXUSDT",
    "WLDUSDT",
    "PUMPUSDT",
    "LINKUSDT",
    "ADAUSDT",
    "AKEUSDT",
    "ONEUSDT",
    "AAVEUSDT",
    "ARBUSDT",
    "AINUSDT",
    "TAOUSDT",
    "INJUSDT",
    "UAIUSDT",
    "TRUMPUSDT",
    "BCHUSDT",
    "LTCUSDT",
    "FILUSDT",
    "IDOLUSDT",
    "HANAUSDT",
    "QNTUSDT",
    "PAXGUSDT",
    "RSRUSDT",
    "ASTERUSDT",
    "ICNTUSDT",
    "LITUSDT",
    "ONDOUSDT",
    "XMRUSDT",
    "XLMUSDT",
    "DOTUSDT",
    "XPLUSDT",
    "PENGUUSDT",
    "BMTUSDT",
    "DASHUSDT",
    "ZROUSDT",
    "TRXUSDT",
    "AIOUSDT",
    "STRKUSDT",
    "APTUSDT",
    "TAUSDT",
    "PIEVERSEUSDT",
    "FETUSDT",
    "QUSDT",
    "SKYAIUSDT",
    "HBARUSDT",
    "1000SHIBUSDT",
    "NXPCUSDT",
    "GTCUSDT",
    "TIAUSDT",
    "ETHFIUSDT",
    "CYBERUSDT",
    "OPUSDT",
    "INITUSDT",
    "BIRBUSDT",
    "ETCUSDT",
    "KOMAUSDT",
    "USELESSUSDT",
    "WLFIUSDT",
    "EVAAUSDT",
    "RENDERUSDT",
    "CRVUSDT",
    "ATOMUSDT",
    "AEROUSDT",
    "METUSDT",
    "HUMAUSDT",
    "B2USDT",
    "ICPUSDT",
    "ZILUSDT",
    "VVVUSDT",
    "ARIAUSDT",
    "FARTCOINUSDT",
    "RAYSOLUSDT",
    "1000BONKUSDT",
    "ERAUSDT",
    "VIRTUALUSDT",
    "BEATUSDT",
    "LSKUSDT",
    "NEIROUSDT",
    "LYNUSDT",
    "AGTUSDT",
    "BEAMXUSDT",
    "ACTUSDT",
    "SEIUSDT",
    "WIFUSDT",
    "MEGAUSDT",
    "LDOUSDT",
    "ESPORTSUSDT",
    "SANDUSDT",
    "MERLUSDT",
    "PYTHUSDT",
    "STXUSDT",
    "APRUSDT",
    "GRASSUSDT",
    "MAGMAUSDT",
    "ALGOUSDT",
    "SIGNUSDT",
    "BATUSDT",
    "ZAMAUSDT",
    "CLANKERUSDT",
    "IRYSUSDT",
    "PENDLEUSDT",
    "JUPUSDT",
    "MONUSDT",
    "EIGENUSDT",
    "NIGHTUSDT",
    "龙虾USDT",
    "POLUSDT",
    "JTOUSDT",
    "RIVERUSDT",
    "GALAUSDT",
    "PARTIUSDT",
    "FOGOUSDT",
    "ELSAUSDT",
    "SUSDT",
    "IMXUSDT",
    "ORDIUSDT",
    "BOMEUSDT",
    "ARUSDT",
    "BERAUSDT",
    "ZENUSDT",
    "SPXUSDT",
    "COTIUSDT",
    "CCUSDT",
    "KAITOUSDT",
    "MORPHOUSDT",
    "LABUSDT",
    "ZKUSDT",
    "USUSDT",
    "JSTUSDT",
    "AXSUSDT",
    "CAKEUSDT",
    "DYDXUSDT",
    "APEUSDT",
    "BANKUSDT",
    "NILUSDT",
    "NAORISUSDT",
    "WUSDT",
    "BIOUSDT",
    "GIGGLEUSDT",
    "SOPHUSDT",
    "BRUSDT",
    "MUBARAKUSDT",
    "XTZUSDT",
    "JASMYUSDT",
    "CHZUSDT",
    "MANAUSDT",
    "SIRENUSDT",
    "RUNEUSDT",
    "FOLKSUSDT",
    "HMSTRUSDT",
    "IOSTUSDT",
    "SKYUSDT",
    "CELOUSDT",
    "ENJUSDT",
    "RLCUSDT",
    "SWARMSUSDT",
    "1000FLOKIUSDT",
    "PLUMEUSDT",
    "VETUSDT",
    "OPENUSDT",
    "XPINUSDT",
    "CFXUSDT",
    "BLESSUSDT",
    "MINAUSDT",
    "DUSKUSDT",
    "REDUSDT",
    "COMPUSDT",
    "SNXUSDT",
    "KITEUSDT",
    "ENSUSDT",
    "KATUSDT",
    "PROMUSDT",
    "MAGICUSDT",
    "DODOXUSDT",
    "PNUTUSDT",
    "HUSDT",
    "ARKUSDT",
    "HAEDALUSDT",
    "SOONUSDT",
    "THEUSDT",
    "WALUSDT",
    "1000LUNCUSDT",
    "ALTUSDT",
    "SYRUPUSDT",
    "DOODUSDT",
    "BULLAUSDT",
    "TRADOORUSDT",
    "KMNOUSDT",
    "DEXEUSDT",
    "PEOPLEUSDT",
    "0GUSDT",
    "PIXELUSDT",
    "GRTUSDT",
    "PLAYUSDT",
    "MOVRUSDT",
    "AVAUSDT",
    "TRBUSDT",
    "PHAUSDT",
    "PORTALUSDT",
    "4USDT",
    "REZUSDT",
    "TRUTHUSDT",
    "SAGAUSDT",
    "1INCHUSDT",
    "ATHUSDT",
    "2ZUSDT",
    "MAVIAUSDT",
    "CYSUSDT",
    "AKTUSDT",
    "GUSDT",
    "OGNUSDT",
    "IOTAUSDT",
    "BLURUSDT",
    "HOMEUSDT",
    "TUSDT",
    "EGLDUSDT",
    "ORDERUSDT",
    "CKBUSDT",
    "ACEUSDT",
    "THETAUSDT",
    "ATUSDT",
    "ORCAUSDT",
    "POWRUSDT",
    "YBUSDT",
    "SENTUSDT",
    "LAUSDT",
    "TREEUSDT",
    "AVNTUSDT",
    "BLUAIUSDT",
    "GPSUSDT",
    "ZBTUSDT",
    "FLOCKUSDT",
    "RVNUSDT",
    "KASUSDT",
    "INUSDT",
    "币安人生USDT",
    "SXTUSDT",
    "CARVUSDT",
    "AUSDT",
    "TUTUSDT",
    "COLLECTUSDT",
    "ALLOUSDT",
    "STABLEUSDT",
    "GWEIUSDT",
    "BABYUSDT",
    "PROVEUSDT",
    "TACUSDT",
    "MEMEUSDT",
    "MYXUSDT",
    "FFUSDT",
    "FLUIDUSDT",
    "FORMUSDT",
    "PIPPINUSDT",
    "OPNUSDT",
    "YFIUSDT",
    "TRUSTUSDT",
    "SUPERUSDT",
    "CVXUSDT",
    "IOUSDT",
    "NMRUSDT",
    "KAIAUSDT",
    "UBUSDT",
    "SYNUSDT",
    "ARKMUSDT",
    "NEOUSDT",
    "COWUSDT",
    "SUSHIUSDT",
    "ROSEUSDT",
    "KAVAUSDT",
    "ANKRUSDT",
    "BROCCOLI714USDT",
    "BBUSDT",
    "ENSOUSDT",
    "IDUSDT",
    "1000CATUSDT",
    "SAFEUSDT",
    "ZKCUSDT",
    "API3USDT",
    "NOMUSDT",
    "1000SATSUSDT",
    "GMXUSDT",
    "KGENUSDT",
    "GMTUSDT",
    "USUALUSDT",
    "ONGUSDT",
    "SOLVUSDT",
    "CHILLGUYUSDT",
    "LINEAUSDT",
    "LUMIAUSDT",
    "MELANIAUSDT",
    "LIGHTUSDT",
    "EULUSDT",
    "CELRUSDT",
    "AVAAIUSDT",
    "QTUMUSDT",
    "AZTECUSDT",
    "VELVETUSDT",
    "EDUUSDT",
    "MOODENGUSDT",
    "HEIUSDT",
    "ZEREBROUSDT",
    "TRIAUSDT",
    "MMTUSDT",
    "GUNUSDT",
    "YGGUSDT",
    "SAHARAUSDT",
    "SSVUSDT",
    "ROBOUSDT",
    "SPKUSDT",
    "MASKUSDT",
    "MEUSDT",
    "NOTUSDT",
    "EDENUSDT",
    "MANTRAUSDT",
    "TURBOUSDT",
    "TSTUSDT",
    "ESPUSDT",
    "BTRUSDT",
    "TOWNSUSDT",
    "ILVUSDT",
    "LPTUSDT",
    "RAVEUSDT",
    "TAGUSDT",
    "BRETTUSDT",
    "GRIFFAINUSDT",
    "HEMIUSDT",
    "ALICEUSDT",
    "1000RATSUSDT",
    "FHEUSDT",
    "ONTUSDT",
    "KSMUSDT",
    "POPCATUSDT",
    "DOGSUSDT",
    "VTHOUSDT",
    "AWEUSDT",
    "LAYERUSDT",
    "C98USDT",
    "CGPTUSDT",
    "ARCUSDT",
    "SCRUSDT",
    "CLOUSDT",
    "LUNA2USDT",
    "1000CHEEMSUSDT",
    "FIGHTUSDT",
    "MIRAUSDT",
    "VANAUSDT",
    "POWERUSDT",
    "BARDUSDT",
    "TAKEUSDT",
    "ZORAUSDT",
    "HYPERUSDT",
    "BIGTIMEUSDT",
    "COOKIEUSDT",
    "TNSRUSDT",
    "MANTAUSDT",
    "ZETAUSDT",
    "TLMUSDT",
    "MOVEUSDT",
    "TOSHIUSDT",
    "RESOLVUSDT",
    "SKRUSDT",
    "FLOWUSDT",
    "ASRUSDT",
    "ANIMEUSDT",
    "OGUSDT",
    "AXLUSDT",
    "INXUSDT",
    "SQDUSDT",
    "HOLOUSDT",
    "XVGUSDT",
    "XANUSDT",
    "AIXBTUSDT",
    "METISUSDT",
    "STOUSDT",
    "SPACEUSDT",
    "WOOUSDT",
    "BUSDT",
    "我踏马来了USDT",
    "RIFUSDT",
    "STEEMUSDT",
    "BREVUSDT",
    "ZKPUSDT",
    "GUAUSDT",
    "MEWUSDT",
    "FIDAUSDT",
    "POLYXUSDT",
    "BICOUSDT"
]
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

# ======================= CHỈNH Ở ĐÂY =======================
# Chỉ báo Adaptive Trend Flow [QuantAlgo] (giá trị mặc định của chỉ báo)
LENGTH = 10            # Main Length
SMOOTH_LEN = 14        # Smoothing Length
SENSITIVITY = 2.0      # Sensitivity

MAX_DELAY_MIN = 30     # tín hiệu cũ hơn số phút này (do bot chạy trễ) sẽ không báo, chỉ cảnh báo
GAP_WARN_MIN = 45      # cảnh báo nếu 2 lần chạy cách nhau quá số phút này
# ===========================================================

INTERVAL = "15m"       # khung thời gian
IV_MS = 900000         # 15 phút tính bằng mili giây
CANDLES = 300          # số nến tải mỗi lần (đủ để chỉ báo ổn định)
WORKERS = 6            # số luồng tải song song
MIN_INTERVAL = 0.1     # giây giữa 2 lần gọi Binance (giữ dưới giới hạn tốc độ)
STATE_FILE = "state_atf.json"

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


def fetch(symbol):
    """Nến M15 ĐÃ ĐÓNG HẲN (đóng ít nhất 3 giây), cũ -> mới: (ts, high, low, close)."""
    cur = now_ms()
    rows = _get("klines", {"symbol": symbol, "interval": INTERVAL, "limit": CANDLES})
    out = []
    for r in rows:
        if r[0] + IV_MS > cur - 3000 or r[6] >= cur - 3000:
            continue
        out.append((int(r[0]), float(r[2]), float(r[3]), float(r[4])))
    return out


# ---------------- Chỉ báo Adaptive Trend Flow [QuantAlgo] ----------------
def ema_series(values, n):
    """ta.ema: nến đầu tiên lấy giá trị gốc làm điểm xuất phát."""
    a = 2 / (n + 1)
    out = [None] * len(values)
    prev = None
    for i, v in enumerate(values):
        if v is None:
            prev = None
            continue
        prev = v if prev is None else a * v + (1 - a) * prev
        out[i] = prev
    return out


def stdev_series(values, n):
    """ta.stdev (độ lệch chuẩn tổng thể, chia cho n)."""
    out = [None] * len(values)
    for i in range(n - 1, len(values)):
        w = values[i - n + 1:i + 1]
        m = sum(w) / n
        out[i] = (sum((x - m) ** 2 for x in w) / n) ** 0.5
    return out


def adaptive_trend(candles):
    """Trả về (xu hướng từng nến: 1 tăng, -1 giảm; đường xu hướng 'level' từng nến)."""
    h = [x[1] for x in candles]
    l = [x[2] for x in candles]
    c = [x[3] for x in candles]
    typ = [(a + b + d) / 3 for a, b, d in zip(h, l, c)]          # hlc3
    fast = ema_series(typ, LENGTH)
    slow = ema_series(typ, LENGTH * 2)
    basis = [(f + s) / 2 for f, s in zip(fast, slow)]
    sv = ema_series(stdev_series(typ, LENGTH), SMOOTH_LEN)
    upper = [None if s is None else b + s * SENSITIVITY for b, s in zip(basis, sv)]
    lower = [None if s is None else b - s * SENSITIVITY for b, s in zip(basis, sv)]

    prev_level, trend = None, 0
    trends, levels = [], []
    for i in range(len(c)):
        close = c[i]
        if prev_level is None:
            trend = 1 if close > basis[i] else -1
            prev_level = lower[i] if trend == 1 else upper[i]
        if trend == 1:
            if lower[i] is not None and close < lower[i]:
                trend = -1
                prev_level = upper[i]
            else:
                prev_level = lower[i]
        else:
            if upper[i] is not None and close > upper[i]:
                trend = 1
                prev_level = lower[i]
            else:
                prev_level = upper[i]
        trends.append(trend)
        levels.append(prev_level)
    return trends, levels


def fmt(x):
    return f"{x:.8g}"


def vn_time(ms):
    return datetime.fromtimestamp(ms / 1000, timezone(timedelta(hours=7))).strftime("%H:%M %d/%m")


def process(pair, last):
    """Xử lý 1 cặp. Trả về dict: ts (nến cuối đã xử lý), sigs (tín hiệu cần báo), stale (số tín hiệu quá cũ)."""
    candles = fetch(pair)
    if len(candles) < 100:
        return {"skip": f"không đủ dữ liệu ({len(candles)} nến)"}
    n = len(candles)
    trends, levels = adaptive_trend(candles)
    flips = [i for i in range(1, n) if levels[i] is not None and trends[i] != trends[i - 1]]
    if last is None:   # lần chạy đầu: chỉ xét nến mới nhất
        new = [i for i in flips if i == n - 1]
    else:
        new = [i for i in flips if candles[i][0] > last]
    sigs, stale = [], 0
    cur = now_ms()
    for i in new:
        t_close = candles[i][0] + IV_MS
        if (cur - t_close) / 60000 > MAX_DELAY_MIN:
            stale += 1
            continue
        sigs.append({"t_close": t_close, "side": trends[i], "close": candles[i][3], "level": levels[i]})
    return {"ts": candles[-1][0], "sigs": sigs, "stale": stale}


def build_message(pair, s):
    late = (now_ms() - s["t_close"]) / 60000
    side, close, level = s["side"], s["close"], s["level"]
    risk = (level - close) / close * 100
    head = f"🟢 {pair} M15: LONG (Adaptive Trend Flow)" if side == 1 else f"🔴 {pair} M15: SHORT (Adaptive Trend Flow)"
    return "\n".join([
        head,
        f"Nến M15 đóng lúc {vn_time(s['t_close'])} (giờ VN)",
        f"Giá đóng: {fmt(close)}",
        f"Đường xu hướng (SL gợi ý): {fmt(level)} ({risk:+.2f}%)",
        f"Bot gửi lúc {vn_time(now_ms())} (trễ {late:.0f} phút)",
    ])


def send_telegram(text):
    token = os.environ["TELEGRAM_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    for attempt in range(4):
        r = requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                          json={"chat_id": chat_id, "text": text}, timeout=20)
        if r.status_code == 429:   # Telegram báo gửi quá nhanh: chờ rồi gửi lại
            try:
                wait = float(r.json()["parameters"]["retry_after"])
            except Exception:
                wait = 5
            time.sleep(min(wait + 1, 60))
            continue
        r.raise_for_status()
        return
    raise RuntimeError("Telegram từ chối vì gửi quá nhanh")


def main():
    state = {}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            state = json.load(f)
    pairs_state = state.setdefault("pairs", {})
    started = time.time()
    cur = now_ms()

    last_run = state.get("_last_run")
    if last_run and (cur - last_run) / 60000 > GAP_WARN_MIN:
        try:
            send_telegram(f"⚠️ Bot bị gián đoạn khoảng {(cur - last_run) / 60000:.0f} phút "
                          f"(lần chạy trước lúc {vn_time(last_run)}). Có thể GitHub chạy trễ, tín hiệu trong khoảng này có thể đã bị lỡ.")
        except Exception as e:
            print(f"Lỗi gửi cảnh báo: {e}")

    def work(pair):
        try:
            return pair, process(pair, pairs_state.get(pair)), None
        except Exception as e:
            return pair, None, str(e)

    ok = fail = sent = stale_total = 0
    stale_pairs = 0
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
                for s in res["sigs"]:
                    send_telegram(build_message(pair, s))
                    sent += 1
                    time.sleep(0.5)
            except Exception as e:
                fail += 1
                last_err = str(e)
                print(f"Lỗi gửi Telegram {pair}: {e}")
                continue
            if res["stale"]:
                stale_total += res["stale"]
                stale_pairs += 1
            pairs_state[pair] = res["ts"]
            ok += 1

    if stale_total:
        try:
            send_telegram(f"⚠️ Bot chạy trễ: bỏ qua {stale_total} tín hiệu cũ hơn {MAX_DELAY_MIN} phút ({stale_pairs} cặp).")
        except Exception as e:
            print(f"Lỗi gửi cảnh báo: {e}")

    if ok == 0 and fail > 0:
        if not state.get("_err"):
            try:
                send_telegram(f"⚠️ Bot không lấy được dữ liệu Binance.\n{last_err}")
                state["_err"] = True
            except Exception as e:
                print(f"Lỗi gửi cảnh báo: {e}")
    elif ok > 0:
        state["_err"] = False

    state["_last_run"] = now_ms()
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)
    print(f"Xong: {ok} cặp OK, {fail} lỗi, {sent} tin, {time.time() - started:.0f} giây")


if __name__ == "__main__":
    main()
