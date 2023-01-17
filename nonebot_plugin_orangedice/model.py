from nonebot import get_driver
from sqlmodel import Field, SQLModel, create_engine,\
    select, Session

from .config import Config


class Player(SQLModel, table=True):
    user_id: int = Field(primary_key=True)
    skills: str


class GroupLOG(SQLModel, table=True):
    group_id: int = Field(primary_key=True)
    log: bool
    msg: list[str]


class DataContainer:

    def __init__(self) -> None:
        config = Config.parse_obj(get_driver().config)
        self.sqlite_file = config.sqlite_file
        self.cache_player: dict[str, dict[str, int]] = {}
        self.cache_log: dict[str, dict[str, bool]] = {}
        self.engine = create_engine(f"sqlite:///{self.sqlite_file}")
        SQLModel.metadata.create_all(self.engine)

    def get_card(self, user_id: int, default: Player = Player(user_id=123456, skills='')) -> Player:
        with Session(self.engine) as session:
            statement = select(Player).where(Player.user_id == user_id)
            player = session.exec(statement).first()
            if player:
                return player
            return default

    def set_card(self, user_id: int, skills: str):
        with Session(self.engine) as session:
            statement = select(Player).where(Player.user_id == user_id)
            player = session.exec(statement).first()
            if player:
                player.skills = skills
                session.add(player)
            else:
                player = Player(user_id=user_id, skills=skills)
                session.add(player)
            session.commit()

    def delete_card(self, user_id: int):
        with Session(self.engine) as session:
            statement = select(Player).where(Player.user_id == user_id)
            player = session.exec(statement).first()
            if player:
                session.delete(player)
                session.commit()

    def get_log(self, group_id: int, default: GroupLOG = GroupLOG(group_id=123456, log=False, msg=[])) -> GroupLOG:
        with Session(self.engine) as session:
            statement = select(GroupLOG).where(GroupLOG.group_id == group_id)
            log = session.exec(statement).first()
            if log:
                return log
            return default

    def save_log(self, group_id: int, log: bool, msg: list[str]):
        with Session(self.engine) as session:
            statement = select(GroupLOG).where(GroupLOG.group_id == group_id)
            logs = session.exec(statement).first()
            if logs:
                logs.log = log
                logs.msg = msg
                session.add(log)
            else:
                logs = GroupLOG(group_id=group_id, log=log, msg=msg)
                session.add(log)
            session.commit()

    def delete_log(self, group_id: int):
        with Session(self.engine) as session:
            statement = select(GroupLOG).where(GroupLOG.group_id == group_id)
            log = session.exec(statement).first()
            if log:
                session.delete(log)
                session.commit()

    def is_logging(self, group_id: int) -> bool:
        with Session(self.engine) as session:
            statement = select(GroupLOG).where(GroupLOG.group_id == group_id)
            log = session.exec(statement).first()
            if log:
                return log.log
            return False

    def open_log(self, group_id: int):
        with Session(self.engine) as session:
            statement = select(GroupLOG).where(GroupLOG.group_id == group_id)
            log = session.exec(statement).first()
            if log:
                log.log = True
                session.add(log)
            else:
                log = GroupLOG(group_id=group_id, log=True, msg=[])
                session.add(log)
            session.commit()

    def close_log(self, group_id: int):
        with Session(self.engine) as session:
            statement = select(GroupLOG).where(GroupLOG.group_id == group_id)
            log = session.exec(statement).first()
            if log:
                log.log = False
                session.add(log)
            else:
                log = GroupLOG(group_id=group_id, log=False, msg=[])
                session.add(log)
            session.commit()

    def log_add(self, group_id: int, msg: str):
        with Session(self.engine) as session:
            statement = select(GroupLOG).where(GroupLOG.group_id == group_id)
            log = session.exec(statement).first()
            if log:
                log.msg.append(msg)
                session.add(log)
            else:
                log = GroupLOG(group_id=group_id, log=False, msg=[msg])
                session.add(log)
            session.commit()
