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

def QuickReply(temp:str,danhsach:str):
    data = {'action_product_configuration':'Cấu hình','action_promotions_and_gift':'Khuyến mãi','action_guarantee':'Bảo hành','action_option_in_box':'Phụ kiện trong hộp','action_is_product_can_buy_on_installment':'Trả góp được không','action_take_photo_erase_background':'Chụp ảnh xóa phông','action_waterproof':'Có chống nước không'}
    listitem = []
    data.pop(temp)
    for item in data:
        btn = {"content_type": "text",
                    "title": data.__getitem__(item),
                    "payload": data.__getitem__(item)}
        listitem.append(btn)
    if danhsach:
        tmp = {"content_type": "text",
                    "title": "Quay lại danh sách",
                    "payload": danhsach}
        listitem.append(tmp)
    message = {
            "text": "Thông tin khác",
            "quick_replies": listitem}
    return message

def BackToList(temp:str):
    message = {"text": "Thông tin khác",
                "quick_replies":[{"content_type": "text",
                                    "title": "Quay lại danh sách",
                                    "payload": temp}]
                                }
    return message
def UrlButton(url:str):
    message_str = {
      "type": "web_url",
      "url": url,
      "title": "Trả góp",
      "webview_height_ratio": "full"
    }
    return message_str