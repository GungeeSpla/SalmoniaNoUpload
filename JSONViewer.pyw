import tkinter as tk
import tkinter.ttk as ttk
import os
import sys
import json
from datetime import datetime
from tkinter import messagebox

class Viewer():
    
    def show_shift(self):
        if self.state != "shift":
            self.state = "shift"
        self.detail_frame_1.pack_forget()
        self.detail_frame_2.pack_forget()
        self.list_frame_1.pack()
        self.list_frame_2.pack()
    
    def show_detail(self):
        if self.state != "detail":
            self.state = "detail"
        self.list_frame_1.pack_forget()
        self.list_frame_2.pack_forget()
        self.detail_frame_1.pack()
        self.detail_frame_2.pack()

    # コンストラクタ
    def __init__(self):
        self.page_num = 0
        self.json_num = 0
        self.job_count_per_page = 6
        self.state = "list"

        root = tk.Tk()
        root.title("JSON Viewer")
        root.geometry("1050x600")
        # root.iconbitmap(default="Salmonia.ico")

        self.list_frame_1 = tk.Frame(root, bg="#eeeeee")
        self.list_frame_1.pack()

        self.list_frame_2 = tk.Frame(root, bg="#ffffff")
        self.list_frame_2.pack()

        btn = tk.Button(self.list_frame_1, text="最初のページ", command=self.first)
        btn.pack(padx=20, pady=20, side="left")

        btn = tk.Button(self.list_frame_1, text="前のページ", command=self.prev)
        btn.pack(padx=20, pady=20, side="left")

        self.page_label = tk.Label(self.list_frame_1, text="1")
        self.page_label.pack(padx=20, pady=20, side="left")

        btn = tk.Button(self.list_frame_1, text="次のページ", command=self.next)
        btn.pack(padx=20, side="left")

        btn = tk.Button(self.list_frame_1, text="最後のページ", command=self.end)
        btn.pack(padx=20, pady=20, side="left")

        btn = tk.Button(self.list_frame_1, text="選択したバイトの詳細を見る", command=self.trans_detail)
        btn.pack(padx=20, pady=20, side="left")

        btn = tk.Button(self.list_frame_1, text="更新", command=self.update)
        btn.pack(padx=20, pady=20, side="left")

        tree = ttk.Treeview(self.list_frame_2, selectmode="browse")
        tree["column"] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
        tree["show"] = "headings"
        tree["height"] = self.job_count_per_page * 4
        tree.heading(1, text="バイトID")
        tree.heading(2, text="ステージ")
        tree.heading(3, text="プレイ開始時刻")
        tree.heading(4, text="キケン度")
        tree.heading(5, text="Wave")
        tree.heading(6, text="潮位")
        tree.heading(7, text="イベント")
        tree.heading(8, text="金イクラ")
        tree.heading(9, text="出現数")
        tree.heading(10, text="ノルマ")
        tree.heading(11, text="赤イクラ")
        tree.heading(12, text="味方1")
        tree.heading(13, text="味方2")
        tree.heading(14, text="味方3")
        tree.column(1, width=60, anchor=tk.CENTER)
        tree.column(2, width=120, anchor=tk.CENTER)
        tree.column(3, width=120, anchor=tk.CENTER)
        tree.column(4, width=50, anchor=tk.CENTER)
        tree.column(5, width=40, anchor=tk.CENTER)
        tree.column(6, width=40, anchor=tk.CENTER)
        tree.column(7, width=100, anchor=tk.CENTER)
        tree.column(8, width=50, anchor=tk.CENTER)
        tree.column(9, width=50, anchor=tk.CENTER)
        tree.column(10, width=50, anchor=tk.CENTER)
        tree.column(11, width=50, anchor=tk.CENTER)
        tree.column(12, width=100)
        tree.column(13, width=100)
        tree.column(14, width=100)
        tree.tag_configure("total", background="#c2e0ff")
        tree.pack(anchor=tk.N)
        self.shift_tree = tree
        self.root = root
        self.get_job_id_list()
        self.update_treeview()

        self.detail_frame_1 = tk.Frame(root, bg="#eeeeee")
        self.detail_frame_2 = tk.Frame(root, bg="#ffffff")

        btn = tk.Button(self.detail_frame_1, text="最初のページ", command=self.first)
        btn.pack(padx=20, pady=20, side="left")

        btn = tk.Button(self.detail_frame_1, text="前のページ", command=self.prev)
        btn.pack(padx=20, pady=20, side="left")

        self.json_label = tk.Label(self.detail_frame_1, text="1")
        self.json_label.pack(padx=20, pady=20, side="left")

        btn = tk.Button(self.detail_frame_1, text="次のページ", command=self.next)
        btn.pack(padx=20, side="left")

        btn = tk.Button(self.detail_frame_1, text="最後のページ", command=self.end)
        btn.pack(padx=20, pady=20, side="left")

        btn = tk.Button(self.detail_frame_1, text="最新", command=self.update)
        btn.pack(padx=20, pady=20, side="left")

        btn = tk.Button(self.detail_frame_1, text="一覧に戻る", command=self.trans_list)
        btn.pack(padx=20, pady=20, side="left")

        self.detail_frame_2_1 = tk.Frame(self.detail_frame_2, bg="#ffffff")
        self.detail_frame_2_1.pack()

        self.detail_frame_2_2 = tk.Frame(self.detail_frame_2, bg="#ffffff")
        self.detail_frame_2_2.pack()

        root.mainloop()

    def trans_list(self):
        self.state = "list"
        self.detail_frame_1.pack_forget()
        self.detail_frame_2.pack_forget()
        self.list_frame_1.pack()
        self.list_frame_2.pack()

    def trans_detail(self):
        selected_items = self.shift_tree.selection()
        if not selected_items:
            return
        job_id = self.shift_tree.item(selected_items[0])['values'][0]
        if job_id == "":
            return
            # num = int(selected_items[0].replace("I", ""))
            # for i in range(3):
            #     num -= 1
            #     item = "I" + str(num).zfill(3)
            #     id = self.shift_tree.item(item)['values'][0]
            #     if id != "":
            #         job_id = id
            #         break
            # if job_id == "":
            #     return
        self.state = "detail"
        self.list_frame_1.pack_forget()
        self.list_frame_2.pack_forget()
        self.detail_frame_1.pack()
        self.detail_frame_2.pack()
        children = self.detail_frame_2_1.winfo_children()
        for child in children:
            child.destroy()
        children = self.detail_frame_2_2.winfo_children()
        for child in children:
            child.destroy()
        self.json_num = self.job_id_list.index(str(job_id))
        self.make_detail_tree(job_id)

    def make_detail_tree(self, job_id):
        path = "json/" + str(job_id) + ".json"
        if not os.path.isfile(path):
            messagebox.showerror("エラー", path + " が存在しません。")
            self.get_job_id_list()
            self.page_num = 0
            self.json_num = 0
            self.update_treeview()
            self.trans_list()
            return

        with open(path) as f:
            # jsonの読み込み
            data = json.load(f)

            # ラベルの変更
            self.json_label["text"] = str(job_id) + ".json"

            # スケジュールツリー
            tree = ttk.Treeview(self.detail_frame_2_1, selectmode="browse")
            tree["column"] = (1, 2, 3, 4, 5, 6, 7)
            tree["show"] = "headings"
            tree.heading( 1, text="ステージ")
            tree.heading( 2, text="ブキ1")
            tree.heading( 3, text="ブキ2")
            tree.heading( 4, text="ブキ3")
            tree.heading( 5, text="ブキ4")
            tree.heading( 6, text="開始時刻")
            tree.heading( 7, text="終了時刻")
            tree.column( 1, width=120, anchor=tk.CENTER)
            tree.column( 2, width=120, anchor=tk.CENTER)
            tree.column( 3, width=120, anchor=tk.CENTER)
            tree.column( 4, width=120, anchor=tk.CENTER)
            tree.column( 5, width=120, anchor=tk.CENTER)
            tree.column( 6, width=120, anchor=tk.CENTER)
            tree.column( 7, width=120, anchor=tk.CENTER)
            tree["height"] = 1
            tree.pack(padx=10, pady=10, anchor=tk.NW, side="top")
            tree.insert("", "end", tags=[], values=(
                data["schedule"]["stage"]["name"],
                data["schedule"]["weapons"][0]["weapon"]["name"] if "weapon" in data["schedule"]["weapons"][0] else "ランダム",
                data["schedule"]["weapons"][1]["weapon"]["name"] if "weapon" in data["schedule"]["weapons"][1] else "ランダム",
                data["schedule"]["weapons"][2]["weapon"]["name"] if "weapon" in data["schedule"]["weapons"][2] else "ランダム",
                data["schedule"]["weapons"][3]["weapon"]["name"] if "weapon" in data["schedule"]["weapons"][3] else "ランダム",
                datetime.fromtimestamp(data["schedule"]["start_time"]),
                datetime.fromtimestamp(data["schedule"]["end_time"])
            ))

            # 総合リザルトツリー
            tree = ttk.Treeview(self.detail_frame_2_1, selectmode="browse")
            tree["column"] = (1, 2, 3, 4, 5, 6)
            tree["show"] = "headings"
            tree.heading( 1, text="バイトID")
            tree.heading( 2, text="プレイ開始時刻")
            tree.heading( 3, text="キケン度")
            tree.heading( 4, text="結果")
            tree.heading( 5, text="金イクラ")
            tree.heading( 6, text="赤イクラ")
            tree.column( 1, width=60, anchor=tk.CENTER)
            tree.column( 2, width=120, anchor=tk.CENTER)
            tree.column( 3, width=100, anchor=tk.CENTER)
            tree.column( 4, width=100, anchor=tk.CENTER)
            tree.column( 5, width=100, anchor=tk.CENTER)
            tree.column( 6, width=100, anchor=tk.CENTER)
            tree.pack(padx=10, pady=10, anchor=tk.NW, side="top")
            tree["height"] = 1
            golden_ikura_num = 0
            ikura_num = 0
            for detail in data["wave_details"]:
                golden_ikura_num += detail["golden_ikura_num"]
                ikura_num += detail["ikura_num"]
            tree.insert("", "end", tags=[], values=(
                data["job_id"],
                datetime.fromtimestamp(data["play_time"]),
                data["danger_rate"],
                "クリア" if data["job_result"]["is_clear"] else "失敗",
                golden_ikura_num,
                ikura_num
            ))

            # プレイヤーリザルトツリー
            tree = ttk.Treeview(self.detail_frame_2_1, selectmode="browse")
            tree["column"] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)
            tree["show"] = "headings"
            tree.heading( 1, text="名前")
            tree.heading( 2, text="スペシャルウェポン")
            tree.heading( 3, text="w1")
            tree.heading( 4, text="w2")
            tree.heading( 5, text="w3")
            tree.heading( 6, text="メインウェポン(w1)")
            tree.heading( 7, text="メインウェポン(w2)")
            tree.heading( 8, text="メインウェポン(w3)")
            tree.heading( 9, text="救助")
            tree.heading(10, text="デス")
            tree.heading(11, text="オオモノ")
            tree.heading(12, text="金イクラ")
            tree.heading(13, text="赤イクラ")
            tree.column( 1, width=100)
            tree.column( 2, width=100)
            tree.column( 3, width=30, anchor=tk.CENTER)
            tree.column( 4, width=30, anchor=tk.CENTER)
            tree.column( 5, width=30, anchor=tk.CENTER)
            tree.column( 6, width=100)
            tree.column( 7, width=100)
            tree.column( 8, width=100)
            tree.column( 9, width=50, anchor=tk.CENTER)
            tree.column(10, width=50, anchor=tk.CENTER)
            tree.column(11, width=50, anchor=tk.CENTER)
            tree.column(12, width=50, anchor=tk.CENTER)
            tree.column(13, width=50, anchor=tk.CENTER)
            tree.tag_configure("even", background="#f2f2f2")
            tree.pack(padx=10, pady=10, anchor=tk.N, side="top")
            player_count = 1 + len(data["other_results"])
            tree["height"] = player_count
            for i in range(player_count):
                result = self.get_player_result(data, i)
                tags = []
                if (i + 1) % 2 == 0:
                    tags.append("even")
                total_boss_kill_count = self.get_total_boss_kill_count(result)
                while len(result["special_counts"]) < 3:
                    result["special_counts"].append("-")
                while len(result["weapon_list"]) < 3:
                    result["weapon_list"].append({"weapon": {"name": "-"}})
                tree.insert("", "end", tags=tags, values=(
                    result["name"],
                    result["special"]["name"].replace("スプラッシュ", ""),
                    result["special_counts"][0],
                    result["special_counts"][1],
                    result["special_counts"][2],
                    result["weapon_list"][0]["weapon"]["name"],
                    result["weapon_list"][1]["weapon"]["name"],
                    result["weapon_list"][2]["weapon"]["name"],
                    result["help_count"],
                    result["dead_count"],
                    total_boss_kill_count,
                    result["golden_ikura_num"],
                    result["ikura_num"]
                ))
            
            # オオモノ討伐数ツリー
            tree = ttk.Treeview(self.detail_frame_2_2, selectmode="browse")
            column = [1]
            for i in range(player_count):
                column.append(i + 2)
            column.append(6)
            column.append(7)
            column.append(8)
            tree["column"] = column
            tree["show"] = "headings"
            tree["height"] = 4
            tree.heading(1, text="オオモノ")
            for i in range(player_count):
                result = self.get_player_result(data, i)
                tree.heading(i + 2, text=result["name"])
            tree.heading(2 + player_count, text="合計討伐数")
            tree.heading(3 + player_count, text="出現数")
            tree.heading(4 + player_count, text="全討伐")
            for i in range(4 + player_count):
                tree.column(i + 1, width=50, anchor=tk.CENTER)
            tree.column(1, width=80)
            tree.tag_configure("even", background="#f2f2f2")
            tree.pack(padx=10, pady=10, anchor=tk.N, side="left")
            insert_num = 0
            for key in data["boss_counts"]:
                tags = []
                if (insert_num + 1) % 2 == 0:
                    tags.append("even")
                values = [ data["boss_counts"][key]["boss"]["name"] ]
                total_count = 0
                for i in range(player_count):
                    result = self.get_player_result(data, i)
                    count = result["boss_kill_counts"][key]["count"]
                    values.append(count)
                    total_count += count
                values.append(total_count)
                values.append(data["boss_counts"][key]["count"])
                if (total_count == data["boss_counts"][key]["count"]):
                    values.append("")
                else:
                    values.append("×")
                tree.insert("", "end", tags=tags, values=values)
                insert_num += 1
            values = ["合計"]
            tags = []
            if (insert_num + 1) % 2 == 0:
                tags.append("even")
            total_kill = 0
            for i in range(player_count):
                result = self.get_player_result(data, i)
                total_boss_kill_count = self.get_total_boss_kill_count(result)
                values.append(total_boss_kill_count)
                total_kill += total_boss_kill_count
            values.append(total_kill)
            total_pop = 0
            for key in data["boss_counts"]:
                total_pop += data["boss_counts"][key]["count"]
            values.append(total_pop)
            if (total_kill == total_pop):
                values.append("")
            else:
                values.append("×")
            tree.insert("", "end", tags=tags, values=values)
            insert_num += 1
            tree["height"] = insert_num
            
            # ウェーブツリー
            tree = ttk.Treeview(self.detail_frame_2_2, selectmode="browse")
            wave_count = len(data["wave_details"])
            column = [1]
            for i in range(wave_count):
                column.append(i + 2)
            tree["column"] = column
            for i in range(1 + wave_count):
                tree.column(i + 1, width=110, anchor=tk.CENTER)
            tree.column(1, width=57)
            tree["show"] = "headings"
            tree["height"] = 6
            tree.heading(1, text="")
            for i in range(wave_count):
                tree.heading(i + 2, text=("WAVE " + str(i + 1)))
            tree.tag_configure("even", background="#f2f2f2")
            tree.pack(padx=10, pady=10, anchor=tk.N, side="left")

            values = ["潮位"]
            for detail in data["wave_details"]:
                values.append(detail["water_level"]["name"])
            tree.insert("", "end", tags=[], values=values)

            values = ["イベント"]
            for detail in data["wave_details"]:
                values.append(detail["event_type"]["name"])
            tree.insert("", "end", tags=["even"], values=values)

            values = ["金イクラ"]
            for detail in data["wave_details"]:
                values.append(detail["golden_ikura_num"])
            tree.insert("", "end", tags=[], values=values)

            values = ["出現数"]
            for detail in data["wave_details"]:
                values.append(detail["golden_ikura_pop_num"])
            tree.insert("", "end", tags=["even"], values=values)

            values = ["ノルマ"]
            for detail in data["wave_details"]:
                values.append(detail["quota_num"])
            tree.insert("", "end", tags=[], values=values)

            values = ["赤イクラ"]
            for detail in data["wave_details"]:
                values.append(detail["ikura_num"])
            tree.insert("", "end", tags=["even"], values=values)

    def get_player_result(self, data, i):
        return data["my_result"] if i == 0 else data["other_results"][i - 1]

    def get_total_boss_kill_count(self, result):
        sum = 0
        for key in result["boss_kill_counts"]:
            sum += result["boss_kill_counts"][key]["count"]
        return sum

    def update(self):
        self.get_job_id_list()
        if self.state == "list":
            self.page_num = 0
            self.update_treeview()
        else:
            self.json_num = 0
            self.update_detail()


    def get_job_id_list(self):
        dir = os.listdir()
        if "json" in dir:
            file = []
            dir = os.listdir("json")
            for p in dir:
                if ".json" in p:
                    file.append(p[0:-5])
            file.sort(key=int, reverse=True)
            self.job_id_list = file
            self.max_page_num = -(-len(file) // self.job_count_per_page) - 1
        else:
            self.job_id_list = []
            self.max_page_num = 0

    def update_label(self):
        self.page_label["text"] = str(self.page_num + 1) + "/" + str(self.max_page_num + 1)

    def update_treeview(self):
        self.update_label()
        tree = self.shift_tree
        for item in tree.get_children():
            tree.delete(item)
        for i in range(self.job_count_per_page):
            tags = []
            job_id_index = self.page_num * self.job_count_per_page + i
            if job_id_index >= len(self.job_id_list):
                break
            job_id = self.job_id_list[job_id_index]
            path = os.path.dirname(os.path.abspath(sys.argv[0])) + "/json/" + str(job_id) + ".json"
            f = open(path, "r")
            json_data = json.load(f)
            wave_count = len(json_data["wave_details"])

            while len(json_data["other_results"]) < 3:
                json_data["other_results"].append({"name": "-"})
            
            total_ikura_num = 0
            total_golden_ikura_num = 0
            total_golden_ikura_pop_num = 0
            total_quota_num = 0
            for wave_detail in json_data["wave_details"]:
                total_ikura_num += wave_detail["ikura_num"]
                total_golden_ikura_num += wave_detail["golden_ikura_num"]
                total_golden_ikura_pop_num += wave_detail["golden_ikura_pop_num"]
                total_quota_num += wave_detail["quota_num"]
            tree.insert("", "end", tags=["total"], values=(
                json_data["job_id"],
                json_data["schedule"]["stage"]["name"],
                datetime.fromtimestamp(json_data["play_time"]),
                json_data["danger_rate"],
                "",
                "",
                "",
                total_golden_ikura_num,
                total_golden_ikura_pop_num,
                total_quota_num,
                total_ikura_num,
                json_data["other_results"][0]["name"],
                json_data["other_results"][1]["name"],
                json_data["other_results"][2]["name"]
            ))
            
            for wave_num in range(wave_count):
                wave_detail = json_data["wave_details"][wave_num]
                tree.insert("", "end", tags=tags, values=(
                    "",
                    "",
                    "",
                    "",
                    wave_num + 1,
                    wave_detail["water_level"]["name"],
                    wave_detail["event_type"]["name"],
                    wave_detail["golden_ikura_num"],
                    wave_detail["golden_ikura_pop_num"],
                    wave_detail["quota_num"],
                    wave_detail["ikura_num"],
                    "",
                    "",
                    ""
                ))

    def update_detail(self):
        children = self.detail_frame_2_1.winfo_children()
        for child in children:
            child.destroy()
        children = self.detail_frame_2_2.winfo_children()
        for child in children:
            child.destroy()
        self.make_detail_tree(self.job_id_list[self.json_num])

    def first(self):
        if self.state == "list":
            self.page_num = 0
            self.update_treeview()
        else:
            self.json_num = 0
            self.update_detail()

    def end(self):
        if self.state == "list":
            self.page_num = self.max_page_num
            self.update_treeview()
        else:
            self.json_num = len(self.job_id_list) - 1
            self.update_detail()

    def next(self):
        if self.state == "list":
            if self.page_num < self.max_page_num:
                self.page_num += 1
                self.update_treeview()
        else:
            if self.page_num < len(self.job_id_list) - 1:
                self.json_num += 1
                self.update_detail()

    def prev(self):
        if self.state == "list":
            if self.page_num > 0:
                self.page_num -= 1
                self.update_treeview()
        else:
            if self.json_num > 0:
                self.json_num -= 1
                self.update_detail()

if __name__ == "__main__":
    viewer = Viewer()