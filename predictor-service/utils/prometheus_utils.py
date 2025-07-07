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

def query_prometheus_range(query, start, end, step):
    try:
        response = requests.get(
            f"{PROMETHEUS_BASE_URL}/api/v1/query_range",
            params={
                "query": query,
                "start": start,
                "end": end,
                "step": step
            }
        )
        response.raise_for_status()
        result = response.json()
        return result.get("data", {}).get("result", [])
    except requests.exceptions.RequestException as e:
        print(f"Prometheus range query error: {e}")
        return []
