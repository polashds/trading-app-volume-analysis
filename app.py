from flask import Flask, render_template, request, redirect, url_for
from utils import get_volume_comparisons
from logging_config import logger


app = Flask(__name__)

#Store stock symbols in memory for simplicity
symbols = ["AAPL", "GOOGL", "MSFT", "AMZN"]

@app.route("/", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        #Handle form submission to add a new stock symbol
        new_symbol = request.form.get("symbol").upper()
        if new_symbol and new_symbol not in symbols:
            symbols.append(new_symbol)
            logger.info(f"Added new stock symbol: {new_symbol}")
        return redirect(url_for("dashboard"))

    #Fetch data and comparisons
    comparisons = []
    for symbol in symbols:
        try: 
            comparison = get_volume_comparisons(symbol)
            if comparison: 
                comparisons.append({
                    "symbol": symbol,
                    "recent_volume": comparisons["recent_volume"],
                    "avg_volume": comparisons["avg_volume"],
                    "comparison": comparisons["comparison"]
                })
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {e}")

        return render_template("dashboard.html", data=comparisons)


# @app.route("/add_stock", methods=["POST"])
# def add_stock():
#     stock = request.form.get("stock")
#     if stock and stock not in stocks:
#         stocks.append(stock)

#     return ("/")


if __name__ == "__main__":
    app.run(debug=True)