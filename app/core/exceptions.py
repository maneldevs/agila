class EntityAlreadyExistsError(Exception):

    def __init__(self, message: str = "Entity already exists", *args, **kwargs) -> None:
        self.message = message
        super().__init__(*args, **kwargs)
