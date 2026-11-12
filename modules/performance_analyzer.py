def calculate_performance(closing_prices):

    # Input validation
    if not closing_prices:
        raise ValueError("No closing prices available")

    if closing_prices[0] == 0:
        raise ValueError("Starting price cannot be zero")

    starting_price = closing_prices[0]
    ending_price = closing_prices[-1]

    highest_price = max(closing_prices)
    lowest_price = min(closing_prices)

    average_price = sum(closing_prices) / len(closing_prices)

    price_change = ending_price - starting_price

    percentage_return = (price_change / starting_price) * 100

    return {
        "starting_price": starting_price,
        "ending_price": ending_price,
        "highest_price": highest_price,
        "lowest_price": lowest_price,
        "average_price": round(average_price, 2),
        "price_change": round(price_change, 2),
        "percentage_return": round(percentage_return, 2)
    }

