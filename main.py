from flask import Flask, jsonify, request
import requests,json,datetime,urllib3,time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
dt = datetime.datetime
application = Flask(__name__)
weekday = {
    "1":"일요일",
    "2":"월요일",
    "3":"화요일",
    "4":"수요일",
    "5":"목요일",
    "6":"금요일",
    "7":"토요일"
}

def get_school_info(sc,n=0):
    scu = "https://open.neis.go.kr/hub/schoolInfo"
    para = {
        "KEY": None,
        "Type": "json",
        "pIndex": None,
        "pSize": None,
        "ATPT_OFCDDC_SC_CODE": None,
        "SD_SCHUL_CODE": None,
        "SCHUL_NM": sc,
        "SCHUL_KND_SC_NM": None,
        "LCTN_SC_NM": None,
        "FOND_SC_NM": None,
    }
    res = requests.get(url=scu, params=para, verify=False, json=True)
    res.encoding = "UTF-8"
    rj = res.json()
    try:
        a = rj["schoolInfo"][1]["row"][n]["LCTN_SC_NM"]
    except:
        a = "없는 학교에요"
        return a
    return {
        "교육청":rj["schoolInfo"][1]["row"][n]["ATPT_OFCDC_SC_NM"],
        "지역":rj["schoolInfo"][1]["row"][n]["LCTN_SC_NM"],
        "주소":rj["schoolInfo"][1]["row"][n]["ORG_RDNMA"],
        "교육지원청":rj["schoolInfo"][1]["row"][n]["JU_ORG_NM"],
        "한글이름":rj["schoolInfo"][1]["row"][n]["SCHUL_NM"],
        "영어이름":rj["schoolInfo"][1]["row"][n]["ENG_SCHUL_NM"],
        "전화":rj["schoolInfo"][1]["row"][n]["ORG_TELNO"],
        "팩스":rj["schoolInfo"][1]["row"][n]["ORG_FAXNO"],
        "사이트":rj["schoolInfo"][1]["row"][n]["HMPG_ADRES"],
        "남녀공학":rj["schoolInfo"][1]["row"][n]["COEDU_SC_NM"],
        "우편번호":rj["schoolInfo"][1]["row"][n]["ORG_RDNZC"],
        "학교코드":rj["schoolInfo"][1]["row"][n]["SD_SCHUL_CODE"],
        "설립일":rj["schoolInfo"][1]["row"][n]["FOND_YMD"]
    }

def get_diet():
    n = 0
    sc = "솔빛중학교"
    today = datetime.datetime.today()
    if today.weekday() >= 5:
        last_monday = today + datetime.timedelta(days = 7 - today.weekday())
    else:
        last_monday = today - datetime.timedelta(days = today.weekday())
    for i in range(5):
        diet = ""
        date = (last_monday + datetime.timedelta(days = i)).strftime("%Y%m%d")
        scu = "https://open.neis.go.kr/hub/schoolInfo"
        para = {
            "KEY": None,
            "Type": "json",
            "pIndex": None,
            "pSize": None,
            "ATPT_OFCDDC_SC_CODE": None,
            "SD_SCHUL_CODE": None,
            "SCHUL_NM": sc,
            "SCHUL_KND_SC_NM": None,
            "LCTN_SC_NM": None,
            "FOND_SC_NM": None,
        }
        res = requests.get(url=scu, params=para, verify=False, json=True)
        res.encoding = "UTF-8"
        rj = res.json()
        try:
            sccode = rj["schoolInfo"][1]["row"][n]["SD_SCHUL_CODE"]
            gccode = rj["schoolInfo"][1]["row"][n]["ATPT_OFCDC_SC_CODE"]
        except:
            diet += "급식이 없어요"
            continue
        mscu = f"https://open.neis.go.kr/hub/mealServiceDietInfo?KEY=c64e056331ce4b28adc65d00b55c2856&Type=json&pIndex=1&pSize=100&ATPT_OFCDC_SC_CODE={gccode}&SD_SCHUL_CODE={sccode}"
        mpara = {
            "KEY": "c64e056331ce4b28adc65d00b55c2856",
            "Type": "json",
            "pIndex":1,
            "pSize":100,
            "ATPT_OFCDDC_SC_CODE": gccode,
            "SD_SCHUL_CODE": sccode,
            "MLSV_YMD": date
        }
        mres = requests.get(url=mscu, params=mpara, verify=False, json=True)
        mres.encoding = "UTF-8"
        mrj = mres.json()
        try:
            diet += mrj["mealServiceDietInfo"][1]["row"][0]["DDISH_NM"].replace("<br/>","\n")
        except:
            diet += "급식이 없어요"
        if i == 0:
            fn = "mdd"
        elif i == 1:
            fn = "tudd"
        elif i == 2:
            fn = "wdd"
        elif i == 3:
            fn = "thdd"
        elif i == 4:
            fn = "fdd"
        now = datetime.datetime.now()
        nowt = now.strftime('%Y-%m-%d %H:%M:%S')
        f = open(fn+".txt","w",encoding="utf-8")
        f.write(diet)
        f.close()
        print(f"{nowt} {fn}.txt 파일 저장\n{diet}")
    return True

def get_time():
    n = 0
    sc = "솔빛중학교"
    grade = 1
    class_ = 4
    today = datetime.datetime.today()
    if today.weekday() >= 5:
        last_monday = today + datetime.timedelta(days = 7 - today.weekday())
    else:
        last_monday = today - datetime.timedelta(days = today.weekday())
    for i in range(5):
        diet = ""
        date = (last_monday + datetime.timedelta(days = i)).strftime("%Y%m%d")
        scu = "https://open.neis.go.kr/hub/schoolInfo"
        para = {
            "KEY": None,
            "Type": "json",
            "pIndex": None,
            "pSize": None,
            "ATPT_OFCDDC_SC_CODE": None,
            "SD_SCHUL_CODE": None,
            "SCHUL_NM": sc,
            "SCHUL_KND_SC_NM": None,
            "LCTN_SC_NM": None,
            "FOND_SC_NM": None,
        }
        res = requests.get(url=scu, params=para, verify=False, json=True)
        res.encoding = "UTF-8"
        rj = res.json()
        try:
            sccode = rj["schoolInfo"][1]["row"][n]["SD_SCHUL_CODE"]
            gccode = rj["schoolInfo"][1]["row"][n]["ATPT_OFCDC_SC_CODE"]
        except:
            diet += "시간표가 없어요"
            continue
        if rj["schoolInfo"][1]["row"][n]["SCHUL_NM"].endswith("초등학교"):
            mscu = f"https://open.neis.go.kr/hub/elsTimetable?KEY=c64e056331ce4b28adc65d00b55c2856&Type=json&pIndex=1&pSize=100&ATPT_OFCDC_SC_CODE={gccode}&SD_SCHUL_CODE={sccode}"
            tb = "elsTimetable"
        elif rj["schoolInfo"][1]["row"][n]["SCHUL_NM"].endswith("중학교"):
            mscu = f"https://open.neis.go.kr/hub/misTimetable?KEY=c64e056331ce4b28adc65d00b55c2856&Type=json&pIndex=1&pSize=100&ATPT_OFCDC_SC_CODE={gccode}&SD_SCHUL_CODE={sccode}"
            tb = "misTimetable"
        elif rj["schoolInfo"][1]["row"][n]["SCHUL_NM"].endswith("고등학교"):
            mscu = f"https://open.neis.go.kr/hub/hisTimetable?KEY=c64e056331ce4b28adc65d00b55c2856&Type=json&pIndex=1&pSize=100&ATPT_OFCDC_SC_CODE={gccode}&SD_SCHUL_CODE={sccode}"
            tb = "hisTimetable"
        mpara = {
            "KEY": "c64e056331ce4b28adc65d00b55c2856",
            "Type": "json",
            "pIndex":1,
            "pSize":100,
            "ATPT_OFCDDC_SC_CODE": gccode,
            "SD_SCHUL_CODE": sccode,
            "TI_FROM_YMD": date,
            "TI_TO_YMD": date,
            "GRADE": grade,
            "CLASS_NM": class_
        }
        mres = requests.get(url=mscu, params=mpara, verify=False, json=True)
        mres.encoding = "UTF-8"
        mrj = mres.json()
        try:
            t = mrj[tb][0]["head"][0]["list_total_count"]
            for q in range(t):
                tn = mrj[tb][1]["row"][q]["ITRT_CNTNT"].replace("-","")
                diet += f"{q+1}교시 : {tn}\n"
        except Exception as e:
            diet += "없는 반이에요"
        if i == 0:
            fn = "mdt"
        elif i == 1:
            fn = "tudt"
        elif i == 2:
            fn = "wdt"
        elif i == 3:
            fn = "thdt"
        elif i == 4:
            fn = "fdt"
        fd = diet[:-1]
        now = datetime.datetime.now()
        nowt = now.strftime('%Y-%m-%d %H:%M:%S')
        f = open(fn+".txt","w",encoding="utf-8")
        f.write(fd)
        f.close()
        print(f"{nowt} {fn}.txt 파일 저장\n{fd}")
    return True

while True:
    get_diet()
    get_time()
    time.sleep(300)