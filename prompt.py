from langchain_core.prompts import PromptTemplate

# Balance Sheet Template
balance_sheet_template = PromptTemplate(
    input_variables=["data"],
    template="""
You are a financial analyst. Analyze the following BALANCE SHEET data and generate a clear summary.

Data:
{data}

Your summary must include:
- Total Assets
- Total Liabilities
- Equity
- Any major change compared to previous periods
- Overall financial health

Provide a simple, human-friendly explanation.
"""
)

# Profit and Loss Template
profit_loss_template = PromptTemplate(
    input_variables=["data"],
    template="""
You are a financial expert. Summarize the following PROFIT AND LOSS STATEMENT.

Data:
{data}

Your summary must include:
- Revenue and trends
- Expenses
- Net profit / loss
- Year-over-year changes
- Key insights for decision making

Generate a simple summary.
"""
)

# Cash Flow Template
cash_flow_template = PromptTemplate(
    input_variables=["data"],
    template="""
You are a financial analyst. Review the CASH FLOW STATEMENT below and create a clear summary.

Data:
{data}

Your summary should include:
- Cash flow from operations
- Cash flow from investing
- Cash flow from financing
- Net cash position
- Important observations

Explain in simple language.
"""
)

templates = {
    "balance_sheet": balance_sheet_template,
    "profit_loss": profit_loss_template,
    "cash_flow": cash_flow_template,
}
