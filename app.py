from flask import Flask, request, abort
import json

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('gVAAZUKCAd5iouqJ2n6xIhcTVymqVFJ7QzswyrmfAG/O+HF/cBE9663Bu+OovVaZpA6Set/2c7k4ygjBLpS3Vr3EmcrxdaP6IORZf+IPVQV4gdND+nDJD6LIDrXcgsb3S6izJxnJaErY7Uz50kK+FgdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('440c699d9821a8b4bc4c7ff0029c9540')

# 監聽所有來自 /callback 的 Post Request
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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    
    with open('card.json',encoding='utf-8-sig', errors='ignore') as f:
        card = json.loads(f.read())
    with open('latest_news.json',encoding='utf-8-sig', errors='ignore') as f:
        latest_news = json.loads(f.read())
    with open('ESG_news.json',encoding='utf-8-sig', errors='ignore') as f:
        ESG_news = json.loads(f.read())
    with open('5G_news.json',encoding='utf-8-sig', errors='ignore') as f:
        news_5G = json.loads(f.read())
    card_message = FlexSendMessage('card',card)
    latest_news_message = FlexSendMessage('latest_news',latest_news)
    ESG_news_message = FlexSendMessage('ESG_news',ESG_news)
    news_5G_message = FlexSendMessage('5G_news',news_5G)
    
    
    quick_reply = TextSendMessage(text='可透過下方類別了解更多：',quick_reply=QuickReply(items=[QuickReplyButton(action=MessageAction(label="5G", text="5G")), QuickReplyButton(action=MessageAction(label="ESG投資", text="ESG投資")),QuickReplyButton(action=MessageAction(label="CIO每周觀點", text="CIO每周觀點")), QuickReplyButton(action=MessageAction(label="股票", text="股票")),QuickReplyButton(action=MessageAction(label="固定收益", text="固定收益")),QuickReplyButton(action=MessageAction(label="新興市場債券", text="新興市場債券"))]))
    if event.message.text == '圖卡':
        line_bot_api.reply_message(event.reply_token,card_message)
    elif event.message.text == '觀點':
        #line_bot_api.reply_message(event.reply_token,card_message)
        line_bot_api.reply_message(event.reply_token,[latest_news_message,quick_reply])
    elif event.message.text == 'ESG投資':
        line_bot_api.reply_message(event.reply_token,[ESG_news_message,quick_reply])
    elif event.message.text == '5G':
        line_bot_api.reply_message(event.reply_token,[news_5G_message,quick_reply])

        
    #else:
        # line_bot_api.reply_message(event.reply_token,flex_message)
        #line_bot_api.reply_message(event.reply_token,[card_message,quick_reply])
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.1', port=port)
