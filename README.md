# Discotify

Shell CLI command and python package to send messages to discord via webhooks.  
Supports aliases to webhooks and user_ids saved to a platform config file.  
When using the config file, shell and python share the added aliases.  

## Installation

You can install this package using pip:

```bash
pip install discotify
```

Or install from source:

```bash
git clone https://github.com/yvvidolov/discotify.git
cd discotify
pip install -e .
```

## Usage

### Using the command line tool

```bash
discotify --help
discotify --user_add my_user 694462935761677102
discotify --hook_add my_channel https://discord.com/api/webhooks/1423340029622751367/rx-ibr-lVxAhFIUWs2
discotify --channel my_channel --mention my_user "Hello Discord!!!"

```

### Using as a Python module

```python
from discotify import Discotify

dis = Discotify(tag='HomeServer', channels='my_channel')
dis.send(text="This is me message", mentions='my_user')
```

```python
dis.get_config_path() # filepath to config.json containing the user/hook aliases
dis.get_users_alias() # return dictionary of alias/user_id
dis.get_hooks_alias() # return dictionary of alias/hook_url
dis.user_add(alias='short', user_id='discord_user_id') # add new user_id alias
dis.user_remove(alias='short') # remove by alias
dis.user_remove(user_id='short') # remove by user_id

Discotify(  
    tag: Optional[str] = None, # add a [tag] before the message
    mentions: Optional[List[str]|str] = None, # add @username for notifications
    channels: Optional[List[str]|str] = None, # send to multiple channels/webhooks
    username: str = "PythonBot", # the username of the sending bot
    no_config_file: bool = False, # do not read/write platform config.json (slightly faster)
    custom_config_file: Optional[str] = None # override the config file path/name
    )
```

### Getting discord webhook and user_id

#### WebHook
- Open: discord.com
- Select channel -> Edit Channel
- Integrations -> Webhooks -> New Webhook -> Copy Webhook URL

#### UserID
- Open: discord.com
- User Settings -> Advanced -> Developer Mode
- Right click User -> Copy User ID

## License

This project is licensed under the MIT License - see the LICENSE file for details.
