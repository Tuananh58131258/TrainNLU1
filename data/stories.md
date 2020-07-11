## storie greet
* greet
  - action_greet
  - slot{"first_name":"Anh"}
  - slot{"last_name":"Nguyễn Tuấn"}

## say goodbye
* goodbye
  - utter_goodbye

## needhelp
* need_help
  - utter_need_help

## thankyou
* thankyou
  - utter_thankyou

## bot challenge
* ask_ability
  - utter_ask_ability

## storie 12
* what_license
  - utter_what_license

## storie 12
* decry
  - utter_decry

## nhieu ho so cung 1 luc
* many_profile
  - utter_many_profile

## storie 12
* praise
  - utter_praise

## storie 12
* what_license
  - utter_what_license

## storie 12
* ask_hardware_info{"product_name":"oppo reno 3"}
  - action_hardware_info
  - slot{"latest_action":"action_hardware_info"}
  - slot{"product_name":"oppo reno 3"}

## storie 13
* product_price{"product_name":"oppo reno x"}
  - action_product_price
  - slot{"latest_action":"action_product_price"}
  - slot{"product_name":"oppo reno x"}
  - slot{"product_name":"giá của oppo reno x"}

## storie product_price
* product_price{"product_name":"oppo reno 2"}
  - action_product_price
  - slot{"latest_action":"action_product_price"}
  - slot{"product_name":"oppo reno 2"}
  - slot{"product_name":"giá của oppo reno 2"}


## storie online_price
* online_price
  - action_online_price
  - slot{"latest_action":"action_online_price"}
  - slot{"product_name":"oppo reno 3"}
  - slot{"get_list":"giá online của oppo reno 3"}

## storie old_product_price
* old_product_price{"product_name": "iphone 8"}
  - action_old_product
  - slot{"latest_action":"action_old_product"}
  - slot{"product_name": "iphone 8"}
  - slot{"get_list":"giá của iphone 8"}

## storie product_configuration
* product_configuration{"product_name": "iphone 8"}
  - action_product_configuration
  - slot{"latest_action":"action_product_configuration"}
  - slot{"product_name": "iphone 8"}

## storie type_of_product
* type_of_product
  - action_type_of_product

## storie list_product
* list_product
  - action_list_product
  - slot{"get_list":"Danh sách điện thoại samsung"}

## order
* order {"product_name":"oppo reno 3","rom":"64GB"}
  - utter_order

## order
* order {"product_name":"iphone xs max","rom":"64GB"}
  - utter_order
## order
* order {"product_name":"iphone 11","rom":"128GB"}
  - utter_order
## storie check_price
* check_price{"product_name":"oppo reno 3"}
  - action_check_price
  - slot{"latest_action":"action_check_price"}
  - slot{"product_name":"oppo reno 3"}

## storie find_product_in_range_price
* find_product_in_range_price{"price":"4 tr","price":"7tr"}
  - action_find_product_in_range_price
  - slot{"get_list":"điện thoại từ 4tr đến 7tr"}

## storie find_product_lower_price
* find_product_lower_price{"price":"mười triệu"}
  - action_find_product_lower_price
  - slot{"get_list":"điện thoại dưới mười triệu"}

## storie find_product_upper_price
* find_product_upper_price{"price":"12 triệu"}
  - action_find_product_upper_price
  - slot{"get_list":"điện thoại trên 12 triệu"}

## storie find_product_around_price
* find_product_around_price{"price":"7000000"}
  - action_find_product_around_price
  - slot{"get_list":"điện thoại khoảng 7000000"}

## storie screen_info
* screen_info{"product_name":"iphone xs max"}
  - action_scree_info
  - slot{"latest_action":"action_scree_info"}
  - slot{"product_name":"iphone xs max"}

## storie pin_info
* pin_info{"product_name":"iphone xs max"}
  - action_pin_info
  - slot{"latest_action":"action_pin_info"}
  - slot{"product_name":"iphone xs max"}

## storie acquisition_old_product
* acquisition_old_product{"product_name":"iphone xs max"}
  - action_acquisition_old_product
  - slot{"latest_action":"action_acquisition_old_product"}
  - slot{"product_name":"iphone xs max"}

## storie pay_per_month
* pay_per_month{"product_name":"iphone xs max","installment_payment_period":"6 tháng"}
  - action_pay_per_month
  - slot{"latest_action":"action_pay_per_month"}
  - slot{"product_name":"iphone xs max"}

## storie pay_per_month
* pay_per_month{"product_name":"oppo find x2","installment_payment_period":"4 tháng"}
  - action_pay_per_month
  - slot{"latest_action":"action_pay_per_month"}
  - slot{"product_name":"oppo find x2"}

## storie pay_per_month
* pay_per_month{"product_name":"oppo find x2","installment_payment_period":"4 tháng"}
  - action_pay_per_month
  - slot{"latest_action":"action_pay_per_month"}
  - slot{"product_name":"oppo find x2"}


## storie pay_per_month
* pay_per_month{"product_name":"oppo find x2","installment_payment_period":"4 tháng","prepay_percent":"30%"}
  - action_pay_per_month
  - slot{"latest_action":"action_pay_per_month"}
  - slot{"product_name":"oppo find x2"}

## storie case_pay_per_month
* case_pay_per_month{"product_name":"iphone xs max"}
  - action_case_pay_per_month
  - slot{"product_name":"iphone xs max"}

## storie is_product_can_buy_on_installment
* is_product_can_buy_on_installment{"product_name":"iphone xs max"}
  - action_is_product_can_buy_on_installment
  - slot{"latest_action":"action_is_product_can_buy_on_installment"}
  - slot{"product_name":"iphone xs max"}

## storie ask_hardware_info
* ask_hardware_info{"product_name":"iphone xs max"}
  - action_hardware_info
  - slot{"latest_action":"action_hardware_info"}
  - slot{"product_name":"iphone xs max"}

## storie ask_main_camera
* ask_main_camera{"product_name":"iphone xs max"}
  - action_main_camera
  - slot{"latest_action":"action_main_camera"}
  - slot{"product_name":"iphone xs max"}

## storie ask_selfie_camera
* ask_selfie_camera{"product_name":"iphone xs max"}
  - action_selfie_camera
  - slot{"latest_action":"action_selfie_camera"}
  - slot{"product_name":"iphone xs max"}

## storie resolution_camera
* resolution_camera{"product_name":"iphone xs max"}
  - action_resolution_camrea
  - slot{"latest_action":"action_resolution_camrea"}
  - slot{"product_name":"iphone xs max"}
  - slot{"loai_camera":"camera sau"}

## storie Guarantee 1
* guarantee{"product_name":"iphone 8"}
  - action_guarantee
  - slot{"product_name":"iphone 8"}
  - slot{"latest_action":"action_guarantee"}

## storie Guarantee 2
* guarantee{"product_name":"iphone xs max"}
  - action_guarantee
  - slot{"product_name":"iphone xs max"}
  - slot{"latest_action":"action_guarantee"}

## storie Guarantee 1
* guarantee{"product_name":"samsung j8+"}
  - action_guarantee
  - slot{"product_name":"samsung j8+"}
  - slot{"latest_action":"action_guarantee"}

## storie Guarantee 1
* guarantee{"product_name":"Samsung Galaxy A10e"}
  - action_guarantee
  - slot{"product_name":"Samsung Galaxy A10e"}
  - slot{"latest_action":"action_guarantee"}

## phu kien khi mua may
* option_in_box
  - action_option_in_box
  - slot{"latest_action": "action_option_in_box"}
  - slot{"product_name": "iPhone 11 Pro"}

## storie promotions_and_gifts
* promotions_and_gifts{"product_name":"iphone xs max"}
  - action_promotions_and_gift
  - slot{"product_name":"iphone xs max"}
  - slot{"latest_action":"action_guarantee"}

## storie find_product
* find_product{"product_name":"oppo reno 3"}
  - action_find_product
  - slot{"latest_action":"action_find_product"}
  - slot{"product_name":"oppo reno 3"}

## storie take photo erase background
* take_photo_erase_background{"product_name":"oppo reno 3"}
  - action_take_photo_erase_background
  - slot{"latest_action":"action_take_photo_erase_background"}
  - slot{"product_name":"oppo reno 3"}

## storie find_another_product
* find_another_product
  - action_find_another_product

## choi game dc khong
* can_play_game
  - action_can_play_game

## phone_number
* phone_number
  - action_get_phone_number
## storie 01
* greet
  - action_greet
  - slot{"first_name":"Anh"}
  - slot{"last_name":"Nguyễn Tuấn"}
* find_product
  - action_find_product
  - slot{"latest_action":"action_find_product"}
  - slot{"product_name":"oppo reno 3"}
* find_another_product
  - action_find_another_product
  - slot{"latest_action":"action_find_product"}
  - slot{"product_name":"oppo reno 3"}

## giao hang
* delivery
  - utter_delivery

## strie 02
* greet
  - action_greet
  - slot{"first_name":"Anh"}
  - slot{"last_name":"Nguyễn Tuấn"}
* product_price
  - action_product_price
  - slot{"latest_action":"action_product_price"}
  - slot{"product_name":"oppo reno 3"}
  - slot{"get_list":"giá của điện thoại oppo reno 3"}

## storie product_configuration
* product_configuration{"product_name": "iphone 11"}
  - action_product_configuration
  - slot{"latest_action":"action_product_configuration"}
  - slot{"product_name": "iphone 11"}

## storie product_configuration
* product_configuration{"product_name": "oppo reno3"}
  - action_product_configuration
  - slot{"latest_action":"action_product_configuration"}
  - slot{"product_name": "oppo reno3"}

## storie product_configuration
* product_configuration{"product_name": "oppo find x2"}
  - action_product_configuration
  - slot{"latest_action":"action_product_configuration"}
  - slot{"product_name": "oppo find xe"}

  ## storie product_configuration
* product_configuration{"product_name": "iphone xs max"}
  - action_product_configuration
  - slot{"latest_action":"action_product_configuration"}
  - slot{"product_name": "iphone xs max"}

## storie get name then number
* full_name
  - action_get_customer_name
* phone_number
  - action_get_phone_number

## storie get number then name
* phone_number
  - action_get_phone_number
* full_name
  - action_get_customer_name

## get contact
* contact
  - action_get_contact

## follow action
* productName
  - action_follow
  - slot{"product_name": "iPhone Xs Max 256GB"}

## age to buy on install ment
* age_installment
  - utter_age_installment

## thoi gian lam ho so tra gop
* installment_registration_period
  - utter_installment_registration_period

## out of scope
* out_of_scope
  - utter_out_of_scope

## storie chống nước
* waterproof{"product_name": "iphone xs max"}
  - action_waterproof
  - slot{"latest_action":"action_waterproof"}
  - slot{"product_name": "iphone xs max"}