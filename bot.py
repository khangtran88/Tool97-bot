"""Bot Telegram báo AlgoAlpha Trend Targets đổi chiều xu hướng (Binance, miễn phí)."""
import json
import os
import time
import requests

# ======================= CHỈNH Ở ĐÂY =======================
# Danh sách cặp tiền Binance (viết liền, không có dấu gạch): BTCUSDT, ETHUSDT...
PAIRS = [
    "ZECUSDT",
    "SOLUSDT",
    "XRPUSDT",
    "NEARUSDT",
    "ONEUSDT",
    "PEPEUSDT",
    "UNIUSDT",
    "HYPEUSDT",
    "UUSDT",
    "DOGEUSDT",
    "ENAUSDT",
    "SUIUSDT",
    "BMTUSDT",
    "PUMPUSDT",
    "TRXUSDT",
    "WLDUSDT",
    "TONUSDT",
    "HOTUSDT",
    "SOXLBUSDT",
    "INJUSDT",
    "METUSDT",
    "AAVEUSDT",
    "LTCUSDT",
    "LINKUSDT",
    "ARBUSDT",
    "RWUSDUSDT",
    "BCHUSDT",
    "ACTUSDT",
    "ADAUSDT",
    "QNTUSDT",
    "HMSTRUSDT",
    "CYBERUSDT",
    "TRUMPUSDT",
    "GRAMUSDT",
    "RSRUSDT",
    "AVAXUSDT",
    "ERAUSDT",
    "MITOUSDT",
    "SNDKBUSDT",
    "NFPUSDT",
    "CELOUSDT",
    "TAOUSDT",
    "FETUSDT",
    "XLMUSDT",
    "XPLUSDT",
    "ONDOUSDT",
    "AEROUSDT",
    "SIGNUSDT",
    "ASTERUSDT",
    "BEAMXUSDT",
    "FILUSDT",
    "GTCUSDT",
    "MSTRBUSDT",
    "NVDABUSDT",
    "CRCLBUSDT",
    "HFTUSDT",
    "牛来USDT",
    "VANRYUSDT",
    "ZROUSDT",
    "DASHUSDT",
    "ETHFIUSDT",
    "HBARUSDT",
    "KORUBUSDT",
    "WLFIUSDT",
    "SPCXBUSDT",
    "HUMAUSDT",
    "MARSCOINUSDT",
    "PENGUUSDT",
    "ICPUSDT",
    "DODOUSDT",
    "TIAUSDT",
    "BUSDUSDT",
    "STRKUSDT",
    "RNDRUSDT",
    "COTIUSDT",
    "THEUSDT",
    "LSKUSDT",
    "QQQBUSDT",
    "MUBUSDT",
    "POLUSDT",
    "GNSUSDT",
    "COCOSUSDT",
    "ZAMAUSDT",
    "SCRTUSDT",
    "POLYUSDT",
    "RAYUSDT",
    "JSTUSDT",
    "SHIBUSDT",
    "MEGAUSDT",
    "OPENUSDT",
    "APTUSDT",
    "INTCBUSDT",
    "FTMUSDT",
    "GALUSDT",
    "DGBUSDT",
    "DOTUSDT",
    "ATMUSDT",
    "INITUSDT",
    "KAVAUSDT",
    "OMNIUSDT",
    "TOMOUSDT",
    "CHIPUSDT",
    "MATICUSDT",
    "MORPHOUSDT",
    "ATUSDT",
    "VICUSDT",
    "SEIUSDT",
    "GOOGLBUSDT",
    "TVKUSDT",
    "JTOUSDT",
    "PROMUSDT",
    "NIGHTUSDT",
    "NILUSDT",
    "STGUSDT",
    "RENDERUSDT",
    "HAEDALUSDT",
    "EOSUSDT",
    "COMPUSDT",
    "LOKAUSDT",
    "STORJUSDT",
    "BLZUSDT",
    "HIFIUSDT",
    "KLAYUSDT",
    "HNTUSDT",
    "BETHUSDT",
    "SOLVUSDT",
    "VIRTUALUSDT",
    "PLUMEUSDT",
    "EIGENUSDT",
    "LDOUSDT",
    "BROCCOLI714USDT",
    "PLAUSDT",
    "EPICUSDT",
    "LITUSDT",
    "AVAUSDT",
    "AGIXUSDT",
    "ZENUSDT",
    "DNTUSDT",
    "AMPUSDT",
    "BONKUSDT",
    "BNXUSDT",
    "YFIIUSDT",
    "PYRUSDT",
    "GLMRUSDT",
    "OPUSDT",
    "MFTUSDT",
    "CELRUSDT",
    "CAKEUSDT",
    "PYTHUSDT",
    "BEAMUSDT",
    "SOPHUSDT",
    "ATOMUSDT",
    "BTGUSDT",
    "DARUSDT",
    "SXTUSDT",
    "OOKIUSDT",
    "XTZUSDT",
    "BAKEUSDT",
    "BONDUSDT",
    "ARKUSDT",
    "PENDLEUSDT",
    "CRVUSDT",
    "AUDIOUSDT",
    "OMGUSDT",
    "FOGOUSDT",
    "API3USDT",
    "BTCSTUSDT",
    "JUPUSDT",
    "ANCUSDT",
    "ADADOWNUSDT",
    "ERNUSDT",
    "ELFUSDT",
    "ZILUSDT",
    "ETCUSDT",
    "LUNCUSDT",
    "MCUSDT",
    "KITEUSDT",
    "RADUSDT",
    "币安人生USDT",
    "AAPLBUSDT",
    "LOOMUSDT",
    "ALGOUSDT",
    "FORMUSDT",
    "STXUSDT",
    "SKHYBUSDT",
    "XMRUSDT",
    "AUTOUSDT",
    "OMUSDT",
    "AIONUSDT",
    "NBSUSDT",
    "BSWUSDT",
    "WUSDT",
    "ANTUSDT",
    "FRONTUSDT",
    "ESPUSDT",
    "GALAUSDT",
    "WIFUSDT",
    "ARUSDT",
    "GTOUSDT",
    "DOGSUSDT",
    "PDAUSDT",
    "GFTUSDT",
    "MIRUSDT",
    "NEBLUSDT",
    "1INCHUSDT",
    "SUSDT",
    "RUNEUSDT",
    "PARTIUSDT",
    "BNCBUSDT",
    "VGXUSDT",
    "SKYUSDT",
    "QUICKUSDT",
    "YBUSDT",
    "TCTUSDT",
    "PHAUSDT",
    "ORNUSDT",
    "PNUTUSDT",
    "TORNUSDT",
    "OSMOUSDT",
    "SYRUPUSDT",
    "WINUSDT",
    "WTCUSDT",
    "TRIBEUSDT",
    "VETUSDT",
    "CKBUSDT",
    "CATIUSDT",
    "RENUSDT",
    "REPUSDT",
    "SRMUSDT",
    "DOCKUSDT",
    "DUSKUSDT",
    "LAUSDT",
    "STPTUSDT",
    "SANDUSDT",
    "FXSUSDT",
    "ETHUPUSDT",
    "AUDUSDT",
    "MUBARAKUSDT",
    "MKRUSDT",
    "WAVESUSDT",
    "BTTCUSDT",
    "MBOXUSDT",
    "EURIUSDT",
    "CVPUSDT",
    "MOVRUSDT",
    "SNXXBUSDT",
    "BATUSDT",
    "BOMEUSDT",
    "REDUSDT",
    "ALPHAUSDT",
    "1000CATUSDT",
    "ADAUPUSDT",
    "FIROUSDT",
    "MITHUSDT",
    "LTOUSDT",
    "GIGGLEUSDT",
    "NEIROUSDT",
    "IOUSDT",
    "DREPUSDT",
    "NOMUSDT",
    "WRXUSDT",
    "GENIUSUSDT",
    "OCEANUSDT",
    "ATAUSDT",
    "PIVXUSDT",
    "REZUSDT",
    "REEFUSDT",
    "UNFIUSDT",
    "LEVERUSDT",
    "BABYUSDT",
    "SAGAUSDT",
    "VIBUSDT",
    "IRISUSDT",
    "CFGUSDT",
    "IOTAUSDT",
    "KATUSDT",
    "TUTUSDT",
    "SXPUSDT",
    "ACAUSDT",
    "FORUSDT",
    "AMBUSDT",
    "KP3RUSDT",
    "GPSUSDT",
    "LINEAUSDT",
    "UTKUSDT",
    "PERLUSDT",
    "BNTUSDT",
    "DEGOUSDT",
    "MOBUSDT",
    "NMRUSDT",
    "CLVUSDT",
    "KDAUSDT",
    "ENSOUSDT",
    "DUSDT",
    "MULTIUSDT",
    "FLOKIUSDT",
    "SNTUSDT",
    "CFXUSDT",
    "WINGUSDT",
    "HIGHUSDT",
    "AXSUSDT",
    "BLURUSDT",
    "SPYBUSDT",
    "ORDIUSDT",
    "EGLDUSDT",
    "BNSOLUSDT",
    "COMBOUSDT",
    "EPXUSDT",
    "TRUUSDT",
    "ADXUSDT",
    "TQQQBUSDT",
    "MDXUSDT",
    "PHBUSDT",
    "IMXUSDT",
    "SLFUSDT",
    "SUPERUSDT",
    "ACMUSDT",
    "BERAUSDT",
    "LUMIAUSDT",
    "XEMUSDT",
    "ALTUSDT",
    "BETAUSDT",
    "ICXUSDT",
    "PONDUSDT",
    "DENTUSDT",
    "ASRUSDT",
    "STMXUSDT",
    "ENSUSDT",
    "MAGICUSDT",
    "CITYUSDT",
    "POLSUSDT",
    "DEXEUSDT",
    "GRTUSDT",
    "BARUSDT",
    "HOOKUSDT",
    "2ZUSDT",
    "RLCUSDT",
    "ALCXUSDT",
    "BANKUSDT",
    "CREAMUSDT",
    "HOMEUSDT",
    "ZBTUSDT",
    "ALPACAUSDT",
    "TWTUSDT",
    "OGNUSDT",
    "CTXCUSDT",
    "EDUUSDT",
    "ARKMUSDT",
    "GUNUSDT",
    "PORTOUSDT",
    "NEXOUSDT",
    "BTSUSDT",
    "PNTUSDT",
    "YFIUSDT",
    "AIUSDT",
    "GUSDT",
    "TSTUSDT",
    "FLMUSDT",
    "ANKRUSDT",
    "ZKUSDT",
    "MANAUSDT",
    "LAZIOUSDT",
    "AVNTUSDT",
    "RVNUSDT",
    "1000CHEEMSUSDT",
    "ARDRUSDT",
    "THETAUSDT",
    "IDUSDT",
    "SENTUSDT",
    "ACEUSDT",
    "A2ZUSDT",
    "VITEUSDT",
    "BALUSDT",
    "BBUSDT",
    "CHZUSDT",
    "SPKUSDT",
    "ALPINEUSDT",
    "BARDUSDT",
    "JUVUSDT",
    "ROSEUSDT",
    "AMDBUSDT",
    "IOSTUSDT",
    "XRPUPUSDT",
    "OXTUSDT",
    "BIFIUSDT",
    "BURGERUSDT",
    "KMDUSDT",
    "OPNUSDT",
    "GBPUSDT",
    "ORCAUSDT",
    "1000SATSUSDT",
    "NBTUSDT",
    "NTRNUSDT",
    "BREVUSDT",
    "DOTUPUSDT",
    "GMXUSDT",
    "AKROUSDT",
    "TREEUSDT",
    "FISUSDT",
    "OAXUSDT",
    "RONINUSDT",
    "POWRUSDT",
    "CVXUSDT",
    "BNBDOWNUSDT",
    "TRBUSDT",
    "WOOUSDT",
    "LRCUSDT",
    "LUNAUSDT",
    "MASKUSDT",
    "ETHDOWNUSDT",
    "1MBABYDOGEUSDT",
    "TSLABUSDT",
    "FIOUSDT",
    "DYDXUSDT",
    "TUSDT",
    "TRXDOWNUSDT",
    "VIDTUSDT",
    "BADGERUSDT",
    "MAVUSDT",
    "APEUSDT",
    "NKNUSDT",
    "OPGUSDT",
    "0GUSDT",
    "C98USDT",
    "REUSDT",
    "FORTHUSDT",
    "DOTDOWNUSDT",
    "WNXMUSDT",
    "LINAUSDT",
    "MANTRAUSDT",
    "USUALUSDT",
    "KAITOUSDT",
    "SOXSBUSDT",
    "MINAUSDT",
    "SUSHIUSDT",
    "MMTUSDT",
    "PROVEUSDT",
    "BIOUSDT",
    "CHESSUSDT",
    "LINKUPUSDT",
    "PEOPLEUSDT",
    "VOXELUSDT",
    "WANUSDT",
    "POLYXUSDT",
    "KNCUSDT",
    "KAIAUSDT",
    "COWUSDT",
    "BNBUPUSDT",
    "NULSUSDT",
    "BTCDOWNUSDT",
    "FFUSDT",
    "CVCUSDT",
    "VELODROMEUSDT",
    "SUNUSDT",
    "NXPCUSDT",
    "FARMUSDT",
    "KMNOUSDT",
    "XNOUSDT",
    "AWEUSDT",
    "XVGUSDT",
    "AXLUSDT",
    "JASMYUSDT",
    "PSGUSDT",
    "NEOUSDT",
    "HYPERUSDT",
    "OGUSDT",
    "COSUSDT",
    "XRPDOWNUSDT",
    "FTTUSDT",
    "FUNUSDT",
    "PUNDIXUSDT",
    "INTWBUSDT",
    "PIXELUSDT",
    "COOKIEUSDT",
    "BTCUPUSDT",
    "MEMEUSDT",
    "TROYUSDT",
    "ACXUSDT",
    "LPTUSDT",
    "TRXUPUSDT",
    "REQUSDT",
    "HEIUSDT",
    "MDTUSDT",
    "HARDUSDT",
    "EDENUSDT",
    "YGGUSDT",
    "WCTUSDT",
    "ZKCUSDT",
    "PORTALUSDT",
    "FRAXUSDT",
    "BICOUSDT",
    "TURBOUSDT",
    "VTHOUSDT",
    "TURTLEUSDT",
    "QIUSDT",
    "IDEXUSDT",
    "SCRUSDT",
    "SYNUSDT",
    "STOUSDT",
    "HEMIUSDT",
    "MIRAUSDT",
    "MEUSDT",
    "KSMUSDT",
    "SHELLUSDT",
    "ZKPUSDT",
    "WALUSDT",
    "IOTXUSDT",
    "USTCUSDT",
    "NEWTUSDT",
    "KEYUSDT",
    "CGPTUSDT",
    "TOWNSUSDT",
    "METABUSDT",
    "RDNTUSDT",
    "SYSUSDT",
    "PROSUSDT",
    "AUSDT",
    "DATAUSDT",
    "EULUSDT",
    "BIGTIMEUSDT",
    "ROBOUSDT",
    "LINKDOWNUSDT",
    "AMZNBUSDT",
    "LQTYUSDT",
    "GHSTUSDT",
    "FIDAUSDT",
    "ENJUSDT",
    "UFTUSDT",
    "FLOWUSDT",
    "MANTAUSDT",
    "ALLOUSDT",
    "DFUSDT",
    "ANIMEUSDT",
    "ASTUSDT",
    "DYMUSDT",
    "LAYERUSDT",
    "SKLUSDT",
    "MTLUSDT",
    "SSVUSDT",
    "AUCTIONUSDT",
    "MRVLBUSDT",
    "AIXBTUSDT",
    "CUSDT",
    "AERGOUSDT",
    "METISUSDT",
    "STEEMUSDT",
    "PERPUSDT",
    "STRAXUSDT",
    "SNXUSDT",
    "ILVUSDT",
    "HOODBUSDT",
    "ARPAUSDT",
    "TNSRUSDT",
    "XAIUSDT",
    "SCUSDT",
    "LITEBUSDT",
    "ONTUSDT",
    "CETUSUSDT",
    "ONGUSDT",
    "AIGENSYNUSDT",
    "MLNUSDT",
    "SANTOSUSDT",
    "XECUSDT",
    "SOMIUSDT",
    "BANANAS31USDT",
    "SAHARAUSDT",
    "NOTUSDT",
    "SMHBUSDT",
    "NBISBUSDT",
    "REIUSDT",
    "FUSDT",
    "XVSUSDT",
    "RIFUSDT",
    "SAPIENUSDT",
    "GMTUSDT",
    "ALICEUSDT",
    "MBLUSDT",
    "CTSIUSDT",
    "MOVEUSDT",
    "ACHUSDT",
    "FLUXUSDT",
    "GLMUSDT",
    "KERNELUSDT",
    "TKOUSDT",
    "ASTRUSDT",
    "ZRXUSDT",
    "COINBUSDT",
    "WAXPUSDT",
    "MUUBUSDT",
    "AGLDUSDT",
    "RESOLVUSDT",
    "SFPUSDT",
    "HOLOUSDT",
    "EWYBUSDT",
    "MSFTBUSDT",
    "DRAMBUSDT",
    "RAREUSDT",
    "TLMUSDT",
    "VANAUSDT",
    "AVGOBUSDT",
    "GASUSDT",
    "LISTAUSDT",
    "CBRSBUSDT",
    "AAOIBUSDT",
    "BEBUSDT",
    "SLPUSDT",
    "DCRUSDT",
    "SPELLUSDT",
    "BMNRBUSDT",
    "PDDBUSDT",
    "CHRUSDT",
    "APPBUSDT",
    "DIAUSDT",
    "GNOUSDT",
    "BANANAUSDT",
    "JOEUSDT",
    "QKCUSDT",
    "UMAUSDT",
    "TSMBUSDT",
    "AEVOUSDT",
    "CTKUSDT",
    "TFUELUSDT",
    "SECZBUSDT",
    "BABABUSDT",
    "BELUSDT",
    "HIVEUSDT",
    "DOLOUSDT",
    "RPLUSDT",
    "QTUMUSDT",
    "NFLXBUSDT",
    "AXTIBUSDT",
    "BANDUSDT",
    "IRENBUSDT",
    "MRNABUSDT",
    "MVLLBUSDT",
    "CRWVBUSDT",
    "RKLBBUSDT",
    "ARMBUSDT",
    "BSPBUSDT",
    "ORCLBUSDT",
    "UVXYBUSDT",
    "BBBUSDT",
    "KSTRBUSDT",
    "SKUUBUSDT",
    "DJTBUSDT",
    "COHRBUSDT",
    "IQUSDT",
    "GEVBUSDT",
    "KGSTUSDT",
    "AGPUBUSDT",
    "GLWBUSDT",
    "PENGBUSDT",
    "QCOMBUSDT",
    "USARBUSDT",
    "DELLBUSDT",
    "CYPHBUSDT",
    "BRKBBUSDT",
    "QNTBUSDT",
    "NOKBUSDT",
    "CRDOBUSDT",
    "WDCBUSDT",
    "ASTSBUSDT",
    "PLTRBUSDT",
    "SQQQBUSDT",
    "BOTBUSDT",
    "ALABBUSDT",
    "SMCIBUSDT",
    "ASMLBUSDT",
    "ADBEBUSDT",
    "IBMBUSDT",
    "STXBUSDT",
    "HIMSBUSDT",
    "FLNCBUSDT",
    "MDBBUSDT",
    "VSTBUSDT",
    "CRWDBUSDT",
    "GPROBUSDT",
    "AMCBUSDT",
    "RDDTBUSDT",
    "LLYBUSDT",
    "SKDDBUSDT",
    "AMATBUSDT",
    "GMEBUSDT",
    "JPMBUSDT",
    "WENBUSDT",
    "FWDIBUSDT",
    "ZMBUSDT",
    "USDEBUSDT",
    "PYPLBUSDT",
    "SHAZBUSDT",
    "CRMBUSDT",
    "TMFBUSDT",
    "GSBUSDT",
    "HPEBUSDT",
    "BCCUSDT",
    "VENUSDT",
    "PAXUSDT",
    "BCHABCUSDT",
    "BCHSVUSDT",
    "BTTUSDT",
    "USDSOLDUSDT",
    "NANOUSDT",
    "USDSBUSDT",
    "ERDUSDT",
    "NPXSUSDT",
    "STORMUSDT",
    "HCUSDT",
    "MCOUSDT",
    "BULLUSDT",
    "BEARUSDT",
    "ETHBULLUSDT",
    "ETHBEARUSDT",
    "EOSBULLUSDT",
    "EOSBEARUSDT",
    "XRPBULLUSDT",
    "XRPBEARUSDT",
    "STRATUSDT",
    "BNBBULLUSDT",
    "BNBBEARUSDT",
    "XZCUSDT",
    "GXSUSDT",
    "LENDUSDT",
    "BKRWUSDT",
    "XTZUPUSDT",
    "XTZDOWNUSDT",
    "BZRXUSDT",
    "EOSUPUSDT",
    "EOSDOWNUSDT",
    "LTCUPUSDT",
    "LTCDOWNUSDT",
    "UNIUPUSDT",
    "UNIDOWNUSDT",
    "SXPUPUSDT",
    "SXPDOWNUSDT",
    "FILUPUSDT",
    "FILDOWNUSDT",
    "YFIUPUSDT",
    "YFIDOWNUSDT",
    "BCHUPUSDT",
    "BCHDOWNUSDT",
    "AAVEUPUSDT",
    "AAVEDOWNUSDT",
    "SUSDUSDT",
    "SUSHIUPUSDT",
    "SUSHIDOWNUSDT",
    "XLMUPUSDT",
    "XLMDOWNUSDT",
    "RAMPUSDT",
    "EPSUSDT",
    "1INCHUPUSDT",
    "1INCHDOWNUSDT",
    "NUUSDT",
    "KEEPUSDT",
    "RGTUSDT",
    "ANYUSDT",
    "USTUSDT"
]
# Khung thời gian: "1h" và "4h"
TIMEFRAMES = ["1h"]

# Thông số chỉ báo (giống cài đặt trên TradingView)
ST_FACTOR = 12.0      # Supertrend Factor
ST_ATR_PERIOD = 90    # Supertrend ATR Period
WMA_LENGTH = 40       # WMA Length
EMA_LENGTH = 14       # EMA Length
ATR_PERIOD = 14       # Volatility (ATR) period
SL_MULT = 5.0         # Stop Loss ATR Multiplier
TP1_MULT = 0.5        # TP1 Multiplier
TP2_MULT = 1.0        # TP2 Multiplier
TP3_MULT = 1.5        # TP3 Multiplier
# ===========================================================

PAGES = 5  # số lần tải nến (mỗi lần 1000 nến) để chỉ báo tính đủ lịch sử
STATE_FILE = "state.json"
HOSTS = [
    "https://data-api.binance.vision",
    "https://api.binance.com",
    "https://api1.binance.com",
    "https://api2.binance.com",
    "https://api3.binance.com",
    "https://api4.binance.com",
    "https://api-gcp.binance.com",
]
_host = None


def _get(path, params):
    """Gọi Binance, tự thử các địa chỉ dự phòng nếu bị chặn."""
    global _host
    order = ([_host] if _host else []) + [h for h in HOSTS if h != _host]
    last = "không rõ"
    for h in order:
        try:
            r = requests.get(h + path, params=params, timeout=20)
        except requests.RequestException as e:
            last = f"{h}: {e}"
            continue
        if r.status_code == 200:
            _host = h
            return r.json()
        if r.status_code == 400:
            raise ValueError(f"Cặp tiền không hợp lệ: {params.get('symbol')}")
        last = f"{h}: HTTP {r.status_code}"
    raise RuntimeError(last)


def get_candles(symbol, interval):
    """Lấy nến ĐÃ ĐÓNG, cũ -> mới. Mỗi nến: (ts, high, low, close)."""
    now_ms = int(time.time() * 1000)
    rows, end = [], None
    for _ in range(PAGES):
        params = {"symbol": symbol, "interval": interval, "limit": 1000}
        if end:
            params["endTime"] = end
        page = _get("/api/v3/klines", params)
        if not page:
            break
        rows = page + rows
        end = page[0][0] - 1
        if len(page) < 1000:
            break
    out = []
    for r in rows:
        if r[6] >= now_ms:  # bỏ nến đang chạy
            continue
        out.append((int(r[0]), float(r[2]), float(r[3]), float(r[4])))
    return out


def rma_atr(h, l, c, n):
    """ta.atr của TradingView (RMA của True Range)."""
    tr = []
    for i in range(len(c)):
        if i == 0:
            tr.append(h[0] - l[0])
        else:
            tr.append(max(h[i] - l[i], abs(h[i] - c[i - 1]), abs(l[i] - c[i - 1])))
    out = [None] * len(c)
    if len(c) < n:
        return out
    prev = sum(tr[:n]) / n
    out[n - 1] = prev
    for i in range(n, len(c)):
        prev = (prev * (n - 1) + tr[i]) / n
        out[i] = prev
    return out


def wma(v, n):
    out = [None] * len(v)
    norm = n * (n + 1) / 2
    for i in range(n - 1, len(v)):
        w = v[i - n + 1:i + 1]
        if None in w:
            continue
        out[i] = sum((k + 1) * x for k, x in enumerate(w)) / norm
    return out


def ema(v, n):
    out = [None] * len(v)
    a = 2 / (n + 1)
    prev = None
    for i in range(n - 1, len(v)):
        if prev is None:
            w = v[i - n + 1:i + 1]
            if None in w:
                continue
            prev = sum(w) / n
        elif v[i] is None:
            prev = None
            continue
        else:
            prev = a * v[i] + (1 - a) * prev
        out[i] = prev
    return out


def supertrend_bands(h, l, c, factor, n):
    """pine_supertrend() trong mã gốc: trả về (lowerBand, upperBand)."""
    atr = rma_atr(h, l, c, n)
    lo = [None] * len(c)
    up = [None] * len(c)
    for i in range(len(c)):
        src = (h[i] + l[i]) / 2
        a = atr[i]
        lb = src - factor * a if a is not None else None
        ub = src + factor * a if a is not None else None
        pl = lo[i - 1] if i > 0 and lo[i - 1] is not None else 0.0
        pu = up[i - 1] if i > 0 and up[i - 1] is not None else 0.0
        cp = c[i - 1] if i > 0 else None
        if (lb is not None and lb > pl) or (cp is not None and cp < pl):
            lo[i] = lb
        else:
            lo[i] = pl
        if (ub is not None and ub < pu) or (cp is not None and cp > pu):
            up[i] = ub
        else:
            up[i] = pu
    return lo, up


def find_signals(candles):
    """Trả về danh sách tín hiệu đổi chiều: (ts, hướng, entry, SL, TP1, TP2, TP3)."""
    h = [x[1] for x in candles]
    l = [x[2] for x in candles]
    c = [x[3] for x in candles]
    n = len(c)
    lo, up = supertrend_bands(h, l, c, ST_FACTOR, ST_ATR_PERIOD)
    mid = [(a + b) / 2 if a is not None and b is not None else None for a, b in zip(lo, up)]
    tl = ema(wma(mid, WMA_LENGTH), EMA_LENGTH)
    vol = rma_atr(h, l, c, ATR_PERIOD)

    trend = [0] * n
    cur = 0
    for i in range(n):
        if i >= 2 and tl[i] is not None and tl[i - 1] is not None and tl[i - 2] is not None:
            if tl[i] > tl[i - 1] and tl[i - 1] <= tl[i - 2]:
                cur = 1
            if tl[i] < tl[i - 1] and tl[i - 1] >= tl[i - 2]:
                cur = -1
        trend[i] = cur

    signals = []
    for i in range(1, n):
        prev = trend[i - 1]
        if vol[i] is None:
            continue
        if trend[i] == 1 and prev <= 0:
            sl = l[i] - vol[i] * SL_MULT
            d = abs(c[i] - sl)
            signals.append((candles[i][0], 1, c[i], sl,
                            c[i] + d * TP1_MULT, c[i] + d * TP2_MULT, c[i] + d * TP3_MULT))
        elif trend[i] == -1 and prev >= 0:
            sl = h[i] + vol[i] * SL_MULT
            d = abs(c[i] - sl)
            signals.append((candles[i][0], -1, c[i], sl,
                            c[i] - d * TP1_MULT, c[i] - d * TP2_MULT, c[i] - d * TP3_MULT))
    return signals


def pick_new(signals, candles, last_ts):
    """Chỉ giữ tín hiệu mới chưa báo."""
    if last_ts is None:  # lần chạy đầu: chỉ xét nến mới nhất
        return [s for s in signals if s[0] == candles[-1][0]]
    return [s for s in signals if s[0] > last_ts]


def fmt(x):
    return f"{x:.8g}"


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

    ok, fail, last_err = 0, 0, ""
    for pair in PAIRS:
        for tf in TIMEFRAMES:
            key = f"{pair}_{tf}"
            try:
                candles = get_candles(pair, tf)
                if len(candles) < 300:
                    print(f"Bỏ qua {key}: không đủ dữ liệu ({len(candles)} nến)")
                    continue
                for ts, d, entry, sl, t1, t2, t3 in pick_new(find_signals(candles), candles, state.get(key)):
                    if d == 1:
                        head = f"🟢 {pair} {tf.upper()}: XU HƯỚNG ĐỔI SANG TĂNG (MUA)"
                    else:
                        head = f"🔴 {pair} {tf.upper()}: XU HƯỚNG ĐỔI SANG GIẢM (BÁN)"
                    msg = (f"{head}\nEntry: {fmt(entry)}\nSL: {fmt(sl)}\n"
                           f"TP1: {fmt(t1)}\nTP2: {fmt(t2)}\nTP3: {fmt(t3)}")
                    send_telegram(msg)
                state[key] = candles[-1][0]
                ok += 1
            except Exception as e:
                fail += 1
                last_err = str(e)
                print(f"Lỗi {key}: {e}")

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


if __name__ == "__main__":
    main()
