"""Django management command that runs a terminal chatbot client."""

from django.core.management.base import BaseCommand

from chatbot.chatbot_engine import initialize_chatbot


class Command(BaseCommand):
    help = "Run a terminal-based Q&A chatbot using ChatterBot."

    def handle(self, *args, **options):
        bot = initialize_chatbot()

        self.stdout.write(self.style.SUCCESS("Chatbot is ready."))
        self.stdout.write("Type 'exit', 'quit', or 'bye' to end the chat.\n")

        while True:
            user_text = input("user: ").strip()

            if user_text.lower() in {"exit", "quit", "bye"}:
                self.stdout.write("bot: Goodbye! Have a great day.")
                break

            # Get a response from the trained chatbot.
            response = bot.get_response(user_text)
            self.stdout.write(f"bot: {response}")
