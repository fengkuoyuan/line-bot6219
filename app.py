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

line_bot_api = LineBotApi('gc/YhXwIGx+esFsvBzWbLIfiYn9y1OpMxzRLKOfsp1ci2vedNUELGpGR0vel3LxXd2CpGQ0AYFsjGoCwAhsptZ5cb9t/4awcbOWhkHWiWYsvscV+W/tYBlaGzwDrTcJFDcvWcyUZQlUnaP/CRJpPJQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a19d4b13b1ff6e507f24f9ef085506ae')


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