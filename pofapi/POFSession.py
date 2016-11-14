import requests
from Parser import Parser
from Helpers import eprint
import requests
from furl import furl
import sqlite3


# Should be bound to POFSession class
class UserHistory():
    def __init__(self, username):
        self.conn = sqlite3.connect("%s.db" % (username))
        if self.conn is not None:
            self.DB = self.conn.cursor()
            self.ensureMessageHistoryTable()
        else:
            eprint("There was an error establishing the user history database connection.  Exiting.")
            exit(1)

    def addUserContactEvent(self, userID, message):
        # adds a contact event to the database
        # uses currentTime

        query = """
			INSERT INTO {tableName} VALUES(
				NULL,
				{user},
				DATETIME('now', 'localtime'),
				{previouslyContacted},
				"{payload}"
			);
		""".format(
            tableName="ContactEvents",
            user=userID,
            previouslyContacted=int(self.isPreviouslyContactedUser(userID)),
            payload=message
        )

        self.DB.execute(query)
        self.conn.commit()
        #print("Added user to db.")

    def canMakeNewContacts(self):
        # Checks to see if 50 messages have been sent out to new users in the last 24 hours.
        pass


    # This returns 0|1
    def isPreviouslyContactedUser(self, userID):
        # checks to see if a specific user has been previously contacted
        # critical that this works to avoid spamming people
        query = """
			SELECT COUNT (firstContact) from {tableName} where targetUserID={uid};
			""".format(
            tableName="ContactEvents",
            uid=userID
        )
        r = self.DB.execute(query)
        rowcount = r.fetchone()[0]
        return rowcount > 0

    def ensureMessageHistoryTable(self):
        query = """
			CREATE TABLE IF NOT EXISTS {tableName} (
				entryID PRIMARY KEY,
				targetUserID integer,
				time DATETIME,
				firstContact integer,
				message text
			);
			""".format(
            tableName="ContactEvents"
        )
        self.DB.execute(query)


class InboxMessage():
    def __init__(self, messageURL, senderName, senderphotoURL, senderProfileURL):
        self.messageURL = "http://www.pof.com/" + messageURL[0]
        self.senderName = senderName[0]
        self.senderPhotoURL = senderphotoURL[0]
        self.senderProfileURL = senderProfileURL[0]


class TranscriptEntry():
    def __init__(self, sender, payload):
        self.sender = sender[0]
        self.payload = payload[0]


class POFSession:
    # debugging method
    def printAllMessages(self):
        if not self.loggedIn:
            eprint("You must be logged in to view your inbox, derp.")
            exit(1)

        for inMsg in self.allMessages():
            print("\n=== New ===")
            for entry in self.viewMessageTranscript(inMsg):
                print(entry.sender + ":\t\t" + entry.payload)

    def viewMessageTranscript(self, InMsg):
        if not self.loggedIn:
            eprint("You must be logged in to view your inbox, derp.")
            exit(1)

        try:
            response = self.Session.get(InMsg.messageURL)
        except requests.exceptions.ConnectError, e:
            eprint("Could not load the specified message.")
            return list()

        transcript = Parser.scrape("viewMessageTranscript", response.content)

        return transcript


    def unreadMessages(self):
        inboxURL = "http://www.pof.com/inbox.aspx"

        if not self.loggedIn:
            eprint("You must be logged in to view your inbox, derp.")
            exit(1)

        try:
            response = self.Session.get(inboxURL)
        except requests.exceptions.ConnectionError, e:
            eprint("Could not get to inbox url: %s"%(inboxURL))
            exit(1)

        # Returns a list of inBoxMessage objects.  List is empty if None.
        newMessages = Parser.scrape("newMessages", response.content)

        return newMessages


    def allMessages(self):
        inboxURL = "http://www.pof.com/inbox.aspx"

        if not self.loggedIn:
            eprint("You must be logged in to view your inbox, derp.")
            exit(1)

        try:
            response = self.Session.get(inboxURL)
        except requests.exceptions.ConnectionError, e:
            eprint("Could not get to inbox url: %s"%(inboxURL))
            exit(1)

        # Returns a list of inBoxMessage objects.  List is empty if None.
        allMessages = Parser.scrape("allMessages", response.content)

        return allMessages


    def login(self, username, password):
        # Get the sid from the front page login form.
        # Can also get this from the response Set-Cookie header as
        loginURLS = {
            "formPage": "http://www.pof.com",
            "processPage": "http://www.pof.com/processLogin.aspx",
        }

        try:
            response = self.Session.get(loginURLS["formPage"])
        except requests.exceptions.ConnectionError, e:
            eprint("Could not reach %s" % (loginURLS["formPage"]), True)
            exit(1)

        sid = Parser.scrape("sid", response.content)
        if sid is None:
            eprint("The site structure has changed since pofapi was written.  Exiting.")
            exit(1)

        loginData = {
            # This is empty but the site still needs it.
            'url': '',
            'username': username,
            'password': password,
            'sid': sid,
            # Also empty.
            'login': '',
        }

        self.Session.headers.update(
            {
                'Accept-Encoding': "gzip, deflate, br",
                'Referer': "http://www.pof.com/",
                'Content-Type': "application/x-www-form-urlencoded",
                'User-Agent': "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
            }
        )

        try:
            login = self.Session.post(loginURLS["processPage"], data=loginData, allow_redirects=True)
        except requests.exceptions.ConnectionError, e:
            eprint("Failed to log in.  Exiting.")
            exit(1)

        if Parser.scrape("isLoginError", login.url):
            print("Failed to log in for username \'%s\'.  Check username and password." % username)
            exit(1)
        else:
            print("Successfully logged in as user %s." % (loginData['username']))
            self.loggedIn = True
            self.username = username
            self.userHistory = UserHistory(username)

        # Give back the requests session object for further interaction.
        return self.Session


    def sendEmail(self, userID, msg):
        # checks database if you've messaged this user before.
        # if user ID is in the database, it will alert the user and not send a message.
        # if user ID is not in the database, it will add the user ID to the database after successfully sending
        # a message.  Failed sends do not append the database.
        messageGateway = "http://www.pof.com/sendmessage.aspx"
        profileURL = "http://www.pof.com/viewprofile.aspx?profile_id=" + userID

        try:
            response = self.Session.get(profileURL)
        except requests.exceptions.ConnectionError, e:
            eprint("Failed to retrieve anti-bot metadata necessary to send the message.  Does the user actually exist?")

        fields = Parser.scrape("msgFormHiddenElements", response.content)

        self.Session.headers.update(
            {
                'Accept-Encoding': "gzip, deflate",
                'Referer': profileURL,
                'Content-Type': "application/x-www-form-urlencoded",
            }
        )
        fields.update(
            {
                "subject": msg,
                "message": msg,
                "sendmesage": "Send Quick Msg",
            }
        )
        try:
            response = self.Session.post(messageGateway, data=fields)
        except requests.exceptions.ConnectionError, e:
            eprint("Connection failure while attempting to send message.  Session dropped?")

        if Parser.sndMsgFailed(response.url):
            eprint("Failed to send a message to user " + userID)
        else:
            print("Successfully sent message to user " + userID)

        self.userHistory.addUserContactEvent(userID, msg)

    def getOnlineUsers(self, count, includePreviousContacts):
        print("Getting online users based on search criteria...")
        # Returns n users online that the user has not contacted before or disables the check based on the {previouslyContactedOK} bool
        users = []
        searchURL = furl("http://www.pof.com/advancedsearch.aspx").add(self.Criteria)
        page = 0

        if not self.loggedIn:
            eprint("You must be logged in to view your inbox, derp.")
            exit(1)

        while (len(users) < count):
            page += 1
            try:
                searchURL.args['page'] = '%d' % page
                #print("Scraping url: %s" % searchURL)
                response = self.Session.get(searchURL.url)
            except requests.exceptions.ConnectionError, e:
                eprint("Could not get to search url: %s"%(searchURL))
                exit(1)

            thisPageUsers = Parser.scrape("onlineUsers", response.content)
            if (len(thisPageUsers) == 0):
                break

            thisPageResults = list()
            for userID in thisPageUsers:
                if includePreviousContacts:
                    # add the user anyway, no check necessary
                    thisPageResults.append(userID)
                else:
                    # includePreviousContacts is false
                    # so check if the user's been contacted previously as indicated in the db
                    # if the user's not been contacted before...add to user list
                    if not self.userHistory.isPreviouslyContactedUser(userID):
                        eprint("UserID %s has been previously contacted.  Skipping." % userID)
                        thisPageResults.append(userID)

            users.extend(thisPageResults)
            users = list(set(users))

        return users[:count]


    def __init__(self):
        self.Session = requests.Session()
        self.loggedIn = False
        self.username = None

        self.Criteria = {
            # Your gender
            'iama': 'f',
            # Minimum Age
            'minage': '18',
            # Maximum Age
            'maxage': '45',
            # Zip Code
            'city': '75201',
            # Desired Gender
            'seekinga': 'f',
            # Search Radius from Zip Code
            'miles': '25',
            # Not implemented
            'interests': '',
            'country': '1',
            'height': '',
            'heightb': '',
            'maritalstatus': '',
            'relationshipage_id': '',
            'wantchildren': '',
            'smoke': '',
            'drugs': '',
            'body': '',
            'smarts': '',
            'pets': '',
            'eyes_id': '',
            'income': '',
            'profession_id': '',
            'haircolor': '',
            'drink': '',
            'religion': '',
            'haschildren': '',
        }
