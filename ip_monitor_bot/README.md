# IP Monitor Bot
A simple bot included in a web page that sends the visitor’s IP address along with extra info — like country and user agent — to a Telegram chat. It uses [ip-api.com](https://ip-ai.com) to fetch the infos.  
The script sets a one-hour cookie to prevent sending duplicate messages if the visitor reloads the page.

## Dependencies
The script uses cURL to fetch info from [ip-api.com](https://ip-api.com).
Make sure to install the `php-curl` package on your distro to enable the PHP cURL extension.

## Configuration
**Warning:** You must specify your Telegram bot token and chat ID:
```php
	$token = "<telegram_bot_token>"; // change this
    $chat_id = "<telegram_chat_id>"; // change this
```

## Usage
Include it in your website's `index.php`
```php
<?php include "ip_monitor_bot/ip_monitor_bot.php"; ?>
```
