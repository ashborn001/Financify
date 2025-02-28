import yfinance as yf
import os
import matplotlib.pyplot as plt
import requests
from datetime import datetime, timedelta
from langchain.tools import tool
from langgraph.graph import StateGraph
from langchain_core.runnables import Runnable
from typing import TypedDict, List
from dotenv import load_dotenv

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

class StockState(TypedDict):
    symbol: str
    result: str

#Stock Data and Generate a Graph
@tool
def fetch_stock_data(symbol: str) -> str:
    """
    Fetches stock data for the given ticker symbol and returns a visualization.
    """
    stock = yf.Ticker(symbol)
    t = input("Enter time period in days (Eg.- 7d): ")
    hist = stock.history(period=t)

    if hist.empty:
        return f"No data found for symbol: {symbol}"
    
    x = hist.index
    y = hist['Close']

    fig = plt.figure(figsize=(15, 8))
    ax = fig.add_subplot(111)
    plt.plot(hist.index, hist['Close'], marker='o', linestyle='-')
    plt.title(f"{symbol} Stock Price (Last {t} Days)")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    
    for i, j in zip(x, round(y, 2)):
        ax.annotate(str(j), xy=(i, j))

    plt.grid()
    filename = f"{symbol}_stock.png"
    plt.savefig(filename)
    
    return f"Stock data visualization for last {t} days saved as {filename}"

#Financial News for the Company
@tool
def fetch_financial_news(symbol: str) -> str:
    """
    Fetches financial news for the given ticker symbol over a user-defined time range. Identify the company through its ticker symbol and then look for financial news related to it as per date.
    """
    days = int(input("Enter the number of past days to fetch news: "))
    end_date = datetime.today()
    start_date = end_date - timedelta(days=days)

    url = f"https://newsapi.org/v2/everything?q={symbol}&from={start_date.date()}&to={end_date.date()}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    
    response = requests.get(url)
    news_data = response.json()

    if "articles" not in news_data or not news_data["articles"]:
        return f"No financial news found for {symbol} in the last {days} days."

    news_by_date = {}
    for article in news_data["articles"]:
        pub_date = article["publishedAt"][:10]
        news_by_date.setdefault(pub_date, []).append(f"- {article['title']}")

    formatted_news = "\n".join([f"{date}:\n" + "\n".join(news) for date, news in sorted(news_by_date.items(), reverse=True)])
    
    return f"Financial News for {symbol} in the last {days} days:\n{formatted_news}"

#Financial Assistant Agent
class StockAgent(Runnable):
    def invoke(self, state: StockState, config=None, **kwargs) -> StockState:
        symbol = state["symbol"]
        task = input("Choose task: [1] Stock Data, [2] Financial News: ")
        
        if task == "1":
            result = fetch_stock_data.invoke(symbol)
        elif task == "2":
            result = fetch_financial_news.invoke(symbol)
        else:
            result = "Invalid choice. Please select 1 or 2."
        
        return {"symbol": symbol, "result": result}

#Workflow
graph = StateGraph(StockState) 
graph.add_node("agent", StockAgent())
graph.set_entry_point("agent")

workflow = graph.compile()

if __name__ == "__main__":
    stock_symbol = input("Enter ticker symbol in capital: ") 
    result = workflow.invoke({"symbol": stock_symbol})
    print(result["result"])
