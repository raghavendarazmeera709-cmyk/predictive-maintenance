import os
from typing import Any, Dict, List, Optional, Tuple, Union
import requests
import streamlit as st

BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")


def _get_headers(token: Optional[str] = None) -> Dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if not token and hasattr(st, "session_state"):
        token = st.session_state.get("access_token")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def check_api_status() -> bool:
    """Check if the backend FastAPI service is responding."""
    try:
        res = requests.get(f"{BASE_URL}/", timeout=3)
        return res.status_code == 200
    except requests.exceptions.RequestException:
        return False


# ============================================================
# 1. AUTHENTICATION
# ============================================================

def login_user(email: str, password: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Authenticate user with email and password."""
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": email.strip(), "password": password},
            timeout=10,
        )
        if response.status_code == 200:
            return response.json(), None
        error_detail = response.json().get("detail", "Authentication failed.") if response.headers.get("content-type") == "application/json" else "Authentication failed."
        return None, error_detail
    except requests.exceptions.RequestException as e:
        return None, f"Network/Server connection error: {str(e)}"


def register_user(
    full_name: str,
    email: str,
    password: str,
    confirm_password: str,
    phone: Optional[str] = None,
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Register a new operator account."""
    try:
        payload = {
            "full_name": full_name.strip(),
            "email": email.strip(),
            "password": password,
            "confirm_password": confirm_password,
            "phone": phone.strip() if phone else None,
        }
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=payload,
            timeout=10,
        )
        if response.status_code in [200, 201]:
            return response.json(), None
        try:
            err = response.json().get("detail", "Registration failed.")
        except Exception:
            err = f"Registration error (Status {response.status_code})"
        return None, err
    except requests.exceptions.RequestException as e:
        return None, f"Server connection error: {str(e)}"


# ============================================================
# 2. ROBOTIC ASSETS
# ============================================================

def get_robots() -> List[Dict[str, Any]]:
    try:
        response = requests.get(f"{BASE_URL}/robots/", headers=_get_headers(), timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data if isinstance(data, list) else data.get("data", [])
        return []
    except requests.exceptions.RequestException:
        return []


def get_robot(robot_id: int) -> Optional[Dict[str, Any]]:
    try:
        response = requests.get(f"{BASE_URL}/robots/{robot_id}", headers=_get_headers(), timeout=10)
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException:
        return None


def create_robot(data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        response = requests.post(f"{BASE_URL}/robots/", json=data, headers=_get_headers(), timeout=10)
        if response.status_code in [200, 201]:
            return response.json(), None
        return None, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)


def update_robot(robot_id: int, data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        response = requests.put(f"{BASE_URL}/robots/{robot_id}", json=data, headers=_get_headers(), timeout=10)
        if response.status_code == 200:
            return response.json(), None
        return None, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)


def delete_robot(robot_id: int) -> Tuple[bool, str]:
    try:
        response = requests.delete(f"{BASE_URL}/robots/{robot_id}", headers=_get_headers(), timeout=10)
        if response.status_code == 200:
            return True, "Robot deleted successfully"
        return False, response.text
    except requests.exceptions.RequestException as e:
        return False, str(e)


# ============================================================
# 3. SENSOR NETWORK
# ============================================================

def get_sensors() -> List[Dict[str, Any]]:
    try:
        response = requests.get(f"{BASE_URL}/sensors/", headers=_get_headers(), timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data if isinstance(data, list) else data.get("data", [])
        return []
    except requests.exceptions.RequestException:
        return []


def get_sensor(sensor_id: int) -> Optional[Dict[str, Any]]:
    try:
        response = requests.get(f"{BASE_URL}/sensors/{sensor_id}", headers=_get_headers(), timeout=10)
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException:
        return None


def create_sensor(data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        response = requests.post(f"{BASE_URL}/sensors/", json=data, headers=_get_headers(), timeout=10)
        if response.status_code in [200, 201]:
            return response.json(), None
        return None, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)


def update_sensor(sensor_id: int, data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        response = requests.put(f"{BASE_URL}/sensors/{sensor_id}", json=data, headers=_get_headers(), timeout=10)
        if response.status_code == 200:
            return response.json(), None
        return None, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)


def delete_sensor(sensor_id: int) -> Tuple[bool, str]:
    try:
        response = requests.delete(f"{BASE_URL}/sensors/{sensor_id}", headers=_get_headers(), timeout=10)
        if response.status_code == 200:
            return True, "Sensor deleted successfully"
        return False, response.text
    except requests.exceptions.RequestException as e:
        return False, str(e)


# ============================================================
# 4. TELEMETRY & JOINT DATA
# ============================================================

def get_all_telemetry() -> List[Dict[str, Any]]:
    try:
        response = requests.get(f"{BASE_URL}/telemetry/", headers=_get_headers(), timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data if isinstance(data, list) else data.get("data", [])
        return []
    except requests.exceptions.RequestException:
        return []


def get_latest_robot_telemetry(robot_id: int) -> Optional[Dict[str, Any]]:
    try:
        response = requests.get(f"{BASE_URL}/telemetry/robot/{robot_id}/latest", headers=_get_headers(), timeout=10)
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException:
        return None


def get_telemetry(telemetry_id: int) -> Optional[Dict[str, Any]]:
    try:
        response = requests.get(f"{BASE_URL}/telemetry/{telemetry_id}", headers=_get_headers(), timeout=10)
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException:
        return None


def create_telemetry(data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        response = requests.post(f"{BASE_URL}/telemetry/", json=data, headers=_get_headers(), timeout=10)
        if response.status_code in [200, 201]:
            return response.json(), None
        return None, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)


def update_telemetry(telemetry_id: int, data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        response = requests.put(f"{BASE_URL}/telemetry/{telemetry_id}", json=data, headers=_get_headers(), timeout=10)
        if response.status_code == 200:
            return response.json(), None
        return None, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)


def delete_telemetry(telemetry_id: int) -> Tuple[bool, str]:
    try:
        response = requests.delete(f"{BASE_URL}/telemetry/{telemetry_id}", headers=_get_headers(), timeout=10)
        if response.status_code == 200:
            return True, "Telemetry deleted successfully"
        return False, response.text
    except requests.exceptions.RequestException as e:
        return False, str(e)


# ============================================================
# 5. PREDICTIONS & MACHINE LEARNING
# ============================================================

def get_all_predictions() -> List[Dict[str, Any]]:
    try:
        response = requests.get(f"{BASE_URL}/predictions/", headers=_get_headers(), timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data if isinstance(data, list) else data.get("data", [])
        return []
    except requests.exceptions.RequestException:
        return []


def get_prediction(prediction_id: int) -> Optional[Dict[str, Any]]:
    try:
        response = requests.get(f"{BASE_URL}/predictions/{prediction_id}", headers=_get_headers(), timeout=10)
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException:
        return None


def create_prediction(data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        response = requests.post(f"{BASE_URL}/predictions/", json=data, headers=_get_headers(), timeout=10)
        if response.status_code in [200, 201]:
            return response.json(), None
        return None, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)


def predict_protective_stop_ml(sensor_data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Run ML prediction on 20 raw sensor features."""
    try:
        response = requests.post(f"{BASE_URL}/predictions/ml", json=sensor_data, headers=_get_headers(), timeout=15)
        if response.status_code in [200, 201]:
            return response.json(), None
        try:
            return None, response.json().get("detail", response.text)
        except Exception:
            return None, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)


def predict_for_robot(robot_id: int) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Run ML prediction on a robot's latest telemetry."""
    try:
        response = requests.post(f"{BASE_URL}/predictions/robot/{robot_id}", headers=_get_headers(), timeout=15)
        if response.status_code in [200, 201]:
            return response.json(), None
        try:
            return None, response.json().get("detail", f"Error {response.status_code}")
        except Exception:
            return None, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)


def update_prediction(prediction_id: int, data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        response = requests.put(f"{BASE_URL}/predictions/{prediction_id}", json=data, headers=_get_headers(), timeout=10)
        if response.status_code == 200:
            return response.json(), None
        return None, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)


def delete_prediction(prediction_id: int) -> Tuple[bool, str]:
    try:
        response = requests.delete(f"{BASE_URL}/predictions/{prediction_id}", headers=_get_headers(), timeout=10)
        if response.status_code == 200:
            return True, "Prediction deleted successfully"
        return False, response.text
    except requests.exceptions.RequestException as e:
        return False, str(e)


# ============================================================
# 6. MAINTENANCE
# ============================================================

def get_all_maintenance() -> List[Dict[str, Any]]:
    try:
        response = requests.get(f"{BASE_URL}/maintenance/", headers=_get_headers(), timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data if isinstance(data, list) else data.get("data", [])
        return []
    except requests.exceptions.RequestException:
        return []


def get_maintenance(maintenance_id: int) -> Optional[Dict[str, Any]]:
    try:
        response = requests.get(f"{BASE_URL}/maintenance/{maintenance_id}", headers=_get_headers(), timeout=10)
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException:
        return None


def create_maintenance(data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        response = requests.post(f"{BASE_URL}/maintenance/", json=data, headers=_get_headers(), timeout=10)
        if response.status_code in [200, 201]:
            return response.json(), None
        return None, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)


def update_maintenance(maintenance_id: int, data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        response = requests.put(f"{BASE_URL}/maintenance/{maintenance_id}", json=data, headers=_get_headers(), timeout=10)
        if response.status_code == 200:
            return response.json(), None
        return None, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)


def delete_maintenance(maintenance_id: int) -> Tuple[bool, str]:
    try:
        response = requests.delete(f"{BASE_URL}/maintenance/{maintenance_id}", headers=_get_headers(), timeout=10)
        if response.status_code == 200:
            return True, "Maintenance record deleted successfully"
        return False, response.text
    except requests.exceptions.RequestException as e:
        return False, str(e)


# ============================================================
# 7. INCIDENTS
# ============================================================

def get_all_incidents() -> List[Dict[str, Any]]:
    try:
        response = requests.get(f"{BASE_URL}/incidents/", headers=_get_headers(), timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data if isinstance(data, list) else data.get("data", [])
        return []
    except requests.exceptions.RequestException:
        return []


def get_incident(incident_id: int) -> Optional[Dict[str, Any]]:
    try:
        response = requests.get(f"{BASE_URL}/incidents/{incident_id}", headers=_get_headers(), timeout=10)
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException:
        return None


def create_incident(data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        response = requests.post(f"{BASE_URL}/incidents/", json=data, headers=_get_headers(), timeout=10)
        if response.status_code in [200, 201]:
            return response.json(), None
        return None, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)


def update_incident(incident_id: int, data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        response = requests.put(f"{BASE_URL}/incidents/{incident_id}", json=data, headers=_get_headers(), timeout=10)
        if response.status_code == 200:
            return response.json(), None
        return None, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)


def delete_incident(incident_id: int) -> Tuple[bool, str]:
    try:
        response = requests.delete(f"{BASE_URL}/incidents/{incident_id}", headers=_get_headers(), timeout=10)
        if response.status_code == 200:
            return True, "Incident deleted successfully"
        return False, response.text
    except requests.exceptions.RequestException as e:
        return False, str(e)


# ============================================================
# 8. NOTIFICATIONS & ALERTS
# ============================================================

def get_all_notifications() -> List[Dict[str, Any]]:
    try:
        response = requests.get(f"{BASE_URL}/notifications/", headers=_get_headers(), timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data if isinstance(data, list) else data.get("data", [])
        return []
    except requests.exceptions.RequestException:
        return []


def get_notification(notification_id: int) -> Optional[Dict[str, Any]]:
    try:
        response = requests.get(f"{BASE_URL}/notifications/{notification_id}", headers=_get_headers(), timeout=10)
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException:
        return None


def create_notification(data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        response = requests.post(f"{BASE_URL}/notifications/", json=data, headers=_get_headers(), timeout=10)
        if response.status_code in [200, 201]:
            return response.json(), None
        return None, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)


def update_notification(notification_id: int, data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        response = requests.put(f"{BASE_URL}/notifications/{notification_id}", json=data, headers=_get_headers(), timeout=10)
        if response.status_code == 200:
            return response.json(), None
        return None, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)


def delete_notification(notification_id: int) -> Tuple[bool, str]:
    try:
        response = requests.delete(f"{BASE_URL}/notifications/{notification_id}", headers=_get_headers(), timeout=10)
        if response.status_code == 200:
            return True, "Notification deleted successfully"
        return False, response.text
    except requests.exceptions.RequestException as e:
        return False, str(e)


# ============================================================
# 9. USERS & OPERATORS
# ============================================================

def get_all_users() -> List[Dict[str, Any]]:
    try:
        response = requests.get(f"{BASE_URL}/users/", headers=_get_headers(), timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data if isinstance(data, list) else data.get("data", [])
        return []
    except requests.exceptions.RequestException:
        return []


def get_user(user_id: int) -> Optional[Dict[str, Any]]:
    try:
        response = requests.get(f"{BASE_URL}/users/{user_id}", headers=_get_headers(), timeout=10)
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException:
        return None


def create_user(data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        response = requests.post(f"{BASE_URL}/users/", json=data, headers=_get_headers(), timeout=10)
        if response.status_code in [200, 201]:
            return response.json(), None
        return None, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)


def update_user(user_id: int, data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        response = requests.put(f"{BASE_URL}/users/{user_id}", json=data, headers=_get_headers(), timeout=10)
        if response.status_code == 200:
            return response.json(), None
        return None, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)


def delete_user(user_id: int) -> Tuple[bool, str]:
    try:
        response = requests.delete(f"{BASE_URL}/users/{user_id}", headers=_get_headers(), timeout=10)
        if response.status_code == 200:
            return True, "User deleted successfully"
        return False, response.text
    except requests.exceptions.RequestException as e:
        return False, str(e)


# ============================================================
# 10. HEALTH MONITORING
# ============================================================

def get_robot_health(robot_id: int) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Calculate real-time health score for a robot."""
    try:
        response = requests.post(
            f"{BASE_URL}/health/",
            json={"robot_id": robot_id},
            headers=_get_headers(),
            timeout=10,
        )
        if response.status_code == 200:
            return response.json(), None
        try:
            return None, response.json().get("detail", f"Error {response.status_code}")
        except Exception:
            return None, response.text
    except requests.exceptions.RequestException as e:
        return None, str(e)