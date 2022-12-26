from flask import Flask, request, abort, send_file
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from ability import Project
from env import *
from fsm import TocMachine
from dotenv import load_dotenv
import os

load_dotenv()


machine = TocMachine(
    states=["user", "name", "lucky", "relax", "trivia", "study", "subject"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "name",
            "conditions": "is_going_to_name",
        },
        {
            "trigger": "advance",
            "source": "name",
            "dest": "lucky",
            "conditions": "is_going_to_lucky",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "relax",
            "conditions": "is_going_to_relax",
        },
        {
            "trigger": "advance",
            "source": "relax",
            "dest": "trivia",
            "conditions": "is_going_to_trivia",
        },
        {
            "trigger": "advance",
            "source": "user",
            "dest": "study",
            "conditions": "is_going_to_study",
        },
        {
            "trigger": "advance",
            "source": "study",
            "dest": "subject",
            "conditions": "is_going_to_subject",
        },
        {"trigger": "go_back", "source": ["name", "lucky", "relax", "trivia", "study", "subject"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)


app = Flask(__name__)

linebot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

person = Project()
person.mode = 0
person.type = 0
person.studying = 0
fun = {"冷知識", "冷笑話"}
trivia = {"動物", "食品", "地理"}
subject = {"資安", "研究所", "寫程式"}
talk = {"謝謝", "你好", "重頭", "歡迎訊息", "功能"}
begin = "歡迎使用本系統\n您可以選擇:\n\"每日運勢\"\n\"輕鬆一下\"\n\"我要讀什麼\"\n或是輸入\"重頭\"重新選擇\n沒事也可以說聲\"你好\"喔~~\n若有需要隨時查看功能，可以輸入\"功能\"\n結束後記得說聲\"謝謝\"喔!!!"

linebot_api.push_message("U2fcb5c86462ec92c0bea34df15b4fd3d", TextSendMessage(text = begin))

@app.route('/callback',  methods=['POST'])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_text = event.message.text
    if message_text == "每日運勢" and person.mode == 0:
        word = "請輸入您的名字:\n(不可輸入之名稱:謝謝, 你好, 歡迎訊息，輸入\"重頭\"將會重頭開始，輸入\"功能\"會跑出功能表)"
        linebot_api.reply_message(event.reply_token, TextSendMessage(text = word))
        person.mode = 1
    elif message_text == "輕鬆一下" and person.mode == 0:
        word = "您要看的是冷笑話還是冷知識?(輸入冷笑話/冷知識):"
        linebot_api.reply_message(event.reply_token, TextSendMessage(text = word))
        person.mode = 2
    elif message_text == "我要讀什麼" and person.mode == 0:
        word = "請選擇:\n讀書科目\n查看清單"
        linebot_api.reply_message(event.reply_token, TextSendMessage(text = word))
        person.mode = 3

    elif person.mode == 1 and message_text not in talk: # 每日運勢
        person.name = message_text
        word = "請輸入您的血型:\n"
        linebot_api.reply_message(event.reply_token, TextSendMessage(text = word))
        person.mode = 5
    elif person.mode == 5 and message_text in {"O", "AB", "B", "A"}:
        person.blood = message_text
        word = person.lucky()
        linebot_api.reply_message(event.reply_token, TextSendMessage(text = word))
        person.initial()

    elif person.mode == 2 and message_text in fun: # 選擇冷笑話還是冷知識
        if message_text == "冷知識":
            word = "請輸入您要看的種類(動物/食品/地理):"
            linebot_api.reply_message(event.reply_token, TextSendMessage(text = word))
            person.mode = 4
        else:
            person.type = 4
            word = person.joke()
            linebot_api.reply_message(event.reply_token, TextSendMessage(text = word))
            person.initial()

    elif person.mode == 3 and message_text == "讀書科目":
        word = "請選擇要讀的科目(資安/研究所/寫程式):"
        linebot_api.reply_message(event.reply_token, TextSendMessage(text = word))
        person.mode = 6
    elif person.mode == 6 and message_text in subject: # 選擇要讀的科目
        if message_text == "資安":
            person.studying = 1
        elif message_text == "研究所":
            person.studying = 2
        elif message_text == "寫程式":
            person.studying = 3
        word = person.study()
        linebot_api.reply_message(event.reply_token, TextSendMessage(text = word))
        person.initial()

    elif person.mode == 3 and message_text == "查看清單":
        word = person.get_study_list()
        linebot_api.reply_message(event.reply_token, TextSendMessage(text = word))
        person.initial()

    elif person.mode == 4 and message_text in trivia: # 選擇冷知識的種類
        if message_text == "動物":
            person.type = 1
        elif message_text == "食品":
            person.type = 2
        elif message_text == "地理":
            person.type = 3
        word = person.joke()
        linebot_api.reply_message(event.reply_token, TextSendMessage(text = word))
        person.initial()
    elif message_text == "重頭":
        word = "您回到最前面，重新輸入\n"
        word += begin
        linebot_api.reply_message(event.reply_token, TextSendMessage(text = word))
        person.initial()
    elif message_text == "你好" and person.mode == 0:
        word = "你好!!\n"
        linebot_api.reply_message(event.reply_token, TextSendMessage(text = word))
        person.initial()
    elif message_text == "歡迎訊息" and person.mode == 0:
        word = begin
        linebot_api.reply_message(event.reply_token, TextSendMessage(text = word))
        person.initial()
    elif message_text == "功能":
        word = "我的功能有:\n每日運勢: 可以看你今天的運氣喔!!!\n輕鬆一下: 偶爾放鬆一下，看一下冷笑話或冷知識嘛~\n我要讀什麼: 不知道要讀甚麼嗎? 這時候我就派上用場啦!\n你好: 我會跟你打招呼\n謝謝: 我很有禮貌，會說不客氣喔!!\n\n\n若須隨時查看功能，可以打\"功能\""
        linebot_api.reply_message(event.reply_token, TextSendMessage(text = word))
    elif message_text == "謝謝" and person.mode == 0:
        word = "不客氣!!\n若想重新使用\n重新輸入即可"
        linebot_api.reply_message(event.reply_token, TextSendMessage(text = word))
        person.initial
    else:
        word = "您打錯東西了\n需要重頭輸入!"
        linebot_api.reply_message(event.reply_token, TextSendMessage(text = word))
        person.initial()

@app.route("/show_fsm", methods=['POST'])            
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")    

if __name__ == "__main__":
    # app.run()
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port = port, debug = True)
    