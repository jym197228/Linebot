from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('aIFxiQj+b/IlHx9ROrXnk8r+nao1Q04vXKngmDnJ8u3AsbCwA4QBb9Pg76uHfhCXZHX9NpNgFVCIhd+fN5f9YmfyMXSHblVG1eJP5V1UA+N6MOf8lz/6xVFZuynwlixPV1VmBa1V7I9NgeivNVTSOwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('978987e646ea444d771e0b6ac8163802')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()