from sqlalchemy.orm import Session


class BaseGateway[T]:
    def __init__(self, session: Session) -> None:
        self.session = session
