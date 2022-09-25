import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from sentiment import *
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 5})
from dbmanager import *
import os
cwd = os.getcwd()

# Plot stock report.
def plot_stock(ticker):

    # Get stock info and setup plot grid.
    stock = yf.Ticker(ticker)
    fig = plt.figure(constrained_layout=True)
    fig.suptitle(f"{ticker} Stock Report", weight="bold", fontsize=7)
    gs = GridSpec(3, 3, figure=fig)

    # Plot stock performance.
    ax1 = fig.add_subplot(gs[0, :])
    ax1.set_title("Performance", weight="bold")
    hist = stock.history(period="max")
    hist.reset_index(inplace=True)
    sns.lineplot(x=hist["Date"], y=hist["Close"], ax=ax1)

    # Plot sentiment.
    ax2 = fig.add_subplot(gs[1, 0])
    sentiment = get_current_sentiment(ticker)
    color = "g" if sentiment[0] >= 0 else "r"
    sentiment_df = pd.DataFrame(
        data={"Label": ["Current Sentiment"], "Sentiment Score": sentiment[0]}
    )
    ax2 = sns.barplot(
        x=sentiment_df["Label"], y=sentiment_df["Sentiment Score"], color=color
    )
    ax2.spines["bottom"].set_position("zero")
    ax2.set(xticklabels=[])
    ax2.set(xlabel=None)
    ax2.tick_params(bottom=False)
    ax2.set_title(f"The Current Sentiment is {sentiment[1]}", weight="bold", fontsize=5)

    # Plot revenue.
    ax3 = fig.add_subplot(gs[1, 1])
    financial_df = stock.quarterly_financials
    financial_df = financial_df.transpose().reset_index()
    financial_df.rename(columns={financial_df.columns[0]: "Date"}, inplace=True)
    financial_df["Total Revenue"] = pd.to_numeric(financial_df["Total Revenue"])
    financial_df["Date"] = pd.to_datetime(
        financial_df["Date"], format="%Y-%m"
    ).dt.strftime("%Y-%m")
    financial_df = financial_df.reindex(index=financial_df.index[::-1])
    sns.barplot(data=financial_df, x="Date", y="Total Revenue", palette="Blues", ax=ax3)
    ax3.set_title("Tota Revenue", weight="bold")

    # Plot traded volume.
    ax4 = fig.add_subplot(gs[1, 2])
    sns.lineplot(x=hist["Date"], y=hist["Volume"], ax=ax4, lw=0.5)
    ax4.set_title("Volume", weight="bold")

    # Plot analyst recommendations.
    ax5 = fig.add_subplot(gs[-1, 0])
    fig.patch.set_visible(False)
    ax5.axis("off")
    ax5.axis("tight")
    df = stock.recommendations
    df = df[["Firm", "To Grade"]].head(5)
    table = ax5.table(
        cellText=df.values, colLabels=df.columns, loc="center", cellLoc="left"
    )
    table.scale(1, 1)
    ax5.set_title("Analyst Recommendations", weight="bold")

    # Plot inst. holders.
    ax6 = fig.add_subplot(gs[-1, 1])
    fig.patch.set_visible(False)
    ax6.axis("off")
    ax6.axis("tight")
    df = stock.institutional_holders
    df = df[["Holder", "% Out"]].head(5)
    table = ax6.table(
        cellText=df.values, colLabels=df.columns, loc="center", cellLoc="left"
    )
    table.scale(1, 1)
    ax6.set_title("Institutional Holders", weight="bold")

    # Plot sustainability
    try:
        ax7 = fig.add_subplot(gs[-1, 2])
        fig.patch.set_visible(False)
        ax7.axis("off")
        ax7.axis("tight")
        sustainability_df = stock.sustainability
        sustainability_df = sustainability_df.reset_index()
        sustainability_df.rename(
            columns={sustainability_df.columns[0]: "Category"}, inplace=True
        )
        # Only social score and sustainability issues. 
        sustainability_df = sustainability_df[
            (sustainability_df["Value"] == True)
            | (sustainability_df["Category"] == "socialScore")
        ]
        table = ax7.table(
            cellText=sustainability_df.values,
            colLabels=sustainability_df.columns,
            loc="center",
            cellLoc="left",
        )
        table.scale(1, 1)
        ax7.set_title("Sustainability Report", weight="bold")
    except:
        return fig

    return fig



# Function to put stock report into PDF. 
def create_stock_report(ticker):
    report = PdfPages(f'{cwd}/Stock_Reports/{ticker}_Report.pdf')
    report_fig = plot_stock(ticker)
    report.savefig(report_fig)
    report.close()

# Function to plot portfolio overview. 
def plot_portfolio(portfolioId):
    
    # Create figure. 
    fig = plt.figure(constrained_layout=True)
    fig.suptitle(f"Portfolio #{portfolioId} Report", weight = "bold", fontsize = 7)
    gs = GridSpec(2, 2, figure=fig)
    
    # Get stock infos. 
    tickers = get_stocks(portfolioId)
    weights = get_weights(portfolioId)
    stock_tuples = list(zip(tickers, weights))
    performance_list = []
    creationdate = get_creation_date(portfolioId)
    for index, tuple in enumerate(stock_tuples):
        stock = yf.Ticker(tuple[0])
        df = stock.history(start = creationdate)
        df[f"{tuple[0]}"] = df["Close"].pct_change()*tuple[1]
        performance_list.append(df[f"{tuple[0]}"])
    df = pd.concat(performance_list, axis=1)
    
    # Plot weighted portfolio performance. 
    ax1 = fig.add_subplot(gs[0, :])
    ax1.set_title('Portfolio Performance', weight = "bold")
    df2 = df.copy()
    df2["sum"] = df2.sum(axis=1) + 1
    df2["cum_change"] = df2["sum"].cumprod()
    sns.lineplot(x = df.index, y = df2["cum_change"], ax=ax1)
    
    # Plot portfolio weights. 
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.set_title(f"Portfolio Weights", weight = "bold", fontsize = 5)
    sns.barplot(x = tickers, y = weights, palette = "Blues", ax = ax2)
    ax2.set_ylabel("Weight")
    ax2.set_xlabel("Stock")

    # Plot correlation heatmap 
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.set_title("Correlation Heatmap", weight = "bold")
    mask = np.triu(np.ones_like(df.corr()))
    sns.heatmap(
    df.corr(),
    cmap="vlag",
    mask=mask,
    vmin = -1, 
    vmax = 1,
    ax = ax3)
    
    return fig 

# Generate PDF portfolio report. 
def create_portfolio_report(portfolioId):
    # Get stocks in portfolio. 
    stock_list = get_stocks(portfolioId)
    
    # Create PDF report. 
    report = PdfPages(f'{cwd}/Portfolio_Reports/Portfolio_#{portfolioId}_Report.pdf')
    
    # Plot portfolio overview. 
    portfolio_fig = plot_portfolio(portfolioId)
    report.savefig(portfolio_fig)
    
    # Attach individual stock reports. 
    for stock in stock_list: 
        report_fig = plot_stock(stock)
        report.savefig(report_fig)
                
    report.close()