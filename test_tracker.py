import unittest
from unittest.mock import patch

import tracker
import executor


class TrackerV3Tests(unittest.TestCase):
    def setUp(self):
        for times in tracker._rpc_times.values():
            times.clear()

    def sample(self, chain="ethereum", count=10):
        contract = "0x" + "a" * 40
        return {
            f"{chain}:{contract}": {
                "chain": chain,
                "contract": contract,
                "symbol": "ABC",
                "name": "Alpha",
                "amount": 25.0,
                "count": count,
                "score": 25.0,
            }
        }

    def test_transfer_topic_and_incoming_wildcard(self):
        self.assertEqual(len(tracker.TRANSFER_TOPIC), 66)

        def fake_rpc(chain, method, params):
            self.assertEqual(chain, "ethereum")
            self.assertEqual(method, "eth_getLogs")
            self.assertIsNone(params[0]["topics"][1])
            return []

        with patch.object(tracker, "rpc", side_effect=fake_rpc):
            self.assertEqual(tracker.transfer_logs("ethereum", "0x" + "1" * 40, "in", 1, 2), [])

    def test_rpc_failure_is_safe(self):
        with patch("tracker.requests.post", side_effect=tracker.requests.RequestException("offline")):
            self.assertIsNone(tracker.rpc("ethereum", "eth_blockNumber", []))

    def test_report_and_opportunity_paths(self):
        wallets = {"Wallet": "0x" + "1" * 40}
        sample = self.sample()
        with patch.object(tracker, "transfers_multi", return_value=sample):
            report = tracker.get_report(60, "out", wallets, chains=["ethereum"])
            opportunity = tracker.get_opportunity(60, wallets, chains=["ethereum"])
        self.assertEqual(report["_meta"]["source"], "multi_rpc")
        self.assertEqual(report["Wallet"]["tokens"][0]["count"], 10)
        self.assertEqual(opportunity["ranked"][0]["symbol"], "ABC")

    def test_less_than_three_is_filtered(self):
        self.assertEqual(tracker.top_from_raw(self.sample(count=2)), [])
        self.assertEqual(len(tracker.top_from_raw(self.sample(count=3))), 1)

    def test_strong_outflow_alert_allows_one_wallet(self):
        wallets = {"Wallet": "0x" + "1" * 40}
        raw = self.sample(count=4)
        raw[next(iter(raw))]["score"] = 25000
        with patch.object(tracker, "transfers_multi", return_value=raw):
            alerts = tracker.get_strong_outflow_alerts(30, wallets, chains=["ethereum"])
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["wallet_count"], 1)

    def test_auto_buy_skips_daily_gainers(self):
        with patch.object(executor.settings, "load", return_value={
            "auto_buy_enabled": True,
            "monitoring_enabled": True,
            "max_open_trades": 3,
            "trade_size_usd": 20,
        }), patch.object(executor.trades_db, "count_open", return_value=0), \
             patch.object(executor.trades_db, "has_open_symbol", return_value=False), \
             patch.object(executor.mexc_trade, "get_price", return_value=1.0), \
             patch.object(executor.mexc_trade, "get_24h_change_percent", return_value=5.1):
            ok, message = executor.try_auto_buy("TEST")
        self.assertFalse(ok)
        self.assertIn("الحد +5%", message)


if __name__ == "__main__":
    unittest.main()
