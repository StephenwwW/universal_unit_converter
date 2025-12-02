import tkinter as tk
from tkinter import ttk

class PriceCalculator:
    def __init__(self, master):
        self.master = master
        master.title("價格計算器")

        self.data = []
        self.entries = []
        self.results = []
        self.cheapest_labels = []
        self.row_counter = 0

        # 標題
        ttk.Label(master, text="每克計算", font=("Arial", 16)).grid(row=0, column=0, columnspan=6, pady=10)

        # 比較方式選擇
        self.compare_var = tk.StringVar(value="per_gram")
        ttk.Radiobutton(master, text="每1g", variable=self.compare_var, value="per_gram").grid(row=1, column=0, sticky="w")
        ttk.Radiobutton(master, text="每100g", variable=self.compare_var, value="per_100g").grid(row=1, column=1, sticky="w")
        ttk.Radiobutton(master, text="每1元", variable=self.compare_var, value="per_yuan").grid(row=1, column=2, sticky="w")

        # 表格標題
        ttk.Label(master, text="重量(克)").grid(row=2, column=0, padx=5, pady=5)
        ttk.Label(master, text="價格(元)").grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(master, text="每1g").grid(row=2, column=2, padx=5, pady=5)
        ttk.Label(master, text="每100g").grid(row=2, column=3, padx=5, pady=5)
        ttk.Label(master, text="每1元").grid(row=2, column=4, padx=5, pady=5)

        # 新增比較項目按鈕
        add_button = ttk.Button(master, text="新增比較項目", command=self.add_item)
        add_button.grid(row=1, column=3, columnspan=2, pady=5)

        # 計算按鈕
        calculate_button = ttk.Button(master, text="計算並比較", command=self.calculate)
        calculate_button.grid(row=20, column=0, columnspan=6, pady=10) # 將計算按鈕放在較下方

        self.add_item() # 預先新增至少一組輸入框
        self.add_item()
        self.add_item()

    def add_item(self):
        row_num = self.row_counter + 3
        weight_entry = ttk.Entry(self.master, width=10)
        weight_entry.grid(row=row_num, column=0, padx=5, pady=5)
        price_entry = ttk.Entry(self.master, width=10)
        price_entry.grid(row=row_num, column=1, padx=5, pady=5)
        self.entries.append((weight_entry, price_entry))

        per_gram_label = ttk.Label(self.master, text="")
        per_gram_label.grid(row=row_num, column=2, padx=5, pady=5)
        per_100g_label = ttk.Label(self.master, text="")
        per_100g_label.grid(row=row_num, column=3, padx=5, pady=5)
        per_yuan_label = ttk.Label(self.master, text="")
        per_yuan_label.grid(row=row_num, column=4, padx=5, pady=5)
        self.results.append((per_gram_label, per_100g_label, per_yuan_label))

        cheapest_label = ttk.Label(self.master, text="")
        cheapest_label.grid(row=row_num, column=5, padx=5, pady=5)
        self.cheapest_labels.append(cheapest_label)

        self.row_counter += 1

    def calculate(self):
        self.data = []
        for i in range(len(self.entries)):
            try:
                weight = float(self.entries[i][0].get())
                price = float(self.entries[i][1].get())
                self.data.append({'weight': weight, 'price': price})
            except ValueError:
                # 如果輸入格式錯誤，則跳過此項目
                self.results[i][0].config(text="請輸入數字")
                self.results[i][1].config(text="請輸入數字")
                self.results[i][2].config(text="請輸入數字")
                continue

        # 清除之前的計算結果和標示
        for i in range(len(self.results)):
            self.results[i][0].config(text="")
            self.results[i][1].config(text="")
            self.results[i][2].config(text="")
            self.cheapest_labels[i].config(text="", foreground="black", font=("Arial", 10))

        valid_data_indices = []
        for i, item in enumerate(self.data):
            if item['weight'] > 0:
                per_gram = item['price'] / item['weight']
                per_100g = per_gram * 100
                per_yuan = item['weight'] / item['price'] if item['price'] > 0 else 0
            else:
                per_gram = 0
                per_100g = 0
                per_yuan = 0

            # 找到 self.entries 中對應的索引
            original_index = -1
            data_index_counter = 0
            for j in range(len(self.entries)):
                try:
                    w = float(self.entries[j][0].get())
                    p = float(self.entries[j][1].get())
                    if data_index_counter == i:
                        original_index = j
                        valid_data_indices.append(j)
                        break
                    data_index_counter += 1
                except ValueError:
                    continue

            if original_index != -1:
                self.results[original_index][0].config(text=f"{per_gram:.2f}元")
                self.results[original_index][1].config(text=f"{per_100g:.2f}元")
                self.results[original_index][2].config(text=f"{per_yuan:.2f}克")

        self.highlight_cheapest(valid_data_indices)

    def highlight_cheapest(self, valid_indices):
        compare_type = self.compare_var.get()
        best_value = None
        best_index = -1

        if not valid_indices:
            return

        for index in valid_indices:
            try:
                weight = float(self.entries[index][0].get())
                price = float(self.entries[index][1].get())

                if weight > 0 and price >= 0: # 允許價格為0的情況
                    if compare_type == "per_gram":
                        value = price / weight
                        if best_value is None or value < best_value:
                            best_value = value
                            best_index = index
                    elif compare_type == "per_100g":
                        value = (price / weight) * 100
                        if best_value is None or value < best_value:
                            best_value = value
                            best_index = index
                    elif compare_type == "per_yuan":
                        if price > 0:
                            value = weight / price
                            if best_value is None or value > best_value:
                                best_value = value
                                best_index = index
                        elif weight > 0 and price == 0: # 如果價格為0，則視為最便宜 (無限大)
                            if best_value is None or float('inf') > best_value:
                                best_value = float('inf')
                                best_index = index
            except ValueError:
                continue # 忽略格式錯誤的行

        if best_index != -1:
            self.cheapest_labels[best_index].config(text="最便宜的", foreground="green", font=("Arial", 10, "bold"))


if __name__ == "__main__":
    root = tk.Tk()
    app = PriceCalculator(root)
    root.mainloop()