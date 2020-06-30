import pya3rt

apikey = ""  # 自分のAPIキーを設定する
client = pya3rt.TalkClient(apikey)

if __name__ == '__main__':
    words = input("あなた> ")
    while words != "":
        response = client.talk(words)
        print("Bot> "+((response['results'])[0])['reply'])
        words = input("あなた> ")
