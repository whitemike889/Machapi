#!/usr/bin/env python3

import sys
sys.path.insert( 0, '..' )

# this will later be a session multiplexer object in a module abstraction library
from Engines.POF_com import Session as POFSession

def Main():
    config = POFSession.Config("config.ini")

    testSession = POFSession(config)
    testSession.login()

    users = testSession.searchUsers(config, 5, online_only=True)

    print("Total Users Found: {0}".format( len(users) ) )

    testSession.broadcastMessage(users, "hey whats up")


if __name__ == '__main__':
    Main()
