from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.trip import Trip
from app.models.trip_member import TripMember
from app.models.user_cloud_account import UserCloudAccount
from app.schemas.trip import TripCreate, TripRead
from app.schemas.trip_invite import TripInviteRequest

router = APIRouter(prefix="/trips", tags=["trips"])


# -------------------------
# Create Trip
# -------------------------
@router.post("", response_model=TripRead)
def create_trip(
    payload: TripCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    trip = Trip(
        name=payload.name,
        created_by=current_user.id,
    )
    db.add(trip)
    db.flush()

    db.add(
        TripMember(
            trip_id=trip.id,
            user_id=current_user.id,
            role="ADMIN",
            allocated_bytes=0,
            used_bytes=0,
        )
    )

    db.commit()
    db.refresh(trip)
    return trip


# -------------------------
# List My Trips
# -------------------------
@router.get("", response_model=list[TripRead])
def list_my_trips(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(Trip)
        .join(TripMember)
        .filter(TripMember.user_id == current_user.id)
        .all()
    )


# -------------------------
# Invite Member (NO quota)
# -------------------------
@router.post("/{trip_id}/invite")
def invite_member(
    trip_id: str,
    payload: TripInviteRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    inviter = (
        db.query(TripMember)
        .filter(
            TripMember.trip_id == trip_id,
            TripMember.user_id == current_user.id,
            TripMember.role == "ADMIN",
        )
        .first()
    )

    if not inviter:
        raise HTTPException(
            status_code=403,
            detail="Only ADMIN can invite members",
        )

    invitee = db.get(User, payload.user_id)
    if not invitee:
        raise HTTPException(404, "User not found")

    existing = (
        db.query(TripMember)
        .filter(
            TripMember.trip_id == trip_id,
            TripMember.user_id == payload.user_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(400, "User already a trip member")

    db.add(
        TripMember(
            trip_id=trip_id,
            user_id=payload.user_id,
            role="MEMBER",
            allocated_bytes=0,
            used_bytes=0,
        )
    )
    db.commit()

    return {"message": "User invited successfully"}


# -------------------------
# Set MY quota (self-managed)
# -------------------------
@router.patch("/{trip_id}/me/quota")
def update_my_quota(
    trip_id: str,
    allocated_bytes: int = Query(..., gt=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    member = (
        db.query(TripMember)
        .filter(
            TripMember.trip_id == trip_id,
            TripMember.user_id == current_user.id,
        )
        .first()
    )

    if not member:
        raise HTTPException(404, "Not a trip member")

    account = (
        db.query(UserCloudAccount)
        .filter(
            UserCloudAccount.user_id == current_user.id,
            UserCloudAccount.provider == "google_drive",
        )
        .first()
    )

    if not account:
        raise HTTPException(
            status_code=400,
            detail="Link Google Drive before contributing storage",
        )

    if allocated_bytes < member.used_bytes:
        raise HTTPException(
            status_code=400,
            detail="Allocated bytes cannot be less than used bytes",
        )

    member.allocated_bytes = allocated_bytes
    db.commit()

    return {
        "trip_id": trip_id,
        "allocated_bytes": allocated_bytes,
    }


# -------------------------
# Leave Trip
# -------------------------
@router.post("/{trip_id}/leave")
def leave_trip(
    trip_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    member = (
        db.query(TripMember)
        .filter(
            TripMember.trip_id == trip_id,
            TripMember.user_id == current_user.id,
        )
        .first()
    )

    if not member:
        raise HTTPException(403, "Not a member")

    if member.used_bytes > 0:
        raise HTTPException(400, "Remove files before leaving")

    if member.role == "ADMIN":
        admin_count = (
            db.query(func.count(TripMember.id))
            .filter(
                TripMember.trip_id == trip_id,
                TripMember.role == "ADMIN",
            )
            .scalar()
        )

        if admin_count <= 1:
            raise HTTPException(400, "Cannot leave as last admin")

    db.delete(member)
    db.commit()

    return {"message": "Left trip"}
