from ai.handlers import OpenRouterHandler


class ChatService:
    def __init__(
        self, handler=OpenRouterHandler, model="openrouter/hunter-alpha"
    ) -> None:
        self.handler = handler()
        self.model = model

    def send_messages(self, messages):
        return self.handler.get_response_with_message_list(messages, self.model)
