"""Client example for sending 'hello world' as direct message"""
from discordproxy.client import DiscordClient

client = DiscordClient()
client.create_direct_message(user_id=123456789, content="Hello, world!")
