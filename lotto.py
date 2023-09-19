import requests

def lotton_prediction():
    # 총 횟수 확인 (23/9/19 기준 1085회까지 진행됨)
    print("로또 현재 회차 찾기 ...")
    num=1085
    while True:
        url="https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=" + str(num)
        req=requests.get(url)
        result=req.json()
        if result.get("returnValue") == "fail":
            break
        num+=1
    
    # 1회차부터 현재차수까지 당첨번호 크롤링
    print("로또 번호 크롤링 ...")
    count_num = {key: 0 for key in range(1, 47)}
    count_bonus = {key: 0 for key in range(1, 47)}
    for i in range(1, num):
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

    print("<", (num-1), "> 회차 까지 !!!")
    top_6_keys = sorted(count_num, key=lambda k: count_num[k], reverse=True)[:6]
    bottom_6_keys = sorted(count_num, key=lambda k: count_num[k])[:6]
    print("가장 많이 뽑힌 번호:", sorted(top_6_keys))
    print("가장 적게 뽑힌 번호:", sorted(bottom_6_keys))
    
    combined_count = {key: count_num[key] + count_bonus[key] for key in range(1, 47)}
    print("[보너스포함] 가장 많이 뽑힌 번호:", sorted(sorted(combined_count, key=lambda k: combined_count[k], reverse=True)[:6]))
    print("[보너스포함] 가장 적게 뽑힌 번호:", sorted(sorted(combined_count, key=lambda k: combined_count[k])[:6]))
    
lotton_prediction()
