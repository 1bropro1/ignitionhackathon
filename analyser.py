from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the Stock Market Analyzer!"

@app.route("/analyze", methods=["GET"])
def analyze_stock():
    symbol = request.args.get("symbol")
    if not symbol:
        return jsonify({"error": "Stock symbol is required"}), 400

    try:
        stock = yf.Ticker(symbol)
        history = stock.history(period="1mo")  # Get data for the last month

        # Calculate simple metrics
        current_price = history['Close'].iloc[-1]
        moving_avg = history['Close'].rolling(window=10).mean().iloc[-1]
        highest_price = history['High'].max()
        lowest_price = history['Low'].min()

        analysis = {
            "symbol": symbol,
            "current_price": round(current_price, 2),
            "10_day_moving_avg": round(moving_avg, 2) if not pd.isna(moving_avg) else "Insufficient data",
            "highest_price_last_month": round(highest_price, 2),
            "lowest_price_last_month": round(lowest_price, 2)
        }

        return jsonify(analysis)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
