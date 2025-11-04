import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Initialize the app with bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Respond to any message event
@app.event("message")
def handle_message_events(body, say, logger):
    # Ignore bot messages to prevent infinite loops
    if body["event"].get("bot_id"):
        return
    
    # Respond with Hello World
    say("Hello World! 👋")

# Respond to app mentions
@app.event("app_mention")
def handle_app_mentions(body, say, logger):
    say("Hello World! 👋")

# Health check endpoint
@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    pass

# Create WSGI app for gunicorn
flask_app = app.to_wsgi_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.start(port=port)
