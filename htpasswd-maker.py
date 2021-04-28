import PySimpleGUI as sg
import bcrypt
import os


path_file = (os.path.dirname(os.path.abspath(__file__)) + '\\.htpasswd')

### window のテーマ ###
sg.theme('Reddit')

### ボタン関係の設定 ###
s_button_enter = sg.Button("Run", font=("Meiryo", 10), size=(5, 1), key="btn_run")
s_button_exit = sg.Button("Exit", font=("Meiryo", 10), size=(5, 1), key="btn_exit", button_color=("#43576b"))

### レイアウトの設定 ###
layout_1 = sg.Text('htpasswd MakingTool', font=('Meiryo', 16, "bold"), text_color=("#161f82")),

layout_2 = sg.Frame ('InPut ID/PW',[
                    [sg.Text(' ID:', font=("Meiryo", 11), size=(3, 1)), sg.InputText(key="-Input-ID-", size=(35, 1))],
                    [sg.Text('PW:', font=("Meiryo", 11), size=(3, 1)), sg.InputText(key="-Input-PW-", size=(35, 1))],
                    [sg.Button("Run", font=("Meiryo", 10), size=(5, 1), key="btn_run"),
                     sg.Button("Exit", font=("Meiryo", 10), size=(5, 1), key="btn_exit", button_color=("#43576b")),
                    sg.Text("                            "),
                     sg.Button("Load", font=("Meiryo", 10), size=(5, 1),key="btn_load")]
                    ],
                relief=sg.RELIEF_SUNKEN, font=("Meiryo", 10, 'bold'), title_color='NAVY', tooltip='登録したいID/PWを入力してね！')

layout_3 = sg.Frame ('Redirect',[
                    [sg.Multiline(size=(83, 10), font=("Meiryo", 10), border_width=2, key='-Ridai-', background_color=("#6d86a1"), text_color=("#edf9ff"))],
                    ],
                relief=sg.RELIEF_SUNKEN, font=("Meiryo", 10, 'bold'), title_color='NAVY')


layout_0 = [
            [layout_1],
            [layout_2],
            [layout_3],
           ]

# セクション 2 - ウィンドウの生成
window = sg.Window('htpasswd MakingTool', layout_0)


# セクション 3 - イベント

##起動時のhtpasswdファイルの新規作成or追記確認
choice = sg.popup_ok_cancel('.htpasswdファイルを新規に作成しますか？ \n [Cancel]=追記')

if choice == 'OK':
        file = open(path_file, 'w') # "w" 書き込みモードで開く。ファイルが存在しない時は新規作成される
        file.close()
        os.remove(path_file) #htpasswdファイルの削除
else:
    #print('tewwwww')
    file = open(path_file, 'a', encoding='UTF-8') # "a 追加書き込みで開く。ファイルが存在しない時は新規作成される
    file.close()


##htpasswd作成処理
while True:
    event, values = window.read()
    print(values)

    #バツボタンの処理
    if event is None:
        break
    #Exitボタンの処理
    if event == "btn_exit":
        show_message_end = "ツールを終了します。 \n"
        value = sg.popup_ok_cancel(show_message_end )
        if value == 'OK':
            show_message_save = ".htpasswdファイルは自動保存されます。"
            sg.popup(show_message_save)
            break
        else:
             continue


    #ID/PWの値の取り出しと出力
    #keyと値を代入
    mydict = values # {'-Input-ID-': '', '-Input-PW-': ''} を代入
                        #print(mydict.get('-Input-ID-'))　 #valuseの中身確認　キー'-Input-ID-'の値を確認
    #キー'-Input-ID-'の値を取り出す          #print(mydict.get('-Input-PW-'))　 #valuseの中身確認　キー'-Input-PD-'の値を確認
    dict_ID = (mydict.get('-Input-ID-'))
    # キー'-Input-PW-'の値を取り出す
    dict_PW = (mydict.get('-Input-PW-'))
    # 空白の判定
    if event == "btn_run":
        if not dict_ID or not dict_PW:
                sg.Popup("値をすべて入力して下さい。")
                continue

    #PW作成
    if event == "btn_run":
        # ポップアップID
        ID = (values["-Input-ID-"])
        pw = (values["-Input-PW-"])
        # 暗号化のバージョンを "2a"に指定。
        salt = bcrypt.gensalt(rounds=10, prefix=b'2a')
        # パスワードをハッシュ化
        hashed = bcrypt.hashpw(pw.encode('utf-8'), salt)
        ##bcrypt.checkpw(pw.encode('utf-8'), hashed) # パスワードを検証
        #print(hashed)  #パスワードのハッシュ値確認
        #print(values["-Input-ID-"])  #入力ID確認

    #.htpasswdへの出力
        #.htpasswdファルのオープン
        f = open(path_file, 'a', encoding='UTF-8')
        #.htpasswdファルへの書き込み
        f.write(dict_ID + ':' + hashed.decode() + '\n')

        # IDテキストボックスをクリアさせる
        window['-Input-ID-'].update("")
        # PWテキストボックスをクリアさせる
        window['-Input-PW-'].update("")

        f.close()
        ##'Redirect'欄への出力
        file = open(path_file, 'r', encoding='UTF-8')
        string = file.read()
        window['-Ridai-'].update("")
        window['-Ridai-'].print(string)
        file.close()

##htpasswdファイルの読み込み
    if event == "btn_load" and os.path.isfile(path_file) is True:
            print("btn_load")
            file = open(path_file, 'r', encoding='UTF-8')  # "w+" 読み書き両対応で開く。ファイルが存在しない時は新規作成される
            string = file.read()
            window['-Ridai-'].update("")
            window['-Ridai-'].print(string)
            file.close()
            continue
    else:
            print('not-eror')
            continue


 # セクション 4 - ウィンドウの破棄と終了
window.close()
