"""Collector class used for defining all data collection points to Atom Finance."""
import jinja2

from pyatom_finance import config
from pyatom_finance.exceptions import StockCollectorRequesterError
from pyatom_finance.requester import Requester


class Collector:
    """Collector Class"""

    def __init__(self):
        self.requester = Requester()
        self.requester.create_session()
        loader = jinja2.FileSystemLoader(searchpath=config.SETTINGS.jinja2_templates)
        self.template_env = jinja2.Environment(loader=loader, autoescape=True)

    def _render_template(self, template, **kwargs):
        template = self.template_env.get_template(template)
        return template.render(**kwargs)

    def check_symbol_exists(self, symbol):
        """Ensure symbol exists before use."""
        payload = {
            "operationName": "getSymbol",
            "variables": {"symbol": symbol},
            "query": self._render_template("get_symbol.j2"),
        }
        resp = self.requester.post_request(payload)
        if not resp["data"]["symbol"]:
            raise StockCollectorRequesterError(
                "Unknown Symbol", f"Unable to find symbol in Atom, please check symbol: {symbol}"
            )
        return True

    def get_better_consensuses(self, symbol):
        """getBetterConsensuses"""
        payload = {
            "operationName": "getBetterConsensuses",
            "variables": {"symbol": symbol},
            "query": self._render_template("get_better_consensuses.j2"),
        }
        return self.requester.post_request(payload)

    def get_brokerage_actions(self, symbol):
        """getBrokerageActions"""
        payload = {
            "operationName": "getBrokerageActions",
            "variables": {"symbols": [symbol]},
            "query": self._render_template("get_brokerage_actions.j2"),
        }
        return self.requester.post_request(payload)

    def get_chart_interday(self, symbol):
        """getChartInterday"""
        payload = {
            "operationName": "getChartInterday",
            "variables": {"symbol": symbol},
            "query": self._render_template("get_chart_interday.j2"),
        }
        return self.requester.post_request(payload)

    def get_chart_intraday(self, symbol):
        """getChartIntraday"""
        payload = {
            "operationName": "getChartIntraday",
            "variables": {"symbol": symbol},
            "query": self._render_template("get_chart_intraday.j2"),
        }
        return self.requester.post_request(payload)

    def get_financial_data(self, symbol):
        """getFinancialData"""
        payload = {
            "operationName": "getFinancialData",
            "variables": {"symbol": symbol},
            "query": self._render_template("get_financial_data.j2"),
        }
        return self.requester.post_request(payload)

    def get_future_events(self, symbol):
        """getFutureEvents"""
        payload = {
            "operationName": "getManyEvents",
            "variables": {"symbols": [symbol]},
            "query": self._render_template("get_future_events.j2"),
        }
        return self.requester.post_request(payload)

    def get_market_cap(self, symbol):
        """getMarketCap"""
        payload = {
            "operationName": "getMarketCap",
            "variables": {"symbol": symbol},
            "query": self._render_template("get_market_cap.j2"),
        }
        return self.requester.post_request(payload)

    def get_many_events(self, symbol):
        """getManyEvents"""
        payload = {
            "operationName": "getManyEvents",
            "variables": {"symbols": [symbol]},
            "query": self._render_template("get_many_events.j2"),
        }
        return self.requester.post_request(payload)

    def get_near_events(self, symbol):
        """getNearEvents"""
        payload = {
            "operationName": "getNearEvents",
            "variables": {"symbols": [symbol]},
            "query": self._render_template("get_near_events.j2"),
        }
        return self.requester.post_request(payload)

    def get_news_feed(self, symbol):
        """getNewsFeed"""
        payload = {
            "operationName": "getNewsFeed",
            "variables": {"symbols": [symbol], "page": 0, "research": False},
            "query": self._render_template("get_news_feed.j2"),
        }
        return self.requester.post_request(payload)

    def get_overview_data(self, symbol):
        """getOverviewData"""
        payload = {
            "operationName": "getOverviewData",
            "variables": {"symbol": symbol},
            "query": self._render_template("get_overview_data.j2"),
        }
        return self.requester.post_request(payload)

    def get_past_events(self, symbol):
        """getPastEvents"""
        payload = {
            "operationName": "getManyEvents",
            "variables": {"symbols": [symbol]},
            "query": self._render_template("get_past_events.j2"),
        }
        return self.requester.post_request(payload)

    def get_period_guidance(self, symbol):
        """getPeriodGuidance"""
        payload = {
            "operationName": "getPeriodGuidance",
            "variables": {"symbol": symbol, "start": 0, "end": 3},
            "query": self._render_template("get_period_guidance.j2"),
        }
        return self.requester.post_request(payload)

    def get_relative_consensuses(self, symbol):
        """getRelativeConsensuses"""
        payload = {
            "operationName": "getRelativeConsensuses",
            "variables": {"symbol": symbol, "start": 0, "end": 3},
            "query": self._render_template("get_relative_consensuses.j2"),
        }
        return self.requester.post_request(payload)

    def get_symbol(self, symbol):
        """getSymbol"""
        payload = {
            "operationName": "getSymbol",
            "variables": {"symbol": symbol},
            "query": self._render_template("get_symbol.j2"),
        }
        return self.requester.post_request(payload)
