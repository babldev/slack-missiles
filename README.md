# Slack Missile Launcher

Fire missiles at your enemies using the [Dream Cheeky missile launcher](http://dreamcheeky.com/thunder-missile-launcher) and Slack! For example `/shoot ben`.

Based on code by https://github.com/codedance/Retaliation

## Setup

You need to run a webserver that you can make Slack command hook too.

```
cp targets_sample.json targets.json
virtualenv venv
pip install -r requirements.txt
source venv/bin/activate
python missile.py
```

Then create the command hook and point it to http://yourserver.com/slack

## Notes

This is super hacky right now, but it works.