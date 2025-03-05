import json

from chain import gaurd_rail


def get_formatting_prompt_by_report_name(name, json_data):
    if name == "NET_SALES":
        return get_net_sales_formatting_prompt(json_data)


def get_net_sales_formatting_prompt(json_data):
    fk_id_transaction_type_dictionary = {
        "1": "Fresh Purchase",
        "2": "Additional Purchase",
        "3": "Partial Redemption",
        "4": "Full Redemption",
        "5": "Bonus",
        "6": "Change of Address",
        "7": "Change of Mandate",
        "8": "Dividend Payout",
        "9": "Dividend Reinvestment",
        "10": "Switch In",
        "11": "Switch Out",
        "12": "Transfer In Change of Broker",
        "13": "Transfer Out Change of Broker",
        "21": "Buy",
        "22": "Sell",
        "31": "Coupon Paid",
        "41": "Subscription",
        "42": "Withdrawl",
        "43": "Close-Out",
        "44": "Top-Up",
        "51": "Put",
        "52": "Call",
        "53": "Maturity",
        "61": "Drawdown",
        "62": "Return on Captial",
        "63": "Return of Capital",
        "71": "TDS",
        "72": "Platform Subscription Fee",
        "73": "Investment",
        "74": "Redemption",
        "75": "Purchase",
        "76": "Transmission - IN",
        "77": "Dematerialization",
        "78": "Consolidation - OUT",
        "79": "Consolidation - IN",
        "80": "Transmission - OUT",
        "109": "Amc",
        "115": "BNS",
        "121": "Fresh Purchase1",
        "122": "Fresh Purchase9",
    }

    fk_id_instrument_category_dictionary = {
        "1": "Equity: Multi Cap",
        "2": "Equity: Thematic-Energy",
        "3": "Equity: Thematic-PSU",
        "4": "Equity: Thematic-ESG-TEST",
        "5": "Equity: Sectoral-Banking",
        "6": "Equity: Sectoral-FMCG",
        "7": "Equity: Sectoral-Infrastructure",
        "8": "Equity: Sectoral-Pharma",
        "9": "Equity: Thematic-Dividend Yield",
        "10": "Equity: Sectoral-Technology",
        "11": "Equity: Thematic-MNC",
        "12": "Hybrid: Balanced Advantage",
        "13": "Equity: Thematic-Consumption",
        "14": "Debt: Floater",
        "15": "Debt: Gilt with 10 year Constant Duration",
        "16": "Debt: Gilt",
        "17": "Equity: Large Cap",
        "18": "Equity: Large & MidCap",
        "19": "Equity: Flexi Cap",
        "20": "Equity: Mid Cap",
        "21": "Equity: Small Cap",
        "22": "Equity: Value Oriented",
        "23": "Equity: ELSS",
        "24": "Equity: Thematic",
        "25": "Equity: International",
        "26": "Debt: Long Duration",
        "27": "Debt: Medium to Long Duration",
        "28": "Debt: Medium Duration",
        "29": "Debt: Short Duration",
        "30": "Debt: Ultra Short Duration",
        "31": "Debt: Low Duration",
        "32": "Debt: Liquid",
        "33": "Debt: Overnight",
        "34": "Debt: Money Market",
        "35": "Debt: Dynamic Bond",
        "36": "Debt: Fixed Maturity",
        "37": "Debt: Credit Risk",
        "38": "Debt: Banking and PSU",
        "39": "Hybrid: Aggressive Hybrid",
        "40": "Debt: Corporate Bond",
        "41": "Hybrid: Balanced Hybrid",
        "42": "Hybrid: Conservative Hybrid",
        "43": "Hybrid: Equity Savings",
        "44": "Hybrid: Arbitrage",
        "45": "Hybrid: Dynamic Asset Allocation",
        "46": "Hybrid: Multi Asset Allocation",
        "47": "Commodities: Gold",
        "48": "Debt: Ultra Short Term(Old)",
        "49": "Debt: Short Term(Old)",
        "50": "Debt: Liquid(Old)",
        "51": "Debt: Income(Old)",
        "52": "Debt: Gilt Short Term(Old)",
        "53": "Debt: Gilt Medium & Long Term(Old)",
        "54": "Debt: FMP(Old)",
        "55": "Equity: Large Cap(Old)",
        "56": "Equity: Multi Cap(Old)",
        "57": "Equity: Mid Cap(Old)",
        "58": "Equity: Small Cap(Old)",
        "59": "Equity: Banking(Old)",
        "60": "Equity: Others(Old)",
        "61": "Equity: Auto(Old)",
        "62": "Equity: Petroleum(Old)",
        "63": "Equity: Pharma(Old)",
        "64": "Equity: Tax Saving(Old)",
        "65": "Equity: FMCG(Old)",
        "66": "Equity: Technology(Old)",
        "67": "Equity: Infrastructure(Old)",
        "68": "Hybrid: Equity-oriented(Old)",
        "69": "Hybrid: Debt-oriented Aggressive(Old)",
        "70": "Equity: International(Old)",
        "71": "Hybrid: Debt-oriented Conservative(Old)",
        "72": "Hybrid: Arbitrage(Old)",
        "73": "Hybrid: Asset Allocation(Old)",
        "74": "Gold: Funds(Old)",
        "75": "Hybrid: Others(Old)",
        "76": "Debt: Others(Old)",
        "77": "Debt: Dynamic Bond(Old)",
        "78": "Debt: Credit Opportunities(Old)",
        "79": "Commodities: Silver",
        "80": "Debt: Deposit",
        "81": "Debt: Target Maturity",
        "84": "Debt: Target Maturity2",
        "85": "Debt: Target Maturity1",
        "91": "Debt: Others",
        "116": "Hybrid: Arbitrage Hybrid",
        "117": "Commodities: Gold",
        "118": "Bitcoin",
        "119": "Bitcoin 2",
        "120": "Debt: Others",
    }

    column_mapping = {
        "fk_id_account": "sw_account_id",
        "uniqueId": "investor_id",
        "bos_code": "bank_customer_id",
    }
    prompt = f"""
       Given the following JSON data:

       ```json
       {json.dumps(json_data, indent=2)}
       ```

       Perform the following transformations:
       1. Replace `fk_id_transaction_type` using this mapping: {fk_id_transaction_type_dictionary}
       2. Replace `fk_id_instrument_category` or `instrument_fk_id_instrument_category` inside `instrument_details` using this mapping: {fk_id_instrument_category_dictionary}
       3. Rename columns according to this mapping: {column_mapping}
       4. Flatten the JSON structure, ensuring that `instrument_details` and `account_details` fields are moved to the top level instead of being nested

       Return the fully transformed JSON output.
       """
    return gaurd_rail.format(prompt)
