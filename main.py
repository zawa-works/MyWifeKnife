
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
import os

app = Flask(__name__)

# 環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["H4wEfz1QjnM2mfWnG0+mJsUrKHWAzOBwKV3bNFjoSCbNNZFn1Wg3GeG56CTHZBWdyNs9hjpqSr4/ixKm7+eMenE0ObGignX8POC4QH1dRXaMg77oEBZB/wBl0Z1qmy49LGV0fOxOpn8W/5yMvsLI8AdB04t89/1O/w1cDnyilFU="]
YOUR_CHANNEL_SECRET = os.environ["6df2a3bbb03118b956c821946eb8b66f"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    #    app.run()

    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
