# Slack Missile Launcher

Fire missiles at your enemies via Slack! For example `/shoot ben`.

<img alt="Launcher Gif" src="https://raw.githubusercontent.com/babldev/slack-missiles/master/launcher.gif" width="240" height="240">

Requires the [Dream Cheeky missile launcher](http://dreamcheeky.com/thunder-missile-launcher).

## Setup

### Run the webserver locally with the device attached

This server will receive commands from Slack.

```
cp targets_sample.json targets.json
virtualenv venv
pip install -r requirements.txt
source venv/bin/activate
python missile.py
```

### Expose the webserver to the public

One quick and dirty way to do this is with [ngrok](https://ngrok.com/)

### Add the Slack command hook

Add a [Slack command hook](https://api.slack.com/slash-commands) and point it to your webserver: http://yourserver.com/slack

### Test the connection

Does `/shoot right 1000` move the device for 1 second?

### Calibrate targets.json to your liking

The format is [X, Y], declaring how much the device moves right and then up before shooting.

## Notes

Based on code by https://github.com/codedance/Retaliation

The code is super hacky right now, but it works.
