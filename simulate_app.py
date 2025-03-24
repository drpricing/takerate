import streamlit as st
import numpy as np

def simulate_take_rate(model1, model2, customer_group, market):
    """Simulate take rates based on predefined logic."""
    np.random.seed(42)
    base_rate = 50  # Start with an even 50-50 split
    
    # Adjust take rate based on attributes
    if model1['brand'] == 'Tesla':
        base_rate += 5
    if model2['brand'] == 'Tesla':
        base_rate -= 5
    
    if model1['price'] < model2['price']:
        base_rate += 10
    elif model1['price'] > model2['price']:
        base_rate -= 10
    
    if model1['electric_range'] > model2['electric_range']:
        base_rate += 5
    elif model1['electric_range'] < model2['electric_range']:
        base_rate -= 5
    
    # Market adjustments
    if market == "Germany":
        base_rate += 2  # A slight preference for local brands in Germany
    elif market == "China":
        base_rate -= 2  # A slight preference for Chinese brands in China
    
    base_rate = max(0, min(100, base_rate))  # Ensure within 0-100 range
    return base_rate, 100 - base_rate

customer_group_descriptions = {
    "Family First": "Families looking for spacious, safe, and cost-efficient EVs.",
    "Urban Single": "Young professionals in cities who value technology and design.",
    "Grey Hair": "Older buyers seeking comfort, safety, and reliability."
}

# Make sure to set a default customer group to prevent access issues
if 'customer_group' not in st.session_state:
    st.session_state.customer_group = "Family First"  # Set a default value

st.title("EV Model Take Rate Simulator")

# Sidebar for Customer Group and Market Selection
st.sidebar.header("Select Customer Group")
customer_group = st.sidebar.selectbox("Customer Group", list(customer_group_descriptions.keys()), index=list(customer_group_descriptions.keys()).index(st.session_state.customer_group))
st.session_state.customer_group = customer_group  # Store the selected customer group
st.sidebar.write(f"**Description:** {customer_group_descriptions[customer_group]}")

st.sidebar.header("Select Market")
market = st.sidebar.selectbox("Market", ["Germany", "China", "US"])

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

# Columns for inputting two models
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

# Simulation button to calculate take rates
if st.button("Simulate Take Rates"):
    model1 = {"brand": brand1, "bodytype": bodytype1, "electric_range": e_range1, "price": price1, "adas": adas1}
    model2 = {"brand": brand2, "bodytype": bodytype2, "electric_range": e_range2, "price": price2, "adas": adas2}
    take_rate1, take_rate2 = simulate_take_rate(model1, model2, customer_group, market)
    
    st.success(f"Take Rate for Model 1: {take_rate1}%")
    st.success(f"Take Rate for Model 2: {take_rate2}%")

    # Display the results in a horizontal bar chart
    st.subheader("Simulation Results")
    st.bar_chart({"Model 1": take_rate1, "Model 2": take_rate2})

# Tabbed interface for additional info
tab1, tab2 = st.tabs(["Simulation", "Take Rate Model Description"])

with tab2:
    st.header("Take Rate Model Description")
    st.markdown("""
    ### Take Rate Model Description

    This model simulates how two electric vehicle (EV) models compete for customer preferences based on key attributes such as **price**, **electric range**, **brand**, and **ADAS (Advanced Driver Assistance Systems)** level. These attributes, along with the selection of a **customer group** and **market**, determine the "take rate" for each model, which reflects the likelihood of customers choosing one model over the other.

    #### Key Components of the Model:
    1. **Price Sensitivity:** The model adjusts the take rates based on the relative price of the two models. A price differential can significantly affect a customer's decision, but the weight of price varies depending on the customer group and market.
       
    2. **Electric Range:** A higher electric range generally increases the attractiveness of an EV. The model adjusts take rates based on this feature, factoring in the customer group's demand for longer range and the market's focus on electric vehicle performance.

    3. **Brand Preference:** Customers have different preferences for certain brands. For instance, Tesla may be more attractive to certain customer groups, while local or less premium brands could appeal to price-sensitive consumers in specific markets.

    4. **ADAS Features:** ADAS (ranging from L2 to L3+ capabilities) plays a growing role in customers' purchasing decisions. The model accounts for how different levels of ADAS influence the take rate, with higher ADAS levels offering a more competitive edge.

    5. **Customer Group Preferences:** The model includes variations in customer behavior based on their type:
       - **Family First:** Focuses on families that prioritize safety, comfort, and affordability.
       - **Urban Single:** A younger, tech-savvy group that values design and technological innovation.
       - **Grey Hair:** Older customers who are more interested in comfort, reliability, and ease of use.

    6. **Market Adjustments:** Different markets (Germany, China, US) have varying degrees of sensitivity to the aforementioned attributes. For example, in Germany, consumers may be more inclined to choose well-established brands, while in China, price might be a more significant factor.

    #### How the Model Works:
    - **Price adjustments** are factored into the take rate based on price differences between the models, but the impact of these adjustments varies depending on customer group preferences and market conditions.
    - **Electric range** is another major factor. The model simulates how a higher range can influence customer decisions, especially for long-distance travel.
    - **Brand** and **ADAS levels** are weighted according to the customer group. For example, urban consumers might place a higher value on modern ADAS features, while families may prioritize safety and reliability.

    To enhance the realism of the simulation, the model also introduces **variability** in the attributes—price and electric range—using a small random deviation. This accounts for factors such as market promotions, price changes, or unforeseen variances in model specifications.

    By running this simulation, users can better understand how each attribute, customer group, and market conditions impact the decision-making process for EV buyers, providing valuable insights into pricing strategies and market positioning.
    """)
