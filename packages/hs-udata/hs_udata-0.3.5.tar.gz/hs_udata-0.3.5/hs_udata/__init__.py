import warnings
import importlib
import pkgutil

__version__ = '0.3.5'

def _init():
    for loader, module_name, is_pkg in pkgutil.walk_packages(__path__, "hs_udata."):
        if module_name.startswith("hs_udata.apis") and not is_pkg:
            try:
                api_module = importlib.import_module(module_name)
            except ImportError as ex:
                warnings.warn("import module[{}] error, msg={}".format(module_name, ex))

            for api_name in api_module.__all__:
                try:
                    api = getattr(api_module, api_name)
                    globals()[api_name] = api
                except AttributeError as ex:
                    warnings.warn("load api[{}] error, msg={}".format(api_name, ex))

_init()

del _init

def set_token(token=None):
    from hs_udata.utils.client import init
    init(username="license", password=token)


from hs_udata.apis.stock.api import stock_list
from hs_udata.apis.stock.api import trading_calendar
from hs_udata.apis.stock.api import ipo_list
from hs_udata.apis.stock.api import company_profile
from hs_udata.apis.stock.api import stock_Info
from hs_udata.apis.stock.api import leader_profile
from hs_udata.apis.stock.api import st_stock_list
from hs_udata.apis.stock.api import shszhk_stock_list
from hs_udata.apis.stock.api import stock_quote_daily
from hs_udata.apis.stock.api import stock_quote_weekly
from hs_udata.apis.stock.api import stock_quote_monthly
from hs_udata.apis.stock.api import stock_quote_yearly
from hs_udata.apis.stock.api import money_flow
from hs_udata.apis.stock.api import suspension_list
from hs_udata.apis.stock.api import shareholder_top10
from hs_udata.apis.stock.api import float_shareholder_top10
from hs_udata.apis.stock.api import lh_daily
from hs_udata.apis.stock.api import lh_stock
from hs_udata.apis.stock.api import stock_quote_minutes
from hs_udata.apis.stock.api import shszhk_capitalflow
from hs_udata.apis.stock.api import shszhk_deal_top10
from hs_udata.apis.stock.api import shszhk_distribution
from hs_udata.apis.stock.api import shszhk_change_top10
from hs_udata.apis.stock.api import quote_stocklist
from hs_udata.apis.stock.api import industry_category
from hs_udata.apis.stock.api import index_constituent
from hs_udata.apis.stock.api import org_hold
from hs_udata.apis.stock.api import holder_num
from hs_udata.apis.stock.api import restricted_schedule
from hs_udata.apis.stock.api import holder_pledge
from hs_udata.apis.stock.api import holder_increase
from hs_udata.apis.stock.api import pledge_repo
from hs_udata.apis.stock.api import stock_pledge
from hs_udata.apis.stock.api import block_trade
from hs_udata.apis.stock.api import margin_trading
from hs_udata.apis.stock.api import interval_margin_trading
from hs_udata.apis.stock.api import margin_trade_detail
from hs_udata.apis.stock.api import margin_trade_total
from hs_udata.apis.stock.api import stock_dividend
from hs_udata.apis.stock.api import stock_additional
from hs_udata.apis.stock.api import stock_additional_all
from hs_udata.apis.stock.api import stock_allotment
from hs_udata.apis.stock.api import stock_asforecastabb
from hs_udata.apis.stock.api import stock_asunderweight
from hs_udata.apis.stock.api import stock_asoverweight
from hs_udata.apis.stock.api import stock_asrighttransfer
from hs_udata.apis.stock.api import stock_asraising
from hs_udata.apis.stock.api import schedule_disclosure
from hs_udata.apis.stock.api import stock_key_indicator
from hs_udata.apis.stock.api import accounting_data
from hs_udata.apis.stock.api import financial_cashflow
from hs_udata.apis.stock.api import financial_income
from hs_udata.apis.stock.api import financial_balance
from hs_udata.apis.stock.api import financial_gene_qincome
from hs_udata.apis.stock.api import financial_bank_qincome
from hs_udata.apis.stock.api import financial_secu_qincome
from hs_udata.apis.stock.api import financial_insu_qincome
from hs_udata.apis.stock.api import financial_gene_qcashflow
from hs_udata.apis.stock.api import financial_bank_qcashflow
from hs_udata.apis.stock.api import financial_secu_qcashflow
from hs_udata.apis.stock.api import financial_insu_qcashflow
from hs_udata.apis.stock.api import performance_forecast
from hs_udata.apis.stock.api import performance_letters
from hs_udata.apis.stock.api import performance_letters_q
from hs_udata.apis.stock.api import main_composition
from hs_udata.apis.stock.api import trading_parties
from hs_udata.apis.stock.api import audit_opinion
from hs_udata.apis.stock.api import per_share_index
from hs_udata.apis.stock.api import profitability
from hs_udata.apis.stock.api import growth_capacity
from hs_udata.apis.stock.api import du_pont_analysis
from hs_udata.apis.stock.api import deri_fin_indicators
from hs_udata.apis.stock.api import q_financial_indicator
from hs_udata.apis.stock.api import valuation_info
from hs_udata.apis.stock.api import corporation_value
from hs_udata.apis.stock.api import star_ipodeclare
from hs_udata.apis.stock.api import star_companyprofile
from hs_udata.apis.stock.api import neeq_basic
from hs_udata.apis.stock.api import neeq_company
from hs_udata.apis.stock.api import neeq_leader
from hs_udata.apis.stock.api import neeq_leader_num
from hs_udata.apis.stock.api import neeq_industry
from hs_udata.apis.stock.api import fund_list
from hs_udata.apis.stock.api import fund_manager_company
from hs_udata.apis.stock.api import fund_manager
from hs_udata.apis.stock.api import fund_profile
from hs_udata.apis.stock.api import fund_institutions
from hs_udata.apis.stock.api import fund_etf
from hs_udata.apis.stock.api import fund_size
from hs_udata.apis.stock.api import fund_charge_rate
from hs_udata.apis.stock.api import fund_index
from hs_udata.apis.stock.api import fund_type
from hs_udata.apis.stock.api import fund_style
from hs_udata.apis.stock.api import fund_holder_public
from hs_udata.apis.stock.api import fund_quote_daily_history
from hs_udata.apis.stock.api import fund_quote_daily
from hs_udata.apis.stock.api import fund_quote_weekly
from hs_udata.apis.stock.api import fund_quote_monthly
from hs_udata.apis.stock.api import fund_quote_yearly
from hs_udata.apis.stock.api import fund_net_value
from hs_udata.apis.stock.api import moneyfund_performance
from hs_udata.apis.stock.api import fund_stock_detail
from hs_udata.apis.stock.api import fund_asset
from hs_udata.apis.stock.api import fund_holder
from hs_udata.apis.stock.api import fund_rangerise
from hs_udata.apis.stock.api import fund_rank
from hs_udata.apis.stock.api import fut_basic
from hs_udata.apis.stock.api import fut_quote_minute
from hs_udata.apis.stock.api import fut_list
from hs_udata.apis.stock.api import fut_count_rank
from hs_udata.apis.stock.api import fut_holding_lh
from hs_udata.apis.stock.api import fut_contract_type
from hs_udata.apis.stock.api import con_price
from hs_udata.apis.stock.api import con_time
from hs_udata.apis.stock.api import con_detail
from hs_udata.apis.stock.api import con_calender
from hs_udata.apis.stock.api import hk_list
from hs_udata.apis.stock.api import hk_ipo
from hs_udata.apis.stock.api import hk_company
from hs_udata.apis.stock.api import hk_secu
from hs_udata.apis.stock.api import hk_leader
from hs_udata.apis.stock.api import hk_daily_quote
from hs_udata.apis.stock.api import hk_weekly_quote
from hs_udata.apis.stock.api import hk_monthly_quote
from hs_udata.apis.stock.api import hk_yearly_quote
from hs_udata.apis.stock.api import hk_section_quote
from hs_udata.apis.stock.api import hk_daily_quote_short
from hs_udata.apis.stock.api import hk_weekly_quote_short
from hs_udata.apis.stock.api import hk_monthly_quote_short
from hs_udata.apis.stock.api import hk_yearly_quote_short
from hs_udata.apis.stock.api import hk_section_quote_short
from hs_udata.apis.stock.api import hk_minutes_hkscclist
from hs_udata.apis.stock.api import hk_minutes_hkscc
from hs_udata.apis.stock.api import hk_share_stru
from hs_udata.apis.stock.api import hk_exgindustry
from hs_udata.apis.stock.api import hk_cap_structure
from hs_udata.apis.stock.api import hk_profit_ability
from hs_udata.apis.stock.api import hk_per_share_index
from hs_udata.apis.stock.api import hk_solvency
from hs_udata.apis.stock.api import hk_mainincomestru
from hs_udata.apis.stock.api import hk_dividend
from hs_udata.apis.stock.api import hk_buyback
from hs_udata.apis.stock.api import chip_data
from hs_udata.apis.stock.api import chip_concentration
from hs_udata.apis.stock.api import chip_support_price
from hs_udata.apis.stock.api import chip_cost_data
from hs_udata.apis.stock.api import stock_quote_daily_list
from hs_udata.apis.stock.api import index_quote
from hs_udata.apis.stock.api import stock_share_holders
from hs_udata.apis.stock.api import con_quote
from hs_udata.apis.stock.api import ec_rate_quote
from hs_udata.apis.stock.api import stock_special_tradedate
from hs_udata.apis.stock.api import stock_org_rate
from hs_udata.apis.stock.api import stock_org_rate_sum
from hs_udata.apis.stock.api import stock_investor_statistics
from hs_udata.apis.stock.api import stock_financial_industry_list
from hs_udata.apis.stock.api import stock_investor_detail
from hs_udata.apis.stock.api import stock_industry_compare
from hs_udata.apis.stock.api import stock_industry_avg
from hs_udata.apis.stock.api import stock_industry_region_list
from hs_udata.apis.stock.api import stock_company_news
from hs_udata.apis.stock.api import stock_news
from hs_udata.apis.stock.api import stock_news_info
from hs_udata.apis.stock.api import stock_main_composition
from hs_udata.apis.stock.api import stock_main_business_total
from hs_udata.apis.stock.api import stock_main_business_indurstry
from hs_udata.apis.stock.api import neeq_perform_fore
from hs_udata.apis.stock.api import neeq_dupont_analysis
from hs_udata.apis.stock.api import neeq_share_stru
from hs_udata.apis.stock.api import neeq_per_share_index
from hs_udata.apis.stock.api import neeq_issue_count
from hs_udata.apis.stock.api import neeq_holder_num
from hs_udata.apis.stock.api import neeq_holder_info
from hs_udata.apis.stock.api import fund_style_code
from hs_udata.apis.stock.api import fund_style_info
from hs_udata.apis.stock.api import fund_index_quote
from hs_udata.apis.stock.api import fund_style_comp
from hs_udata.apis.stock.api import fund_index_gr
from hs_udata.apis.stock.api import hk_company_news

from hs_udata.apis.stock.api import get_factor_list
from hs_udata.apis.stock.api import get_beta_factor
from hs_udata.apis.stock.api import get_volatility_factor
from hs_udata.apis.stock.api import get_solvency_factor
from hs_udata.apis.stock.api import get_growth_factor
from hs_udata.apis.stock.api import get_momentum_factor
from hs_udata.apis.stock.api import get_minute_factor
from hs_udata.apis.stock.api import get_barra_basic_factor
from hs_udata.apis.stock.api import get_barra_description_factor
from hs_udata.apis.stock.api import get_leverage_factor
from hs_udata.apis.stock.api import get_valueation_factor
from hs_udata.apis.stock.api import get_liquidity_factor
from hs_udata.apis.stock.api import get_sentiment_factor
from hs_udata.apis.stock.api import get_size_factor
from hs_udata.apis.stock.api import get_event_factor
from hs_udata.apis.stock.api import get_cash_flow_factor
from hs_udata.apis.stock.api import get_consensus_factor
from hs_udata.apis.stock.api import get_earning_factor
from hs_udata.apis.stock.api import get_operation_factor
from hs_udata.apis.stock.api import get_quality_factor
from hs_udata.apis.stock.api import get_barra_factor
