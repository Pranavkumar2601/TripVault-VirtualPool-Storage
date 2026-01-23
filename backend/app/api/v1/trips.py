from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.trip import Trip
from app.models.trip_member import TripMember
from app.schemas.trip import TripCreate, TripRead
from app.schemas.trip_invite import TripInviteRequest

router = APIRouter(prefix="/trips", tags=["trips"])


@router.post("", response_model=TripRead)
def create_trip(
    payload: TripCreate,
    user_id: str = Query(..., description="Current user ID"),
    db: Session = Depends(get_db),
):
    # 1. Create trip
    trip = Trip(
        name=payload.name,
        created_by=user_id,
    )
    db.add(trip)
    db.flush()  # get trip.id without committing yet

    # 2. Add creator as ADMIN member
    member = TripMember(
        trip_id=trip.id,
        user_id=user_id,
        role="ADMIN",
        allocated_bytes=0,
        used_bytes=0,
    )
    db.add(member)

    db.commit()
    db.refresh(trip)

    return trip

@router.get("", response_model=list[TripRead])
def list_user_trips(
    user_id: str = Query(..., description="Current user ID"),
    db: Session = Depends(get_db),
):
    return (
        db.query(Trip)
        .join(TripMember)
        .filter(TripMember.user_id == user_id)
        .all()
    )


# //trip TripInviteRequest
@router.post("/{trip_id}/invite")
def invite_member(
    trip_id: str,
    payload: TripInviteRequest,
    inviter_user_id: str = Query(..., description="Inviter user ID"),
    db: Session = Depends(get_db),
):
    # 1. Check inviter is ADMIN
    inviter = (
        db.query(TripMember)
        .filter(
            TripMember.trip_id == trip_id,
            TripMember.user_id == inviter_user_id,
            TripMember.role == "ADMIN",
        )
        .first()
    )

    if not inviter:
        raise HTTPException(
            status_code=403,
            detail="Only ADMIN can invite members"
        )

    # 2. Check invitee exists
    invitee = db.query(User).filter(User.id == payload.user_id).first()
    if not invitee:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # 3. Prevent duplicate membership
    existing = (
        db.query(TripMember)
        .filter(
            TripMember.trip_id == trip_id,
            TripMember.user_id == payload.user_id,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="User already a trip member"
        )

    # 4. Add new MEMBER
    member = TripMember(
        trip_id=trip_id,
        user_id=payload.user_id,
        role="MEMBER",
        allocated_bytes=payload.allocated_bytes,
        used_bytes=0,
    )

    db.add(member)
    db.commit()

    return {"message": "User invited successfully"}
