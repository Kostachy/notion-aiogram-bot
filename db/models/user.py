from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class User(Base):
    __tablename__ = 'user'

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    db_link: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return "user_id={}, db_link={}".format(self.user_id, self.db_link)
