import requests
from tqdm import tqdm

FILE_PATH="./lotto/weekly/count.log"

count_num = {key: 0 for key in range(1, 46)}
count_bonus = {key: 0 for key in range(1, 46)}
combined_count = {key: 0 for key in range(1, 46)}
    
def prediction_lotto(ocnt):
    print("로또 현재 회차 찾기 ...")
    num=ocnt
    while True:
        url="https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=" + str(num)
        req=requests.get(url)
        result=req.json()
        if result.get("returnValue") == "fail" and num != 0:
            num-=1
            break
        num+=1
    
    print("로또 번호 크롤링 ...", ocnt, num)
    for i in tqdm(range(ocnt+1, num+1)):
        url="https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo="+str(i)
        req=requests.get(url)
        result=req.json()
        count_num[int(result["drwtNo1"])] += 1
        count_num[int(result["drwtNo2"])] += 1
        count_num[int(result["drwtNo3"])] += 1
        count_num[int(result["drwtNo4"])] += 1
        count_num[int(result["drwtNo5"])] += 1
        count_num[int(result["drwtNo6"])] += 1
        count_bonus[int(result["bnusNo"])] += 1
    
    top_6_keys = sorted(count_num, key=lambda k: count_num[k], reverse=True)[:6]
    bottom_6_keys = sorted(count_num, key=lambda k: count_num[k])[:6]
    combined_count = {key: count_num[key] + count_bonus[key] for key in range(1, 46)}
    print("<", (num), "> 회차 까지 !!!")
    print("가장 많이 뽑힌 번호:", sorted(top_6_keys))
    print("가장 적게 뽑힌 번호:", sorted(bottom_6_keys))
    print("[보너스포함] 가장 많이 뽑힌 번호:", sorted(sorted(combined_count, key=lambda k: combined_count[k], reverse=True)[:6]))
    print("[보너스포함] 가장 적게 뽑힌 번호:", sorted(sorted(combined_count, key=lambda k: combined_count[k])[:6]))
    
    return (num)


def load_lotto_count():
    rstr=""
    try:
        with open(FILE_PATH, "r") as file:
            rstr = file.read()
    except:
        print("no such file...")
        return 0

    rstr_split=rstr.split("\n")    
    count_num_str = rstr_split[1].split(';')
    count_bonus_str = rstr_split[2].split(';')

    idx=1
    for val in count_num_str:
        if (len(count_num_str) != idx):
            count_num[idx]=int(val)
        idx+=1
    idx=1
    for val in count_bonus_str:
        if (len(count_bonus_str) != idx):
            count_bonus[idx]=int(val)
        idx+=1

    print("[LOAD] count :", count_num)
    print("[LOAD] bonus :", count_bonus)

    return int(rstr_split[0])


def save_lotto_count(lcnt):
    cstr=""
    bstr=""
    for val in count_num:
        cstr += str(count_num[val]) + ";"
        bstr += str(count_bonus[val]) + ";"
    with open(FILE_PATH, "w") as file:
        file.write(str(lcnt) + "\n")
        file.write(cstr + "\n")
        file.write(bstr + "\n")
    with open("lotto.log", "r") as file:
        print("[SAVE] ", file.read())


ocnt = load_lotto_count()
ncnt = prediction_lotto(ocnt)
save_lotto_count(ncnt)
