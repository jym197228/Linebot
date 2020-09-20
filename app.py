from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,StickerSendMessage
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
    msg = event.message.text
    
    r = '我看不懂你想要幹嘛?'
    if msg in ['hi', 'Hi', 'HI', '嗨']:
        r = '嗨'
    elif msg == '你想要出去玩嗎?':
        r = '我不想要喔！'
    elif '訂位' in msg:
        r = '您想要訂位嗎?'
        
    sticker_message = StickerSendMessage(
        package_id='11537',
        sticker_id='52002736'
    )
    
    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=r)
            )
    line_bot_api.reply_message(
            event.reply_token,
            sticker_message
            )



if __name__ == "__main__":
    app.run()