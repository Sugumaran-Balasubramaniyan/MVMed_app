import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.holtwinters import SimpleExpSmoothing



# Function to train ARIMA model and generate forecast
def train_arima_model(data, forecast_days):
    # Prepare data for ARIMA
    product_data = data.copy()
    product_data.set_index('Date', inplace=True)
    
    # Fit ARIMA model
    model = ARIMA(product_data['Dispensation'], order=(5,1,0))
    model_fit = model.fit()
    
    # Forecast for next selected days
    forecast = model_fit.forecast(steps=forecast_days)
    
    return forecast

# Function to train SARIMA model and generate forecast
def train_sarima_model(data, forecast_days):
    # Prepare data for SARIMA
    product_data = data.copy()
    product_data.set_index('Date', inplace=True)
    
    # Fit SARIMA model
    model = SARIMAX(product_data['Dispensation'], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    model_fit = model.fit()
    
    # Forecast for next selected days
    forecast = model_fit.forecast(steps=forecast_days)
    
    return forecast

# Function to train Holt Winters model and generate forecast
def train_holt_winters_model(data, forecast_days):
    # Prepare data for Holt Winters
    product_data = data.copy()
    product_data.set_index('Date', inplace=True)
    
    # Fit Holt Winters model
    model = ExponentialSmoothing(product_data['Dispensation'], seasonal_periods=12, trend='add', seasonal='add')
    model_fit = model.fit()
    
    # Forecast for next selected days
    forecast = model_fit.forecast(steps=forecast_days)
    
    return forecast



def train_ma_model(data, rolling_window, forecast_days):
    """
    Train Moving Average (MA) model and return forecasted values for the next selected days.
    
    Parameters:
        data (pd.DataFrame): Historical dispensation data with 'Date' and 'Dispensation' columns.
        rolling_window (int): Size of the rolling window for calculating the moving average.
        
    Returns:
        np.array: Forecasted values for the next selected days.
    """
    # Calculate moving average
    moving_avg = data['Dispensation'].rolling(window=rolling_window, min_periods=1).mean()
    
    # Use the last value as the forecast for the next selected days
    last_value = moving_avg.iloc[-1]
    forecast = np.full(forecast_days, last_value)
    
    return forecast

