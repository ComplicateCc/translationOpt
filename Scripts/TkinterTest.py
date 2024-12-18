# -*- coding: utf-8 -*-

#绘制一个窗口，设置窗口标题
import tkinter as tk
from tkinter import filedialog

window = tk.Tk()
window.title('翻译整理工具')

#设置窗口大小
window.geometry('500x300')

#设置窗口内容
#设置标签
l = tk.Label(window, text='翻译整理工具', bg='green', font=('Arial', 12), width=30, height=2)
l.pack()

#设置打开按钮 读取文本
def open_file():
    print('打开文件')
    file_path = tk.filedialog.askopenfilename()
    print(file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            print(line)

b1 = tk.Button(window, text='打开文件', width=15, height=2, command=open_file)
b1.pack()

#设置保存按钮 保存文本
def save_file():
    print('保存文件')
    file_path = tk.filedialog.asksaveasfilename()
    print(file_path)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('Hello, world!')

b2 = tk.Button(window, text='保存文件', width=15, height=2, command=save_file)
b2.pack()

#设置文本框
t = tk.Text(window, height=2)
t.pack()

#设置主循环

window.mainloop()

