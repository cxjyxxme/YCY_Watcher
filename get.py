from urllib.request import urlopen
import os
import json
import time
import urllib
import tensorboardX

time_delta = 30

def get_data():
    headers = {'Host': 'm.ke.qq.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Cookie': 'RK=hDvvFmJ6OS; ptcz=363fa7b454cf298fb60b83646bf6abedf379c9c82e13e8818e7e60892223bbda; pgv_pvi=5688375296; pgv_pvid=9469554733; ue_ts=1542715426; ue_uk=ef7897b8197bf6e3dccd64f467591860; ue_uid=e134ea8fad119023d304c304e3dd5492; ue_skey=94c56e4cbd724c7f8e2b13b91d7551e1; LW_pid=9822c7de256e39209818f2c32b4b17cf; tvfe_boss_uuid=e6270a1f4f3a7de8; o_cookie=498731903; pac_uid=1_498731903; pgv_pvid_new=498731903_72e9902939; mobileUV=1_163cfc0fee2_452f9; eas_sid=d1W54491y8h9i979j3T0m6C1P8; LW_uid=G1L5M4522721K5N4c278o550U1; LW_sid=M1q5r5C3h8t6D8w8l7y4v9L1e6; ke_login_type=1; ts_uid=1287994245; Hm_lvt_0c196c536f609d373a16d246a117fd44=1554726143,1554726232,1554727140,1554779748; luin=o0498731903; lskey=0001000050ea20a6e379e181a81eb3d802c44f121feae29bdb2079c8eae331d0c215c14200ba33a5de4e6240; p_luin=o0498731903; p_lskey=00040000f82b8889949ac94b5921fd7bf569792ec6cd55bf8d2077998532be5e273204a23331c1304aa3e4eb; ts_refer=cybbcds.ke.qq.com/; course_origin=[{"cid":391905,"ext":{"pagelocation":"newagencyhome,1.5"}},{"cid":392455,"ext":{"pagelocation":"newagencyhome,1.1"}},{"cid":392885,"ext":{"pagelocation":"newagencyhome,1.1"}},{"cid":393749,"ext":{"pagelocation":"newagencyhome,1.26"}},{"cid":392968,"ext":{"pagelocation":"newagencyhome,1.1"}}]; localInterest=[2002]',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0, no-cache',
    'TE': 'Trailers',
    'Referer': 'https://m.ke.qq.com/mcates/ccyy/rank.html?act_id=1',
    'Pragma': 'no-cache'}
    url = 'https://m.ke.qq.com/cgi-proxy/vote_activity/work/ranklist?act_id=1&limit=200&bkn=1945095306&_=1554870680367'
    req = urllib.request.Request(url, None, headers)
    response = urllib.request.urlopen(req)
    html = response.read()
    with open('temp.txt', 'wb') as f:
        f.write(html)
    with open('temp.txt', 'r') as f:
        temp = f.readlines()
    return json.loads(temp[0])['result']['rank_list']

if os.path.exists('start.txt'):
    with open('start.txt', 'r') as f:
        temp = f.readlines()
    start = float(temp[0])
else:
    start = time.time()
    with open('start.txt', 'w') as f:
        f.write(str(start))

writers = {}
while (True):
    step = int(time.time() - start)
    print('getting votes')
    datas = get_data()
    for data in datas:
        id = data['work_no']
        if not id in writers:
            writers['id'] = tensorboardX.SummaryWriter(os.path.join('logs', str(id)))
        writers['id'].add_scalar('votes', data['votes'], step)
    print('done')
    time.sleep(time_delta)



