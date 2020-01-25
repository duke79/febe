# # from pyinrail import pyinrail
# #
# # enq = pyinrail.RailwayEnquiry(
# #     src='new delhi', dest='ahmedabad', date='12-05-2019')
# # df = enq.get_trains_between_stations(as_df=True)
# # print(df)
#
# # Python program to find live train
# # status using RAILWAY API
#
# # import required modules
# import requests, json
#
# # enter your api key here
# api_key = "6uu8vcypeq"
#
# # base_url variable to store url
# base_url = "https://api.railwayapi.com/v2/live/train/"
#
# # enter train_number here
# train_number = "12056"
#
# # enter current date in dd-mm-yyyy format
# current_date = "05-05-2019"
#
# # complete_url variable to
# # store complete url address
# complete_url = base_url + train_number + "/date/" + current_date + "/apikey/" + api_key + "/"
#
# # get method of requests module
# # return response object
# response_ob = requests.get(complete_url)
#
# # json method of response object convert
# # json format data into python format data
# print(response_ob.content)
# result = response_ob.json()
#
# # Now result contains list of nested dictionaries
# # Check the value of "response_code" key is equal
# # to "200" or not if equal that means record is
# # found otherwise record is not found
# if result["response_code"] == 200:
#
#     # train name is extracting from
#     # the result variable data
#     train_name = result["train"]["name"]
#
#     # store the value or data of
#     # "route" key in variable y
#     y = result["route"]
#
#     # source station name is extracting
#     # from the y variable data
#     source_station = y[0]["station"]["name"]
#
#     # destination station name is
#     # extracting from the y varibale data
#     destination_station = y[len(y) - 1]["station"]["name"]
#
#     # store the value of "position"
#     # key in variable position
#     position = result["position"]
#
#     # print following values
#     print(" train name : " + str(train_name)
#           + "\n source station : " + str(source_station)
#           + "\n destination station : " + str(destination_station)
#           + "\n current status : " + str(position))
#
# else:
#     print("record is not found for given request")
import json

from selenium.webdriver.common.keys import Keys

from lib.py.core.traces import print_exception_traces
from lib.py.misc.spider import Spider


def cbse(roll_number, standard=10, year=2006):
    with Spider() as spider:
        driver = spider.driver()
        url = "http://resultsarchives.nic.in/cbseresults/cbseresults{0}/class{1}/cbse{1}.htm".format(year, standard)
        driver.get(url)
        input = driver.find_element_by_tag_name("input")
        input.clear()
        input.send_keys(roll_number)
        input.send_keys(Keys.RETURN)

        result = {}
        columns = [column.text for column in
                   driver.find_elements_by_css_selector("body > div:nth-child(7) > table  tr  td  font")]

        result["roll_number"] = columns[1]
        assert result["roll_number"] == roll_number
        result["name"] = columns[4]
        result["mother_name"] = columns[6]
        result["father_name"] = columns[8]
        result["d_o_b"] = columns[10]

        result["subjects"] = []
        rows = driver.find_elements_by_css_selector("center table tr")
        for row in rows[1:-1]:
            columns = row.find_elements_by_css_selector("td font")
            subject = {}
            subject["code"] = columns[0].text
            subject["name"] = columns[1].text
            subject["marks"] = columns[2].text
            subject["grade"] = columns[3].text
            result["subjects"].append(subject)
        status_raw = rows[-1].find_element_by_css_selector("td font").text
        result["status"] = str(status_raw).split(":")[-1].strip()
        return result


ret = cbse(roll_number="5725352", year="2008", standard="12")
try:
    json_data = json.dumps(ret)
    print(json_data)
except TypeError as e:
    print_exception_traces(e)
print(ret)
