import sqlite3
from datetime import datetime
from constants import * 

# Create class for database access. 
class DBManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('PRAGMA foreign_keys = ON')

    def insert_data(self, tableName, columns, data):
        try:
            sql = 'INSERT OR REPLACE INTO ' + tableName + columns 
            self.cursor.execute(sql, data)
            self.conn.commit()
        except Exception as e:
            pass

    def query_data(self, query, params): 
        result = self.cursor.execute(query, params)
        self.conn.commit()
        return result.fetchall()

    def remove_data(self, query, params):
        self.cursor.execute(query, params)
        self.conn.commit()

# Connect to database.
dbManager = DBManager(db_name)

# Define function to transform query results into list.
def query_result_to_list(result):
    result_list = []
    for entry in result: 
        result_list.append(entry[0])
    return result_list

# Get all stored portfolios. 
def get_portfolios():
    query_result = \
        dbManager.query_data("SELECT DISTINCT PortfolioId FROM stocks", ())
    return query_result_to_list(query_result)

# Get all stocks from portfolio. 
def get_stocks(portfolioId):
    query_result = \
        dbManager.query_data("SELECT ticker FROM stocks WHERE portfolioId = ?", (portfolioId,))
    return query_result_to_list(query_result)

# Get all weights from portfolio. 
def get_weights(portfolioId):
    query_result = \
        dbManager.query_data("SELECT weight FROM stocks WHERE portfolioId = ?", (portfolioId,))
    return query_result_to_list(query_result)

# Get creation date from portfolio.
def get_creation_date(portfolioId):
    query_result = dbManager.query_data(
        "SELECT DISTINCT CreationDate FROM stocks WHERE portfolioId = ?", (portfolioId,)
    )
    return query_result_to_list(query_result)[0]

# Add additional stock to portfolio. 
def add_stock(portfolioId, date, ticker, weight): 
    dbManager.insert_data(
        "Stocks", "(PortfolioId, CreationDate, Ticker, Weight) VALUES(?, ?, ?, ?)",
            (portfolioId, date, ticker, weight),)

# Add new stock to portfolio. 
def add_new_stock(portfolioId, ticker, weight): 
    date = get_creation_date(portfolioId)
    add_stock(portfolioId, date, ticker, weight)

# Add portfolio. 
def add_portfolio(stocks):
    portfolioId = (dbManager.query_data("SELECT MAX(PortfolioId) FROM Stocks", ())[0][0] + 1) 
    date = datetime.today().strftime('%Y-%m-%d')
    for stock in stocks:
        add_stock(portfolioId, date, stock[0], stock[1])

# Update portfolio. 
def update_portfolio(stocks, portfolioId, date):
    for stock in stocks:
        add_stock(portfolioId, date, stock[0], stock[1])

# Delete stock.
def delete_stock(portfolioId, ticker):
    dbManager.remove_data(
        "DELETE FROM STOCKS WHERE Stocks.PortfolioId = ? AND Stocks.Ticker = ?",
        (portfolioId, ticker),
    )

# Delete portfolio.
def delete_portfolio(portfolioId):
    dbManager.remove_data(
        "DELETE FROM STOCKS WHERE Stocks.PortfolioId = ? ", (portfolioId,)
    )
