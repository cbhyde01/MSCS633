# Hands-On Assignment 3: Simple Q&A Chatbot

This repository contains a **Django + Python + ChatterBot** terminal chatbot for Advanced AI Assignment 3.

## Project Structure

- `manage.py` - Django command runner
- `chatbot_project/` - Django project settings
- `chatbot/` - Chatbot app with training + terminal command
- `requirements.txt` - Dependency manifest
- `MANIFEST.in` - Packaging manifest

## Setup

1. Create and activate a virtual environment (Python 3.11 recommended).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

If you need to create the exact environment used for this project:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Run Django migrations:

```bash
python manage.py migrate
```

4. Start the terminal chatbot:

```bash
python manage.py chatbot_terminal
```

## Example Interaction

```text
user: Good morning! How are you doing?
bot: I am doing very well, thank you for asking.
user: You're welcome.
bot: Do you like hats?
```

## Notes

- The chatbot is trained on first run and then reuses local trained data.
- Use this terminal output to capture the screenshot required by the assignment.
