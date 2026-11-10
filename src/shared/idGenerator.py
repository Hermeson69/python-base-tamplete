from uuid import uuid4


class IDGenerator:
    """
    A utility class for generating unique IDs.

    Methods:
        generate_id: Generates a unique ID using UUID4.
        generate_user_id: Generates a unique user ID prefixed with 'user_'.
    """

    @staticmethod
    def generate_id() -> str:
        """
        Generates a unique ID using UUID4.
        """
        return str(uuid4())

    @staticmethod
    def generate_user_id() -> str:
        """
        Generates a unique user ID prefixed with 'user_'.
        """
        return f"user_{IDGenerator.generate_id()}"