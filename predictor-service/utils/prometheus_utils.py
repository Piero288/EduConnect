import requests
from configuration.config import PROMETHEUS_BASE_URL

def query_prometheus(query):
    try:
        response = requests.get(f"{PROMETHEUS_BASE_URL}/api/v1/query", params={"query": query})
        response.raise_for_status()
        result = response.json()
        return result.get("data", {}).get("result", [])
    except requests.exceptions.RequestException as e:
        print(f"Prometheus query error: {e}")
        return []
