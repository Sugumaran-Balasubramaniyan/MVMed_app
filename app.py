import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
data = pd.read_csv('product_dispensation_data.csv')
data['Date'] = pd.to_datetime(data['Date'])

warehouse_df = pd.read_csv('warehouse_data.csv')

# Function to detect sudden increase
def detect_sudden_increase(product_to_analyze, threshold):
    product_data = data[data['Product'] == product_to_analyze]
    product_data['Moving_Avg'] = product_data['Dispensation'].rolling(window=7, min_periods=1).mean()
    product_data['Dispensation_Diff'] = product_data['Dispensation'] - product_data['Moving_Avg']
    sudden_increase = product_data[product_data['Dispensation_Diff'] > threshold]
    return sudden_increase, product_data

# Streamlit app
st.set_page_config(layout="wide") 

# Company logo
st.image('myverimed logo transparent.png', width=300)

# Title
st.title('Dispensation and Warehouse Stock Monitoring Application')

# Sidebar
st.sidebar.title('Settings')
selected_product = st.sidebar.selectbox('Select Product', data['Product'].unique())
start_date = st.sidebar.date_input('Start Date', min_value=data['Date'].min(), max_value=data['Date'].max())
end_date = st.sidebar.date_input('End Date', min_value=start_date, max_value=data['Date'].max())
# threshold = st.sidebar.slider('Threshold', min_value=0, max_value=10, step=1, value=2)
threshold = 2

# Button to trigger detection
if st.sidebar.button('Detect Sudden Increase'):
    sudden_increase, product_data = detect_sudden_increase(selected_product, threshold)
    
    # Convert start and end dates to pandas Timestamp objects
    start_date = pd.Timestamp(start_date)
    end_date = pd.Timestamp(end_date)
    
    # Filter product data based on selected date range
    filtered_data = product_data.loc[(product_data['Date'] >= start_date) & (product_data['Date'] <= end_date)]

    # Filter sudden increase data within the selected date range
    sudden_increase_filtered = sudden_increase.loc[(sudden_increase['Date'] >= start_date) & (sudden_increase['Date'] <= end_date)]

    # Display result
    if not sudden_increase_filtered.empty:
        st.warning(f"Alert: Sudden increase in dispensation of {selected_product} detected!")
        st.dataframe(sudden_increase_filtered)
    else:
        st.info(f"No sudden increase in dispensation of {selected_product} detected within the specified date range.")
    
    # Plot
    fig, ax = plt.subplots()
    ax.plot(filtered_data['Date'], filtered_data['Dispensation'], label='Dispensation')
    ax.plot(filtered_data['Date'], filtered_data['Moving_Avg'], label='Moving Average', linestyle='--', color='red')
    
    for idx, row in sudden_increase_filtered.iterrows():
        ax.scatter(row['Date'], row['Dispensation'], color='red', marker='o')
        
    ax.set_xlabel('Date')
    ax.set_ylabel('Dispensation')
    ax.set_title('Dispensation Trend')
    ax.legend()
    # Rotate x-axis labels vertically
    plt.xticks(rotation=90)
    st.pyplot(fig)

# Set minimum stock levels
st.sidebar.title('Set Minimum Stock Levels')
min_stock_levels = {}
for warehouse in warehouse_df['Warehouse'].unique():
    min_stock_levels[warehouse] = st.sidebar.number_input(f'Min Stock Level for {warehouse}', min_value=0)

# Button to trigger analysis
if st.sidebar.button('Analyze Stock Levels'):
    warehouse_df['Below Minimum'] = warehouse_df['Stock Level'] < warehouse_df['Warehouse'].map(min_stock_levels)
    
    st.subheader('Warehouse Stock Levels')
    st.dataframe(warehouse_df.style.apply(lambda x: ['background: lightcoral' if x['Below Minimum'] else '' for _ in x], axis=1))
    
    st.subheader('Summary of Deficiencies')
    for warehouse in warehouse_df['Warehouse'].unique():
        deficiency_count = warehouse_df[(warehouse_df['Warehouse'] == warehouse) & (warehouse_df['Below Minimum'])].shape[0]
        st.write(f"{warehouse}: {deficiency_count} product(s) below minimum stock level")



