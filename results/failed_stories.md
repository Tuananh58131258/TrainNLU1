## sad path 2 (C:\Users\TuanAnh\AppData\Local\Temp\tmpojii9g_o\0524449e34c841c994acf0f41e0fb122_conversation_tests.md)
* greet: hello
    - utter_greet   <!-- predicted: action_greet -->
* resolution_camera: camera sau của máy như thế nào   <!-- predicted: ask_main_camera: camera sau của máy như thế nào -->
    - action_resolution_camrea   <!-- predicted: action_main_camera -->
* product_name: iphone 11   <!-- predicted: productName: [iphone 11](product_name) -->
    - slot{"product_name": "iphone 11"}
    - action_follow
    - action_resolution_camrea   <!-- predicted: action_listen -->


## sad path 3 (C:\Users\TuanAnh\AppData\Local\Temp\tmpojii9g_o\0524449e34c841c994acf0f41e0fb122_conversation_tests.md)
* greet: hi
    - utter_greet   <!-- predicted: action_greet -->
* need_help: tôi muốn mua một chiệc điện thoại
    - utter_need_help
* find_product_lower_price: dưới 15 triệu   <!-- predicted: find_product_lower_price: dưới [15 triệu](price) -->
    - action_find_product_lower_price


## bot challenge (C:\Users\TuanAnh\AppData\Local\Temp\tmpojii9g_o\0524449e34c841c994acf0f41e0fb122_conversation_tests.md)
* product_price: san pham [Realme 5 Pro](product_name) mua moi bao nhieu tien
    - slot{"product_name": "Realme 5 Pro"}
    - utter_iamabot   <!-- predicted: action_product_price -->


## find product (C:\Users\TuanAnh\AppData\Local\Temp\tmpojii9g_o\0524449e34c841c994acf0f41e0fb122_conversation_tests.md)
* find_product: co may samsung j8+ khong   <!-- predicted: screen_info: co may [samsung j8+](product_name) khong -->
    - slot{"product_name": "samsung j8+"}
    - action_find_product   <!-- predicted: action_custom_fallback -->


