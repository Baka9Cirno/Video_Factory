import os, argparse
from aip import AipSpeech 

# 所有api选项 短文本在线合成https://ai.baidu.com/ai-doc/SPEECH/mlbxh7xie

if __name__ == "__main__":
    args = argparse.ArgumentParser("run_baidu_sound")

    args.add_argument("--baiduapi_app_id", type=str, default='118390401')
    args.add_argument("--baiduapi_key", type=str, default='env5ziVefrt3VldcLWTVcTiO')
    args.add_argument("--baiduapi_secret_key", type=str, default='BshG4BoANJumUG4W43CffJ5JLbKYJisb')
    # args.add_argument("--baiduapi_app_id", type=str)
    # args.add_argument("--baiduapi_key", type=str)
    # args.add_argument("--baiduapi_secret_key", type=str)

    args.add_argument("--save_as", type=str, default="./workspace/audio/debug_baidu_sound.wav")
    args.add_argument("--content", type=str, default="月光轻洒，夜色如诗，星辰闪烁，梦境依稀。")
    args.add_argument("--voice_id", type=int, default=4)
    options = args.parse_args()

    app_id = options.baiduapi_app_id
    api_key = options.baiduapi_key
    api_secret_key = options.baiduapi_secret_key

    save_as = options.save_as
    content = options.content
    voice_id = options.voice_id

    client=AipSpeech(app_id, api_key, api_secret_key)
    result=client.synthesis(content,
                        'zh',   #中文
                        1,      #客户端类型选择，web端填写1
        {'vol':5,    # 合成音频文件的准音量
        'spd':3,     # 语速取值0-9,默认为5中语速
        'pit':5,     # 语调音量,取值0-9,默认为5中语调
        'per':voice_id   # 发音人选择,0为女声,1为男生,3为情感合成-度逍遥,4为情感合成-度丫丫,默认为普通女
        })
    
    if not isinstance(result, dict):  
        # 如果结果不是字典（即没有错误），则打开指定的文件路径，并将合成的语音数据写入文件。  
        # 'wb'模式表示以二进制写模式打开文件。  
        with open(save_as,'wb') as f:  
            f.write(result)  # 将语音数据写入文件。  
    else:  
        # 如果结果是字典，那么打印“错误”，表示语音合成过程中可能出现了问题。  
        raise Exception("Internal error, failed to use baidu sound service.")

    

