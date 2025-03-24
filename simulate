import streamlit as st
import numpy as np

def simulate_take_rate(model1, model2, customer_group):
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
    
    base_rate = max(0, min(100, base_rate))  # Ensure within 0-100 range
    return base_rate, 100 - base_rate

st.title("EV Model Take Rate Simulator")

st.sidebar.header("Select Customer Group")
customer_group = st.sidebar.selectbox("Customer Group", ["Family First", "Urban Single", "Grey Hair"])
market = st.sidebar.selectbox("Market", ["Germany", "China", "US"])

st.subheader("Model 1")
brand1 = st.selectbox("Brand", ["Tesla", "BYD", "Nio", "Xpeng", "Lucid"], key='brand1')
bodytype1 = st.selectbox("Body Type", ["Sedan", "SUV"], key='body1')
e_range1 = st.slider("Electric Range (km)", 100, 1500, 500, key='range1')
price1 = st.slider("Price (k USD)", 20, 150, 50, key='price1')
adas1 = st.selectbox("ADAS Level", ["L2", "L3", "L3+"], key='adas1')

st.subheader("Model 2")
brand2 = st.selectbox("Brand", ["Tesla", "BYD", "Nio", "Xpeng", "Lucid"], key='brand2')
bodytype2 = st.selectbox("Body Type", ["Sedan", "SUV"], key='body2')
e_range2 = st.slider("Electric Range (km)", 100, 1500, 500, key='range2')
price2 = st.slider("Price (k USD)", 20, 150, 50, key='price2')
adas2 = st.selectbox("ADAS Level", ["L2", "L3", "L3+"], key='adas2')

if st.button("Simulate Take Rates"):
    model1 = {"brand": brand1, "bodytype": bodytype1, "electric_range": e_range1, "price": price1, "adas": adas1}
    model2 = {"brand": brand2, "bodytype": bodytype2, "electric_range": e_range2, "price": price2, "adas": adas2}
    take_rate1, take_rate2 = simulate_take_rate(model1, model2, customer_group)
    
    st.success(f"Take Rate for Model 1: {take_rate1}%")
    st.success(f"Take Rate for Model 2: {take_rate2}%")
