import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Define take rate model
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

# Run Monte Carlo simulation
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

# Customer group descriptions
customer_group_descriptions = {
    "Family First": "Families looking for spacious, safe, and cost-efficient EVs.",
    "Urban Single": "Young professionals in cities who value technology and design.",
    "Grey Hair": "Older buyers seeking comfort, safety, and reliability."
}

# Streamlit app structure
st.title("EV Model Take Rate Simulator")

tab1, tab2, tab3 = st.tabs(["Simulation", "Monte Carlo Simulation", "Take Rate Model Description"])

with tab1:
    st.sidebar.header("Select Customer Group")
    customer_group = st.sidebar.selectbox("Customer Group", list(customer_group_descriptions.keys()))
    market = st.sidebar.selectbox("Market", ["Germany", "China", "US"])
    st.sidebar.write(f"**Description:** {customer_group_descriptions[customer_group]}")

    def reset_values():
        st.session_state.brand1 = "Tesla"
        st.session_state.body1 = "Sedan"
        st.session_state.range1 = 500
        st.session_state.price1 = 50
        st.session_state.adas1 = "L2"
        st.session_state.brand2 = "BYD"
        st.session_state.body2 = "SUV"
        st.session_state.range2 = 500
        st.session_state.price2 = 50
        st.session_state.adas2 = "L2"

    st.button("Reset", on_click=reset_values)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Model 1")
        brand1 = st.selectbox("Brand", ["Tesla", "BYD", "Nio", "Xpeng", "Lucid"], key='brand1')
        bodytype1 = st.selectbox("Body Type", ["Sedan", "SUV"], key='body1')
        e_range1 = st.slider("Electric Range (km)", 100, 1500, 500, key='range1')
        price1 = st.slider("Price (k USD)", 20, 150, 50, key='price1')
        adas1 = st.selectbox("ADAS Level", ["L2", "L3", "L3+"], key='adas1')

    with col2:
        st.subheader("Model 2")
        brand2 = st.selectbox("Brand", ["Tesla", "BYD", "Nio", "Xpeng", "Lucid"], key='brand2')
        bodytype2 = st.selectbox("Body Type", ["Sedan", "SUV"], key='body2')
        e_range2 = st.slider("Electric Range (km)", 100, 1500, 500, key='range2')
        price2 = st.slider("Price (k USD)", 20, 150, 50, key='price2')
        adas2 = st.selectbox("ADAS Level", ["L2", "L3", "L3+"], key='adas2')

    if st.button("Simulate Take Rates"):
        model1 = {"brand": brand1, "bodytype": bodytype1, "electric_range": e_range1, "price": price1, "adas": adas1}
        model2 = {"brand": brand2, "bodytype": bodytype2, "electric_range": e_range2, "price": price2, "adas": adas2}
        take_rate1, take_rate2 = simulate_take_rate_with_variability(model1, model2, customer_group)
        
        st.success(f"Take Rate for Model 1: {take_rate1}%")
        st.success(f"Take Rate for Model 2: {take_rate2}%")

with tab2:
    st.subheader("Monte Carlo Simulation Results")
    model1 = {"brand": "Tesla", "electric_range": 500, "price": 50, "adas": "L3"}
    model2 = {"brand": "BYD", "electric_range": 500, "price": 55, "adas": "L3+"}
    customer_group = "Urban Single"
    
    # Run the simulation
    take_rate_model1, take_rate_model2 = run_monte_carlo_simulation(model1, model2, customer_group)
    
    st.write(f"Take Rate Distribution for Model 1 (Mean: {np.mean(take_rate_model1):.2f}%)")
    st.write(f"Take Rate Distribution for Model 2 (Mean: {np.mean(take_rate_model2):.2f}%)")

    # Visualize as a histogram
    plt.figure(figsize=(10, 6))
    plt.hist(take_rate_model1, bins=30, alpha=0.5, label="Model 1")
    plt.hist(take_rate_model2, bins=30, alpha=0.5, label="Model 2")
    plt.legend(loc="upper right")
    plt.xlabel("Take Rate (%)")
    plt.ylabel("Frequency")
    plt.title("Monte Carlo Simulation of Take Rates")
    st.pyplot(plt)

with tab3:
    st.subheader("How the Take Rate Model Works")
    st.write("""
    The take rate model simulates the percentage of customers choosing one EV model over another based on various attributes such as:
    - **Brand**: Certain brands, like Tesla, may have a higher influence on take rate.
    - **Price**: The price difference between models affects the take rate, with lower prices generally attracting more customers.
    - **Electric Range**: Customers often prefer models with longer electric ranges.
    - **ADAS Level**: Advanced Driver Assistance Systems (ADAS) can also influence consumer decisions.
    
    Customer group preferences are also taken into account. For example:
    - **Family First**: Values spacious, safe, and cost-effective EVs.
    - **Urban Single**: Prefers trendy, tech-savvy EVs.
    - **Grey Hair**: Seeks comfort and reliability.

    These preferences, combined with the attributes, determine the resulting take rate.
    """)

