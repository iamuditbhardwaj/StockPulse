def calculate_trend(closing_prices):

    # Input validation
    if not closing_prices:
        raise ValueError("No closing prices available")

    starting_price = closing_prices[0]
    ending_price = closing_prices[-1]

    highest_price = max(closing_prices)
    lowest_price = min(closing_prices)

    price_range = highest_price - lowest_price

    # Determine trend
    if ending_price > starting_price:
        trend = "Uptrend"

    elif ending_price < starting_price:
        trend = "Downtrend"

    else:
        trend = "Sideways"

    return {
        "starting_price": starting_price,
        "ending_price": ending_price,
        "trend": trend,
        "highest_price": highest_price,
        "lowest_price": lowest_price,
        "price_range": price_range
    }

# # Testing
# closing_prices = []

# result = calculate_trend(closing_prices)

# print(result)