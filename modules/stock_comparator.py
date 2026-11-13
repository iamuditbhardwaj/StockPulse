# Import the existing Performance Analyzer
from modules.performance_analyzer import calculate_performance


# Comparison function
def compare_stocks(symbol1, result1, symbol2, result2):

    return1 = result1["percentage_return"]
    return2 = result2["percentage_return"]

    if return1 > return2:
        better_performer = symbol1

    elif return2 > return1:
        better_performer = symbol2

    else:
        better_performer = "Equal Performance"

    return {
        "stock_1": symbol1,
        "stock_2": symbol2,
        "stock_1_return": return1,
        "stock_2_return": return2,
        "better_performer": better_performer
    }


# # Testing code
# demo1_prices = [108, 112, 115, 109, 118]
# demo2_prices = [205, 212, 215, 209, 218]

# demo1_result = calculate_performance(demo1_prices)
# demo2_result = calculate_performance(demo2_prices)

# comparison = compare_stocks(
#     "DEMO1",
#     demo1_result,
#     "DEMO2",
#     demo2_result
# )

# print(comparison)