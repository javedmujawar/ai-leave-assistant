from fastapi import APIRouter, HTTPException

from app.schemas.leave import (
    LeaveApplication,
    LeaveCancellation,
)

from app.services.leave_service import (
    apply_leave,
    cancel_leave,
    get_leave_balance,
    get_leave_history,
)


router = APIRouter(
    prefix="/api/leave",
    tags=["Leave"]
)


@router.get("/{user_id}/balance")
def leave_balance(user_id: str):
    try:
        return get_leave_balance(user_id)
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.get("/{user_id}/history")
def leave_history(user_id: str):
    try:
        return get_leave_history(user_id)
    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )


@router.post("/{user_id}/apply")
def apply_leave_route(
    user_id: str,
    request: LeaveApplication
):
    try:
        return apply_leave(user_id, request)
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.post("/{user_id}/cancel")
def cancel_leave_route(
    user_id: str,
    request: LeaveCancellation
):
    try:
        return cancel_leave(user_id, request.leave_id)
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )