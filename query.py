from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import daemon, sys, requests, logging, configparser, logging.handlers
from subprocess import call, PIPE, run

#from dbConfig import conn,cur

app = ''

# home path
home_path = '/home/tommygood/telegram_bot'

#
async def podMemUseInNode(update,context) :
    result = run(["python3", f"{home_path}/call_prom.py", '-t', 'podMemUseInNode'], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    #await update.message.reply_text(os.getcwd())
    output_len = int(result.stdout.split(':')[1])
    for i in range(output_len) :
        #send_photo(f'{home_path}/image/output{i}.png')
        with open(f'{home_path}/image/output{i}.png', 'rb') as file:
            await update.message.reply_photo(photo=file)

#
async def eachConatinerMemUsage(update,context) :
    result = run(["python3", f"{home_path}/call_prom.py", '-t', 'eachConatinerMemUsage'], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    #await update.message.reply_text(os.getcwd())
    output_len = int(result.stdout.split(':')[1])
    for i in range(output_len) :
        #send_photo(f'{home_path}/image/output{i}.png')
        with open(f'{home_path}/image/output{i}.png', 'rb') as file:
            await update.message.reply_photo(photo=file)

#
async def weirdPodNumInNamespace(update,context) :
    result = run(["python3", f"{home_path}/call_prom.py", '-t', 'weirdPodNumInNamespace'], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    #await update.message.reply_text(os.getcwd())
    output_len = int(result.stdout.split(':')[1])
    for i in range(output_len) :
        #send_photo(f'{home_path}/image/output{i}.png')
        with open(f'{home_path}/image/output{i}.png', 'rb') as file:
            await update.message.reply_photo(photo=file)

#
async def runningPodNumInNamespace(update,context) :
    result = run(["python3", f"{home_path}/call_prom.py", '-t', 'runningPodNumInNamespace'], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    #await update.message.reply_text(os.getcwd())
    output_len = int(result.stdout.split(':')[1])
    for i in range(output_len) :
        #send_photo(f'{home_path}/image/output{i}.png')
        with open(f'{home_path}/image/output{i}.png', 'rb') as file:
            await update.message.reply_photo(photo=file)

# 
async def nodeMemSecTotal(update,context) :
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
    result = run(["python3", f"{home_path}/call_prom.py", '-t', 'nodeCpuSecTotal'], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    #await update.message.reply_text(os.getcwd())
    output_len = int(result.stdout.split(':')[1])
    for i in range(output_len) :
        #send_photo(f'{home_path}/image/output{i}.png')
        with open(f'{home_path}/image/output{i}.png', 'rb') as file:
            await update.message.reply_photo(photo=file)

# kube-state exporter 

# total container cpu usage percentage
async def conatinerCpuPerSecTotal(update,context) :
    # execute command
    result = run(["python3", f"{home_path}/call_prom.py", '-t', 'conatinerCpuPerSecTotal'], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    output_len = int(result.stdout.split(':')[1])
    for i in range(output_len) :
        with open(f'{home_path}/image/output{i}.png', 'rb') as file:
            await update.message.reply_photo(photo=file)

# each container cpu usage percentage
async def conatinerPerCpuUsage(update,context) :
    result = run(["python3", f"{home_path}/call_prom.py", '-t', 'conatinerPerCpuUsage'], stdout=PIPE, stderr=PIPE, universal_newlines=True)
    output_len = int(result.stdout.split(':')[1])
    for i in range(output_len) :
        with open(f'{home_path}/image/output{i}.png', 'rb') as file:
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
    sql = "select * from alluser where `id`=%s;"
    cur.execute(sql,(str(update.message.from_user.id),))
    record = cur.fetchall()
    if len(record)==0:
        await update.message.reply_text("user "+str(update.message.from_user.id)+" not registered")
    else:
        uid = record[0][0]
        uname = record[0][1]
        await update.message.reply_text("your id: "+uid+" name: "+uname)

# create user
async def addUser(update,context):
    sql = "select * from alluser where `id`=%s;"
    cur.execute(sql,(str(update.message.from_user.id),))
    record = cur.fetchall()
    if len(record)==0:
        sql = "insert into alluser(id,name) values(%s,%s);"
        cur.execute(sql,(str(update.message.from_user.id),str(update.message.from_user.full_name)))
        conn.commit()
        await update.message.reply_text("create user "+str(update.message.from_user.id)+" successfully")
    else:
        await update.message.reply_text("user "+str(update.message.from_user.id)+" has registered")

# show all command
async def allCommand(update,context):
    sql = "select * from alluser where `id`=%s;"
    cur.execute(sql,(str(update.message.from_user.id),))
    record = cur.fetchall()
    if len(record)==0:
        await update.message.reply_text("user "+str(update.message.from_user.id)+" not registered"+"\n"+"use /au to regist")
    else:
        sql = "select * from allcommand;"
        cur.execute(sql,())
        record = cur.fetchall()
        result = "all command:\n"
        for i in range(len(record)):
            result += record[i][0]+" "+record[i][1]+"\n"
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
    app = ApplicationBuilder().token("6062324742:AAEqo43jhwayn0kmF-9SnnnZ8ZLCbOZcVEg").build()
    # all command
    all_command = [['podMemUseInNode', podMemUseInNode], ['eachConatinerMemUsage', eachConatinerMemUsage], ['weirdPodNumInNamespace', weirdPodNumInNamespace], ['runningPodNumInNamespace', runningPodNumInNamespace], ['nodeMemSecTotal', nodeMemSecTotal], ['namespacePerPodCpuUsage', namespacePerPodCpuUsage], ['conatinerPerCpuUsage',conatinerPerCpuUsage], ['conatinerCpuPerSecTotal', conatinerCpuPerSecTotal], ["nodeCpuSecTotal", nodeCpuSecTotal],["hello",hello],["ac",allCommand],["gu",getUser],["au",addUser]]
    for i in range(len(all_command)):
        app.add_handler(CommandHandler(all_command[i][0],all_command[i][1]))
    # run bot
    app.run_polling()

# run with daemon
with daemon.DaemonContext():
    main()

# run without daemon
#main()
