from app.schemas.leave import LeaveApplication
from app.store.leave_store import users


def get_user(user_id: str):
    user = users.get(user_id)

    if user is None:
        raise ValueError("User not found")

    return user


def get_leave_balance(user_id: str):
    user = get_user(user_id)

    return user["leave_balances"]


def get_leave_history(user_id: str):
    user = get_user(user_id)

    return user["leave_history"]


def apply_leave(user_id: str, request: LeaveApplication):
    user = get_user(user_id)

    days = (request.to_date - request.from_date).days + 1

    balance = user["leave_balances"]

    if balance[request.leave_type] < days:
        raise ValueError("Insufficient leave balance")

    balance[request.leave_type] -= days

    history = user["leave_history"]

    leave = {
        "id": len(history) + 1,
        "leave_type": request.leave_type,
        "from_date": request.from_date,
        "to_date": request.to_date,
        "reason": request.reason,
        "days": days,
        "status": "pending"
    }

    history.append(leave)

    return leave


def cancel_leave(user_id: str, leave_id: int):
    user = get_user(user_id)

    leave = next(
        (item for item in user["leave_history"]
         if item["id"] == leave_id),
        None
    )

    if leave is None:
        raise ValueError("Leave not found")

    if leave["status"] == "cancelled":
        raise ValueError("Leave already cancelled")

    leave["status"] = "cancelled"

    user["leave_balances"][leave["leave_type"]] += leave["days"]

    return leave