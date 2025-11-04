# Slack Hello World Bot (Python)

A simple Slack bot built with Python and `slack-bolt` that responds with "Hello World! 👋" to any message.

## Why Python?

- **Simpler code**: The `slack-bolt` framework handles most of the complexity
- **Less boilerplate**: No manual request verification needed
- **Official Slack SDK**: Built and maintained by Slack
- **Easy to extend**: Clean, readable Python code

## Setup Instructions

### 1. Deploy to Railway

1. Push this code to a GitHub repository
2. Go to [Railway](https://railway.app/) and create a new project
3. Select "Deploy from GitHub repo" and choose your repository
4. Railway will automatically detect the Python app and deploy it
5. Once deployed, copy your Railway app URL (e.g., `https://your-app.up.railway.app`)

### 2. Create Slack App

1. Go to [https://api.slack.com/apps](https://api.slack.com/apps)
2. Click "Create New App"
3. Choose "From an app manifest"
4. Select your workspace
5. Copy the contents of `slack-manifest.yml`
6. **Important**: Replace `YOUR_RAILWAY_URL` with your actual Railway URL in the manifest
7. Paste the manifest and create the app

### 3. Get Your Credentials

After creating the app:

1. Go to **Basic Information** → **App Credentials**
   - Copy the **Signing Secret**

2. Go to **OAuth & Permissions**
   - Click "Install to Workspace"
   - Authorize the app
   - Copy the **Bot User OAuth Token** (starts with `xoxb-`)

### 4. Configure Railway Environment Variables

In your Railway project, add these environment variables:

```
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_SIGNING_SECRET=your_signing_secret_here
```

### 5. Test Your Bot

1. Go to your Slack workspace
2. Invite the bot to a channel: `/invite @Hello World Bot`
3. Send any message in that channel
4. The bot should respond with "Hello World! 👋"

You can also DM the bot directly!

## How It Works

- Uses the official `slack-bolt` framework
- Listens for `message` and `app_mention` events
- Automatically handles request verification and retries
- Ignores bot messages to prevent infinite loops
- Runs on gunicorn for production deployment

## Local Development

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your credentials:
   ```
   SLACK_BOT_TOKEN=xoxb-your-token
   SLACK_SIGNING_SECRET=your_signing_secret
   PORT=3000
   ```

4. Run the app:
   ```bash
   python app.py
   ```

5. Use a tool like [ngrok](https://ngrok.com/) to expose your local server:
   ```bash
   ngrok http 3000
   ```

6. Update your Slack app's Request URL with the ngrok URL

## Project Structure

```
.
├── app.py                  # Main application file
├── requirements.txt        # Python dependencies
├── Procfile               # Railway/Heroku deployment config
├── runtime.txt            # Python version specification
├── slack-manifest.yml     # Slack app configuration
└── README.md              # This file
```

## Troubleshooting

- **Bot not responding**: Check Railway logs with `railway logs`
- **Module not found**: Make sure `requirements.txt` is installed
- **Events not received**: Verify the Request URL in Slack app settings
- **403 errors**: Double-check your `SLACK_BOT_TOKEN`

## Extending the Bot

To add more functionality, simply add more event handlers:

```python
@app.command("/hello")
def handle_command(ack, say, command):
    ack()
    say(f"Hello <@{command['user_id']}>!")
```

## License

MIT
