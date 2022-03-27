from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from server.cruds.base import CRUDBase, CreateSchemaType
from server.models import Transfer, Player
from server.schemas import TransferCreate, TransferUpdate


class CRUDTransfer(CRUDBase[Transfer, TransferCreate, TransferUpdate]):

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> Transfer:
        """
        Overrides creation method to update user team on creation
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        player = db.query(Player).filter(Player.id == db_obj.player_id).first()
        player.team_id = db_obj.destination_team_id
        db.add(player)
        db.commit()
        db.refresh(db_obj)
        return db_obj


transfer = CRUDTransfer(Transfer)
