from flask import Blueprint, jsonify, request
from configuration.config import logger
from service.predictor_service import (get_average_response_time,
                                       get_total_http_requests,
                                       get_container_memory_usage, 
                                       get_container_start_time, 
                                       get_network_transmit_errors,
                                       get_response_time_series, 
                                       predict_response_time_with_arima)

predictor_bp = Blueprint('predictor', __name__)

#white-box -> tempo medio di risposta
@predictor_bp.route('/avg_response_time', methods=['GET'])
def get_average_response_time_prediction():
    logger.info("A new request has arrived to recover the average response time for requests.")
    try:
        minutes = int(request.args.get("minutes", 5))
    except ValueError:
        logger.error("Invalid 'minutes' parameter")
        return jsonify({"error": "Invalid 'minutes' parameter"}), 400

    result = get_average_response_time(minutes)
    return jsonify(result)

#white-box -> totale richieste
@predictor_bp.route('/total_requests', methods=['GET'])
def get_total_requests():
    logger.info("A new request has arrived to recover the total number of requests received.")
    try:
        minutes = int(request.args.get("minutes", 5))
    except ValueError:
        logger.error("Invalid 'minutes' parameter")
        return jsonify({"error": "Invalid 'minutes' parameter"}), 400
    
    result = get_total_http_requests(minutes)
    return jsonify(result)


#black-box -> memoria usata dal container
@predictor_bp.route('/memory_usage', methods=['GET'])
def get_memory_usage():
    container_name = request.args.get("container_name", "api-gateway")
    logger.info(f"A new request has arrived to retrieve the memory value used by the container '{container_name}'.")
    result = get_container_memory_usage(container_name)
    return jsonify(result)

#black-box -> tempo di avvio del container
@predictor_bp.route('/start_time', methods=['GET'])
def get_start_time():
    container_name = request.args.get("container_name", "api-gateway")
    logger.info("A new request has arrived to retrieve the startup time from the '{container_name}' container.")
    result = get_container_start_time(container_name)
    return jsonify(result)

#black-box -> totale errori rete 
@predictor_bp.route('/network_errors', methods=['GET'])
def get_network_errors():
    container_name = request.args.get("container_name", "api-gateway")
    logger.info(f"A new request has arrived to retrieve the total network errors from the '{container_name}' container.")
    result = get_network_transmit_errors(container_name)
    return jsonify(result)

#predittore con ARIMA su tempo medio di risposta
@predictor_bp.route('/predict_response_time', methods=['GET'])
def predict_response_time():
    logger.info(f"A new request has arrived to predict the response time for requests.")
    try:
        steps = int(request.args.get('steps', 5))  # default: 5 minuti
        minutes = int(request.args.get('minutes', 6))
        series = get_response_time_series(minutes)
        if not series:
            logger.error("No data retrieved.")
            return jsonify({"error": "No data retrieved"}), 404

        result = predict_response_time_with_arima(series, steps=steps)
        logger.info(f"Pedict: {result}")
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({"error": "Internal server error"}), 500
