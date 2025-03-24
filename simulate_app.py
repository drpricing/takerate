import numpy as np
import streamlit as st

def simulate_take_rate_with_variability(model1, model2, customer_group, price_stddev=0.05, range_stddev=0.05):
    """Simulate take rates based on predefined logic with customer group preferences and variability."""
    np.random.seed(42)
    base_rate = 50  # Start with an even 50-50 split
    
    # Define customer group preferences (weights)
    customer_group_weights = {
        "Family First": {
            "price": 0.4,  # 40% impact of price
            "electric_range": 0.3,  # 30% impact of electric range
            "brand": 0.1,  # 10% impact of brand
            "adas": 0.2  # 20% impact of ADAS
        },
        "Urban Single": {
            "price": 0.2,
            "electric_range": 0.2,
            "brand": 0.4,
            "adas": 0.2
        },
        "Grey Hair": {
            "price": 0.3,
            "electric_range": 0.3,
            "brand": 0.2,
            "adas": 0.2
        }
    }
    
    # Get the weights for the selected customer group
    weights = customer_group_weights[customer_group]
    
    # Simulate price variation (add random deviation within a given range)
    price_diff = np.random.normal(0, price_stddev * model1['price'])
    model1_price = model1['price'] + price_diff
    model2_price = model2['price'] + price_diff  # We can also add variability to model2's price if needed
    
    # Simulate electric range variation
    range_diff = np.random.normal(0, range_stddev * model1['electric_range'])
    model1_range = model1['electric_range'] + range_diff
    model2_range = model2['electric_range'] + range_diff
    
    # Adjust take rate based on brand
    if model1['brand'] == 'Tesla':
        base_rate += weights["brand"] * 10  # Adjust by weight
    if model2['brand'] == 'Tesla':
        base_rate -= weights["brand"] * 10  # Adjust by weight
    
    # Adjust take rate based on price
    price_diff = model1_price - model2_price
    if price_diff < 0:  # Model 1 is cheaper
        base_rate += weights["price"] * max(0, min(20, abs(price_diff) * 0.1))  # Adjust by weight
    elif price_diff > 0:  # Model 1 is more expensive
        base_rate -= weights["price"] * max(0, min(20, abs(price_diff) * 0.1))  # Adjust by weight
    
    # Adjust take rate based on electric range
    if model1_range > model2_range:
        base_rate += weights["electric_range"] * 5  # Adjust by weight
    elif model1_range < model2_range:
        base_rate -= weights["electric_range"] * 5  # Adjust by weight
    
    # Adjust take rate based on ADAS level
    if model1['adas'] == 'L3+' and model2['adas'] != 'L3+':
        base_rate += weights["adas"] * 5
    elif model2['adas'] == 'L3+' and model1['adas'] != 'L3+':
        base_rate -= weights["adas"] * 5
    
    base_rate = max(0, min(100, base_rate))  # Ensure within 0-100 range
    return base_rate, 100 - base_rate


def run_monte_carlo_simulation(model1, model2, customer_group, n_simulations=1000):
    """Run Monte Carlo simulations to estimate take rate variability."""
    take_rate_model1 = []
    take_rate_model2 = []
    
    for _ in range(n_simulations):
        tr1, tr2 = simulate_take_rate_with_variability(model1, model2, customer_group)
        take_rate_model1.append(tr1)
        take_rate_model2.append(tr2)
    
    # Return results as distributions
    return take_rate_model1, take_rate_model2

# Example usage in Streamlit

st.title("EV Model Take Rate Simulator with Monte Carlo Simulation")

# Inputs
model1 = {"brand": "Tesla", "electric_range": 500, "price": 50, "adas": "L3"}
model2 = {"brand": "BYD", "electric_range": 500, "price": 55, "adas": "L3+"}
customer_group = "Urban Single"

# Run the simulation
take_rate_model1, take_rate_model2 = run_monte_carlo_simulation(model1, model2, customer_group)

# Show the results as histograms or other visualization
st.subheader("Monte Carlo Simulation Results")
st.write(f"Take Rate Distribution for Model 1 (Mean: {np.mean(take_rate_model1):.2f}%)")
st.write(f"Take Rate Distribution for Model 2 (Mean: {np.mean(take_rate_model2):.2f}%)")

# Visualize as a histogram or a distribution chart
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.hist(take_rate_model1, bins=30, alpha=0.5, label="Model 1")
plt.hist(take_rate_model2, bins=30, alpha=0.5, label="Model 2")
plt.legend(loc="upper right")
plt.xlabel("Take Rate (%)")
plt.ylabel("Frequency")
plt.title("Monte Carlo Simulation of Take Rates")
st.pyplot(plt)
