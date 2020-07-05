# import json
def GenericTemplate(template_items:list):
    message_str = {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": template_items

                    }
                }
            }
    return message_str
def ButtonPostbackTemplate(btn_tittle:str,btn_payload:str):
    button = {
        "type":"postback",
        "title":btn_tittle,
        "payload":btn_payload
    }
    return button
def ItemsTemplate(title:str,url_img:str,subtitle:str,list_button:list):
    template_item = {
                    "title": title,
                    "image_url": url_img,
                    "subtitle": subtitle,
                    "default_action": {
                        "type": "web_url",
                        "url": url_img,
                        "webview_height_ratio": "full"
                    },
                    "buttons": list_button
                }

    return template_item

def HardwareAnswer(name:str,TypeQ:str,answer:str):
    template  = {'YorN':{"yes":"Máy có {} ạ.".format(name),"no":"Sản phẩm không có {} ạ".format(name)},
                'WHQ':{"yes":"Máy sử dụng {} ạ.".format(name),"no":"Sản phẩm không có {} ạ".format(name)}}
    result = template[TypeQ][answer]
    return result

def PersistentMenu(list_button:list):
    message_str = {"persistent_menu": [
                        {
                            "locale": "default",
                            "composer_input_disabled": "false",
                            "call_to_actions": list_button
                        }
                    ]}
    return message_str
# list_btn = [ButtonTemplate("button1","this is test"),ButtonTemplate("button2","this is test too")]
# res = TemplateItems("this is test","url ne","subtitle chăng",list_btn)
# print(json_message=res)
# print(Hardware('Đèn flash','YorN','yes'))