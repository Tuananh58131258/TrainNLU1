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
    data = {'action_product_configuration':'Cấu hình','action_promotions_and_gift':'Khuyến mãi','action_guarantee':'Bảo hành','action_option_in_box':'Phụ kiện trong hộp'}
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

def BillMessage():
    message_str = {"message":{
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"receipt",
        "recipient_name":"Stephane Crozatier",
        "order_number":"12345678902",
        "currency":"USD",
        "payment_method":"Visa 2345",
        "timestamp":"1428444852",
        "address":{
          "street_1":"1 Hacker Way",
          "street_2":"",
          "city":"Menlo Park",
          "postal_code":"94025",
          "state":"CA",
          "country":"US"
        },
        "summary":{
          "subtotal":75.00,
          "shipping_cost":4.95,
          "total_tax":6.19,
          "total_cost":56.14
        },
        "adjustments":[
          {
            "name":"New Customer Discount",
            "amount":20
          },
          {
            "name":"$10 Off Coupon",
            "amount":10
          }
        ],
        "elements":[
          {
            "title":"Classic White T-Shirt",
            "subtitle":"100% Soft and Luxurious Cotton",
            "quantity":2,
            "price":50,
            "currency":"USD",
            "image_url":"https://www.nretnil.com/avatar/LawrenceEzekielAmos.png"
          },
          {
            "title":"Classic Gray T-Shirt",
            "subtitle":"100% Soft and Luxurious Cotton",
            "quantity":1,
            "price":25,
            "currency":"USD",
            "image_url":"https://www.nretnil.com/avatar/LawrenceEzekielAmos.png"
          }
        ]
      }
    }
    }}
    return message_str

# list_btn = [ButtonTemplate("button1","this is test"),ButtonTemplate("button2","this is test too")]
# res = TemplateItems("this is test","url ne","subtitle chăng",list_btn)
# print(json_message=res)
# print(Hardware('Đèn flash','YorN','yes'))