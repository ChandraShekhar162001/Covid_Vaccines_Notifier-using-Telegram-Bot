import requests
from datetime import datetime 

base_url="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
now=datetime.now()
today_date=now.strftime("%d-%m-%Y")
group_id="surat_corporation"
api_telegram="https://api.telegram.org/bot1748658539:AAG3tabLdWBU06BCFe5Ho5AF4gOmc0lJPCI/sendMessage?chat_id=@__groupid__&text=Vaccination Centers for 18-44 age group:"

Gujarat_District_id={776}

def fetch_data_cowin(district_id):
  query_params="?district_id={}&date={}".format(district_id,today_date)
  headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
  final_url=base_url+query_params
  response=requests.get(final_url,headers=headers)
  extract_availability_data(response)
  #print(response.text)

def fetch_data_for_state(district_id):
  for district_id in district_ids:
    fetch_data_from_cowin(district_id)

def extract_availability_data(response):
  response_json=response.json()
  for center in response_json["centers"]:
    for session in center["sessions"]:
      if session["available_capacity_dose1"]>0 and session["min_age_limit"]<=45:
        message="\n {} ({}) - Pin:{},\n Vaccine: {},\n Cost: {} \n Total {} slots are available for dose 1 on {}\n (Dose1: {}, Dose2: {}) ".format(
            center["name"],center["block_name"],center["pincode"],session["vaccine"],center["fee_type"],session["available_capacity_dose1"],session["date"],session["available_capacity_dose1"],session["available_capacity_dose2"])
        send_message_telegram(message)

def send_message_telegram(message):
  final_telegram_url=api_telegram.replace("__groupid__", group_id)
  final_telegram_url=final_telegram_url+message
  response=requests.get(final_telegram_url)
  print(response)

if __name__=="__main__":
  fetch_data_cowin(776)
