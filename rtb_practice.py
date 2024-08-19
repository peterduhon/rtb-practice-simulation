import json
import random
from datetime import datetime
import matplotlib.pyplot as plt  # <-- Import matplotlib.pyplot here

# 1. Simulating an OpenRTB Bid Request

def generate_bid_request():
    return {
        "id": f"bid-{random.randint(1000, 9999)}",
        "imp": [{
            "id": "1",
            "banner": {
                "w": 300,
                "h": 250,
                "pos": 1
            },
            "bidfloor": 0.01
        }],
        "site": {
            "id": "site-123",
            "domain": "example.com"
        },
        "device": {
            "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "ip": "192.168.1.1"
        },
        "user": {
            "id": "user-abc"
        }
    }

# 2. Simulating a Bid Response

def generate_bid_response(request):
    return {
        "id": request["id"],
        "seatbid": [{
            "bid": [{
                "id": f"bid-{random.randint(1000, 9999)}",
                "impid": "1",
                "price": round(random.uniform(0.1, 2.0), 2),
                "adm": "<ad markup>",
                "crid": "creative-123",
                "w": 300,
                "h": 250
            }]
        }],
        "bidid": f"bidid-{random.randint(1000, 9999)}"
    }

# 3. Simulating an RTB Auction

def run_rtb_auction(bid_request, num_bidders=3):
    bids = []
    for i in range(num_bidders):
        bid_response = generate_bid_response(bid_request)
        bids.append(bid_response["seatbid"][0]["bid"][0])
    
    winning_bid = max(bids, key=lambda x: x["price"])
    return winning_bid

# 4. Analyzing Auction Results

def analyze_auction_results(auctions):
    total_bids = len(auctions)
    total_value = sum(auction["price"] for auction in auctions)
    avg_bid = total_value / total_bids
    max_bid = max(auctions, key=lambda x: x["price"])
    min_bid = min(auctions, key=lambda x: x["price"])
    
    return {
        "total_auctions": total_bids,
        "total_value": round(total_value, 2),
        "average_bid": round(avg_bid, 2),
        "highest_bid": max_bid["price"],
        "lowest_bid": min_bid["price"]
    }

# 5. Running a simulation

def run_simulation(num_auctions=100):
    auction_results = []
    for _ in range(num_auctions):
        bid_request = generate_bid_request()
        winning_bid = run_rtb_auction(bid_request)
        auction_results.append(winning_bid)
    
    analysis = analyze_auction_results(auction_results)
    return auction_results, analysis

# Run the simulation
auction_results, simulation_results = run_simulation()
print("Simulation Results:")
print(json.dumps(simulation_results, indent=2))

# 6. Exercise: Implement a basic bidding strategy

def bidding_strategy(bid_request, budget, target_impressions):
    remaining_budget = budget
    remaining_impressions = target_impressions
    
    if remaining_impressions > 0:
        max_bid = remaining_budget / remaining_impressions
        actual_bid = min(max_bid, bid_request["imp"][0]["bidfloor"] * 1.1)  # Bid 10% above floor
        return round(actual_bid, 2)
    else:
        return 0

# Test the bidding strategy
test_request = generate_bid_request()
test_bid = bidding_strategy(test_request, budget=100, target_impressions=1000)
print(f"\nTest bid: ${test_bid}")

# 7. Exercise: Implement bid price adjustments based on user data

def adjust_bid_price(base_bid, user_data):
    if user_data.get("returning_user"):
        base_bid *= 1.2  # Increase bid by 20% for returning users
    if user_data.get("high_value_segment"):
        base_bid *= 1.5  # Increase bid by 50% for high-value segments
    return round(base_bid, 2)

# Test the bid adjustment
test_user_data = {"returning_user": True, "high_value_segment": False}
adjusted_bid = adjust_bid_price(1.0, test_user_data)
print(f"Adjusted bid: ${adjusted_bid}")

# 8. Exercise: Implement basic reporting
import matplotlib.pyplot as plt

def generate_daily_report(auction_results):
    total_impressions = len(auction_results)
    total_spend = sum(bid["price"] for bid in auction_results)
    average_cpm = (total_spend / total_impressions) * 1000
    
    report = {
        "exchange_name": "AdVantageX",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "total_impressions": total_impressions,
        "total_spend": total_spend,
        "average_cpm": average_cpm
    }

    # Visualization for the daily report
    metrics = ["Total Impressions", "Total Spend ($)", "Average CPM ($)"]
    values = [total_impressions, total_spend, average_cpm]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(metrics, values, color=['skyblue', 'lightgreen', 'lightcoral'])

    # Add labels on top of the bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05, round(yval, 2), ha='center', va='bottom')

    plt.title("AdVantageX Daily Report Metrics")
    plt.ylabel("Values")
    plt.ylim(0, max(values) * 1.2)  # Add some space above the tallest bar for the labels
    plt.grid(axis='y', linestyle='--', alpha=0.7)  # Add a grid for better readability
    plt.show()

    return report

# Test the reporting function
daily_report = generate_daily_report(run_simulation(1000)[0])  # Use [0] to get just the auction results
print("\nDaily Report from AdVantageX:")
print(json.dumps(daily_report, indent=2))
