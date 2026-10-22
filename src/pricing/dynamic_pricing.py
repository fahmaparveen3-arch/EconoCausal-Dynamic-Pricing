
"""Basic pricing utilities for the dynamic-pricing component."""


def calculate_discounted_price(original_price, discount_rate):
    """Calculate a price after applying a discount rate."""
    if original_price < 0:
        raise ValueError("Original price cannot be negative.")

    if not 0 <= discount_rate <= 1:
        raise ValueError("Discount rate must be between 0 and 1.")

    return round(original_price * (1 - discount_rate), 2)


if __name__ == "__main__":
    price = 100.00
    discount = 0.15

    new_price = calculate_discounted_price(price, discount)

    print(f"Original price: {price:.2f}")
    print(f"Discount: {discount:.0%}")
    print(f"Discounted price: {new_price:.2f}")
