class EntityAlreadyExistsError(Exception):

    def __init__(self, message: str = "Entity already exists", *args, **kwargs) -> None:
        self.message = message
        self.status_code = 400
        super().__init__(*args, **kwargs)
