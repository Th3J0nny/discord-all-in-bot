class FeaturesInterface:

    # Return if this feature is responsible for the message response
    @staticmethod
    async def get_commands() -> list:
        # Return a list of commands used by this feature (without !)
        raise NotImplementedError

    # Handle messages
    @staticmethod
    async def handle(client, message) -> None:
        # Handle incoming user commands
        raise NotImplementedError
