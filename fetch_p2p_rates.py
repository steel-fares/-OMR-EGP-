import requests
import json

def fetch_p2p_rate(fiat, trade_type, asset="USDT"):
    """
    trade_type: 'BUY' (to get price if you want to buy USDT with fiat) 
                'SELL' (to get price if you want to sell USDT for fiat)
    """
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    payload = {
        "asset": asset,
        "fiat": fiat,
        "merchantCheck": False,
        "page": 1,
        "payTypes": [],
        "publisherType": None,
        "rows": 5,
        "tradeType": trade_type
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        if data.get("code") == "000000" and data.get("data"):
            prices = [float(item['adv']['price']) for item in data['data']]
            avg_price = sum(prices) / len(prices)
            return avg_price
        return None
    except Exception:
        return None

if __name__ == "__main__":
    print("--- أسعار السوق الحية (Binance P2P) ---")
    
    # مسار عمان -> مصر
    omr_buy = fetch_p2p_rate("OMR", "BUY")   # سعر شرائك للـ USDT بالريال
    egp_sell = fetch_p2p_rate("EGP", "SELL") # سعر بيعك للـ USDT بالجنيه
    
    # مسار مصر -> عمان
    egp_buy = fetch_p2p_rate("EGP", "BUY")   # سعر شرائك للـ USDT بالجنيه
    omr_sell = fetch_p2p_rate("OMR", "SELL") # سعر بيعك للـ USDT بالريال
    
    print(f"1. مسار عمان إلى مصر:")
    print(f"   - سعر شراء USDT بالريال: {omr_buy}")
    print(f"   - سعر بيع USDT بالجنيه: {egp_sell}")
    if omr_buy and egp_sell:
        print(f"   - سعر الصرف العادل: 1 OMR = {egp_sell/omr_buy:.2f} EGP")

    print(f"\n2. مسار مصر إلى عمان:")
    print(f"   - سعر شراء USDT بالجنيه: {egp_buy}")
    print(f"   - سعر بيع USDT بالريال: {omr_sell}")
    if egp_buy and omr_sell:
        print(f"   - سعر الصرف العادل: 1 OMR = {egp_buy/omr_sell:.2f} EGP")
