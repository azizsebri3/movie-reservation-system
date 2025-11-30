from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.models.reservation import Reservation as ReservationModel
from app.models.showtime import Showtime as ShowtimeModel
from ..utils.seats import generate_seats


def get_all_reservations(db: Session):
    return db.query(ReservationModel).all()

def create_reservation_service(reservation_data, db: Session, user_name: str):
    try:
        # ✅ DÉBUT TRANSACTION
        with db.begin():

            # 1️⃣ Verrouiller la séance
            showtime = db.query(ShowtimeModel).filter(
                ShowtimeModel.id == reservation_data.showtime_id
            ).with_for_update().first()   # ✅ LOCK SQL

            if not showtime:
                raise HTTPException(status_code=404, detail="Showtime not found")

            if showtime.capacity <= 0:
                raise HTTPException(status_code=400, detail="Showtime has no seats configured")

            # 2️⃣ Génération des sièges
            all_seats = generate_seats(showtime.capacity)

            if reservation_data.seat_number not in all_seats:
                raise HTTPException(status_code=400, detail="Seat does not exist in this hall")

            # 3️⃣ Vérifier si le siège est déjà réservé (LOCK aussi)
            reserved = db.query(ReservationModel).filter(
                ReservationModel.showtime_id == reservation_data.showtime_id,
                ReservationModel.seat_number == reservation_data.seat_number,
                ReservationModel.status == "confirmed"
            ).with_for_update().first()   # ✅ LOCK

            if reserved:
                raise HTTPException(status_code=400, detail="Seat already reserved")

            # 4️⃣ Créer la réservation
            db_reservation = ReservationModel(
                **reservation_data.model_dump(),
                user_name=user_name,
                status="confirmed"
            )

            db.add(db_reservation)

        # ✅ COMMIT AUTOMATIQUE ICI (si aucune exception)
        db.refresh(db_reservation)
        return db_reservation

    except Exception:
        db.rollback()  # ✅ Sécurité supplémentaire
        raise

def update_reservation_service(
    reservation_id: int,
    reservation_data,
    db: Session,
    user_name: str
):
    try:
        reservation = (
            db.query(ReservationModel)
            .filter(ReservationModel.id == reservation_id)
            .with_for_update()
            .first()
        )

        if not reservation:
            raise HTTPException(status_code=404, detail="Reservation not found")

        if reservation.user_name != user_name:
            raise HTTPException(status_code=403, detail="Forbidden")

        # 🔒 Lock du showtime aussi (important)
        showtime = (
            db.query(ShowtimeModel)
            .filter(ShowtimeModel.id == reservation.showtime_id)
            .with_for_update()
            .first()
        )

        # ✅ Changement de siège
        if reservation_data.seat_number:
            all_seats = generate_seats(showtime.capacity)

            if reservation_data.seat_number not in all_seats:
                raise HTTPException(status_code=400, detail="Seat does not exist")

            already_reserved = (
                db.query(ReservationModel)
                .filter(
                    ReservationModel.showtime_id == reservation.showtime_id,
                    ReservationModel.seat_number == reservation_data.seat_number,
                    ReservationModel.status == "confirmed",
                    ReservationModel.id != reservation.id
                )
                .with_for_update()
                .first()
            )

            if already_reserved:
                raise HTTPException(status_code=400, detail="Seat already reserved")

            reservation.seat_number = reservation_data.seat_number

        # ✅ Changement de statut
        if reservation_data.status:
            allowed_status = ["confirmed", "cancelled"]

            if reservation_data.status not in allowed_status:
                raise HTTPException(status_code=400, detail="Invalid status")

            reservation.status = reservation_data.status

        db.commit()
        db.refresh(reservation)
        return reservation

    except Exception:
        db.rollback()
        raise


def delete_reservation_service(reservation_id: int, db: Session):
    try:
        with db.begin():

            reservation = (
                db.query(ReservationModel)
                .filter(ReservationModel.id == reservation_id)
                .with_for_update()
                .first()
            )

            if not reservation:
                raise HTTPException(status_code=404, detail="Reservation not found")

            db.delete(reservation)

        return reservation

    except Exception:
        raise

def cancel_reservation_service(reservation_id: int, db: Session):
    try:
        with db.begin():

            reservation = (
                db.query(ReservationModel)
                .filter(ReservationModel.id == reservation_id)
                .with_for_update()
                .first()
            )

            if not reservation:
                raise HTTPException(status_code=404, detail="Reservation not found")

            showtime = (
                db.query(ShowtimeModel)
                .filter(ShowtimeModel.id == reservation.showtime_id)
                .with_for_update()
                .first()
            )

            if not showtime:
                raise HTTPException(status_code=404, detail="Showtime not found")

            if showtime.start_time <= datetime.now(timezone.utc):
                raise HTTPException(status_code=400, detail="Cannot cancel past reservations")

            reservation.status = "cancelled"

        return {"message": "Reservation cancelled successfully", "reservation": reservation}

    except Exception:
        raise
