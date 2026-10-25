
"""Basic pricing utilities for the dynamic-pricing component."""


def calculate_discounted_price(original_price, discount_rate):
    """Calculate a price after applying a discount rate."""
    if original_price < 0:
        raise ValueError("Original price cannot be negative.")

    if not 0 <= discount_rate <= 1:
        raise ValueError("Discount rate must be between 0 and 1.")

    return round(original_price * (1 - discount_rate), 2)


# Candidate discounts to compare in the synthetic pricing simulation.
CANDIDATE_DISCOUNTS = (0.00, 0.05, 0.10, 0.15, 0.20)

# Illustrative product costs as a fraction of original price.
UNIT_COST_RATIOS = {
    "Electronics": 0.60,
    "Clothing": 0.50,
    "Home": 0.55,
    "Beauty": 0.40,
}


def estimate_purchase_probability(
    age, income, past_purchases, product_category, discount_rate
):
    """Estimate purchase probability using the synthetic generator formula."""
    if not 18 <= age <= 70:
        raise ValueError("Age must be between 18 and 70.")

    if income < 0 or past_purchases < 0:
        raise ValueError("Income and past purchases cannot be negative.")

    if not 0 <= discount_rate <= 1:
        raise ValueError("Discount rate must be between 0 and 1.")

    if product_category not in UNIT_COST_RATIOS:
        raise ValueError(f"Unknown product category: {product_category}")

    baseline_log_odds = (
        -2.0
        + 0.025 * (age - 40)
        + 0.000015 * (income - 45000)
        + 0.12 * past_purchases
        + 0.20 * (product_category == "Beauty")
        - 0.15 * (product_category == "Electronics")
    )

    discount_sensitivity = (
        3.0
        + 0.08 * past_purchases
        + 0.00001 * (income - 45000)
    )

    log_odds = baseline_log_odds + discount_sensitivity * discount_rate
    return 1 / (1 + __import__("math").exp(-log_odds))

def calculate_expected_profit(
    original_price,
    age,
    income,
    past_purchases,
    product_category,
    discount_rate,
):
    """Estimate expected profit per customer for a given discount."""
    if original_price <= 0:
        raise ValueError("Original price must be greater than zero.")

    purchase_probability = estimate_purchase_probability(
        age,
        income,
        past_purchases,
        product_category,
        discount_rate,
    )

    discounted_price = calculate_discounted_price(
        original_price, discount_rate
    )

    unit_cost = original_price * UNIT_COST_RATIOS[product_category]
    profit_if_purchased = discounted_price - unit_cost

    return purchase_probability * profit_if_purchased


def compare_candidate_discounts(
    original_price,
    age,
    income,
    past_purchases,
    product_category,
):
    """Compare candidate discounts by expected profit per customer."""
    results = []

    for discount_rate in CANDIDATE_DISCOUNTS:
        expected_profit = calculate_expected_profit(
            original_price=original_price,
            age=age,
            income=income,
            past_purchases=past_purchases,
            product_category=product_category,
            discount_rate=discount_rate,
        )

        results.append({
            "discount_rate": discount_rate,
            "expected_profit": round(expected_profit, 2),
        })

    return sorted(
        results,
        key=lambda result: result["expected_profit"],
        reverse=True,
    )




if __name__ == "__main__":
    results = compare_candidate_discounts(
        original_price=100.00,
        age=30,
        income=40000,
        past_purchases=3,
        product_category="Clothing",
    )

    print("Expected profit by discount:")
    for result in results:
        print(
            f"Discount: {result['discount_rate']:.0%} | "
            f"Expected profit: {result['expected_profit']:.2f}"
        )

    best = results[0]
    print(
        f"\nBest discount for this example: "
        f"{best['discount_rate']:.0%}"
    )
