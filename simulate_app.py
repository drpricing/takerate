def simulate_take_rate(model1, model2, customer_group):
    """Simulate take rates based on predefined logic with customer group preferences."""
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
    
    # Adjust take rate based on brand
    if model1['brand'] == 'Tesla':
        base_rate += weights["brand"] * 10  # Adjust by weight
    if model2['brand'] == 'Tesla':
        base_rate -= weights["brand"] * 10  # Adjust by weight
    
    # Adjust take rate based on price
    price_diff = model1['price'] - model2['price']
    if price_diff < 0:  # Model 1 is cheaper
        base_rate += weights["price"] * max(0, min(20, abs(price_diff) * 0.1))  # Adjust by weight
    elif price_diff > 0:  # Model 1 is more expensive
        base_rate -= weights["price"] * max(0, min(20, abs(price_diff) * 0.1))  # Adjust by weight
    
    # Adjust take rate based on electric range
    if model1['electric_range'] > model2['electric_range']:
        base_rate += weights["electric_range"] * 5  # Adjust by weight
    elif model1['electric_range'] < model2['electric_range']:
        base_rate -= weights["electric_range"] * 5  # Adjust by weight
    
    # Adjust take rate based on ADAS level
    if model1['adas'] == 'L3+' and model2['adas'] != 'L3+':
        base_rate += weights["adas"] * 5
    elif model2['adas'] == 'L3+' and model1['adas'] != 'L3+':
        base_rate -= weights["adas"] * 5
    
    base_rate = max(0, min(100, base_rate))  # Ensure within 0-100 range
    return base_rate, 100 - base_rate
