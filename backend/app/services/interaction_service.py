from sqlalchemy.orm import Session

from app import models
from app.schemas import InteractionCreate


def create_interaction(db: Session, interaction: InteractionCreate) -> models.Interaction:
    db_interaction = models.Interaction(**interaction.model_dump())
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)
    return db_interaction


def list_interactions(db: Session) -> list[models.Interaction]:
    return (
        db.query(models.Interaction)
        .order_by(models.Interaction.created_at.desc())
        .all()
    )

