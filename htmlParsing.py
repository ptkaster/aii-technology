from sys import platform
from bs4 import BeautifulSoup
# from deepface import DeepFace
import concurrent.futures
import urllib.request
import random
import os
import time
import json


if(platform == "darwin"):
    FILE_PATH = ""
elif(platform == "linux"):
    FILE_PATH = ""

def parse_linkedin_to_csv(file_link):
    try:
        print(file_link)
        list_of_profiles = []
        with open(FILE_PATH + file_link) as raw_html:
            html = BeautifulSoup(raw_html, 'html.parser')
            company_name = html.find('h1', 'org-top-card-summary__title').find('span').text.strip()
            for p in html.find_all('li', 'org-people-profiles-module__profile-item'):
                profile = {}
                # This is for if they have a name
                # try:
                #     name = (p.find('div', 'org-people-profile-card__profile-title')).text.strip()
                #     profile["name"] = name
                #     print(name)
                #     title = (p.find('div', 'lt-line-clamp--multi-line')).text.strip()
                #     profile["title"] = title
                #     for image in p.find_all('img'):
                #         try:
                #             # This removes the profiles of connections of someone
                #             if(not "EntityPhoto-circle-1" in image['class']):
                #                 # This removes the ghost profiles
                #                 if(not "ghost-person" in image['class']):
                #                     # This removes the cover photos
                #                     if(not "org-people-profile-card__cover-photo" in image['class']):
                #                         profile["image"] = image['src']
                #         except:
                #             pass
                #     list_of_profiles.append(profile)
                # except Exception as asc:
                #     print("Error in parsing personal profile: " + str(asc))
                # Or for if they don't
                try:
                    name = (p.find('div', 'artdeco-entity-lockup__title')).text.strip()
                    profile["name"] = name
                    print(name)
                    title = (p.find('div', 'lt-line-clamp--multi-line')).text.strip()
                    profile["title"] = title
                    profile_link = (p.find('a'))['href'].strip()
                    profile["profile_link"] = "https://www.linkedin.com" + str(profile_link)
                    for image in p.find_all('img'):
                        try:
                            # This removes the profiles of connections of someone
                            if(not "EntityPhoto-circle-1" in image['class']):
                                # This removes the ghost profiles
                                if(not "ghost-person" in image['class']):
                                    # This removes the cover photos
                                    if(not "org-people-profile-card__cover-photo" in image['class']):
                                        profile["image"] = image['src']
                        except:
                            pass
                    list_of_profiles.append(profile)
                except Exception as asc:
                    print("Error in parsing personal profile: " + str(asc))

        csv_string = "Company Name,Employee Name,Title,Profile,Image\n"

        for profile in list_of_profiles:
            csv_string += company_name + ","
            csv_string += profile["name"].replace(",","") + ","
            print("Name: " + profile["name"].replace(",",""))
            csv_string += profile["title"].replace(",","") + ","
            print("Title: " + profile["title"].replace(",",""))
            csv_string += "=HYPERLINK(\"" + profile["profile_link"].replace(",","") + "\")"
            try:
                csv_string += "," + "=HYPERLINK(\"" + profile["image"].replace(",","") + "\")"
            except Exception as asc:
                print(asc)
            csv_string += "\n"

        delete_files([FILE_PATH + file_link])
        return csv_string


    except Exception as asc:
        print("Error in parsing html: " + str(asc))

def ai_output(file_link):
    try:
        print(file_link)
        list_of_profiles = []
        with open(FILE_PATH + file_link) as raw_html:
            html = BeautifulSoup(raw_html, 'html.parser')
            for p in html.find_all('li', 'org-people-profiles-module__profile-item'):
                profile = {}
                try:
                    name = (p.find('div', 'org-people-profile-card__profile-title')).text.strip()
                    profile["name"] = name
                    print(name)
                    title = (p.find('div', 'lt-line-clamp--multi-line')).text.strip()
                    profile["title"] = title
                    for image in p.find_all('img'):
                        try:
                            # This removes the profiles of connections of someone
                            if(not "EntityPhoto-circle-1" in image['class']):
                                # This removes the ghost profiles
                                if(not "ghost-person" in image['class']):
                                    # This removes the cover photos
                                    if(not "org-people-profile-card__cover-photo" in image['class']):
                                        # This makes sure there is a face in the photo
                                        if(verify_face_exists(image['src'])):
                                            profile["image"] = image['src']
                                        else:
                                            print("Failed verification for face of " + name)
                        except:
                            pass
                    list_of_profiles.append(profile)
                except Exception as asc:
                    print("Error in parsing personal profile: " + str(asc))

        url_list = []
        for profile in list_of_profiles:
            try:
                url_list.append(profile["image"])
            except:
                pass

        weights = classify_images(url_list)

        image_iterator = 0
        return_string = ""
        for profile in list_of_profiles:
            return_string += "<br><br>"
            return_string += "Name: " + profile["name"] + "<br>"
            return_string += "Title: " + profile["title"] + "<br>"
            print("Name: " + profile["name"])
            print("Title: " + profile["title"])
            try:
                profile["image"]
                return_string += "Photo classification: " + str(weights[image_iterator]["dominant_race"]) + "<br>"
                return_string += "Photo classification: " + str(weights[image_iterator]) + "<br>"
                try:
                    return_string += "Name classification: " + str(namsor_race(profile["name"].split(" ")[0], profile["name"].split(" ")[1])) + "<br>"
                except:
                    pass
                print("Classification: " + str(weights[image_iterator]["dominant_race"]))
                image_iterator += 1
            except Exception as asc:
                print(asc)

        delete_files([FILE_PATH + file_link])
        return return_string


    except Exception as asc:
        print("Error in parsing html: " + str(asc))

# Pulls racial / ethnic data from Namsor API
def namsor_race(first_name, last_name):
    url = "https://v2.namsor.com/NamSorAPIv2/api2/json/usRaceEthnicity/" + first_name.strip() + "/" + last_name.strip()

    req = urllib.request.Request(url)
    req.add_header('X-API-KEY', '9e68cc643f7e4c7e0490f68f56024703')
    response = urllib.request.urlopen(req)
    data = json.loads(str(response.read().decode('UTF-8')))
    return_dict = {}
    return_dict["namsor_race_ethnicity_main"] = data["raceEthnicity"]
    return_dict["namsor_race_ethnicity_confidence"] = data["probabilityCalibrated"]

    return return_dict

# Checks if the face exists in the image or not, otherwise we get errors. Very quick
def verify_face_exists(img_link):
    img_name = download_image(img_link)
    try:

        DeepFace.detectFace(img_name)
        delete_files([img_name])
        return True
    except Exception as asc:
        delete_files([img_name])
        return False

def download_image(link):
    filename = "temp_images/" + str(random.randrange(1000000, 999999999999999999999999999)) + '.jpg'
    time.sleep(.25)
    urllib.request.urlretrieve(link, filename)
    return filename

def delete_files(link_list):
    for link in link_list:
        os.remove(link)

# def classify_profiles(list_of_profiles):
#
#     for

def classify_images(url_list):
    filenames = []
    for url in url_list:
        filenames.append(download_image(url))
    objs = DeepFace.analyze(filenames, actions = ['gender', 'race'])
    delete_files(filenames)
    output = []
    for instance in range(1,len(objs.keys()) + 1):
        output.append(objs["instance_" + str(instance)])

    return output

if __name__ == "__main__":
    print(namsor_race("paul", "kaster"))
