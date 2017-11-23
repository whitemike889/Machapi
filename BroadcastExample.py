from pofapi.POFSession import POFSession

# not POFSession Library
def Main():
    config = POFSession.Config("config.ini")

    testSession = POFSession(config)
    testSession.login(config.username, config.password)

    users = testSession.searchUsers(config, 5, online_only=True)

    print("Total Users Found: {0}".format( len(users) ) )

    testSession.broadcastMessage(users, "hey whats up")


if __name__ == '__main__':
    Main()
