"""ChatBot setup and training utilities."""

from pathlib import Path

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer


def initialize_chatbot() -> ChatBot:
    """
    Create and optionally train the chatbot.

    Training is done only on first run to keep subsequent launches fast.
    """
    data_dir = Path(__file__).resolve().parent.parent / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    trained_flag = data_dir / "trained.flag"
    db_path = data_dir / "chatbot_storage.sqlite3"

    bot = ChatBot(
        "AssignmentBot",
        storage_adapter="chatterbot.storage.SQLStorageAdapter",
        logic_adapters=[
            "chatterbot.logic.BestMatch",
        ],
        database_uri=f"sqlite:///{db_path}",
    )

    if not trained_flag.exists():
        # Train with both corpus data and a short custom conversation list.
        corpus_trainer = ChatterBotCorpusTrainer(bot)
        corpus_trainer.train("chatterbot.corpus.english.greetings")
        corpus_trainer.train("chatterbot.corpus.english.conversations")

        list_trainer = ListTrainer(bot)
        list_trainer.train(
            [
                "Good morning! How are you doing?",
                "I am doing very well, thank you for asking.",
                "You're welcome.",
                "Do you like hats?",
                "What is your name?",
                "I am AssignmentBot, your class chatbot.",
                "What can you do?",
                "I can answer simple questions in this terminal chat.",
                "bye",
                "Goodbye! Have a great day.",
            ]
        )

        trained_flag.write_text("trained\n", encoding="utf-8")

    return bot
