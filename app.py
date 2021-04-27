import time
import random
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

# 1段目...アクセストークン  2段目...シークレット
line_bot_api = LineBotApi('アクセス')
handler = WebhookHandler('シークレット')

@app.route("/")
def test():
  return "OK"

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
    
    if event.message.text == "使い方" or event.message.text == "つかいかた" or event.message.text == "取説" or event.message.text == "とりせつ" or event.message.text == "トリセツ":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"[App一覧]\nおはよう:あいさつを返してくれます\n料理開始:料理の開始時間とカウントをスタートします\n料理終了:料理開始からの時間を表示します\n"))
    
    # 料理時間--------------------------
    if event.message.text == "料理開始"or event.message.text == "料理" or event.message.text == "りょうり":
        # sttをglobal変数に(これしないと料理終了時に開始時間を持ってきて計算できない)
        global stt
        stt = time.gmtime()
        line_bot_api.reply_message(
            event.reply_token,
            # .zfill(2)は、str型メソッド strで文字列にして変換
            TextSendMessage(text=f"[アナウンス]\n料理を開始しました。\n開始時刻→" + str(stt.tm_hour + 9) + ":" + str(stt.tm_min).zfill(2) + "\nレッツ、クッキング！"))
        
    if event.message.text == "料理終了" or event.message.text == "終了" or event.message.text == "しゅうりょう":
        # ft→終了時間(finish time)
        ft = time.gmtime()

        stru = stt.tm_hour
        strf = ft.tm_hour

        # rh→料理時間(result hour)
        rh = strf - stru
        # rh→料理時間(result min)
        rm = (ft.tm_min - stt.tm_min) + (rh * 60)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"[アナウンス]\n料理お疲れ様です<(^~^)/\n終了時刻→" + str(ft.tm_hour + 9) + ":" + str(ft.tm_min).zfill(2) + "\nかかった時間は" + str(rm) + "分です！"))

    # 生活系-----------------------------------
    if event.message.text == "検温" or event.message.text == "けんおん" or event.message.text == "井上" or event.message.text == "井上先生":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"[ミッション]\n井上 第二形態の阻止！\n9:00になる前に検温を入力し、井上の第二形態化を食い止めよ。\nhttps://docs.google.com/forms/d/e/1FAIpQLScPXjH2eQytZEFAnENB2V7CyGhZMfLIbGzpilXbDXrUv1WdLA/viewform"))
    
    if event.message.text == "おはよう" or event.message.text == "おはようございます" or event.message.text == "おはよ":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"おはようございます！\n今日も充実した1日をお過ごしください"))

    # 当たるか当たらないか分からないクジ 6000000～7000000だと出てきやすい-----------
    if event.message.text == "クックパッド" or event.message.text == "くっくぱっど":
        rand = random.randint(1, 9999999)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"https://cookpad.com/recipe/" + str(rand).zfill(7)))
    
    # 麺類のレシピ保管庫--------------------------
    if event.message.text == "パスタ" or event.message.text == "ぱすた":
        list = ["6668407", "6660327", "6675758", "6673486", "6675949", "6675655", "6670428", "6668242", "6674104"]
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"パスタのレシピを5つご提案します♪\nhttps://cookpad.com/recipe/" + random.choice(list)))
    
    if event.message.text == "ラーメン" or event.message.text == "らーめん" or event.message.text == "拉麺":
        list = ["6629513", "6660725", "6670996", "6580750", "6674107", "6675712", "6671834", "6676538", "6671381"]
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"ラーメンのレシピを5つご提案します♪\nhttps://cookpad.com/recipe/" + random.choice(list)))

    # ご飯もののレシピ保管庫-----------------------
    if event.message.text == "カレーライス" or event.message.text == "カレー" or event.message.text == "かれー" or event.message.text == "かれーらいす":
        list = ["6670333", "6674901", "6674024", "6669046", "6670716", "6666112", "6647644", "6644933"]
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"カレーライスのレシピを5つご提案します♪\nhttps://cookpad.com/recipe/" + random.choice(list)))

    # ハンバーグのレシピ保管庫-----------------------
    if event.message.text == "ハンバーグ" or event.message.text == "はんばーぐ":
        list = ["6669169", "6677919", "6665107", "6580286", "6676779", "6666112", "6677510", "6669929"]
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"ハンバーグのレシピを5つご提案します♪\nhttps://cookpad.com/recipe/" + random.choice(list)))

    # 鍋のレシピ保管庫-----------------------
    if event.message.text == "鍋" or event.message.text == "なべ" or event.message.text == "お鍋" or event.message.text == "おなべ":
        list = ["6667368", "6676384", "6636003", "6668838", "6639358", "6647856", "6646007", "6645019"]
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"鍋のレシピを5つご提案します♪\nhttps://cookpad.com/recipe/" + random.choice(list)))
    
    # ステーキのレシピ保管庫-----------------------
    if event.message.text == "ステーキ" or event.message.text == "すてーき":
        list = ["6606487", "6646862", "6676318", "6676394", "6677321", "6661983", "6662763", "6552059"]
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"ステーキのレシピを5つご提案します♪\nhttps://cookpad.com/recipe/" + random.choice(list)))
    
    # グラタンのレシピ保管庫-----------------------
    if event.message.text == "グラタン" or event.message.text == "ぐらたん":
        list = ["6655694", "6668337", "6677217", "6675766", "6675395", "6658673", "6652908", "6653879"]
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"グラタンのレシピを5つご提案します♪\nhttps://cookpad.com/recipe/" + random.choice(list)))
    
    # パエリアのレシピ保管庫-----------------------
    if event.message.text == "パエリア" or event.message.text == "ぱえりあ":
        list = ["6669872", "6663826", "6577668", "6388446", "6573607", "6556762", "6561481", "6464863"]
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"パエリアのレシピを5つご提案します♪\nhttps://cookpad.com/recipe/" + random.choice(list)))
    
    # 味噌汁のレシピ保管庫-----------------------
    if event.message.text == "みそしる" or event.message.text == "味噌汁" or event.message.text == "お味噌汁" or event.message.text == "おみそしる":
        list = ["6673575", "6640056", "6660259", "6642812", "6669881", "6677276", "6675256", "6674118"]
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"お味噌汁のレシピを5つご提案します♪\nhttps://cookpad.com/recipe/" + random.choice(list)))

    # その他 全てをcookpadの検索後のurlで返す
    else:
        guzai = event.message.text
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f"[提案]\n" + guzai + "に関連する料理です↓\nhttps://cookpad.com/search/" + guzai))

if __name__ == "__main__":
    app.run()
