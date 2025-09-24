
# Calculate discounted price from given price and discount (%)
def calculateDiscount(price, discountPercent):
    
    try:
        # If price is negitive. throw error
        if (price < 0):
            raise ValueError("price must be non-negative")

        # If discount is not in the range of 0-100. then error
        if not (0 <= discountPercent <= 100):
            raise ValueError("discountPercent must be between 0 and 100")

        # No exeption. so calc discount
        return price * (1 - discountPercent / 100)

    # Test if price and discount are both numbers
    except TypeError as exc:
        raise TypeError("price and discountPercent must be numeric") from exc

