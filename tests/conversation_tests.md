#### This file contains tests to evaluate that your bot behaves as expected.
#### If you want to learn more, please see the docs: https://rasa.com/docs/rasa/user-guide/testing-your-assistant/

## sad path 2
* greet: hello
  - utter_greet
* resolution_camera: camera sau của máy như thế nào
  - action_resolution_camrea
* product_name: iphone 11
  - action_follow
  - action_resolution_camrea

## sad path 3
* greet: hi
  - utter_greet
* need_help: tôi muốn mua một chiệc điện thoại
  - utter_need_help
* find_product_lower_price: dưới 15 triệu
  - action_find_product_lower_price

## say goodbye
* goodbye: bye-bye!
  - utter_goodbye

## bot challenge
* product_price: san pham [Realme 5 Pro](product_name) mua moi bao nhieu tien
  - utter_iamabot

## find product
* find_product: co may samsung j8+ khong
  - action_find_product
