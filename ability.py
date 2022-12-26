import time
import random
from transitions.extensions import GraphMachine

fun = {"冷知識", "冷笑話"}
trivia = {"動物", "食品", "地理"}
subject = {"資安", "研究所", "寫程式"}

class Project(GraphMachine):
    def __init__(self):
        self.study_list_info = ("Web", "Pwn", "Reverse", "Forensic", "Crypto", "Misc")
        self.study_list_graduate = ("Data Structure", "Algorithm", "Discrete Mathematics", "Linear Algebra", "Computer Architecture", "Operating System")
        self.study_list_program = ("LeetCode", "UVa", "Kattis", "Codeforces")
        self.luck = ("特大吉", "大吉", "中吉", "小吉", "吉", "末吉", "凶", "大凶")
        self.trivia_animal = ("北極熊的皮膚是黑色的!\n來源: https://reurl.cc/jRo9vZ\n",
                              "狗狗的嗅覺敏感度是人類的10萬~100萬倍!\n來源: https://reurl.cc/jRo9vZ\n",
                              "狗狗的鼻紋跟人類一樣，都是獨一無二的!\n來源: https://reurl.cc/jRo9vZ\n",
                              "抹香鯨睡覺時是直立的!\n來源: https://reurl.cc/jRo9vZ\n",
                              "同一窩有不同花色的小貓，是因為同一胎的小貓中，可能都來自不同父親!\n來源: https://www.greenconut.com/trivia/cat-simultaneous-repregnancy-color_1128/\n",
                              "兔子其實很討厭吃紅蘿蔔，因為兔子如果腸胃狀況不好時，吃了可能會拉肚子!\n來源: https://www.greenconut.com/trivia/rabbit-vision-dont-eat-carrot_1126/\n",
                              "氣候會影響烏龜生男或是生女，而且烏龜是用屁股呼吸的!\n來源: https://www.greenconut.com/trivia/testudines-turtles-breathe-trivia_1125/\n",
                              "公皇帝企鵝為了孵蛋，會需要60天不吃不喝等母企鵝回來!\n來源: https://www.greenconut.com/trivia/emperor-penguin-hatch-eggs_1020/\n",
                              "紅鶴單腳站立比雙腳站立更能保持平衡，因為不需要用任何肌肉!\n來源: https://www.greenconut.com/trivia/flamingo_1018/\n",
                              "如果鼴鼠三到四個小時內沒有吃到食物，就會因為缺乏能量，最終餓死\n來源: https://www.greenconut.com/trivia/mole-animal-hungry_1017/\n",
                              "豬是世界上第五聰明的動物，甚至可以在電子遊戲中擊敗黑猩猩!\n來源: https://www.greenconut.com/trivia/pigs-are-intelligent-than-dog_1008/\n")
        self.trivia_food = ("蜂蜜在常溫且正確保存下，幾乎永遠不會變質!\n來源: https://reurl.cc/jRo9vZ\n",
                            "冰糖葫蘆源自於南宋，最早是用來治病的!\n來源: https://www.greenconut.com/trivia/crispy-sugar-coated-fruit_1110/\n",
                            "早餐玉米片具有磁性，所以是可以被磁鐵吸引的!\n來源: https://www.greenconut.com/trivia/cereal-magnetic_0929/\n",
                            "愛吃垃圾食物，其實是人類的本能!\n來源: https://www.greenconut.com/trivia/junk-food_0817/\n",
                            "以前歐洲人是用乳酪來清潔傷口!\n來源: https://www.greenconut.com/trivia/platter-of-various-cheeses-penicillin_1203/\n",
                            "嚼口香糖可以幫助手術快速復原!\n來源: https://www.greenconut.com/trivia/chewing-gum-help-surgery_1202/\n",
                            "心情不好時，吃甜或吃辣都可以讓我們感到快樂!\n來源: https://www.greenconut.com/trivia/emotionfood_0522/\n")
        self.trivia_geography = ("屏東火車站比高雄火車站還要北邊!\n來源: https://reurl.cc/jRo9vZ\n",
                                 "澎湖不只有雙心石滬，實際上有其他種類，甚至還多達六百座!\n來源: https://smiletaiwan.cw.com.tw/article/4600\n",
                                 "台南圓環多是因為當時的技師長前往法國巴黎，發現當地的設計是圓環加上放射狀道路，因為很方便，所以最終引進台南!\n來源: https://smiletaiwan.cw.com.tw/article/4600\n",
                                 "高鐵台南站離高雄只有兩公里\n來源: https://reurl.cc/bGAW33\n",
                                 "台南車站是全台最西邊的鐵路車站\n來源: https://reurl.cc/OEnY5D\n",
                                 "台南境內高速公路長度全台第一\n來源: https://reurl.cc/OEnY5D\n",
                                 "南區的公英七街是全台灣最短的街\n來源: https://reurl.cc/OEnY5D\n")
        self.cold_joke = ("先深呼吸:\n一個阿姨去醫院打針，\n護理師:「先深呼吸。」\n阿姨:「我是小姐」\n(先深呼吸->先生呼吸)\n來源: https://arielhsu.tw/cold-joke/\n",
                          "濁水溪跟曾文溪不能在一起:\n為甚麼濁水溪跟曾文溪不能在一起?\n因為他們不是河(不適合)\n來源: https://arielhsu.tw/cold-joke/",
                          "字:\n劉備字玄德\n張飛字翼德\n五百字...\n\n\n\n心得\n來源: https://reurl.cc/91aDDd\n",
                          "軟糖:\n有一天軟糖難過的哭了\n然後他就變成QQ軟糖了\n來源: https://reurl.cc/91aDDd\n",
                          "吵架:\n有一對情侶吵架\n女生就很生氣的奪門而出\n然後男生就很快速地跑出去\n把門奪回來\n來源: https://reurl.cc/91aDDd\n",
                          "皮卡丘:\n皮卡丘走路怎麼說?\nA: 乒乓乒乓乒乓乒乓乒乓\n來源: https://reurl.cc/91aDDd\n",
                          "綁架:\n甚麼人最容易被綁架?\nA: 模範生，因為他們都是好榜樣\n來源: https://reurl.cc/91aDDd\n",
                          "鮭魚:\n為甚麼吃完鮭魚肚子會痛?\nA: 因為鮭魚在胃食道逆流\n來源: https://reurl.cc/91aDDd\n",
                          "麵包超人:\n麵包超人扭到腳會變成甚麼?\nA: 牛角麵包(扭腳麵包)\n來源: https://arielhsu.tw/cold-joke/\n",
                          "醫生:\n爸爸:「你從醫院回來了啊，沒什麼事吧?醫生怎麼說?」\n小明:「Doctor」\n來源: https://reurl.cc/X5yAQg\n",
                          "三角形:\n有一天長方形、正方形、三角形約好一起出去玩，\n結果大家都到了，剩下三角形沒到，\n這種情況叫甚麼?\nA: 全等三角形\n來源: https://reurl.cc/X5yAQg\n",
                          "恐怖分子:\n恐怖分子樓下住誰?\nA: 恐怖分母\n來源: https://reurl.cc/X5yAQg\n",
                          "液晶:\n液晶的媽媽叫甚麼名字?\nA: 液晶螢幕(台語)\n來源: https://reurl.cc/7jmKbD\n",
                          "起司:\n剛剛吃了起司後，\n我突然變得很強壯，\n因為芝士就是力量(知識就是力量)。\n來源: https://reurl.cc/7jmKbD\n")

    def lucky(self): # 運勢
        name_list = list(self.name)
        if len(self.name) > 20:
            index = ord(name_list[15])
        elif len(self.name) > 14:
            index = ord(name_list[12])
        elif len(self.name) > 10:
            index = ord(name_list[8])
        elif len(self.name) > 5:
            index = ord(name_list[3])
        else:
            index = ord(name_list[0])
        result = time.localtime(time.time())
        result = result.tm_year + result.tm_mon * (result.tm_wday + 1) + result.tm_mday * index
        result %= 8
        destiny = self.luck[result]
        word = f"{self.name}，你抽到的是: {destiny}\n"
        if destiny == "特大吉":
            word += f"{self.blood}型的你今天是運氣爆棚的一天\n不論做甚麼事情都會很順利的!!!\n"
        elif destiny == "大吉":
            word += f"{self.blood}型的你今天運氣很好喔\n可以試著做做看平常不敢做的事情喔!!!\n"
        elif destiny == "中吉":
            word += f"{self.blood}型的你今天運氣還蠻好的\n可以挑戰看看想做的事情喔!!!\n"
        elif destiny == "小吉":
            word += f"{self.blood}型的你今天運氣還蠻不錯的\n那就充滿活力的前進吧!!!\n"
        elif destiny == "吉":
            word += f"{self.blood}型的你今天運氣還可以\n但也要好好努力喔!!!\n"
        elif destiny == "末吉":
            word += f"{self.blood}型的你今天運氣有點不太好\n但也沒關係\n靠著自己的努力勇往直前吧!!!\n"
        elif destiny == "凶":
            word += f"{self.blood}型的你今天運氣不好\n不過也沒關係\n一步一步穩穩地來吧!!!\n"
        elif destiny == "大凶":
            word += f"{self.blood}型的你今天運氣很不好\n所以得小心行事喔!!!\n"
        word += "*以上結果僅供參考*\n"
        return word

    def joke(self): # 輕鬆
        word = ""
        if self.type == 1: # 冷知識:動物
            word += random.choice(self.trivia_animal)
        elif self.type == 2: # 冷知識:食品
            word += random.choice(self.trivia_food)
        elif self.type == 3: # 冷知識:地理
            word += random.choice(self.trivia_geography)
        elif self.type == 4: # 冷笑話
            word += random.choice(self.cold_joke)
        return word

    def study(self):
        word = ""
        if self.studying == 1: # information security
            word += "資安:\n"
            word += random.choice(self.study_list_info)
        elif self.studying == 2: # graduate school
            word += "研究所:\n"
            word += random.choice(self.study_list_graduate)
        elif self.studying == 3: # programming
            word += "寫程式:\n"
            word += random.choice(self.study_list_program)
        return word
        
    def get_study_list(self):
        word = "資安:\n"
        for i in range(len(self.study_list_info)):
            word += self.study_list_info[i]
            word += " "
        word += "\n研究所:\n"
        for i in range(len(self.study_list_graduate)):
            word += self.study_list_graduate[i]
            word += " "
        word += "\n寫程式:\n"
        for i in range(len(self.study_list_program)):
            word += self.study_list_program[i]
            word += " "
        return word

    def initial(self):
        self.mode = 0
        self.type = 0
        self.studying = 0

if __name__ == "__main__":
    pass