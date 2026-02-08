from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.trip import Trip
from app.models.trip_member import TripMember
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
    trip = Trip(name=payload.name, created_by=current_user.id)
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
    admin = (
        db.query(TripMember)
        .filter_by(
            trip_id=trip_id,
            user_id=current_user.id,
            role="ADMIN",
        )
        .first()
    )
    if not admin:
        raise HTTPException(403, "Only ADMIN can invite")

    if db.query(TripMember).filter_by(
        trip_id=trip_id, user_id=payload.user_id
    ).first():
        raise HTTPException(400, "User already a member")

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

    return {"message": "User invited"}


# -------------------------
# Set MY quota
# -------------------------
@router.patch("/{trip_id}/me/quota")
def update_my_quota(
    trip_id: str,
    allocated_bytes: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    member = (
        db.query(TripMember)
        .filter_by(trip_id=trip_id, user_id=current_user.id)
        .first()
    )
    if not member:
        raise HTTPException(403, "Not a trip member")

    if allocated_bytes < member.used_bytes:
        raise HTTPException(400, "Allocated < used")

    member.allocated_bytes = allocated_bytes
    db.commit()

    return {"allocated_bytes": member.allocated_bytes}


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
        .filter_by(trip_id=trip_id, user_id=current_user.id)
        .first()
    )
    if not member:
        raise HTTPException(403, "Not a member")

    if member.used_bytes > 0:
        raise HTTPException(400, "Remove files before leaving")

    if member.role == "ADMIN":
        admin_count = (
            db.query(func.count(TripMember.id))
            .filter_by(trip_id=trip_id, role="ADMIN")
            .scalar()
        )
        if admin_count <= 1:
            raise HTTPException(400, "Cannot leave as last admin")

    db.delete(member)
    db.commit()

    return {"message": "Left trip"}
