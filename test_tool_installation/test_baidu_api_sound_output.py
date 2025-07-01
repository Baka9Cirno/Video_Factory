# conda 环境：BaiduAPI-Py37

# 从aip模块中导入AipSpeech类，这是百度提供的一个用于语音处理的类。  
from aip import AipSpeech  
  
# 下面的三行代码定义了连接到百度AIP服务所需的三个关键参数：APP_ID、API_KEY和SECRET_KEY。  
# 这些参数是用于身份验证的，确保只有授权的用户才能访问服务。  
APP_ID='118390401'  
API_KEY='env5ziVefrt3VldcLWTVcTiO'  
SECRET_KEY='BshG4BoANJumUG4W43CffJ5JLbKYJisb'  
  
# 使用上面定义的三个参数来初始化AipSpeech类的一个实例，命名为client。  
# 这个实例将用于后续与百度AIP服务的交互。  
client=AipSpeech(APP_ID, API_KEY, SECRET_KEY) 

# 定义要合成为语音的文本内容。这里是一段中文绕口令。  
Text='八百标兵奔北坡，炮兵并排北边跑，炮兵怕把标兵碰，标兵怕碰炮兵炮。'  
Text='Once upon a time, in a small village nestled at the foot of a great mountain, lived a curious boy named Leo. One sunny afternoon, Leo decided to explore the mountain trails but wandered too far and got lost as dusk fell.'
  
# 定义合成后的语音文件将要保存的路径和文件名。  (这里是语音名字)
filePath= "./workspace/audio/myVoice.mp3"  

# 调用client的synthesis方法来进行语音合成。参数包括要合成的文本、语言类型（这里是中文'zh'）、语音的音量（这里是5）等。 
# 方法的返回值将是一个二进制数据（如果合成成功）或一个字典（如果发生错误）。  
result=client.synthesis(Text,
                        'zh',   #中文
                        1,      #客户端类型选择，web端填写1
        {'vol':5,    # 合成音频文件的准音量
        'spd':5,     # 语速取值0-9,默认为5中语速
        'pit':5,     # 语调音量,取值0-9,默认为5中语调
        'per':0   # 发音人选择,0为女声,1为男生,3为情感合成-度逍遥,4为情感合成-度丫丫,默认为普通女
        })  

# （所有api选项 短文本在线合成https://ai.baidu.com/ai-doc/SPEECH/mlbxh7xie）
  
# 下面的代码块检查返回的结果是否是一个字典。如果是字典，那么很可能是一个错误信息。  
# 如果不是字典，那么结果应该是包含合成语音的二进制数据。  
if not isinstance(result, dict):  
    # 如果结果不是字典（即没有错误），则打开指定的文件路径，并将合成的语音数据写入文件。  
    # 'wb'模式表示以二进制写模式打开文件。  
    with open(filePath,'wb') as f:  
        f.write(result)  # 将语音数据写入文件。  
else:  
    # 如果结果是字典，那么打印“错误”，表示语音合成过程中可能出现了问题。  
    print("错误")
