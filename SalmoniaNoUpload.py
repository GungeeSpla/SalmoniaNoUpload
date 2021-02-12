# -*- coding: utf-8 -*-
# requests: HTTP通信を行うライブラリ
import requests
# sys: 実行環境に関する情報を扱うライブラリ
import sys
# json: JSONの読み書きを行うライブラリ
import json
# os: ファイルやディレクトリを操作するライブラリ
import os
# webbouser: Webサイトを表示するライブラリ
import webbrowser
# datetime型: 日付+時刻(year, month, day, hour, minute, second, microsecond)を扱うクラス
from datetime import datetime
# time: 処理を一時停止するためのモジュール
from time import sleep
# iksm: iksm_sessionを取得するためのライブラリ
import iksm
from result_table import print_result

# バージョン
VERSION = "1.0.8"
# 言語
LANG = "en-US"
# SalmonStatsのURL
URL = "https://salmon-stats.yuki.games/"
# SalmonStatsを使いかどうか
FLAG_SALMON_STATS = False

# Paramクラス
class Param():

    # コンストラクタ
    def __init__(self):
        # splanet2, local プロパティにゼロを代入
        self.splatnet2 = 0
        self.local = 0

    # setup
    # selfに代入していく
    def setup(self, iksm_session="", session_token="", api_token="", salmonstats=0, api_errors=0):
        self.iksm_session = iksm_session
        self.session_token = session_token
        self.api_token = api_token
        self.salmonstats = salmonstats
        self.api_errors = api_errors
        self.output()

    # output
    # selfの内容をconfig.jsonに書き出す
    def output(self):
        # 書き込みモードでconfig.jsonにアクセスする
        with open("config.json", mode="w") as f:
            data = {
                "iksm_session": self.iksm_session,
                "session_token": self.session_token,
                "api-token": self.api_token,
                "job_id": {
                    "splatnet2": self.splatnet2,
                    "salmonstats": self.salmonstats,
                    "local": self.local,
                },
                "api_errors": self.api_errors
            }
            # 辞書型をJSONで書き出す
            json.dump(data, f, indent=4)

# SalmonRecクラス
class SalmonRec():
    # コンストラクタ
    def __init__(self):
        print(datetime.now().strftime("%H:%M:%S ") + "Salmonia version " + VERSION)
        print(datetime.now().strftime("%H:%M:%S ") + "Thanks @Yukinkling and @barley_ural!")
        # os.path.dirname(path)
        # パス文字列からフォルダ名（ディレクトリ名）を取得する
        # ./dir/subdir/file.txt -> ./dir/subdir
        #
        # os.path.abspath(path)
        # 相対パス文字列から絶対パス文字列を取得
        # ./dir/subdir/file.txt -> C:\Uses\gungee\Documents\dir\subdir\file.txt
        #
        # sys.argv[0]
        # スクリプトのパス文字列
        #
        # config.jsonのパスを決定する
        path = os.path.dirname(os.path.abspath(sys.argv[0])) + "/config.json"
        self.param = Param()

        # 既存のconfig.jsonがあったら
        try:
            with open(path) as f: # Exist
                # 正常にロードできたら
                try:
                    # json.load(file)
                    # ファイルオブジェクトをJSONとして解釈して辞書を取得
                    df = json.load(f)
                    # setup
                    self.param.setup(df["iksm_session"], df["session_token"], df["api-token"], df["job_id"]["salmonstats"], df["api_errors"])
                # 正常にロードできなかったら
                except json.decoder.JSONDecodeError:
                    print(datetime.now().strftime("%H:%M:%S ") + "config.json is broken.")
                    print(datetime.now().strftime("%H:%M:%S ") + "Regenerate config.json.")
        # 既存のconfig.jsonがなかったら
        except FileNotFoundError: # None
            print(datetime.now().strftime("%H:%M:%S ") + "config.json is not found.")
            # config.jsonのテンプレートを書き出す
            self.param.setup()
            # setConfig
            self.setConfig()

        # このスクリプトと同階層にあるファイルとフォルダのリストを取得する
        dir = os.listdir() # Directory Checking
        # jsonフォルダが存在しないならば
        if "json" not in dir:
            print(datetime.now().strftime("%H:%M:%S ") + "Make directory...")
            # 作る
            os.mkdir("json")
        # jsonフォルダが存在するならば
        else:
            # jsonフォルダ内にあるファイルのリストを取得する
            file = []
            dir = os.listdir("json")
            for p in dir:
                # 後ろの5文字".json"を除いたファイル名をfileに入れていく
                file.append(p[0:-5])
            # 大きい整数から小さい整数に向けて並び替え
            file.sort(key=int, reverse=True)
            # その先頭の要素をlocalにセット
            try:
                self.param.local = int(file[0])
            # 要素がなければlocalは0
            except IndexError:
                self.param.local = 0

        # iksm_sessionが有効かどうかを確かめる
        url = "https://app.splatoon2.nintendo.net"
        print(datetime.now().strftime("%H:%M:%S ") + "Checking iksm_session's validation.")
        res = requests.get(url, cookies=dict(iksm_session=self.param.iksm_session))
        # 200: リクエストが成功
        if res.status_code == 200:
            print(datetime.now().strftime("%H:%M:%S ") + "Your iksm_session is valid.")
        # 403: リクエストが失敗
        if res.status_code == 403:
            # 認証エラーならば
            if res.text == "Forbidden":
                print(datetime.now().strftime("%H:%M:%S ") + "Your iksm_session is expired.")
                if self.param.session_token != "":
                    # iksm_sessionの再生成を行う
                    print(datetime.now().strftime("%H:%M:%S ") + "Regenerate iksm_session.")
                    try:
                        self.param.iksm_session = iksm.get_cookie(self.param.session_token, LANG, VERSION)
                        self.param.api_errors = 0
                        print(datetime.now().strftime("%H:%M:%S ") + "Done.")
                    except:
                        self.param.api_errors += 1
                        self.param.output()
                        input('iksm_sessionの再生成に失敗しました。終了するにはエンターキーを押してください。');
                        sys.exit(1)
            # それ以外ならば
            else:
                print(datetime.now().strftime("%H:%M:%S ") + "Unknown error.")
                message = datetime.now().strftime("%H:%M:%S Unknown error.\n")
                self.writeLog(message)
                input('不明なエラーが発生しました。終了するにはエンターキーを押してください。');
                sys.exit(1)

        url = "https://app.splatoon2.nintendo.net/api/coop_results"
        print(datetime.now().strftime("%H:%M:%S ") + "Getting latest job id from SplatNet2.")
        res = requests.get(url, cookies=dict(iksm_session=self.param.iksm_session)).json()
        print(datetime.now().strftime("%H:%M:%S ") + str(res["summary"]["card"]["job_num"]) + '.')
        self.param.splatnet2 = int(res["summary"]["card"]["job_num"])
        self.param.output()

    def setConfig(self):
        session_token = iksm.log_in(VERSION)
        iksm_session = iksm.get_cookie(session_token, LANG, VERSION)
        if FLAG_SALMON_STATS:
            webbrowser.open(URL)
            print(datetime.now().strftime("%H:%M:%S ") + "Login and Paste API token.")
            while True: # Waiting Input session_token & api-token
                try:
                    token = input("")
                    if len(token) == 64: # Simple Validation of api-token length
                        try:
                            int(token, 16) # Convert to Hex
                            print(datetime.now().strftime("%H:%M:%S ") + "Valid token.")
                            api_token = token
                            break
                        except ValueError:
                            print(datetime.now().strftime("%H:%M:%S ") + "Paste API token again.")
                    else:
                        print(datetime.now().strftime("%H:%M:%S ") + "Paste API token again.")
                except KeyboardInterrupt:
                    print("\nBye!")
                    sys.exit(1)
        else:
            api_token = "none"
        self.param.setup(iksm_session, session_token, api_token)

    def getJobId(self):
        url = "https://app.splatoon2.nintendo.net/api/coop_results"
        res = requests.get(url, cookies=dict(iksm_session=self.param.iksm_session)).json()
        return int(res["summary"]["card"]["job_num"])

    def upload(self, resid):
        resid = str(resid)
        path = "json/" + resid + ".json"
        file = json.load(open(path, "r"))
        result = {"results": [file]}
        url = "https://salmon-stats-api.yuki.games/api/results"
        headers = {"Content-type": "application/json",
                   "Authorization": "Bearer " + self.param.api_token}
        res = requests.post(url, data=json.dumps(result), headers=headers)

        if res.status_code == 401:  # 認証エラー
            message = datetime.now().strftime("%H:%M:%S API token is invalid.\n")
            self.writeLog(message)
            sys.exit()
        if res.status_code == 200:  # 認証成功
            # レスポンスの変換
            text = json.loads(res.text)[0]
            if text["created"] == False:
                print(datetime.now().strftime("%H:%M:%S Result ID:") + resid + " skip.")
            else:
                print(datetime.now().strftime("%H:%M:%S Result ID:") + resid + " upload!")
        if res.status_code == 500:
            print(datetime.now().strftime("%H:%M:%S Result ID:") + resid + " failure.")
            message = datetime.now().strftime("%H:%M:%S Result ID:" + resid + " : unrecoginized schedule id.\n")
            self.writeLog(message)
            with open("unupload_list.txt", mode="a") as f:
                f.write(resid + ".json\n")

    def writeLog(self, message):
        with open("error.log", mode="a") as f:
            f.write(message)
        f.close()

    def uploadAll(self):
        # jsonフォルダ内のファイル一覧を取得する
        file = []
        dir = os.listdir("json")
        for p in dir:
            file.append(p[0:-5])
        file.sort(key=int)

        results = []
        headers = {"Content-type": "application/json", "Authorization": "Bearer " + self.param.api_token}

        # jsonフォルダ内に存在するすべてのファイルについて
        url = "https://salmon-stats-api.yuki.games/api/results"
        for job_id in file:
            # self.param.salmonstatsよりも新しいならば
            if self.param.salmonstats < int(job_id):
                path = "json/" + job_id + ".json"
                results += [json.load(open(path, "r"))]
                if len(results) % 10 == 0:
                    res = requests.post(url, data=json.dumps({"results": results}), headers=headers)
                    results = []
                    if res.status_code == 200:
                        res = json.loads(res.text)
                        for r in res:
                            if r["created"] == False:
                                print(datetime.now().strftime("%H:%M:%S ") + str(r["job_id"]) + " skip.")
                            else:
                                print(datetime.now().strftime("%H:%M:%S ") + str(r["job_id"]) + " upload!.")
                            self.param.salmonstats = r["job_id"]
                            self.param.output()
                    sleep(5)

        # Remind Upload
        res = requests.post(url, data=json.dumps({"results": results}), headers=headers)
        if res.status_code == 200:
            res = json.loads(res.text)
            for r in res:
                if r["created"] == False:
                    print(datetime.now().strftime("%H:%M:%S ") + str(r["job_id"]) + " skip.")
                else:
                    print(datetime.now().strftime("%H:%M:%S ") + str(r["job_id"]) + " upload!.")
                self.param.salmonstats = r["job_id"]
                self.param.output()

    def getResults(self):
        # SplaNet2から取得できる最新のJobIdを取得
        self.param.splatnet2 = self.getJobId()
        # self.param.splatnet2 - 50 >  self.param.local ならば
        # すなわち、SplaNet2から取得できる最古のJobId-1がjsonフォルダに存在しないならば count = self.param.splatnet2 - 49
        # SplaNet2から取得できる最古のJobId-1がjsonフォルダに存在するならば count = self.param.local + 1
        count = self.param.splatnet2 - 49 if self.param.splatnet2 - 50 >  self.param.local else self.param.local + 1
        # SplaNet2から取得できる最新のJobIdがjsonフォルダに存在するならば何もしなくていい
        if self.param.local == self.param.splatnet2:
            return
        # plaNet2から取得できる最新のJobIdがjsonフォルダに存在しないならば取得しに行く
        for job_id in range(count, self.param.splatnet2 + 1):
            url = "https://app.splatoon2.nintendo.net/api/coop_results/" + str(job_id)
            res = requests.get(url, cookies=dict(iksm_session=self.param.iksm_session)).text
            path = os.path.dirname(os.path.abspath(sys.argv[0])) + "/json/" + str(job_id) + ".json"
            with open(path, mode="w") as f:
                f.write(res)
            print(datetime.now().strftime("%H:%M:%S ") + "Saved " + str(job_id) + " from SplatNet2.")
            
            # print
            ret = json.loads(res)
            print_result(ret)
            
            # localの更新
            self.param.local = job_id

            # SalmonStatsにアップロードする
            if FLAG_SALMON_STATS:
                if job_id > self.param.salmonstats:
                    self.upload(job_id)

            # config.jsonを書き出す
            self.param.output()

if __name__ == "__main__":
    # SalmonRecインスタンスを作成
    user = SalmonRec()

    # jsonフォルダ内のjsonファイルをすべてアップロードする
    if FLAG_SALMON_STATS:
        user.uploadAll()
    else:
        print(datetime.now().strftime("%H:%M:%S ") + "No upload to SalmonStats.")

    print(datetime.now().strftime("%H:%M:%S ") + "Waiting New Result.")

    while True:
        user.getResults()
        sleep(10)