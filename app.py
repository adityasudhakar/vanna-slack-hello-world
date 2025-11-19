import os
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request
from openai import OpenAI

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Initialize Slack app
slack_app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Respond to app mentions only
def format_llm_response(llm_text):
    """
    Convert LLM response to Slack Block Kit format.
    Parses HEADER: prefix for header block, rest becomes mrkdwn body.
    """
    lines = llm_text.strip().split('\n', 1)

    blocks = []

    # Check if first line is a header
    if lines[0].startswith('HEADER:'):
        header_text = lines[0].replace('HEADER:', '').strip()
        blocks.append({
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": header_text
            }
        })
        body_text = lines[1] if len(lines) > 1 else ""
    else:
        # No header, treat everything as body
        body_text = llm_text

    # Add body as mrkdwn section
    if body_text.strip():
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": body_text.strip()
            }
        })

    return {"blocks": blocks}

@slack_app.event("app_mention")
def handle_app_mentions(body, client):
    # Get the user's message and channel
    user_message = body["event"]["text"]
    channel = body["event"]["channel"]

    # Post a placeholder message with typing effect
    placeholder = client.chat_postMessage(
        channel=channel,
        text=":thought_balloon: _Thinking..._"
    )

    # Call OpenAI to generate a response
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """You are a business analyst providing sales and business updates.
Generate fake but realistic sales data and business insights.

Format your response as follows:
- First line: "HEADER: <your title>" (e.g., "HEADER: Weekly Sales Report")
- Rest: Body text using Slack mrkdwn format
  - Use *bold* for emphasis (e.g., *Revenue Growth:* 15%)
  - Use • for bullets
  - Include specific numbers and insights

Example:
HEADER: Q4 2025 Sales Update
Here's this week's performance:

*Revenue:* $2.3M (+12% vs last week)
*Key Wins:*
• Closed 3 enterprise deals worth $450K
• Customer retention improved to 94%
• New product line launched successfully"""
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        max_tokens=500,
        temperature=0.7
    )

    llm_response = response.choices[0].message.content

    # Update the placeholder with the actual response
    client.chat_update(
        channel=channel,
        ts=placeholder["ts"],
        **format_llm_response(llm_response)
    )

# Initialize Flask app
flask_app = Flask(__name__)
handler = SlackRequestHandler(slack_app)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)

@flask_app.route("/", methods=["GET"])
def health_check():
    return "Slack Hello World Bot is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    flask_app.run(host="0.0.0.0", port=port)
