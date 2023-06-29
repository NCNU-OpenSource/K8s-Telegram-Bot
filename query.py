from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import daemon, sys, requests, logging, configparser, logging.handlers
from subprocess import call, PIPE, run, Popen
import mysql.connector, re
import configparser

# home path
home_path = '/home/tommygood/telegram_bot'

# config
config = configparser.ConfigParser()
config.read(home_path + '/config.ini')
token = config["env"]["bot_token"]

# db
db_user = config["db"]["user"]
db_password = config["db"]["password"]
db_host = config["db"]["host"]
db_port = config["db"]["port"] 
db = config["db"]["database"]

# bot token
#token = "6062324742:AAEqo43jhwayn0kmF-9SnnnZ8ZLCbOZcVEg"

# db
def connectDB():
    conn = mysql.connector.connect(
            user = db_user,
            password = db_password,
            host = db_host,
            port = db_port,
            database = db
    )
    cur = conn.cursor()
    return conn,cur

# check user 確認使用者是否已註冊
def checkuser(uid):
    sql = "select * from all_user where uid=%s;"
    conn,cur = connectDB()
    cur.execute(sql,(str(uid),))
    record = cur.fetchall()
    if len(record)==0:
        return 0
    else:
        return record

# check command 確認使用者可以使用該指令
def checkcommand(permission,command):
    sql = "select * from all_command where name=%s;"
    conn,cur = connectDB()
    cur.execute(sql,(command,))
    record = cur.fetchall()
    if permission <= record[0][2]:
        return True
    else:
        return False
# check namespace 找該使用者的所有namespace
def checknamespace(uid):
    sql = "select name from all_namespace where uid=%s;"
    conn,cur = connectDB()
    cur.execute(sql,(uid,))
    record = cur.fetchall()
    namespace = []
    for i in range(len(record)):
        namespace.append(record[i][0])
    return namespace

#
async def podMemUseInNode(update,context) :
    record = checkuser(update.message.from_user.id)
    if record == 0:
        await update.message.reply_text("user "+str(update.message.from_user.id)+" not registered"+"\n"+"use /au to regist")
    else:
        utype = record[0][2]
        result = checkcommand(utype,update.message.text)
        if result == False:
            await update.message.reply_text("您沒有權限執行該指令!")
        else:
            result = run(["python3", f"{home_path}/call_prom.py", '-t', 'podMemUseInNode'], stdout=PIPE, stderr=PIPE, universal_newlines=True)
            #await update.message.reply_text(os.getcwd())
            output_len = int(result.stdout.split(':')[1])
            for i in range(output_len) :
                #send_photo(f'{home_path}/image/output{i}.png')
                with open(f'{home_path}/image/output{i}.png', 'rb') as file:
                    await update.message.reply_photo(photo=file)

#
async def eachConatinerMemUsage(update,context) :
    record = checkuser(update.message.from_user.id)
    if record == 0:
        await update.message.reply_text("user "+str(update.message.from_user.id)+" not registered"+"\n"+"use /au to regist")
    else:
        utype = record[0][2]
        result = checkcommand(utype,update.message.text)
        if result == False:
            await update.message.reply_text("您沒有權限執行該指令!")
        else:
            namespace = []
            if utype == 1:
                namespace = ['']# k8s namespace
            else:
                namespace = checknamespace(update.message.from_user.id)
            for i in range(len(namespace)):
                result = run(["python3", f"{home_path}/call_prom.py", '-t', 'eachConatinerMemUsage', '-n', namespace[i]], stdout=PIPE, stderr=PIPE, universal_newlines=True)
                #await update.message.reply_text(os.getcwd())
                print(result.stdout)
                output_len = int(result.stdout.split(':')[1])
                for j in range(output_len) :
                    #send_photo(f'{home_path}/image/output{i}.png')
                    with open(f'{home_path}/image/output{j}.png', 'rb') as file:
                        await update.message.reply_photo(photo=file)

#
async def weirdPodNumInNamespace(update,context) :
    record = checkuser(update.message.from_user.id)
    if record == 0:
        await update.message.reply_text("user "+str(update.message.from_user.id)+" not registered"+"\n"+"use /au to regist")
    else:
        utype = record[0][2]
        result = checkcommand(utype,update.message.text)
        if result == False:
            await update.message.reply_text("您沒有權限執行該指令!")
        else:
            namespace = []
            if utype == 1:
                namespace = ['']# k8s namespace
            else:
                namespace = checknamespace(update.message.from_user.id)
            for i in range(len(namespace)):
                result = run(["python3", f"{home_path}/call_prom.py", '-t', 'weirdPodNumInNamespace', '-n', namespace[i]], stdout=PIPE, stderr=PIPE, universal_newlines=True)
                #await update.message.reply_text(os.getcwd())
                print(result.stdout)
                print(result.stdout.split(':'))
                output_len = int(result.stdout.split(':')[1])
                for j in range(output_len) :
                    #send_photo(f'{home_path}/image/output{i}.png')
                    with open(f'{home_path}/image/output{j}.png', 'rb') as file:
                        await update.message.reply_photo(photo=file)

#
async def runningPodNumInNamespace(update,context) :
    record = checkuser(update.message.from_user.id)
    if record == 0:
        await update.message.reply_text("user "+str(update.message.from_user.id)+" not registered"+"\n"+"use /au to regist")
    else:
        utype = record[0][2]
        result = checkcommand(utype,update.message.text)
        if result == False:
            await update.message.reply_text("您沒有權限執行該指令!")
        else:
            namespace = []
            if utype == 1:
                namespace = ['']# k8s namespace
            else:
                namespace = checknamespace(update.message.from_user.id)
            for i in range(len(namespace)):
                result = run(["python3", f"{home_path}/call_prom.py", '-t', 'runningPodNumInNamespace', '-n', namespace[i]], stdout=PIPE, stderr=PIPE, universal_newlines=True)
                #await update.message.reply_text(os.getcwd())
                output_len = int(result.stdout.split(':')[1])
                for j in range(output_len) :
                    #send_photo(f'{home_path}/image/output{i}.png')
                    with open(f'{home_path}/image/output{j}.png', 'rb') as file:
                        await update.message.reply_photo(photo=file)

# 
async def nodeMemSecTotal(update,context) :
    record = checkuser(update.message.from_user.id)
    if record == 0:
        await update.message.reply_text("user "+str(update.message.from_user.id)+" not registered"+"\n"+"use /au to regist")
    else:
        utype = record[0][2]
        result = checkcommand(utype,update.message.text)
        if result == False:
            await update.message.reply_text("您沒有權限執行該指令!")
        else:
            result = run(["python3", f"{home_path}/call_prom.py", '-t', 'nodeMemSecTotal'], stdout=PIPE, stderr=PIPE, universal_newlines=True)
            #await update.message.reply_text(os.getcwd())
            print(result.stdout)
            output_len = int(result.stdout.split(':')[1])
            for i in range(output_len) :
                #send_photo(f'{home_path}/image/output{i}.png')
                with open(f'{home_path}/image/output{i}.png', 'rb') as file:
                    await update.message.reply_photo(photo=file)


# node exporter - node cpu
async def nodeCpuSecTotal(update,context) :
    record = checkuser(update.message.from_user.id)
    if record == 0:
        await update.message.reply_text("user "+str(update.message.from_user.id)+" not registered"+"\n"+"use /au to regist")
    else:
        utype = record[0][2]
        result = checkcommand(utype,update.message.text)
        if result == False:
            await update.message.reply_text("您沒有權限執行該指令!")
        else:
            result = run(["python3", f"{home_path}/call_prom.py", '-t', 'nodeCpuSecTotal'], stdout=PIPE, stderr=PIPE, universal_newlines=True)
            #await update.message.reply_text(os.getcwd())
            output_len = int(result.stdout.split(':')[1])
            for i in range(output_len) :
                #send_photo(f'{home_path}/image/output{i}.png')
                with open(f'{home_path}/image/output{i}.png', 'rb') as file:
                    await update.message.reply_photo(photo=file)

# kube-state exporter 

# total container cpu usage percentage
async def containerCpuPerSecTotal(update,context) :
    record = checkuser(update.message.from_user.id)
    if record == 0:
        await update.message.reply_text("user "+str(update.message.from_user.id)+" not registered"+"\n"+"use /au to regist")
    else:
        utype = record[0][2]
        result = checkcommand(utype,update.message.text)
        if result == False:
            await update.message.reply_text("您沒有權限執行該指令!")
        else:
            # execute command
            result = run(["python3", f"{home_path}/call_prom.py", '-t', 'containerCpuPerSecTotal'], stdout=PIPE, stderr=PIPE, universal_newlines=True)
            output_len = int(result.stdout.split(':')[1])
            for i in range(output_len) :
                with open(f'{home_path}/image/output{i}.png', 'rb') as file:
                    await update.message.reply_photo(photo=file)

# each container cpu usage percentage
async def conatinerPerCpuUsage(update,context) :
    record = checkuser(update.message.from_user.id)
    if record == 0:
        await update.message.reply_text("user "+str(update.message.from_user.id)+" not registered"+"\n"+"use /au to regist")
    else:
        utype = record[0][2]
        result = checkcommand(utype,update.message.text)
        if result == False:
            await update.message.reply_text("您沒有權限執行該指令!")
        else:
            namespace = []
            if utype == 1:
                namespace = ['']# k8s namespace
            else:
                namespace = checknamespace(update.message.from_user.id)
            for i in range(len(namespace)):
                result = run(["python3", f"{home_path}/call_prom.py", '-t', 'conatinerPerCpuUsage', '-n', namespace[i]], stdout=PIPE, stderr=PIPE, universal_newlines=True)
                output_len = int(result.stdout.split(':')[1])
                for j in range(output_len) :
                    with open(f'{home_path}/image/output{j}.png', 'rb') as file:
                        await update.message.reply_photo(photo=file)

# the cpu usage percentage of per container in each namespace
async def namespacePerPodCpuUsage(update,context) :
    result = run(["python3", f"{home_path}/call_prom.py", '-t', 'namespacePerPodCpuUsage', '-n', 'default'], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    print(result.stdout)
    output_len = int(result.stdout.split(':')[1])
    for i in range(output_len) :
        with open(f'{home_path}/image/output{i}.png', 'rb') as file:
            await update.message.reply_photo(photo=file)

# 確認使用者的建置狀態
def checkUserStatus(uid):
    conn,cur = connectDB()
    sql = "select status from all_user where uid=%s;"
    cur.execute(sql,(uid,))
    return cur.fetchall()[0][0]

async def clear(update,context): 
    record = checkuser(update.message.from_user.id)
    if record == 0:
        await update.message.reply_text("user "+str(update.message.from_user.id)+" not registered"+"\n"+"use /au to regist")
    else: 
        utype = record[0][2]
        result = checkcommand(utype,update.message.text)
        if result == False:
            await update.message.reply_text("您沒有權限執行該指令!")
        else:
            conn,cur = connectDB()
            sql = "update all_user set status = 0 where uid = %s;"
            cur.execute(sql,(update.message.from_user.id,))
            conn.commit()
            sql = "delete from all_wordpress where uid=%s AND (app_name IS NULL OR namespace IS NULL OR replicas IS NULL);"
            cur.execute(sql,(update.message.from_user.id,))
            conn.commit()

            reply_markup = ReplyKeyboardRemove()
            await update.message.reply_text("已清除未完成的建置，請輸入指令 /cw 重新建置",reply_markup=reply_markup)

# enter replicas
async def enterReplicas(update,context):
    record = checkuser(update.message.from_user.id)
    if record == 0:
        await update.message.reply_text("user "+str(update.message.from_user.id)+" not registered"+"\n"+"use /au to regist")
    else: 
        utype = record[0][2]
        result = checkcommand(utype,update.message.text.split(" ")[0])
        if result == False:
            await update.message.reply_text("您沒有權限執行該指令!")
        else:
            status = checkUserStatus(update.message.from_user.id)
            if status != 3: # 狀態不是要輸入replicas數量
                if status == 0:
                    await update.message.reply_text('之前尚未開始建置，請輸入 /cw 開始建置')
                elif status == 1:
                    await update.message.reply_text('之前已建到第'+str(status)+'階段，請從輸入App名稱(指令/app)開始，若確認要重新建置請輸入 /clear')
                else:
                    await update.message.reply_text('之前已建到第'+str(status)+'階段，請從輸入namespace名稱(指令/ns)開始，若確認要重新建置請輸入 /clear')
            else:
                if len(update.message.text.split(" ")) != 2:
                    await update.message.reply_text('輸入格式為"/replicas 數量"，數量只可為1~3的整數')
                else:
                    legal_replicas = True
                    try:
                        replicas = int(update.message.text.split(" ")[1])
                    except:
                        await update.message.reply_text('輸入格式為"/replicas 數量"，數量只可為1~3的整數')
                        legal_replicas = False
                    if legal_replicas == True:
                        if replicas > 3 or replicas < 1:
                            await update.message.reply_text('replicas數量只可為1~3，請重新輸入！')
                        else: # 更改建置資料
                            conn,cur = connectDB()
                            sql = "update all_user set status = 0 where uid=%s;"
                            cur.execute(sql,(update.message.from_user.id,))
                            conn.commit()
                            sql = "update all_wordpress set replicas = %s where uid = %s and replicas IS NULL;"
                            cur.execute(sql,(replicas,update.message.from_user.id))
                            conn.commit()
                            # create deploy and service
                            sql = "select * from all_wordpress where uid = %s order by id desc limit 0,1;"
                            cur.execute(sql,(update.message.from_user.id,))
                            record = cur.fetchall()
                            #app_name = record[0][1]
                            #namespace = record[0][2]
                            #replicas = record[0][3]
                            #deployWordpress(app_name,namespace,replicas)
                            Popen(['python3', f'{home_path}/deployWordpress.py',record[0][1],record[0][2],str(record[0][3]),str(update.message.from_user.id)])
                            reply_markup = ReplyKeyboardRemove()
                            await update.message.reply_text('成功輸入replicas數量！\n以下為您的建置配置：\nApp Name： '+record[0][1]+'\nnamespace: '+record[0][2]+'\nreplicas: '+str(record[0][3])+'\n請稍待WordPress建置完成~', reply_markup=reply_markup)

# enter namespace
async def enterNamespace(update,context): 
    record = checkuser(update.message.from_user.id)
    if record == 0:
        await update.message.reply_text("user "+str(update.message.from_user.id)+" not registered"+"\n"+"use /au to regist")
    else: 
        utype = record[0][2]
        result = checkcommand(utype,update.message.text.split(" ")[0])
        if result == False:
            await update.message.reply_text("您沒有權限執行該指令!")
        else:
            status = checkUserStatus(update.message.from_user.id)
            if status != 2: # 狀態不是要輸入namespace名稱
                if status == 0:
                    await update.message.reply_text('之前尚未開始建置，請輸入 /cw 開始建置')
                elif status == 1:
                    await update.message.reply_text('之前已建到第'+str(status)+'階段，請從輸入App名稱(指令/app)開始，若確認要重新建置請輸入 /clear')
                else:
                    await update.message.reply_text('之前已建到第'+str(status)+'階段，請從輸入replicas數量(指令/rs)開始，若確認要重新建置請輸入 /clear')
            else:
                # 更改建置資料
                if len(update.message.text.split(" ")) != 2:
                    await update.message.reply_text('輸入格式為"/ns 名稱"，且名稱內不可有空格')
                else:
                    # 確認namespace存在,權限1可以管全部,權限2只能管自己有的
                    conn,cur = connectDB()
                    sql = "select permission from all_user where uid = %s;"
                    cur.execute(sql,(update.message.from_user.id,))
                    permission = cur.fetchall()[0][0] 
                    namespace = update.message.text.split(" ")[1]
                    hasNamespace = True
                    if permission == 1: # 可管全部
                        sql = "select * from k8s_namespace where namespace = %s;"
                        cur.execute(sql,(namespace,))
                        if len(cur.fetchall()) == 0: # 沒有該namespace
                            await update.message.reply_text('namespace "'+namespace+'" 不存在，請重新輸入！')
                            hasNamespace = False
                    elif permission == 2: # 只可管自己有的
                        sql = "select * from all_namespace where name = %s and uid = %s"
                        cur.execute(sql,(namespace,update.message.from_user.id))
                        if len(cur.fetchall()) == 0: # 沒有該namespace
                            await update.message.reply_text('namespace "'+namespace+'" 不存在，請重新輸入！')
                            hasNamespace = False
                    if hasNamespace == True:
                        sql = "update all_user set status = 3 where uid=%s;"
                        cur.execute(sql,(update.message.from_user.id,))
                        conn.commit()
                        sql = "update all_wordpress set namespace = %s where uid = %s and namespace IS NULL;"
                        cur.execute(sql,(namespace,update.message.from_user.id))
                        conn.commit()
                        keyboard = [
                            [KeyboardButton("/rs 1")],
                            [KeyboardButton("/rs 2")],
                            [KeyboardButton("/rs 3")],
                        ]
                        reply_markup = ReplyKeyboardMarkup(keyboard)
                        await update.message.reply_text('成功輸入namespace！\n請輸入replicas數量，指令為 "/rs 數量(1~3)"，也可以按鍵盤的按鈕，會選擇按鈕對應的數量', reply_markup=reply_markup)
# 檢查是否只有英文數字
def is_alphanumeric(string):
    pattern = "^[a-zA-Z0-9]+$"
    if re.match(pattern, string):
        return True
    else:
        return False
# enter app name
async def enterAppName(update,context): 
    record = checkuser(update.message.from_user.id)
    if record == 0:
        await update.message.reply_text("user "+str(update.message.from_user.id)+" not registered"+"\n"+"use /au to regist")
    else:
        utype = record[0][2]
        result = checkcommand(utype,update.message.text.split(" ")[0])
        if result == False:
            await update.message.reply_text("您沒有權限執行該指令!")
        else:
            status = checkUserStatus(update.message.from_user.id) 
            if status != 1: # 狀態不是要輸入App名稱
                if status == 0:
                    await update.message.reply_text('之前尚未開始建置，請輸入 /cw 開始建置')
                elif status == 2:
                    await update.message.reply_text('之前已建到第'+str(status)+'階段，請從輸入namespace名稱(指令/ns)開始，若確認要重新建置請輸入 /clear')
                else:
                    await update.message.reply_text('之前已建到第'+str(status)+'階段，請從輸入replicas數量(指令/rs)開始，若確認要重新建置請輸入 /clear')
            else:
                # 更改建置資料
                if len(update.message.text.split(" ")) != 2:
                    await update.message.reply_text('輸入格式為"/app 名稱"，名稱只可由英文和數字組成且不可有空格')
                else:
                    # 確認名稱只有英文數字且沒被使用過
                    app_name = update.message.text.split(" ")[1]
                    if is_alphanumeric(app_name) == False:
                        await update.message.reply_text("名稱只可由英文和數字組成，請重新輸入！")
                    else:
                        conn,cur = connectDB()
                        sql = "select * from all_wordpress where app_name=%s;"
                        cur.execute(sql,(app_name,))
                        if len(cur.fetchall()) != 0:
                            await update.message.reply_text("此名稱已被使用過，請重新輸入!")
                        else:
                            if app_name == "default":
                                sql = "select count(*) from all_wordpress where uid = %s;"
                                cur.execute(sql,(update.message.from_user.id,))
                                num = cur.fetchall()[0][0]
                                app_name = str(update.message.from_user.id)+str(num)
                            sql = "update all_wordpress set app_name = %s where uid = %s and app_name IS NULL;"
                            cur.execute(sql,(app_name,update.message.from_user.id))
                            conn.commit() 
                            sql = "update all_user set status = 2 where uid=%s;"
                            cur.execute(sql,(update.message.from_user.id,))
                            conn.commit()
                            # 列出這位使用者可用的namespace
                            sql = "select permission from all_user where uid = %s"
                            cur.execute(sql,(update.message.from_user.id,))
                            permission = cur.fetchall()[0][0]
                            # 權限1可使用全部,2只可用自己有的
                            if permission == 1:
                                sql = "select namespace from k8s_namespace;"
                                cur.execute(sql,())
                                namespace = cur.fetchall()
                            elif permission == 2:
                                sql = "select name from all_namespace where uid = %s;"
                                cur.execute(sql,(update.message.from_user.id,))
                                namespace = cur.fetchall()
                            if len(namespace) != 0:
                                keyboard = []
                                for i in range(len(namespace)):
                                    keyboard.append([KeyboardButton("/ns "+namespace[i][0])])
                                reply_markup = ReplyKeyboardMarkup(keyboard)
                            else:
                                reply_markup = ReplyKeyboardRemove()
                            await update.message.reply_text('成功輸入App名稱！\n請輸入namespace，指令為 "/ns 名稱"，也可以按鍵盤的按鈕選擇自己可使用的namespace', reply_markup=reply_markup)
# start create wordpress deploy and service
async def createWordpress(update,context): 
    record = checkuser(update.message.from_user.id)
    if record == 0:
        await update.message.reply_text("user "+str(update.message.from_user.id)+" not registered"+"\n"+"use /au to regist")
    else:
        utype = record[0][2]
        result = checkcommand(utype,update.message.text)
        if result == False:
            await update.message.reply_text("您沒有權限執行該指令!")
        else:
            # 判斷使用者目前的建置狀態
            # 0: 未建置 1: 要輸入App name 2: 要輸入namespace 3: 要輸入replicas->0
            status = checkUserStatus(update.message.from_user.id)
            if status != 0: # 狀態不是重頭開始建 
                if status == 1:
                    await update.message.reply_text('之前已建到第'+str(status)+'階段，請從輸入App名稱(指令/app)開始，若確認要重新建置請輸入 /clear')
                elif status == 2:
                    await update.message.reply_text('之前已建到第'+str(status)+'階段，請從輸入namespace名稱(指令/ns)開始，若確認要重新建置請輸入 /clear')
                else:
                    await update.message.reply_text('之前已建到第'+str(status)+'階段，請從輸入replicas數量(指令/rs)開始，若確認要重新建置請輸入 /clear')
            else:
                # 更改使用者建置狀態
                conn,cur = connectDB()
                sql = "update all_user set status = 1 where uid=%s;"
                cur.execute(sql,(update.message.from_user.id,))
                conn.commit() 
                # 更改建置資料
                sql = "insert into all_wordpress(uid)values(%s);"
                cur.execute(sql,(update.message.from_user.id,))
                conn.commit()
                # 可以選 default
                keyboard = [
                    [KeyboardButton("/app default")],
                ]
                reply_markup = ReplyKeyboardMarkup(keyboard)
                await update.message.reply_text('請輸入App名稱，指令為 "/app 名稱"，也可以按鍵盤的預設按鈕，會以使用者id和編號命名', reply_markup=reply_markup)
##### telegram

async def hello(update,context):
    print(update.message.text)
    await update.message.reply_text("hello world!")
    send_photo('/home/tommygood/telegram_bot/image/output1.png')
    #with open('./image/output0.png', 'rb') as file:
    #    await update.message.reply_photo(photo=file)

# get user info
async def getUser(update,context):
    record = checkuser(update.message.from_user.id)
    if record==0:
        await update.message.reply_text("使用者 "+str(update.message.from_user.id)+" 尚未註冊")
    else:
        uid = record[0][0]
        uname = record[0][1]
        utype = record[0][2]
        status = record[0][3]
        await update.message.reply_text("your id: "+uid+"\nname: "+uname+"\npermission: "+str(utype)+"\nWordPress建置狀態: "+str(status))

# create user
async def addUser(update,context):
    record = checkuser(update.message.from_user.id)
    if record==0:
        sql = "insert into all_user(uid,name,permission,status) values(%s,%s,%s,%s);"
        conn,cur = connectDB()
        cur.execute(sql,(str(update.message.from_user.id),str(update.message.from_user.full_name),3,0))
        conn.commit()
        await update.message.reply_text("使用者 "+str(update.message.from_user.id)+" 註冊成功")
    else:
        await update.message.reply_text("使用者 "+str(update.message.from_user.id)+" 已被註冊過")

# show all command
async def allCommand(update,context):
    record = checkuser(update.message.from_user.id)
    if record==0:
        await update.message.reply_text("user "+str(update.message.from_user.id)+" not registered"+"\n"+"use /au to regist")
    else:
        utype = record[0][2]
        sql = "select * from all_command where permission >= %s order by permission desc,name;"
        conn,cur = connectDB()
        cur.execute(sql,(utype,))
        record = cur.fetchall()
        result = "可執行的指令 - 指令說明\n"
        for i in range(len(record)):
            result += record[i][0]+" - "+record[i][1]+"\n"
        await update.message.reply_text(result)

def send_photo(photo_path):
    #bot_token = '6062324742:AAEqo43jhwayn0kmF-9SnnnZ8ZLCbOZcVEg'
    chat_id = '1697361994'
    with open(photo_path, 'rb') as photo_file:
        response = requests.post(
            f'https://api.telegram.org/bot{token}/sendPhoto',
            files={'photo': photo_file},
            data={'chat_id': chat_id}
        )
        response.raise_for_status()

def main():
    # bot token
    app = ApplicationBuilder().token(token).build()
    # all command
    all_command = [['cw',createWordpress],['app',enterAppName],['ns',enterNamespace],['rs',enterReplicas],['clear',clear],['pmuin', podMemUseInNode], ['ecmu', eachConatinerMemUsage], ['wpnin', weirdPodNumInNamespace], ['rpnin', runningPodNumInNamespace], ['nmst', nodeMemSecTotal], ['namespacePerPodCpuUsage', namespacePerPodCpuUsage], ['cpcu',conatinerPerCpuUsage], ['ccpst', containerCpuPerSecTotal], ["ncst", nodeCpuSecTotal],["hello",hello],["ac",allCommand],["gu",getUser],["au",addUser]]
    for i in range(len(all_command)):
        app.add_handler(CommandHandler(all_command[i][0],all_command[i][1]))
    # run bot
    app.run_polling()

# run with daemon
with daemon.DaemonContext():
    main()

# run without daemon
#main()
