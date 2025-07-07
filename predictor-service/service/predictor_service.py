from utils.prometheus_utils import query_prometheus
from configuration.config import logger
from datetime import datetime, timezone, timedelta
from utils.prometheus_utils import query_prometheus_range
from statsmodels.tsa.arima.model import ARIMA

def get_average_response_time(minutes):
    
    query = (
        f"avg(rate(flask_http_request_duration_seconds_sum[{minutes}m])) / "
        f"avg(rate(flask_http_request_duration_seconds_count[{minutes}m]))"
    )
    result = query_prometheus(query)

    if not result:
        logger.info("No data returned")
        return {"message": "No data returned", "value": None}

    try:
        avg = float(result[0]['value'][1])
        message = f"Average response time (last {minutes} min)"
        logger.info(message + f"value: {avg}")
        return {"message": message, "value": avg}
    except (IndexError, KeyError, ValueError):
        logger.error("Error parsing result")
        return {"message": "Error parsing result", "value": None}

def get_total_http_requests(minutes):
    query = f'sum(rate(flask_http_request_total[{minutes}m]))'
    result = query_prometheus(query)
    if not result:
        logger.info("No data")
        return {"message": "No data", "value": None}
    try:
        value_per_sec = float(result[0]["value"][1])
        total_requests = int(value_per_sec * 60 * minutes)
        logger.info(f"Total HTTP requests: {total_requests}")
        return {"message": "Total HTTP requests", "value": total_requests}
    except:
        logger.error("Error parsing result")
        return {"message": "Error parsing result", "value": None}


def get_container_memory_usage(container_name):
    query = f'container_memory_usage_bytes{{container_label_com_docker_compose_service="{container_name}"}}'
    result = query_prometheus(query)
    if not result:
        logger.info("No data")
        return {"message": "No data", "value": None}
    try:
        value = float(result[0]["value"][1])
        memory_mb = value / 1_000_000
        logger.info(f"Memory usage of {container_name}: {memory_mb} MB")
        return {"message": f"Memory usage of {container_name}", "value": f"{memory_mb:.2f} MB"}
    except:
        logger.error("Error parsing result")
        return {"message": "Error parsing result", "value": None}

def get_container_start_time(container_name):
    query = f'container_start_time_seconds{{container_label_com_docker_compose_service="{container_name}"}}'
    result = query_prometheus(query)
    if not result:
        logger.info("No data")
        return {"message": "No data", "value": None}
    try:
        value = float(result[0]["value"][1])
        readable_time = datetime.fromtimestamp(value, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f"Start time of {container_name}: {readable_time} UTC")
        return {"message": f"Start time of {container_name}", "value": f"{readable_time} UTC"}
    except:
        logger.error("Error parsing result")
        return {"message": "Error parsing result", "value": None}

def get_network_transmit_errors(container_name):
    query = f'container_network_transmit_errors_total{{container_label_com_docker_compose_service="{container_name}"}}'
    result = query_prometheus(query)
    if not result:
        logger.info("No data")
        return {"message": "No data", "value": None}
    try:
        value = float(result[0]["value"][1])
        logger.info(f"Network errors of {container_name}: {value}")
        return {"message": f"Network errors of {container_name}", "value": value}
    except:
        logger.error("Error parsing result")
        return {"message": "Error parsing result", "value": None}

def get_response_time_series(minutes):
    query = (
        f"rate(flask_http_request_duration_seconds_sum[1m]) / "
        f"rate(flask_http_request_duration_seconds_count[1m])"
    )
    end = int(datetime.now(timezone.utc).timestamp())
    start = int((datetime.now(timezone.utc) - timedelta(minutes=minutes)).timestamp())
    step = 30  

    result = query_prometheus_range(query, start, end, step)
    if not result:
        logger.info("No data retrieved from prometheus.")
        return []

    try:
        values = result[0]['values']
        numeric_values = [float(v[1]) for v in values if v[1] != 'NaN']
        logger.info(f"Data retrieved from prometheus: {[round(val, 2) for val in numeric_values]}")
        return numeric_values
    except (IndexError, KeyError, ValueError):
        return []

def predict_response_time_with_arima(series, steps=10):
    if len(series) < 3:
        logger.info("Not enough data for prediction with ARIMA")
        return {"message": "Not enough data for prediction", "predictions": []}
    
    model = ARIMA(series, order=(2, 1, 2))  # Parametri ARIMA base
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=steps)
    forecast_list = forecast.tolist()
    rounded_forecast = [round(val, 2) for val in forecast_list]
    logger.info(f"Forecast for next {steps} minutes: {rounded_forecast}")
    return {
        "message": f"Forecast for next {steps} minutes",
        "predictions": rounded_forecast
    }