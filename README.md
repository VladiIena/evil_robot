# evil_robot
一个基于nonebotv11的G7人

***有什么用？***

*扮演赛博女友（bushi），复读姬，通过神秘数字下载学习资料，说早安。*

add1插件实现复读

change_preference插件实现/cp命令

deepseek_test插件实现d指导与c指导的api调用与语音输出（需要搭配GPT-SoVITS的api_v2使用）

helloevery插件实现每日早安

jm插件实现/jm神秘数字小功能

quick_response插件实现/lr/dr命令与快速回复响应

sitting_preference插件实现/sp命令

voice插件实现/vc，/vcm命令

***命令***

默认基准模版为：回复应当口语化，不得超过30个字

**/lr可以使机器人记住你要求的自动回复**

示例：/lr AAA & BBB

注：AAA为触发词BBB为回复

**/dr可以删除触发词及其回复**
示例：/dr AAA

**/dr可以删除自动回复**

示例：/dr AAA

注：AAA为触发词
    
**/cp 可以使用预设风格（prompt），在自定义风格（prompt）存在时预设模版不会触发！重启预设模板需要/dp**

示例：/cp 温和 or /cp 变温和 
    
**/sp 可以设置自定义回复风格（prompt）**

示例：/sp 风趣诙谐、机智俏皮，适时融入幽默元素和轻松的措辞。
    
**/dp可以删除自定义的回复风格（prompt），重新使用预设模板**

示例：/dp
    
**/dc 删除对话记录**

示例：/dc
    
**/cm 更改对话模型，可选参数：deepseek-r1，gpt-4o**

示例：/cm gpt-4o

**/vc 更改回复模式（语音/文字），可选参数：on，off**

示例：/vc on

**/vcm 更改回复模型**

示例：/vcm 七海
    
**/jm 神秘小功能**

示例：/jm <一串神秘数字>
    
**！目前只支持文本消息，每个人的bot都是独立的，bot有上下文联系的能力但是一句话尽量不要分开发**
    
~~如果你希望看看怎么个事~~可以加qq*3859053607*
