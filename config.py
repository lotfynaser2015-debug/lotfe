import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()
ETHEREUM_RPC_URL = os.getenv("ETHEREUM_RPC_URL", "https://eth.llamarpc.com").strip()
ETHEREUM_RPC_BACKUP_URL = os.getenv(
    "ETHEREUM_RPC_BACKUP_URL", "https://ethereum-rpc.publicnode.com"
).strip()
TOP_N = 10
MIN_TRANSFERS = 3
# Continuous monitoring (free-friendly)
MONITOR_INTERVAL_SEC = 300          # كل 5 دقايق
ALERT_COOLDOWN_SEC = 1200           # 20 دقيقة cooldown لنفس التوكن
MIN_WALLETS_FOR_ALERT = 1           # محفظة واحدة على الأقل
MIN_SCORE_FOR_ALERT = 20000
MAX_WALLETS_PER_CYCLE = 1           # محفظة واحدة في كل دورة لتجنب تجاوز حد RPC

DEFAULT_WALLETS = {
    "MEXC 1": "0x9642b23ed1e01df1092b92641051881a322f5d4e",
    "MEXC 2": "0x4982085c9e2f89f2ecb8131eca71afad896e89cb",
}

TIME_PERIODS = [
    ("5 دقائق", 5),
    ("15 دقيقة", 15),
    ("30 دقيقة", 30),
    ("ساعة", 60),
    ("ساعتان", 120),
    ("4 ساعات", 240),
    ("6 ساعات", 360),
    ("12 ساعة", 720),
    ("24 ساعة", 1440),
]

# Ethereum Mainnet only. Both endpoints support the JSON-RPC calls used by the tracker.
CHAINS = {
    "ethereum": {
        "name": "Ethereum",
        "rpc": ETHEREUM_RPC_URL,
        "rpc_backup": ETHEREUM_RPC_BACKUP_URL,
        "dex": "ethereum",
        "explorer": "https://etherscan.io",
        "native": "ETH",
        "blocks_per_min": 5,
    },
}
ACTIVE_CHAINS = ["ethereum"]
