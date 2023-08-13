To start the bot, just provide the token in config.yml and run \_\_main\_\_.py :)

<code>python3 -m bot</code>

**Please note!**

If you are using webhooks, you should set the delay to more than one second. 
This can be done manually, or using the helper method.
```python
def main() -> None:
    dp = Dispatcher()
    dp.message.middleware(AlbumMiddleware.webhook_mode())
    ... # run webhook
```
