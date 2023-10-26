class SqlDB:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    def exists(self) -> bool:
        pass

    def query(self) -> dict:
        pass
