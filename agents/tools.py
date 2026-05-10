from langchain_core.tools import tool

@tool
def fetch_user_details(username: str):
    """Fetch user details and permissions"""
    return {"username": username, "department": "Finance", "location": "Mumbai", "role": "Employee", "is_vip": False}

@tool
def fetch_logs(server: str, hours: int = 24):
    """Fetch recent logs for a given server or application"""
    return f"Sample logs from {server}: [ERROR] Connection timeout... [INFO] Reboot initiated..."

@tool
def reset_password(username: str):
    """Reset user password. Highly sensitive. Requires human approval."""
    return f"Password reset link sent to {username}. MFA reset initiated."

@tool
def check_service_status(service_name: str):
    """Check if a service is currently running."""
    return {"service": service_name, "status": "Stopped", "uptime": "0h"}

@tool
def restart_service(service_name: str):
    """Restart a critical service. Highly sensitive. Requires human approval."""
    return f"Service {service_name} restarted successfully."
