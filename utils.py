import pandas as pd
from database import SessionLocal, StockData
import smtplib
from email.mime.text import MIMEText


def get_volume_comparisons(symbol, timeframe="5D"):
    session = SessionLocal()
    #Query the database for selected stock
    query= session.query(StockData).filter(StockData.symbol==symbol).all()
    
    #convert data into dataframe
    data = pd.DataFrame([{
        "timestamp": stock.timestamp,
        "volume": stock.volume
    } for stock in query])

    #process the data
    data.set_index("timestamp", inplace=True)
    recent_volume = data["volume"].iloc[-1]
    avg_volume = data["volume"].resample("2T").mean() # resample to 2T (2 minutes)
    
    return {
        "recent_volume": recent_volume,
        "avg_volume": avg_volume.mean(),
        "comparison": (recent_volume - avg_volume.mean()) / avg_volume.mean() * 100
        }


def check_alers(symbol):
    comparison = get_volume_comparisons(symbol)
    alerts = []
    if comparison["comparison"] > 20:
        alerts.append(f"Volume for {symbol} is up by {comparison['comparison']:.2f}% compared to the 5-day average")
        if comparison["recent_volume"] > 2 * comparison["avg_volume"]:
            alerts.append(f"Recent volume for {symbol} is twice the 5-day average.")
            return alerts
        
def send_email(subject, body):
    sender_email = "siddiquembio2012@gmail.com"
    receiver_email = "polashtechai@gmail.com"
    password = "prime121"
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        