# Slack Missile Launcher

Fire missiles at your enemies via Slack! For example `/shoot ben`.

<img alt="Launcher Gif" src="https://raw.githubusercontent.com/babldev/slack-missiles/master/launcher.gif" width="240" height="240">

Requires the [Dream Cheeky missile launcher](http://dreamcheeky.com/thunder-missile-launcher).

## Setup

### Run the webserver locally with the device attached

This server will receive commands from Slack.

```
cp settings_sample.py settings.py
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python missile.py
```

### Expose the webserver to the public

One quick and dirty way to do this is with [ngrok](https://ngrok.com/)

### Add the Slack command hook

Add a [Slack command hook](https://api.slack.com/slash-commands) and point it to your webserver: http://yourserver.com/slack

### Test the connection

Does `/shoot right 1000` move the device for 1 second?

### Update settings.py

The format is [X, Y], declaring how much the device moves right and then up before shooting. Add a slackbot remote control command if you'd like to have launch alerts.

## Notes

Based on code by https://github.com/codedance/Retaliation

The code is super hacky right now, but it works.
