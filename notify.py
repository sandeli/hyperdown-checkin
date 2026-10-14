#!/usr/bin/env python3
"""Telegram Bot 通知（仅用标准库，无新增依赖）。

配置（二选一）：
  环境变量：TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID
  config.toml：telegram_bot_token / telegram_chat_id

获取方式：
  1. 与 @BotFather 对话创建 Bot，拿到 token
  2. 与 Bot 随意发一句话，然后访问
     https://api.telegram.org/bot<TOKEN>/getUpdates
     找到 chat.id，即为 TELEGRAM_CHAT_ID
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request


def send_telegram(bot_token: str, chat_id: str, text: str, timeout: int = 15) -> bool:
    """发送 Telegram 消息，成功返回 True，失败返回 False（不抛异常）。"""
    if not bot_token or not chat_id:
        return False
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = urllib.parse.urlencode(
            {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
        ).encode()
        req = urllib.request.Request(url, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return bool(body.get("ok"))
    except Exception:
        return False


def build_checkin_msg(
    ok: bool,
    reward: str,
    balance: str,
    ts: str,
    already: bool = False,
    error: str = "",
) -> str:
    """组装签到通知正文。"""
    if not ok:
        return (
            "❌ <b>Hyperdown 签到失败</b>\n"
            f"原因：{error or '未知错误'}\n"
            f"🕐 {ts}"
        )
    if already:
        return (
            "ℹ️ <b>Hyperdown 今日已签到</b>\n"
            f"💰 当前余额：{balance}\n"
            f"🕐 {ts}"
        )
    return (
        "✅ <b>Hyperdown 签到成功</b>\n"
        f"📦 本次获得：{reward}\n"
        f"💰 当前余额：{balance}\n"
        f"🕐 {ts}"
    )
