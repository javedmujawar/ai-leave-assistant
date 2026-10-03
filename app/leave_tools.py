import requests
from langchain_core.tools import tool


@tool
def get_leave_balance() -> str:
    """Get the user's current leave balance from the Leave API."""

    response = requests.get("http://127.0.0.1:8000/api/leave/user_1/balance")

    response.raise_for_status()

    data = response.json()

    return str(data)


@tool
def apply_leave(
    user_id: str,
    leave_type: str,
    from_date: str,
    to_date: str,
    reason: str,
) -> str:
    """Apply for casual, sick, or earned leave for a specific user."""

    payload = {
        "leave_type": leave_type,
        "from_date": from_date,
        "to_date": to_date,
        "reason": reason,
    }

    response = requests.post(
        f"http://127.0.0.1:8000/api/leave/{user_id}/apply",
        json=payload,
    )

    response.raise_for_status()

    return str(response.json())
