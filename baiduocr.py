import requests
import json
import urllib

# 替换为您的API Key和Secret Key
API_KEY = "pAxw2C0GwQ2mxj8pzFUE2Z3q"
SECRET_KEY = "ySptlFEsKDiiTj5LS3fAC3Ybg4lds5ME"

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))
def get_file_content_as_base64(path, urlencoded=False):
    """
    获取文件base64编码
    :param path: 文件路径
    :param urlencoded: 是否对结果进行urlencoded 
    :return: base64编码信息
    """
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content

def ocr_image(encodedimg):
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/handwriting?access_token=" + get_access_token()
    
    payload="image="+encodedimg+'&dencodedimg+t_direction=false&probability=false&detect_alteration=false'
    content = urllib.parse.quote_plus(payload)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=content)
    print(response.text)
    data = json.loads(response.text)
    extracted_words = [item['words'] for item in data['words_result']]  
    text = ""
    for words in extracted_words:
        text= text + words + "\n"
    
    return text
    
