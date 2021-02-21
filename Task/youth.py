#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# 此脚本参考 https://github.com/Sunert/Scripts/blob/master/Task/youth.js

import traceback
import time
import re
import json
import sys
import os
from util import send, requests_session
from datetime import datetime, timezone, timedelta

# YOUTH_HEADER 为对象, 其他参数为字符串
# 选择微信提现30元，立即兑换，在请求包中找到withdraw2的请求，拷贝请求body类型 p=****** 的字符串，放入下面对应参数即可 YOUTH_WITHDRAWBODY
# 分享一篇文章，找到 put.json 的请求，拷贝请求体，放入对应参数 YOUTH_SHAREBODY
# 清除App后台，重新启动App，找到 start.json 的请求，拷贝请求体，放入对应参数 YOUTH_STARTBODY

cookies1 = {
  'YOUTH_HEADER': {"Accept-Encoding":"gzip, deflate, br","Cookie":"Hm_lpvt_268f0a31fc0d047e5253dd69ad3a4775=1613206584; Hm_lvt_268f0a31fc0d047e5253dd69ad3a4775=1613204438,1613205271,1613206186,1613206244; sensorsdata2019jssdkcross=%7B%22distinct_id%22%3A%2253542328%22%2C%22%24device_id%22%3A%2217780b93d0f736-035886632b29908-754c1251-396328-17780b93d1019c2%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%2217780b93d0f736-035886632b29908-754c1251-396328-17780b93d1019c2%22%7D; Hm_lvt_6c30047a5b80400b0fd3f410638b8f0c=1613085747,1613111363,1613197617,1613205271; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2253434546%22%2C%22%24device_id%22%3A%22177858ce26f1331-0701efec5b4eca-754c1251-396328-177858ce270220c%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22177858ce26f1331-0701efec5b4eca-754c1251-396328-177858ce270220c%22%7D","Connection":"keep-alive","Content-Type":"","Accept":"*/*","Host":"kd.youth.cn","User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148","Referer":"https://kd.youth.cn/h5/20190301taskcenter/ios/index.html?uuid=33bba387c03803a9a1436cc0c1a9d67b&sign=289404f8765763cc1a003c351224e3dd&channel_code=80000000&uid=52138103&channel=80000000&access=WIfI&app_version=2.0.0&device_platform=iphone&cookie_id=92e2eb291e1c07162031e05e89360620&openudid=33bba387c03803a9a1436cc0c1a9d67b&device_type=1&device_brand=iphone&sm_device_id=202012122304588665b7f68f86872d495138275c7da35301a7b4e7ec7cfaa9&device_id=48921299&version_code=200&os_version=14.5&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWOwzXmzhnx63a7eqmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonrgrs-iZoF5n7OEY2Ft&device_model=iPhone_6_Plus&subv=1.5.1&&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWOwzXmzhnx63a7eqmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonrgrs-iZoF5n7OEY2Ft&cookie_id=92e2eb291e1c07162031e05e89360620","Accept-Language":"zh-cn","X-Requested-With":"XMLHttpRequest"},
  'YOUTH_READBODY': 'p=9NwGV8Ov71o%3DgW5NEpb6rjb84bkaCQyOq-myT0C-Ktb_pYgxM135XoUfaIpfBqAxRGnFAl1k71C_zMPfUdFlHJTcuxYW9LgBCdTzuda7fnA8r2K-D8AqSYWzt-6LIEcC8SPkaeAgjjv1iCeYI_yckjGbVxJEy1xSQc4qp-_g8cJecymP34l6mTd4qLghgvul8SlZ-AFjVHQWhKZ0UraWUUgK-K2HRcHDaQJ2NTFqUoT1RlRrCFzNOWd3v4YSS8pDi6LKgxMzzSc9ksA5DajYD5nFt9nwD57iJBNNwPYVbS2F9bNIt8owvM4r1VXBcu04yGWhyFvoprBU0lkIGfhD0Gem4LQ8oLJDdDhq2jRGdxzydJp4bDdW1DLzf5C7xTo6Sm-RrLdgMK-X2XRCTHgXyl4Lk0i20CVcVuJSUpYYoD_T4er7DGfuOCtMsz24ILu87yGrHPa8tsAnnLUBdvQ6nQU6eOuW-CfsC8RuXwCh-pbz-y-Snel45XJ_TltZXh6FCkq0QPACp4VHabZR8CHaqklHNCdov-MkHhoF605ln8IMnfuxr-Jd5McIOXM_yTblpjCer5MxDv_5tvtxkmhn3730t0qDYDQwYTAOHSfuBgAo0qBAcb9Ky_wZU-ov_leA1GauvY8UvMAgNkj73TzC_BW5RUE2OVpD2tQYbbixV2er7XkzjiFEmsWNpuY7Iq9LAxS_hsyEOoFMXFEzX-ct78OZuP0EO-4Qj1_SCjC6eKKuK9GDdx6G40ZIPx0cxjgKl10xLoaSnhqoH-E1JOmAX07_tKE55fXyZPQVBKVsE92mTEeZnIp95i2r5R1c5M5Ydtl6JdekWAGifk2Q7Rs17lPfV-YALYnBmg%3D%3D',
  'YOUTH_REDBODY': '',
  'YOUTH_READTIMEBODY': 'p=9NwGV8Ov71o%3DgW5NEpb6rjb84bkaCQyOq-myT0C-Ktb_pYgxM135XoUfaIpfBqAxRGnFAl1k71C_zMPfUdFlHJTcuxYW9LgBCdTzuda7fnA8r2K-D8AqSYWzt-6LIEcC8SPkaeAgjjv1iCeYI_yckjGbVxJEy1xSQc4qp-_g8cJecymP34l6mTd4qLghgvul8SlZ-AFjVHQWhKZ0UraWUUgK-K2HRcHDaQJ2NTFqUoT1RlRrCFzNOWd3v4YSS8pDi6LKgxMzzSc9ksA5DajYD5kmEdcMUaYbpYBEuxGAUrNePOUY1ZtmD8K1G7m83cs4HpZueC8kXFJ_vISGRWlaLexvxyWD6D4FhP42CFocz_NUNKeD_rB7HsiRigdse4se3y2q-IB_hshtuOPnVIRbYNQQIJpfYodvDZ8UDzXtIDyawg2dYUa3Nxh5POS-B_8AXDedazou8nw_UM0WcFM_gJGl22NRJBsceoCqhJuBeSzZVfjzD30Ok4zXM5GNaWzXE_W0uY2tbi4LhMCuQWQtUDiJRkVt9TAinYJxwzCwEJv32zXDKA0m7CJpElSSyCcrGfXxejLDtZzA7bbOsOJcm-hrx9MV8XzJUtvS2rmhj7GpGqY7ID-_VBk34MioxEqx6_Y46KwCxB2fQjabuZZhj88TxfQ4h7UJbujIbAz-0hknHa3mQakxvthuW2WEfV-0qUJ-Tt7o7FnZk9fiJOXethaskviF51ofnARpeCTsc0bllpXgwPofDmoh7_uqZesSB63Lh2aj-ddJL77aiTQ03jZjpo8A2MKR15z3pEMoM-Pu1ZNKeFYFsJAGj-aw4frmIOc_MZjzPvVdfmzW-aSV6kg%3D',
  'YOUTH_WITHDRAWBODY': '',
  'YOUTH_SHAREBODY': 'access=WIFI&app_version=2.0.0&article_id=36309449&channel=80000000&channel_code=80000000&cid=80000000&client_version=2.0.0&device_brand=iphone&device_id=48921299&device_model=iPhone&device_platform=iphone&device_type=iphone&from=0&is_hot=0&isnew=1&mobile_type=2&net_type=1&openudid=33bba387c03803a9a1436cc0c1a9d67b&os_version=14.5&phone_code=33bba387c03803a9a1436cc0c1a9d67b&phone_network=WIFI&platform=3&request_time=1613229696&resolution=856x1852&sign=cb71bc451ba856480ea2c1456ca8fd2e&sm_device_id=202012122304588665b7f68f86872d495138275c7da35301a7b4e7ec7cfaa9&stype=WEIXIN&szlm_ddid=D22dXQ1gJKVeQAMKAF48ixV5BJG4QQf2VlECXmh7wlq7AXa8&time=1613229696&uid=52138103&uuid=33bba387c03803a9a1436cc0c1a9d67b'
}
cookies2 = {
  'YOUTH_HEADER': {"Accept-Encoding":"gzip, deflate, br","Cookie":"Hm_lpvt_268f0a31fc0d047e5253dd69ad3a4775=1613209463; Hm_lvt_268f0a31fc0d047e5253dd69ad3a4775=1613205271,1613206186,1613206244,1613209459; sensorsdata2019jssdkcross=%7B%22distinct_id%22%3A%2253434546%22%2C%22%24device_id%22%3A%2217780b93d0f736-035886632b29908-754c1251-396328-17780b93d1019c2%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%2217780b93d0f736-035886632b29908-754c1251-396328-17780b93d1019c2%22%7D; Hm_lpvt_6c30047a5b80400b0fd3f410638b8f0c=1613209458; Hm_lvt_6c30047a5b80400b0fd3f410638b8f0c=1613197617,1613205271,1613209282,1613209458; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2253434546%22%2C%22%24device_id%22%3A%22177858ce26f1331-0701efec5b4eca-754c1251-396328-177858ce270220c%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22177858ce26f1331-0701efec5b4eca-754c1251-396328-177858ce270220c%22%7D","Connection":"keep-alive","Content-Type":"","Accept":"*/*","Host":"kd.youth.cn","User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148","Referer":"https://kd.youth.cn/h5/20190301taskcenter/ios/index.html?uuid=33bba387c03803a9a1436cc0c1a9d67b&sign=a246ee00f6487ee88be65f766f021d66&channel_code=80000000&uid=53434546&channel=80000000&access=WIfI&app_version=2.0.0&device_platform=iphone&cookie_id=98e1cf5da39021d7a4912520256ef609&openudid=33bba387c03803a9a1436cc0c1a9d67b&device_type=1&device_brand=iphone&sm_device_id=202012122304588665b7f68f86872d495138275c7da35301a7b4e7ec7cfaa9&device_id=48921299&version_code=200&os_version=14.5&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWOw3YWzhXyKlq_OqmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonrgrs-iaIJ5hWyEY2Ft&device_model=iPhone_6_Plus&subv=1.5.1&&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWOw3YWzhXyKlq_OqmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonrgrs-iaIJ5hWyEY2Ft&cookie_id=98e1cf5da39021d7a4912520256ef609","Accept-Language":"zh-cn","X-Requested-With":"XMLHttpRequest"},
  'YOUTH_READBODY': 'p=9NwGV8Ov71o%3DgW5NEpb6rjab0hHSxXenkWHSkCwB26b0x_gtnWSAWxdTXCgxxOuanGgyauM8npV4yOZZonvZ1c4pKdlgrlKdOtZMg8UfxQpxU7riPYL5LPUwaZ0M1ASG9IgOsaBNdFn-2rcpx0-NIjTVXMnuWlAzmNqMyA4AaB20-hmFuaVSFyTsDRsX_pMraZC6jThVTjkpERUpURM5oqsMXYEX37zvJNIrAbJNMS_AkMnqvTC1yepdD7TxnuAjVL1pkJBLWOeHyza_k9aKganxwxbbYV_KH1BHrc8C-62C1VHaVKhJdGszEIvXyCsnSflzm-cmtPnj6yfxztNE9Tt6QabprONczzZjTNo952ATixhlQMUeKKY8-p8HOwKhCmSjG5R60gBBhFQ1jY-Q_B-lXwkRDyMVXPBUhZyoDoisIVNq4FKySm0v2VwTUqAffEO4dmbCeWrdswqnrTY8XfMV3nR1yE_YbjioDg-b0K01JypYyfRghlK-BqtXsS1r_oyt5tFvYIXT9mZSG9RkrbMQ1w1Y_phQ-lQotVW1KDYEs3tSlpOV0PPizAu4Mb2h8v7WQ1iov-kLb5ub5XY2A96sVIjP2fePpdGlBqzJAlJwZolMozqR3D-nNqvBLFooegVNJyNs-z44IbBAHnou-w-ID7iYEdeatTZaEm3iSjwSg449Si4mtwrXkC2cG7D26qjbIMq-w9dGgqrwAbZmvib8RkYmYtV3IWY38ipc6k_LxR_PzyHNBsJtEU6IZHy8TsJEROT88qdtHrdOci1suinjFFZVCgKboAdU4JmtwVxl4Cpa9WIWdEeye-3IlRNWDmm2QlQOiboiwiMKRGzcO2kjnsTgH-N7GSEC7IEqWUBXWArjAbq5L_d8_sXLCSyD_9IKUUxnyf3p',
  'YOUTH_REDBODY': '',
  'YOUTH_READTIMEBODY': 'p=9NwGV8Ov71o%3DgW5NEpb6rjb84bkaCQyOq-myT0C-Ktb_pYgxM135XoUfaIpfBqAxRGnFAl1k71C_zMPfUdFlHJTcuxYW9LgBCdTzuda7fnA8r2K-D8AqSYWzt-6LIEcC8SPkaeAgjjv1iCeYI_yckjGbVxJEy1xSQc4qp-_g8cJecymP34l6mTd4qLghgvul8SlZ-AFjVHQWhKZ0UraWUUgK-K2HRcHDaQJ2NTFqUoT1RlRrCFzNOWd3v4YSS8pDi6LKgxMzzSc9ksA5DajYD5kmEdcMUaYbpYBEuxGAUrNePOUY1ZtmD8K1G7m83cs4HpZueC8kXFJ_vISGRWlaLexvxyWD6D4FhP42CFocz_NUNKeD_rB7HsiRigdse4se3y2q-IB_hshtuOPnVIRbYNQQIJpfYodvDZ8UDzXtIDyawg2dYUa3Nxh5POS-B_8AXDedazou8nw_UM0WcFM_gJGl22NRJBsceoCqhJuBeSzZVfjzD30Ok4zXM5GNaWzXE_W0uY2tbi4Lq-PMR1RTSUBoHLxxmFAkZwUryb4j3N_K-3BLuYkqOLK0vEEr1Cx49b6UGkcxIZWgr2ZwPrTR8mQkdE5Ivni2ZZRoue1eUwDe3445zV3IysEy-3eCGu7e6RlXVg4kXDmHRuGSp9n4seREaYPlC2GaNw7fjnd2fZw85rnpuYUYwkaNBPra3Z4QVbw2cMCTl51Lp9FSXIkuC-AYhJ17mlFmmRQbawdsPOvtFsGAPGu-LNcx2jYK1px_5ulRNi0QlP5AiIY1lShvkUqO7Gk7LozpQj3mDBfDUltTUgYCpL4Gup3jgEuvAoPOFJgrKHGpTkp46aC9Tljm9QQ%3D',
  'YOUTH_WITHDRAWBODY': '',
  'YOUTH_SHAREBODY': 'access=WIFI&app_version=2.0.0&article_id=36309667&channel=80000000&channel_code=80000000&cid=80000000&client_version=2.0.0&device_brand=iphone&device_id=50166125&device_model=iPhone&device_platform=iphone&device_type=iphone&from=0&is_hot=0&isnew=1&mobile_type=2&net_type=1&openudid=c8c5b8165acb92625b350dde7a375b8f&os_version=14.4&phone_code=c8c5b8165acb92625b350dde7a375b8f&phone_network=WIFI&platform=3&request_time=1613230345&resolution=828x1472&sign=0ec5e685298daa6029126aa5e9929ce6&sm_device_id=202102012113482dcaf0b454f0fa9a3591cd3989b96bb601a07d1c395cb0fe&stype=WEIXIN&szlm_ddid=D2MvOmPRjbaUGuKj5sz8%2B3MT60EHdFHfFsECXmh7wlq7AX66&time=1613230346&uid=53434546&uuid=c8c5b8165acb92625b350dde7a375b8f'
}
cookies3 = {
  'YOUTH_HEADER': {"Accept-Encoding":"gzip, deflate, br","Cookie":"Hm_lpvt_268f0a31fc0d047e5253dd69ad3a4775=1613209631; Hm_lvt_268f0a31fc0d047e5253dd69ad3a4775=1613206186,1613206244,1613209459,1613209626; sensorsdata2019jssdkcross=%7B%22distinct_id%22%3A%2253436621%22%2C%22%24device_id%22%3A%2217780b93d0f736-035886632b29908-754c1251-396328-17780b93d1019c2%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%2217780b93d0f736-035886632b29908-754c1251-396328-17780b93d1019c2%22%7D; Hm_lpvt_6c30047a5b80400b0fd3f410638b8f0c=1613209626; Hm_lvt_6c30047a5b80400b0fd3f410638b8f0c=1613205271,1613209282,1613209458,1613209626; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2253434546%22%2C%22%24device_id%22%3A%22177858ce26f1331-0701efec5b4eca-754c1251-396328-177858ce270220c%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22177858ce26f1331-0701efec5b4eca-754c1251-396328-177858ce270220c%22%7D","Connection":"keep-alive","Content-Type":"","Accept":"*/*","Host":"kd.youth.cn","User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148","Referer":"https://kd.youth.cn/h5/20190301taskcenter/ios/index.html?uuid=33bba387c03803a9a1436cc0c1a9d67b&sign=cae330435d179f6fc55f17138b60d513&channel_code=80000000&uid=53436621&channel=80000000&access=WIfI&app_version=2.0.0&device_platform=iphone&cookie_id=5af4f1fac88846af4fc2aa8eb6845168&openudid=33bba387c03803a9a1436cc0c1a9d67b&device_type=1&device_brand=iphone&sm_device_id=202012122304588665b7f68f86872d495138275c7da35301a7b4e7ec7cfaa9&device_id=48921299&version_code=200&os_version=14.5&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWOw3YWzhaKO3664qmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonrgrs-iaIKfebCEY2Ft&device_model=iPhone_6_Plus&subv=1.5.1&&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWOw3YWzhaKO3664qmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonrgrs-iaIKfebCEY2Ft&cookie_id=5af4f1fac88846af4fc2aa8eb6845168","Accept-Language":"zh-cn","X-Requested-With":"XMLHttpRequest"},
  'YOUTH_READBODY': '9NwGV8Ov71o%3DgW5NEpb6rjab0hHSxXenkWHSkCwB26b0x_gtnWSAWxdTXCgxxOuanMJmTsyKyJTcxMLhQ5cUAW50xvC9jIuNHe7nYcfL-oUrepU-OIgosERaI5tqLFJP4CUiriP_i8RIWcXqJtdQRCnM-id8KIbfyA4i_NFMXkoemhQCcKkMWiBVapmH16teBe31UbfsLXCd6m2UkF6iooLzHP3CUdfwgRGujcb6nveud5lIRMuy5Ai6T7ko6lPDTwCjvCDvpMRtjkQlVGX8R03x4gwlYYeHZKZiBmFRgSXUVaI2uowUKvfPPc-vMQZrUpC2IgILI9USikN3iRoZo5FCuo9eSiuxHSaM-bC8dXJjq1Q9Fyb28RoilD07dm_3x9b3abbkra6ApzNOKpFWbSWhV3UTtt_79PLfYnuAZMRSehiozjF4BE3XHAgVPVyQ-rH0l1H1CH0D6h6Q6lYyAovZU2CRrZzbfvv_uz8tLeTYW3oNFOT_Wk6qRMN1E6S66umx5yp3QN-g4WCq_sPPYGOTzvm6q2ZF-Gw3VHgttXNhcH2WVgkiY2SCH6To090_vxHzMcoonip3W8i-oc9uNRzCGtiOZhtf_t8QpU-e6gotpJ2gppGHwpx9k5roQ1R7w_-CwuKoE8-i4beZb3Tinfyk___QRNydCVmzrXmYZIHtWjN6FQcSV5lIGb4VaQ-djKXkDcLCGn0Lk3ksswN7Uw4gBk2XOmf8MxzbQMc4OFNkxdCOH3pU5yfv5QNPPRyGtDWd9fVkZJa7kUtHHTCHKSgNvNInb_bdzZkzgmW2CsziBZKFVP7AVpwLKdLLku3SQSn-ALT5UoA6KsHsXbg1eAUF3rkh_ebyTRIcIjnpQPZ4wPJl6T-UdxQ%3D',
  'YOUTH_REDBODY': '',
  'YOUTH_READTIMEBODY': 'p=9NwGV8Ov71o%3DgW5NEpb6rjb84bkaCQyOq-myT0C-Ktb_pYgxM135XoUfaIpfBqAxRGnFAl1k71C_zMPfUdFlHJTcuxYW9LgBCdTzuda7fnA8r2K-D8AqSYWzt-6LIEcC8SPkaeAgjjv1iCeYI_yckjGbVxJEy1xSQc4qp-_g8cJecymP34l6mTdqYe06k684hmkCn9bUAt50GbhY_PjceuHMz5GyR4w8PzRHUHV7LuattHm8DkE3kYEwpqKFIaLF_EZPNPakz9umuLoY-YchOY9hDFN9Aa5oa71L2_hduFFP-H57W4j9TmIwonaoVBPkbERvCAyhE9XmDePNJ7EHkPXdzrfiqyYs89G6PRDm4VaAwBHyZSx3JI4SXRQyjaOsd5oatxLgA0HLsK8OidKx7vpYiAKiWqzzg_wZ_vBmtb7bqOgzgrNiSu1VMzTAcMjtbrJuYNvNsAADndh6bVO7HHoA2ZWKCbPmGdIZL1-0ppkVn-Fzr5s0RGeLKkmvOCy_Iq2_vvPj_ruQ0Ne7YgegNfVkw0mjA9uTDXDObuh5HtMXdHV9VJ4U9nUbcgDvj5oO3rASKYSdMZPP6rwQnkQH8-jU_EfW3WIFrsq2Vpkyz5L2fYcE9dQRdsiCrbUOnqAkZftLfHXxDxlokBmUq1rFHPUdCg3dWfTFLsnICd2B_tK8WYBHJJEfguitvPmjB_xr5M-WnzMRc3HSG3kSmxMQa0kdJP4u7iTmM1eMAY1LvfanvlpUzG8jfiy1BzpUnna4Bqpll8iHB2bjhZXJHvmxXdIGyuf_c6jGph7lqV4ccNqcGBJ6GK-5fXznpSVD9IgNrqDHUBBmkU5PgqMhQ1EaXEQ%3D',
  'YOUTH_WITHDRAWBODY': '',
  'YOUTH_SHAREBODY': 'access=WIFI&app_version=2.0.0&article_id=36283958&channel=80000000&channel_code=80000000&cid=80000000&client_version=2.0.0&device_brand=iphone&device_id=50168116&device_model=iPhone&device_platform=iphone&device_type=iphone&from=0&is_hot=0&isnew=1&mobile_type=2&net_type=1&openudid=df4917b74d58ea59a53ca27f12fa7c92&os_version=14.4&phone_code=df4917b74d58ea59a53ca27f12fa7c92&phone_network=WIFI&platform=3&request_time=1613230496&resolution=780x1688&sign=69dac5a243fb2f24a43b5779a33c95ee&sm_device_id=20210201224214b0311784482a6fd09c95eda69ea86b300144710630209057&stype=WEIXIN&szlm_ddid=D2C/eO80JdtEltNZ4UTb2evEXxYcN081EVECXmh7wlq7AX11&time=1613230496&uid=53436621&uuid=df4917b74d58ea59a53ca27f12fa7c92'
}
cookies4 = {
  'YOUTH_HEADER': {"Accept-Encoding":"gzip, deflate, br","Cookie":"Hm_lpvt_268f0a31fc0d047e5253dd69ad3a4775=1613209761; Hm_lvt_268f0a31fc0d047e5253dd69ad3a4775=1613206244,1613209459,1613209626,1613209748; sensorsdata2019jssdkcross=%7B%22distinct_id%22%3A%2253542328%22%2C%22%24device_id%22%3A%2217780b93d0f736-035886632b29908-754c1251-396328-17780b93d1019c2%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%2217780b93d0f736-035886632b29908-754c1251-396328-17780b93d1019c2%22%7D; Hm_lpvt_6c30047a5b80400b0fd3f410638b8f0c=1613209749; Hm_lvt_6c30047a5b80400b0fd3f410638b8f0c=1613209282,1613209458,1613209626,1613209749; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2253434546%22%2C%22%24device_id%22%3A%22177858ce26f1331-0701efec5b4eca-754c1251-396328-177858ce270220c%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%22177858ce26f1331-0701efec5b4eca-754c1251-396328-177858ce270220c%22%7D","Connection":"keep-alive","Content-Type":"","Accept":"*/*","Host":"kd.youth.cn","User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148","Referer":"https://kd.youth.cn/h5/20190301taskcenter/ios/index.html?uuid=33bba387c03803a9a1436cc0c1a9d67b&sign=934e06cd70c7ce3da8f2b4dc5755e430&channel_code=80000000&uid=53542328&channel=80000000&access=WIfI&app_version=2.0.0&device_platform=iphone&cookie_id=ad0a4b4d94b62ac92798e027ca177a57&openudid=33bba387c03803a9a1436cc0c1a9d67b&device_type=1&device_brand=iphone&sm_device_id=202012122304588665b7f68f86872d495138275c7da35301a7b4e7ec7cfaa9&device_id=48921299&version_code=200&os_version=14.5&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWOw3YlphKKC37CoqmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonrgrs-iaIKvgWyEY2Ft&device_model=iPhone_6_Plus&subv=1.5.1&&cookie=MDAwMDAwMDAwMJCMpN-w09Wtg5-Bb36eh6CPqHualq2jmrCarWOw3YlphKKC37CoqmqXr6NthJl7mI-shMmXeqDau4StacS3o7GFonrgrs-iaIKvgWyEY2Ft&cookie_id=ad0a4b4d94b62ac92798e027ca177a57","Accept-Language":"zh-cn","X-Requested-With":"XMLHttpRequest"},
  'YOUTH_READBODY': 'p=9NwGV8Ov71o%3DgW5NEpb6rjab0hHSxXenkWHSkCwB26b0x_gtnWSAWxdTXCgxxOuanNdjJbP3fdNd69mqMdlwMpBuvdNelhC5GBRj9eN6ZlVZaTaaS5nOlqIPEhgFBAA8CYnGExsfZ7X0iuDsmDkELBHjzA29A6SaKWV5Hu9WJF-GNX0oAirC4HhuPGYV269_KmtYUB1VLpDzNya-HTVBk8VCVy5JEYnpaPXFA1VGOyT8tSPsJu3NjWCo8AqWvs9u18avZnWwp0r_H_UZHZDoOMekecuW8NbLp_FccMO7cPTBg0MaXibDrsYRy4rckeBtLgDpsodMyfqLZihq3Lh_0TK7bfXsIWiLyD9M1frTPn6g1yHMsJKFm5UKzzQw0fHACIPh6YyB1oJ_qbD_QuLS0-efVnEaUOGhEpcAMRWo8uf2gsp8DUZTMdjW_fOXecHVX2rUGXjp_7d8o0iLTDsho2dYIxdpPUaCqLWUZuCtwmoRZHzXxP9Gqn6maCHX9CqPXqJzUkPkbr5Iw_vTJZyVFySzBVpMTuZ33nt3pOYBtx_LmCxz6EB80kfqIDD3KHNMZt6LtGLkPaqllGlCU7YcOK5ibvYWqcef9F9G0BuB9CEjUN6sZoRRf9uZvCvGLn1kvJjvWTeVekoQxmlP91tEr0pkCp6uxFGaRzULSjkfQxp6i4L0nF2myRdxltTOow1NERauebc5mp7gPHC_FS04gn3-yFjGSfmlL9TmLyvdjrPj-PQmZth4-gPBD2ubkyiEZm1exPPkfjE7QEk8GOTfJVnGutThfnVH27PKMx96S28pNhjhIdWVex1rC_7v5VUmpObDR9dNtPNZlE7VL3mREeJxyArLvJVY8vEzxkurHtZNXaG5L_X-J-139dlMNZR0KTmlLjPeckGm',
  'YOUTH_REDBODY': '',
  'YOUTH_READTIMEBODY': 'p=9NwGV8Ov71o%3DgW5NEpb6rjb84bkaCQyOq-myT0C-Ktb_pYgxM135XoUfaIpfBqAxRGnFAl1k71C_zMPfUdFlHJTcuxYW9LgBCdTzuda7fnA8r2K-D8AqSYWzt-6LIEcC8SPkaeAgjjv1iCeYI_yckjGbVxJEy1xSQc4qp-_g8cJecymP34l6mTd_I3FW1HUB-vIPDTZVlRqgSTiTsrGFj8diJGChAABbt0de3t84PgJIOECKjViqegiFPatti8pjge-nUpXOiEe4xpM6vovaHyScGypFOwN6NeMJBh1H_NR__MIsycnhEJxAXgC_ufB1oOhrJ_l3EYe0hN8lDDKJLXJmPCJrhtVI-hEkvEYhMFpd-arV-8HgIJIOstGjZ5I16P7awHSKi7yRdt5gRmb9eOonGHuqtiLblvOutDHm7pMvyiZUELS7FmWKLTLoKL_mctsUtkig8Hc55Xyrl7S8zy9eQ4LBSkLXGP_cqkb-gQEXSOPKBVHmUuUBFr62sAhJ6uXOQZjwRANkNwBz_Cm5WS0DtMN6xUHJwkkp0mYz846bbjFFGR6ldcdwQEtEDcAcICB2bRMqPaUXBTMBwKjelsQQXgWD_Gn_CSK1ET5GfVQOjxD6OxF_Bs01rtVb-G63JaoT5vTz4xpyBw0gNRnGeNFOA1xtek9wxCdbDv8f2Qub3eJMZSozWBBIhhI-0fpcmI9WsyexW2GN90LsPrkHasLEGRfQ6pmthVxLa_Ejvsh9aQxWamBgAQ-NR0Tpn0RLiycFG0dshHmuBin2YwBb9D8a5iLbJo8bCpVPI6ZTVThMl-lnJZ-SzywZmfR9wY6veCh0SjQsyVdREcFbAZNO1AI%3D',
  'YOUTH_WITHDRAWBODY': '',
  'YOUTH_SHAREBODY': 'access=WIFI&app_version=2.0.0&article_id=36293466&channel=80000000&channel_code=80000000&cid=80000000&client_version=2.0.0&device_brand=iphone&device_id=50439354&device_model=iPhone&device_platform=iphone&device_type=iphone&from=0&is_hot=0&isnew=1&mobile_type=2&net_type=1&openudid=85150c005bd9f8fc27aec8207edba97f&os_version=14.4&phone_code=85150c005bd9f8fc27aec8207edba97f&phone_network=WIFI&platform=3&request_time=1613230218&resolution=750x1334&sign=c01cfef9e7f93e891080deceadb48b5d&sm_device_id=202102132328498d3df2ef06822516e8569ed7b597927701827f800a3a8f66&stype=WEIXIN&szlm_ddid=D2s0xF/n0oQer17ESZCTITPj6gLOVhhC%2Bgt6UZzFTN47wX1a&time=1613230219&uid=53542328&uuid=85150c005bd9f8fc27aec8207edba97f'
}

COOKIELIST = [cookies1,cookies2,cookies3,cookies4,]  # 多账号准备

# ac读取环境变量
if "YOUTH_HEADER1" in os.environ:
  COOKIELIST = []
  for i in range(5):
    headerVar = f'YOUTH_HEADER{str(i+1)}'
    readBodyVar = f'YOUTH_READBODY{str(i+1)}'
    redBodyVar = f'YOUTH_REDBODY{str(i+1)}'
    readTimeBodyVar = f'YOUTH_READTIMEBODY{str(i+1)}'
    withdrawBodyVar = f'YOUTH_WITHDRAWBODY{str(i+1)}'
    shareBodyVar = f'YOUTH_SHAREBODY{str(i+1)}'
    startBodyVar = f'YOUTH_STARTBODY{str(i+1)}'
    if headerVar in os.environ and os.environ[headerVar] and readBodyVar in os.environ and os.environ[readBodyVar] and redBodyVar in os.environ and os.environ[redBodyVar] and readTimeBodyVar in os.environ and os.environ[readTimeBodyVar]:
      globals()['cookies'+str(i + 1)]["YOUTH_HEADER"] = json.loads(os.environ[headerVar])
      globals()['cookies'+str(i + 1)]["YOUTH_READBODY"] = os.environ[readBodyVar]
      globals()['cookies'+str(i + 1)]["YOUTH_REDBODY"] = os.environ[redBodyVar]
      globals()['cookies' + str(i + 1)]["YOUTH_READTIMEBODY"] = os.environ[readTimeBodyVar]
      globals()['cookies' + str(i + 1)]["YOUTH_WITHDRAWBODY"] = os.environ[withdrawBodyVar]
      globals()['cookies' + str(i + 1)]["YOUTH_SHAREBODY"] = os.environ[shareBodyVar]
      globals()['cookies' + str(i + 1)]["YOUTH_STARTBODY"] = os.environ[startBodyVar]
      COOKIELIST.append(globals()['cookies'+str(i + 1)])
  print(COOKIELIST)

cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)
YOUTH_HOST = "https://kd.youth.cn/WebApi/"

def get_standard_time():
  """
  获取utc时间和北京时间
  :return:
  """
  # <class 'datetime.datetime'>
  utc_datetime = datetime.utcnow().replace(tzinfo=timezone.utc)  # utc时间
  beijing_datetime = utc_datetime.astimezone(timezone(timedelta(hours=8)))  # 北京时间
  return beijing_datetime

def pretty_dict(dict):
    """
    格式化输出 json 或者 dict 格式的变量
    :param dict:
    :return:
    """
    return print(json.dumps(dict, indent=4, ensure_ascii=False))

def sign(headers):
  """
  签到
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://kd.youth.cn/TaskCenter/sign'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('签到')
    print(response)
    if response['status'] == 1:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def signInfo(headers):
  """
  签到详情
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://kd.youth.cn/TaskCenter/getSign'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('签到详情')
    print(response)
    if response['status'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def punchCard(headers):
  """
  打卡报名
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}PunchCard/signUp'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('打卡报名')
    print(response)
    if response['code'] == 1:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def doCard(headers):
  """
  早起打卡
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}PunchCard/doCard'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('早起打卡')
    print(response)
    if response['code'] == 1:
      shareCard(headers=headers)
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def shareCard(headers):
  """
  打卡分享
  :param headers:
  :return:
  """
  time.sleep(0.3)
  startUrl = f'{YOUTH_HOST}PunchCard/shareStart'
  endUrl = f'{YOUTH_HOST}PunchCard/shareEnd'
  try:
    response = requests_session().post(url=startUrl, headers=headers, timeout=30).json()
    print('打卡分享')
    print(response)
    if response['code'] == 1:
      time.sleep(0.3)
      responseEnd = requests_session().post(url=endUrl, headers=headers, timeout=30).json()
      if responseEnd['code'] == 1:
        return responseEnd
    else:
      return
  except:
    print(traceback.format_exc())
    return

def luckDraw(headers):
  """
  打卡分享
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}PunchCard/luckdraw'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('七日签到')
    print(response)
    if response['code'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def timePacket(headers):
  """
  计时红包
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}TimePacket/getReward'
  try:
    response = requests_session().post(url=url, data=f'{headers["Referer"].split("?")[1]}', headers=headers, timeout=30).json()
    print('计时红包')
    print(response)
    return
  except:
    print(traceback.format_exc())
    return

def watchWelfareVideo(headers):
  """
  观看福利视频
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}NewTaskIos/recordNum?{headers["Referer"].split("?")[1]}'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=30).json()
    print('观看福利视频')
    print(response)
    return
  except:
    print(traceback.format_exc())
    return

def shareArticle(headers, body):
  """
  分享文章
  :param headers:
  :return:
  """
  url = 'https://ios.baertt.com/v2/article/share/put.json'
  headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('分享文章')
    print(response)
    return
  except:
    print(traceback.format_exc())
    return

def threeShare(headers, action):
  """
  三餐分享
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}ShareNew/execExtractTask'
  headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
  body = f'{headers["Referer"].split("?")[1]}&action={action}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('三餐分享')
    print(response)
    return
  except:
    print(traceback.format_exc())
    return

def openBox(headers):
  """
  开启宝箱
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}invite/openHourRed'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('开启宝箱')
    print(response)
    if response['code'] == 1:
      share_box_res = shareBox(headers=headers)
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def shareBox(headers):
  """
  宝箱分享
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}invite/shareEnd'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('宝箱分享')
    print(response)
    if response['code'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def friendList(headers):
  """
  好友列表
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}ShareSignNew/getFriendActiveList'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=30).json()
    print('好友列表')
    print(response)
    if response['error_code'] == '0':
      if len(response['data']['active_list']) > 0:
        for friend in response['data']['active_list']:
          if friend['button'] == 1:
            time.sleep(1)
            friendSign(headers=headers, uid=friend['uid'])
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def friendSign(headers, uid):
  """
  好友签到
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}ShareSignNew/sendScoreV2?friend_uid={uid}'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=30).json()
    print('好友签到')
    print(response)
    if response['error_code'] == '0':
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def sendTwentyScore(headers, action):
  """
  每日任务
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}NewTaskIos/sendTwentyScore?{headers["Referer"].split("?")[1]}&action={action}'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=30).json()
    print(f'每日任务 {action}')
    print(response)
    if response['status'] == 1:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def watchAdVideo(headers):
  """
  看广告视频
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://kd.youth.cn/taskCenter/getAdVideoReward'
  headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
  try:
    response = requests_session().post(url=url, data="type=taskCenter", headers=headers, timeout=30).json()
    print('看广告视频')
    print(response)
    if response['status'] == 1:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def watchGameVideo(body):
  """
  激励视频
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/Game/GameVideoReward.json'
  headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
  try:
    response = requests_session().post(url=url, headers=headers, data=body, timeout=30).json()
    print('激励视频')
    print(response)
    if response['success'] == True:
      return response['items']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def visitReward(body):
  """
  回访奖励
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/mission/msgRed.json'
  headers = {
    'User-Agent': 'KDApp/1.8.0 (iPhone; iOS 14.2; Scale/3.00)',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('回访奖励')
    print(response)
    if response['success'] == True:
      return response['items']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def articleRed(body):
  """
  惊喜红包
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/article/red_packet.json'
  headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('惊喜红包')
    print(response)
    if response['success'] == True:
      return response['items']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def readTime(body):
  """
  阅读时长
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/user/stay.json'
  headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('阅读时长')
    print(response)
    if response['error_code'] == '0':
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def rotary(headers, body):
  """
  转盘任务
  :param headers:
  :return:
  """
  time.sleep(0.3)
  currentTime = time.time()
  url = f'{YOUTH_HOST}RotaryTable/turnRotary?_={currentTime}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('转盘任务')
    print(response)
    return response
  except:
    print(traceback.format_exc())
    return

def rotaryChestReward(headers, body):
  """
  转盘宝箱
  :param headers:
  :return:
  """
  time.sleep(0.3)
  currentTime = time.time()
  url = f'{YOUTH_HOST}RotaryTable/getData?_={currentTime}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('转盘宝箱')
    print(response)
    if response['status'] == 1:
      i = 0
      while (i <= 3):
        chest = response['data']['chestOpen'][i]
        if response['data']['opened'] >= int(chest['times']) and chest['received'] != 1:
          time.sleep(1)
          runRotary(headers=headers, body=f'{body}&num={i+1}')
        i += 1
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def runRotary(headers, body):
  """
  转盘宝箱
  :param headers:
  :return:
  """
  time.sleep(0.3)
  currentTime = time.time()
  url = f'{YOUTH_HOST}RotaryTable/chestReward?_={currentTime}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('领取宝箱')
    print(response)
    if response['status'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def doubleRotary(headers, body):
  """
  转盘双倍
  :param headers:
  :return:
  """
  time.sleep(0.3)
  currentTime = time.time()
  url = f'{YOUTH_HOST}RotaryTable/toTurnDouble?_={currentTime}'
  try:
    response = requests_session().post(url=url, data=body, headers=headers, timeout=30).json()
    print('转盘双倍')
    print(response)
    if response['status'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def incomeStat(headers):
  """
  收益统计
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'https://kd.youth.cn/wap/user/balance?{headers["Referer"].split("?")[1]}'
  try:
    response = requests_session().get(url=url, headers=headers, timeout=50).json()
    print('收益统计')
    print(response)
    if response['status'] == 0:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def withdraw(body):
  """
  自动提现
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v5/wechat/withdraw2.json'
  headers = {
    'User-Agent': 'KDApp/1.8.0 (iPhone; iOS 14.2; Scale/3.00)',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, headers=headers, data=body, timeout=30).json()
    print('自动提现')
    print(response)
    if response['success'] == True:
      return response['items']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def bereadRed(headers):
  """
  时段红包
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = f'{YOUTH_HOST}Task/receiveBereadRed'
  try:
    response = requests_session().post(url=url, headers=headers, timeout=30).json()
    print('时段红包')
    print(response)
    if response['code'] == 1:
      return response['data']
    else:
      return
  except:
    print(traceback.format_exc())
    return

def startApp(headers, body):
  """
  启动App
  :param headers:
  :return:
  """
  time.sleep(0.3)
  url = 'https://ios.baertt.com/v6/count/start.json'
  headers = {
    'User-Agent': 'KDApp/1.8.0 (iPhone; iOS 14.2; Scale/3.00)',
    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
  }
  try:
    response = requests_session().post(url=url, headers=headers, data=body, timeout=30).json()
    print('启动App')
    print(response)
    if response['success'] == True:
      return response
    else:
      return
  except:
    print(traceback.format_exc())
    return

def run():
  title = f'📚中青看点'
  content = ''
  result = ''
  beijing_datetime = get_standard_time()
  print(f'\n【中青看点】{beijing_datetime.strftime("%Y-%m-%d %H:%M:%S")}')
  hour = beijing_datetime.hour
  for i, account in enumerate(COOKIELIST):
    headers = account.get('YOUTH_HEADER')
    readBody = account.get('YOUTH_READBODY')
    redBody = account.get('YOUTH_REDBODY')
    readTimeBody = account.get('YOUTH_READTIMEBODY')
    withdrawBody = account.get('YOUTH_WITHDRAWBODY')
    shareBody = account.get('YOUTH_SHAREBODY')
    startBody = account.get('YOUTH_STARTBODY')
    rotaryBody = f'{headers["Referer"].split("&")[15]}&{headers["Referer"].split("&")[8]}'

    if startBody:
      startApp(headers=headers, body=startBody)
    sign_res = sign(headers=headers)
    if sign_res and sign_res['status'] == 1:
      content += f'【签到结果】：成功 🎉 明日+{sign_res["nextScore"]}青豆'
    elif sign_res and sign_res['status'] == 2:
      send(title=title, content=f'【账户{i+1}】Cookie已过期，请及时重新获取')
      continue

    sign_info = signInfo(headers=headers)
    if sign_info:
      content += f'\n【账号】：{sign_info["user"]["nickname"]}'
      content += f'\n【签到】：+{sign_info["sign_score"]}青豆 已连签{sign_info["total_sign_days"]}天'
      result += f'【账号】: {sign_info["user"]["nickname"]}'
    friendList(headers=headers)
    if hour > 12:
      punch_card_res = punchCard(headers=headers)
      if punch_card_res:
        content += f'\n【打卡报名】：打卡报名{punch_card_res["msg"]} ✅'
    if hour >= 5 and hour <= 8:
      do_card_res = doCard(headers=headers)
      if do_card_res:
        content += f'\n【早起打卡】：{do_card_res["card_time"]} ✅'
    luck_draw_res = luckDraw(headers=headers)
    if luck_draw_res:
      content += f'\n【七日签到】：+{luck_draw_res["score"]}青豆'
    visit_reward_res = visitReward(body=readBody)
    if visit_reward_res:
      content += f'\n【回访奖励】：+{visit_reward_res["score"]}青豆'
    if shareBody:
      shareArticle(headers=headers, body=shareBody)
      for action in ['beread_extra_reward_one', 'beread_extra_reward_two', 'beread_extra_reward_three']:
        time.sleep(5)
        threeShare(headers=headers, action=action)
    open_box_res = openBox(headers=headers)
    if open_box_res:
      content += f'\n【开启宝箱】：+{open_box_res["score"]}青豆 下次奖励{open_box_res["time"] / 60}分钟'
    watch_ad_video_res = watchAdVideo(headers=headers)
    if watch_ad_video_res:
      content += f'\n【观看视频】：+{watch_ad_video_res["score"]}个青豆'
    watch_game_video_res = watchGameVideo(body=readBody)
    if watch_game_video_res:
      content += f'\n【激励视频】：{watch_game_video_res["score"]}个青豆'
    # article_red_res = articleRed(body=redBody)
    # if article_red_res:
    #   content += f'\n【惊喜红包】：+{article_red_res["score"]}个青豆'
    read_time_res = readTime(body=readTimeBody)
    if read_time_res:
      content += f'\n【阅读时长】：共计{int(read_time_res["time"]) // 60}分钟'
    if (hour >= 6 and hour <= 8) or (hour >= 11 and hour <= 13) or (hour >= 19 and hour <= 21):
      beread_red_res = bereadRed(headers=headers)
      if beread_red_res:
        content += f'\n【时段红包】：+{beread_red_res["score"]}个青豆'
    for i in range(0, 5):
      time.sleep(5)
      rotary_res = rotary(headers=headers, body=rotaryBody)
      if rotary_res:
        if rotary_res['status'] == 0:
          break
        elif rotary_res['status'] == 1:
          content += f'\n【转盘抽奖】：+{rotary_res["data"]["score"]}个青豆 剩余{rotary_res["data"]["remainTurn"]}次'
          if rotary_res['data']['doubleNum'] != 0 and rotary_res['data']['score'] > 0:
            double_rotary_res = doubleRotary(headers=headers, body=rotaryBody)
            if double_rotary_res:
              content += f'\n【转盘双倍】：+{double_rotary_res["score"]}青豆 剩余{double_rotary_res["doubleNum"]}次'

    rotaryChestReward(headers=headers, body=rotaryBody)
    for i in range(5):
      watchWelfareVideo(headers=headers)
    timePacket(headers=headers)
    for action in ['watch_article_reward', 'watch_video_reward', 'read_time_two_minutes', 'read_time_sixty_minutes', 'new_fresh_five_video_reward', 'first_share_article']:
      time.sleep(5)
      sendTwentyScore(headers=headers, action=action)
    stat_res = incomeStat(headers=headers)
    if stat_res['status'] == 0:
      for group in stat_res['history'][0]['group']:
        content += f'\n【{group["name"]}】：+{group["money"]}青豆'
      today_score = int(stat_res["user"]["today_score"])
      score = int(stat_res["user"]["score"])
      total_score = int(stat_res["user"]["total_score"])

      if score >= 300000 and withdrawBody:
        with_draw_res = withdraw(body=withdrawBody)
        if with_draw_res:
          result += f'\n【自动提现】：发起提现30元成功'
          content += f'\n【自动提现】：发起提现30元成功'
          send(title=title, content=f'【账号】: {sign_info["user"]["nickname"]} 发起提现30元成功')

      result += f'\n【今日收益】：+{"{:4.2f}".format(today_score / 10000)}'
      content += f'\n【今日收益】：+{"{:4.2f}".format(today_score / 10000)}'
      result += f'\n【账户剩余】：{"{:4.2f}".format(score / 10000)}'
      content += f'\n【账户剩余】：{"{:4.2f}".format(score / 10000)}'
      result += f'\n【历史收益】：{"{:4.2f}".format(total_score / 10000)}\n\n'
      content += f'\n【历史收益】：{"{:4.2f}".format(total_score / 10000)}\n'

  print(content)

  # 每天 21:00 发送消息推送
  if beijing_datetime.hour == 21 and beijing_datetime.minute >= 0 and beijing_datetime.minute < 59:
    send(title=title, content=result)
  elif not beijing_datetime.hour == 21:
    print('未进行消息推送，原因：没到对应的推送时间点\n')
  else:
    print('未在规定的时间范围内\n')

if __name__ == '__main__':
    run()
