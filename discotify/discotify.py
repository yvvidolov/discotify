"""
Main implementation of the package
Discotify will save and read webhooks and user aliases from system cached files
Discotify will send messages to discord sync/async
"""

from typing import List, Optional, Dict

from pathlib import Path
import json

from platformdirs import user_cache_dir
import requests


# Discord Notify
class Discotify:
    """
    Send discord messages to channels(webhook) users(mentions).  
    Can also use aliases saved to system.  
    > $ pip install Discotify  
    > from discotify import Discotify  
    > dis = Discotify()  
    > dis.send("hello discord")  
    """
    
    CACHE_FILE_NAME='config.json'
    
    def __init__(self, tag: Optional[str] = None, mentions: Optional[List[str]|str] = None, channels: Optional[List[str]|str] = None, username: str = "PythonBot", no_config_file: bool = False, custom_config_file: Optional[str] = None):
        self.no_config_file = no_config_file
        self.cache_dir = Discotify.get_cache_dir(create_if_not_exists=True)
        self.cache_path = self.cache_dir.joinpath(self.CACHE_FILE_NAME) if custom_config_file is None else Path(custom_config_file)

        self.user_alias_map: Dict[str, str] = {}
        self.hook_alias_map: Dict[str, str] = {}
        
        if self.no_config_file is False:
            self.config_read(self.cache_path)
        
        self.m_mentions: Optional[List[str]] = [next(iter(self.user_alias_map.values()))] if self.user_alias_map else []
        self.m_channels: Optional[List[str]] = [next(iter(self.hook_alias_map.values()))] if self.hook_alias_map else []
        self.m_tag = f'[{tag}] ' if tag is not None else ''
        self.m_username = username
        
        if mentions is not None:
            if isinstance(mentions, str):
                mentions = [mentions]
            self.m_mentions = [m if m not in self.user_alias_map else self.user_alias_map[m] for m in mentions]
        
        if channels is not None:
            if isinstance(channels, str):
                channels = [channels]
            self.m_channels = [c if c not in self.hook_alias_map else self.hook_alias_map[c] for c in channels]
    #end
    
    def send(self, text: str, tag: Optional[str] = None, mentions: Optional[List[str]|str] = None, channels: Optional[List[str]|str] = None):
        '''Send discord channel message with user mention using webhook'''
        tag = f'[{tag}] ' if tag is not None else self.m_tag
        
        if mentions is not None:
            if isinstance(mentions, str):
                mentions = [mentions]
            mentions = [m if m not in self.user_alias_map else self.user_alias_map[m] for m in mentions]
        else:
            mentions = self.m_mentions
        #end
            
        if channels is not None:
            if isinstance(channels, str):
                channels = [channels]
            channels = [c if c not in self.hook_alias_map else self.hook_alias_map[c] for c in channels]
        else:
            channels = self.m_channels
        #end
       
        mention_str = ''.join([f'<@{m}>' for m in mentions])+' ' if mentions else ''
        payload = {"content": f'{mention_str}{tag}{text}', "username": self.m_username}
        
        if channels:
            for channel in channels:
                r = requests.post(channel, json=payload, timeout=5)
                r.raise_for_status()
        #end
    #end
    
    def get_config_path(self):
        """Get filepath to configuration file"""
        return str(self.cache_path)
    
    def get_users_alias(self):
        """Get all user aliases"""
        return self.user_alias_map
    
    def get_hooks_alias(self):
        """Get all hook aliases"""
        return self.hook_alias_map
    
    def user_add(self, alias: str, user_id: str):
        """Add alias for user_id in config"""
        self.user_alias_map[alias] = user_id
        if self.no_config_file is False:
            self.config_write(self.cache_path)
    #end
    
    def user_remove(self, alias: Optional[str] = None, user_id: Optional[str] = None) -> bool:
        """Remove a user by alias or by user_id from the config"""
        entry_removed = False
        
        if alias is not None:
            if alias in self.user_alias_map:
                del self.user_alias_map[alias]
                entry_removed = True
            
        if user_id is not None:
            aliases_to_remove = [alias for alias, uid in self.user_alias_map.items() if uid == user_id]
            for alias in aliases_to_remove:
                del self.user_alias_map[alias]
                entry_removed = True
            
        if entry_removed and self.no_config_file is False:
            self.config_write(self.cache_path)
            
        return entry_removed
    #end
    
    def hook_add(self, alias: str, hook_url: str):
        """Add alias for hook_url in config"""
        self.hook_alias_map[alias] = hook_url
        if self.no_config_file is False:
            self.config_write(self.cache_path)
    #end

    def hook_remove(self, alias: Optional[str] = None, hook_url: Optional[str] = None) -> bool:
        """Remove a hook by alias or by hook_url from the config"""
        entry_removed = False
        
        if alias is not None:
            if alias in self.hook_alias_map:
                del self.hook_alias_map[alias]
                entry_removed = True
            
        if hook_url is not None:
            aliases_to_remove = [alias for alias, url in self.hook_alias_map.items() if url == hook_url]
            for alias in aliases_to_remove:
                del self.hook_alias_map[alias]
                entry_removed = True
            
        if entry_removed and self.no_config_file is False:
            self.config_write(self.cache_path)
            
        return entry_removed
    #end
    
    def config_read(self, filepath: Path):
        """Read user and hook list from file"""
        if self.no_config_file is True:
            raise RuntimeError("To use config file, create instance with no_config_file=True")
        
        if not filepath or not filepath.exists():
            return
        
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                self.user_alias_map = data.get("user_alias_map", {})
                self.hook_alias_map = data.get("hook_alias_map", {})
            except json.JSONDecodeError:
                self.user_alias_map = {}
                self.hook_alias_map = {}
    #end
    
    def config_write(self, filepath: Path):
        """Write user and hook list to file"""
        if self.no_config_file is True:
            raise RuntimeError("To use config file, create instance with no_config_file=True")
        
        data = {
            "user_alias_map": self.user_alias_map,
            "hook_alias_map": self.hook_alias_map
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    #end
    
    @staticmethod
    def get_cache_dir(create_if_not_exists: bool = False) -> Path:
        """
        Get platform cache dir, to save state information. Function can optionally create the directory if it doesn't exist.
        """
        APP_NAME = "discotify"
        APP_AUTHOR = "yv"

        cache_dir = Path(user_cache_dir(APP_NAME, APP_AUTHOR)) # user_data_dir, user_config_dir
        if create_if_not_exists:
            cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir
    #end
#end
