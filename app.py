import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


from medications_info import display_info
from timeseries_models import train_arima_model, train_ma_model, train_holt_winters_model

# Load data
data = pd.read_csv('product_dispensation_data_v2.csv')
data['Date'] = pd.to_datetime(data['Date'])

warehouse_df = pd.read_csv('warehouse_data.csv')


# Function to detect sudden increase
def detect_sudden_increase(product_to_analyze, threshold, rolling_window):
    product_data = data[data['Product'] == product_to_analyze]
    product_data['Moving_Avg'] = product_data['Dispensation'].rolling(window=rolling_window, min_periods=1).mean()
    product_data['Dispensation_Diff'] = product_data['Dispensation'] - product_data['Moving_Avg']
    sudden_increase = product_data[product_data['Dispensation_Diff'] > threshold]
    return sudden_increase, product_data

# Streamlit app
st.set_page_config(layout="wide") 

# remove header
st.markdown("""
            <style>
            .st-emotion-cache-zq5wmm
            {
                visibility: hidden;
            }
            .viewerBadge_container__r5tak styles_viewerBadge__CvC9N
            {
                visibility: hidden;
            }
            </style>
            """, unsafe_allow_html = True)


# Company logo
st.image('myverimed logo transparent.png', width=300)

# Title
st.title('Dispensation and Warehouse Stock Monitoring Application')

# Sidebar
st.sidebar.title('Settings')
st.sidebar.header('Historical Analysis')
selected_product = st.sidebar.selectbox('Select Product', data['Product'].unique())
start_date = st.sidebar.date_input('Start Date', min_value=data['Date'].min(), max_value=data['Date'].max())
end_date = st.sidebar.date_input('End Date', min_value=start_date, max_value=data['Date'].max())
rolling_window = st.sidebar.slider('Rolling Window', min_value=0, max_value=30, step=1, value=7)
threshold = 2



# Button to trigger detection
if st.sidebar.button('Detect Sudden Increase'):
    sudden_increase, product_data = detect_sudden_increase(selected_product, threshold, rolling_window)
    
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
        st.write(display_info(selected_product))
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

# Forecasting using selected model

# Dropdown to select forecasting model
st.sidebar.header('Forecast Dispensation')
product_to_forecast = st.sidebar.selectbox('Select Product to forecast', data['Product'].unique())
product_data_to_forecast = data[data['Product'] == product_to_forecast]
selected_model = 'ARIMA'
#selected_model = st.sidebar.selectbox('Select Forecasting Model', ['ARIMA', 'Holt Winters', 'Moving Average'])
forecast_days = st.sidebar.slider('Forecast days', min_value=0, max_value=31, step=1, value=7)
#st.sidebar.subheader('Select rolling window only for Moving Average model')
#moving_avg_rolling_window_to_forecast = st.sidebar.slider('Moving Avg Rolling Window', min_value=0, max_value=30, step=1, value=1)





# Button to trigger analysis and forecasting
if st.sidebar.button('Forecast'):
    forecast = train_arima_model(product_data_to_forecast, forecast_days)
    #if selected_model == 'ARIMA':
    #    forecast = train_arima_model(product_data_to_forecast, forecast_days)
    #elif selected_model == 'Holt Winters':
    #    forecast = train_holt_winters_model(product_data_to_forecast, forecast_days)
    #elif selected_model == 'Moving Average':
    #    forecast = train_ma_model(product_data_to_forecast, moving_avg_rolling_window_to_forecast, forecast_days)
        
     # Round the forecast values
    forecast = [round(value) for value in forecast]

    # Display forecasted values
    st.subheader(f"Forecasted Dispensation for the next *{forecast_days}* Days",
                divider='green')
    forecast_dates = pd.date_range(start=end_date + pd.Timedelta(days=1), periods=forecast_days)
    forecast_df = pd.DataFrame({'Date': forecast_dates, 'Forecast': forecast})
    st.write(forecast_df)
    if selected_model == "Moving Average":
        st.subheader("Note:")
        st.write("The forecasted values are all the same for the selected days because the Moving Average (MA) model simply uses the last computed moving average value as the forecast for all the selected days into the future.")

    # Plot historical data and forecast
    fig, ax = plt.subplots()
    #ax.plot(product_data_to_forecast['Date'], product_data_to_forecast['Dispensation'], label='Historical Dispensation')
    ax.plot(forecast_df['Date'], forecast_df['Forecast'], label='Forecast', linestyle='--', color='red')
    ax.set_xlabel('Date')
    ax.set_ylabel('Dispensation')
    ax.set_title('Historical Dispensation and Forecast')
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






# Load GTIN data
gtin_df = pd.read_csv('GTIN.csv',  encoding='ISO-8859-1')

# Sidebar title and input for GTIN
st.sidebar.title('Check GTIN')
gtin_input = st.sidebar.number_input('GTIN:', value=0)


def check_gtin(gtin):
    result = gtin_df[gtin_df['GTIN'] == gtin]
    if not result.empty:
        st.success("Sender: " + result['Sender'].values[0])
    else:
        st.error("GTIN not found in database.")

# Check if GTIN input is provided and call the function
if gtin_input:
    check_gtin(gtin_input)


