from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import daemon, sys, requests, logging, configparser, logging.handlers
from subprocess import call, PIPE, run
import mysql.connector

# home path
home_path = '/home/tommygood/telegram_bot'


# bot token
token = "6062324742:AAEqo43jhwayn0kmF-9SnnnZ8ZLCbOZcVEg"

# db
def connectDB():
    conn = mysql.connector.connect(
            user="kenny",
            password="Kenny061256",
            host="localhost",
            port=3306,
            database="telegram_db"
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
        await update.message.reply_text("your id: "+uid+"\nname: "+uname+"\npermission: "+str(utype))

# create user
async def addUser(update,context):
    record = checkuser(update.message.from_user.id)
    if record==0:
        sql = "insert into all_user(uid,name,permission) values(%s,%s,%s);"
        conn,cur = connectDB()
        cur.execute(sql,(str(update.message.from_user.id),str(update.message.from_user.full_name),3))
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
        sql = "select * from all_command where permission >= %s order by permission desc;"
        conn,cur = connectDB()
        cur.execute(sql,(utype,))
        record = cur.fetchall()
        result = "可執行的指令 - 指令說明\n"
        for i in range(len(record)):
            result += record[i][0]+" - "+record[i][1]+"\n"
        await update.message.reply_text(result)

def send_photo(photo_path):
    bot_token = '6062324742:AAEqo43jhwayn0kmF-9SnnnZ8ZLCbOZcVEg'
    chat_id = '1697361994'
    with open(photo_path, 'rb') as photo_file:
        response = requests.post(
            f'https://api.telegram.org/bot{bot_token}/sendPhoto',
            files={'photo': photo_file},
            data={'chat_id': chat_id}
        )
        response.raise_for_status()

def main():
    # bot token
    app = ApplicationBuilder().token(token).build()
    # all command
    all_command = [['pmuin', podMemUseInNode], ['ecmu', eachConatinerMemUsage], ['wpnin', weirdPodNumInNamespace], ['rpnin', runningPodNumInNamespace], ['nmst', nodeMemSecTotal], ['namespacePerPodCpuUsage', namespacePerPodCpuUsage], ['cpcu',conatinerPerCpuUsage], ['ccpst', containerCpuPerSecTotal], ["ncst", nodeCpuSecTotal],["hello",hello],["ac",allCommand],["gu",getUser],["au",addUser]]
    for i in range(len(all_command)):
        app.add_handler(CommandHandler(all_command[i][0],all_command[i][1]))
    # run bot
    app.run_polling()

# run with daemon
with daemon.DaemonContext():
    main()

# run without daemon
#main()
