#!/usr/bin/python
import json

from pofapi import POFSession

def Main():
    config = {}

    with open('config.json', 'r') as f:
        config = json.load(f)

    Session = POFSession.POFSession()
    Session.Criteria = config["SearchCriteria"]

    Session.login(config["Credentials"]["Username"], config["Credentials"]["Password"])

    userIDs = Session.getOnlineUsers(30, False)
    for userID in userIDs:
        Session.sendEmail(userID, "Hey, what's up?")


if __name__ == '__main__':
    Main()


# Credentials = {
#     'Username': '***********',
#     'Password': '***********'
# }
#
# Session.Criteria = {
#     # Your gender
#     'iama': 'm',
#     # Minimum Age
#     'minage': '18',
#     # Maximum Age
#     'maxage': '45',
#     # Zip Code
#     'city': '90210',
#     # Desired Gender
#     'seekinga': 'f',
#     # Search Radius from Zip Code
#     'miles': '25',
#     # Not implemented but required to be present.
#     'interests': '',
#     'country': '1',
#     'height': '',
#     'heightb': '',
#     'maritalstatus': '',
#     'relationshipage_id': '',
#     'wantchildren': '',
#     'smoke': '',
#     'drugs': '',
#     'body': '',
#     'smarts': '',
#     'pets': '',
#     'eyes_id': '',
#     'income': '',
#     'profession_id': '',
#     'haircolor': '',
#     'drink': '',
#     'religion': '',
#     'haschildren': '',
# }

# Config = {
#    'Credentials': Credentials,
#    'SearchCriteria': Session.Criteria,
# }

# with open('config.json', 'w') as f:
#    json.dump(Config, f, indent=4)