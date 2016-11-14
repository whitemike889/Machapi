from lxml import html
import re
import urlparse

class Parser():
    # Generic scraping engine.
    @staticmethod
    def scrape(name, raw):
        # Ties parsed input to a common identifier
        cases = {
            "sid": Parser.SID,
            "isLoginError": Parser.isLoginError,
            "newMessages": Parser.newMessages,
            "allMessages": Parser.allMessages,
            "viewMessageTranscript": Parser.viewMessageTranscript,
            "msgFormHiddenElements": Parser.msgFormHiddenElements,
            "sndMsgFailed": Parser.sndMsgFailed,
            "userIDfromURL": Parser.userIDfromURL,
            "onlineUsers": Parser.onlineUsers,
        }
        return cases[name](raw)



    # @staticmethod
    # def limitReached(m):
    #     re.search("new people in a 24 hour period.")
    #
    #     return result


    @staticmethod
    def onlineUsers(m):
        users = list()

        Tree = html.fromstring(m)
        resultTrees = Tree.xpath('//div[@id="wrapper"]/div[@id="container"]/div[@id="searchresults"]/div[contains(@class, "white-row")]/div[@class="results"]')

        propertyPaths = {
            'userURL': 'div[@class="profile"]/a/@href',
            'status': 'div[@class="description"]/div[@class="about"]/font/text()',
        }
        for result in resultTrees:
            # print(html.tostring(messageTree, pretty_print=True, method="html"))
            userURL = result.xpath(propertyPaths['userURL'])
            userID = Parser.scrape("userIDfromURL", userURL[0])
            status = result.xpath(propertyPaths['status'])
            if status[0] == "Online Now":
                users.append(userID[0])
                #print("Found user %s." % userID[0])
        return users

    @staticmethod
    def userIDfromURL(url):
        parsed = urlparse.urlparse(url)
        return urlparse.parse_qs(parsed.query)["profile_id"]

    @staticmethod
    def msgFormHiddenElements(m):
        # Add error handling
        msgFormTree = html.fromstring(m)

        # Add error handling
        hiddenElementsTree = msgFormTree.xpath('//form[@name="sendmessage"]/input[@type="hidden"]')

        hiddenElements = {}
        for entry in hiddenElementsTree:
            hiddenElements[entry.attrib['name']] = entry.attrib['value']

        return hiddenElements

    @staticmethod
    def SID(m):
        # Add error handling
        loginFormTree = html.fromstring(m)

        # Add error handling
        sidxpath = loginFormTree.xpath('//form[@name="frmLogin"]//input[@name="sid"]')
        if len(sidxpath) > 0:
            sid = sidxpath[0].value
        else:
            eprint("Failed to get session ID.")
            sid = None
        return sid


    @staticmethod
    def isLoginError(m):
        return re.search("loginError", m)

    @staticmethod
    def sndMsgFailed(m):
        return not re.search("messagesent=1", m)


    @staticmethod
    def viewMessageTranscript(m):
        # Pagination is not currently supported.  Yet.
        transcript = list()

        # Get ready to burn your eyes out with bleach.
        Tree = html.fromstring(m)
        messageTrees = Tree.xpath('//table[@class="msg-row"]')

        propertyPaths = {
            'sender': 'tr/td/span[@class="username-inbox"]/a/text()',
            'payload': 'tr/td/div[@class="message-content"]/text()',
        }
        for messageTree in messageTrees:
            # print(html.tostring(messageTree, pretty_print=True, method="html"))
            sender = messageTree.xpath(propertyPaths['sender'])
            sender = [x.strip() for x in sender]

            # Fix this.
            payload = messageTree.xpath(propertyPaths['payload'])
            payload = [x.strip() for x in payload]

            transcript.append(TranscriptEntry(sender, payload))
        return transcript


    # Should later merge both these methods as if the site structure changes it'll affect them both in the same way, and alot of the search strings were reused.
    @staticmethod
    def newMessages(m):
        # Pagination is not currently supported.  Yet.
        messages = list()

        Tree = html.fromstring(m)
        messageTrees = Tree.xpath('//form[@name="delete"]/div[@id="inbox-message-list"]/ul[@id="inbox-message-list-messages"]/li[@class="inbox-message-new-bg"]/div[@class="inbox-message-wrapper"]')

        propertyPaths = {
            # 'allMessagesDebug': '//div[@class="inbox-message-wrapper"]/a[contains(@id, "inbox-readmessage-link")]/@href',
            'messageURL': 'a[contains(@id, "inbox-readmessage-link")]/@href',
            'senderName': 'a[contains(@id, "inbox-readmessage-link")]/div[@class="inbox-message-inner-wrapper"]/div[@class="inbox-message-user-name"]/text()',
            'senderPhotoURL': 'a/div[@class="inbox-message-profile-image"]/img[@class="inbox-profile-image"]/@src',
            'senderProfileURL': 'a[1]/@href',
        }
        for messageTree in messageTrees:
            # print(html.tostring(messageTree, pretty_print=True, method="html"))
            messageURL = messageTree.xpath(propertyPaths['messageURL'])

            # Fix this.
            senderName = messageTree.xpath(propertyPaths['senderName'])
            senderName = [x.strip() for x in senderName]

            senderPhotoURL = messageTree.xpath(propertyPaths['senderPhotoURL'])
            senderProfileURL = messageTree.xpath(propertyPaths['senderProfileURL'])

            messages.append(InboxMessage(messageURL, senderName, senderPhotoURL, senderProfileURL))
        return messages


    @staticmethod
    def allMessages(m):
        # Pagination is not currently supported.  Yet.

        messages = list()

        Tree = html.fromstring(m)
        messageTrees = Tree.xpath('//form[@name="delete"]/div[@id="inbox-message-list"]/ul[@id="inbox-message-list-messages"]/li[contains(@id, "inbox-message")]/div[@class="inbox-message-wrapper"]')

        propertyPaths = {
            'messageURL': 'a[contains(@id, "inbox-readmessage-link")]/@href',
            'senderName': 'a[contains(@id, "inbox-readmessage-link")]/div[@class="inbox-message-inner-wrapper"]/div[@class="inbox-message-user-name"]/text()',
            'senderPhotoURL': 'a/div[@class="inbox-message-profile-image"]/img[@class="inbox-profile-image"]/@src',
            'senderProfileURL': 'a[1]/@href',
        }
        for messageTree in messageTrees:
            # print(html.tostring(messageTree, pretty_print=True, method="html"))
            messageURL = messageTree.xpath(propertyPaths['messageURL'])

            # Fix this.
            senderName = messageTree.xpath(propertyPaths['senderName'])
            senderName = [x.strip() for x in senderName]

            senderPhotoURL = messageTree.xpath(propertyPaths['senderPhotoURL'])
            senderProfileURL = messageTree.xpath(propertyPaths['senderProfileURL'])

            messages.append(InboxMessage(messageURL, senderName, senderPhotoURL, senderProfileURL))
        return messages


    # Static, Parser doesn't need instantiated because it is built to be stateless.
    # State management is in the POFSession class.
    def __init__(self):
        pass
