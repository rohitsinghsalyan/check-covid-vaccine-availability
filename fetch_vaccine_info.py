'''
python3 fetch_vaccine_info.py --date "31-05-2021" --city "bangalore" --token "" --save_csv "y" --dose 2 --age_limit 45

'''
import requests
import json
import pandas as pd
import argparse
import time
import beepy
import sys

# Fucntions
def get_vaccine_df(pincode, date, token):
    '''
    get the API output and extract the required fields
    '''
    if token != "":
        req_text = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByPin?pincode={}&date={}".format(pincode,date)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',\
            'Authorization': token}
        with requests.get(req_text,headers=headers) as r:
            output = r.text
        if r.status_code != 200:
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
            req_text = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(pincode,date)
            with requests.get(req_text,headers=headers) as r:
                if r.status_code != 200:
                    print(r.status_code)
                output = r.text
    else:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
        req_text = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(pincode,date)
        with requests.get(req_text,headers=headers) as r:
            if r.status_code != 200:
                print(r.status_code)
            output = r.text
    try:
        output_json = json.loads(output)
        centers = output_json.get("centers")
    except:
        centers = []
    return centers

def get_schedule_df(centers_payload, age_limit):
    '''
    converts the API output to DF and filters as required by the user
    '''
    vaccine_schedule_df = pd.DataFrame()
    for i in centers_payload:
        name = i['name']
        address = i['address']
        pincode = i['pincode']
        lat = i['lat']
        lon = i['long']
        fee_type = i['fee_type']
        sessions = i['sessions']
        try:
            vaccine_fees = i['vaccine_fees'][0]['vaccine']+":"+i['vaccine_fees'][0]['fee']
        except:
            vaccine_fees = 'free'
        for j in sessions:
            date = j['date']
            available_capacity_dose1 = j['available_capacity_dose1']
            available_capacity_dose2 = j['available_capacity_dose2']
            min_age_limit = j['min_age_limit']
            if min_age_limit != age_limit:
                continue
            vaccine = j['vaccine']
            slots = "|".join(j['slots'])
            temp = pd.DataFrame({"name":[name],"address":[address],"pincode":[pincode],"lat":[lat],"lon":[lon],\
                                 "fee_type":[fee_type],"vaccine_fees":[vaccine_fees],"date":[date],"available_capacity_dose1":[available_capacity_dose1],"available_capacity_dose2":[available_capacity_dose2],"min_age_limit":[min_age_limit],\
                                 "vaccine":[vaccine],"slots":[slots]})
            vaccine_schedule_df = vaccine_schedule_df.append(temp,ignore_index=True)
    return vaccine_schedule_df

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Fecth Vaccine availability')
    parser.add_argument('--date', type=str,
                        help='specify the date', required=True)
    parser.add_argument('--city', type=str,
                        help='specify the city', required=True)
    parser.add_argument('--token', type=str,
                        help='specify the token', required=True)
    parser.add_argument('--save_csv', type=str,
                        help='specify if output is to be written', required=True)
    parser.add_argument('--dose', type=int,
                        help='specify the dose', required=True)
    parser.add_argument('--age_limit', type=int,
                        help='specify the age limit', required=True)    
    args = parser.parse_args()
    date_req = str(args.date)
    city = str(args.city)
    token = str(args.token)
    save_csv = str(args.save_csv)
    dose = args.dose
    age_limit = args.age_limit
    city_pincodes = pd.read_csv("pincode_list.csv")
    print("looking for vaccine slots in {} for date {} onwards".format(city, date_req))
    list_of_pincodes = list(set(city_pincodes[city_pincodes["district"].str.contains(city, case=True, regex=True)].pincode))
    print(len(list_of_pincodes))
    if len(list_of_pincodes) == 0:
        print("sorry your region pincodes could not be found, check spelling or try some variation!!")
        sys.exit()
    availablity = 0
    while availablity < 500:
        t1 = time.time()
        all_vaccination_schedule = pd.DataFrame()
        for pincode in list_of_pincodes:
            centers_data = get_vaccine_df(pincode, date_req, token)
            if len(centers_data) == 0:
                continue
            pincode_wise_vac_df = get_schedule_df(centers_data, age_limit)
            all_vaccination_schedule = all_vaccination_schedule.append(pincode_wise_vac_df,ignore_index=True)
        availablity = sum(all_vaccination_schedule["available_capacity_dose{}".format(dose)])
        print("Total Dose {} available in {}:".format(dose, city), availablity)
        pincodes_non_zero_dose = all_vaccination_schedule[all_vaccination_schedule["available_capacity_dose{}".format(dose)]>0]
        if save_csv == "y":
            pincodes_non_zero_dose.to_csv("{}_{}_{}_plus_dose-{}.csv".format(date_req, city, age_limit, dose), index=False)
        if (availablity > 5) & (availablity <= 200):
            beepy.beep(sound='coin')
        elif availablity > 200:
            beepy.beep(sound='success')
        else:
            pass
        for i in range(len(pincodes_non_zero_dose)):
            print("{} | {} | {} | {} | {}".format(pincodes_non_zero_dose["pincode"].iloc[i], pincodes_non_zero_dose["fee_type"].iloc[i], pincodes_non_zero_dose["date"].iloc[i], pincodes_non_zero_dose["name"].iloc[i], pincodes_non_zero_dose["vaccine"].iloc[i]))
        t2 = time.time()
        print("time taken = ", t2 - t1)
