## @package Engines
# The superior method to solving complex problems is by easily consumable and scalable design, not complex code.
#
# The engines package consists of virtual classes and methods that define the structure of the engine modules.
#
# New modules are installed simply by dropping a compliant engine module in the Engines package directory.
#
# The virtual classes and methods are what defines compliance with the engine.  One could simply build these out
# manually without using these but this is highly discouraged unless you really know what you're doing, so long as
# you're okay with future changes in the engine breaking the functionality of the module you are developing.
#
# Your code scanner is probably going to whine because I deviate from PEP8.  That's mostly because the PEP8 is
# worthless bullshit and its evangelical adherents are mostly just eating each others' regurgitations instead of
# thinking.
from abc import ABCMeta
from abc import abstractmethod

import configparser
import requests

## SessionSpec
#
# The SessionSpec class is the core of the module.  This contains the structure of the class you must implement,
# prepackaged for you.  Exceptions will be thrown as required until you have implemented all the necessary minimum
# pieces in the structure required to be used by a multiplexor, which is not required to utilize a module but forces
# continuity between modules when all modules use it.  You are strongly advised not to build a module that does not
# use the base classes defined here if you wish to contribute.
#
# This file also serves as an excellent atomic, academic example of abstract method usage and OOP inheritance in Python.
class SessionSpec:
    __metaclass__ = ABCMeta

    ## Sessionspec.__init__
    #
    # The initialization method for SessionSpec.  It is recommended that you inherit from SessionSpec for your Session
    # class and then call the parent initialization method, and then implement your own module-specific calls in your
    # Session init.  This allows commonalities between modules to be implemented here while also allowing modules to
    # have their own, which will be a necessity as you'll notice while you're building.
    def __init__( self, config ):
        # bind the configuration to the Session object
        self.config = config

        # handle to use for getting new pages with the Session object
        self.client = requests.Session()

        # But wait -- there's more!
        # Throwing in rudimentary proxy support:
        if self.config.proxy_enabled:
            proxies = { 'http', self.config.proxy }
            self.client.proxies.update( proxies )

    ## SessionSpec.SessionError
    #
    # The SessionError subclass defines the Generic exception to be the Session class you are implementing.
    #
    # In the example modules, we use this for just about everything, but a better practice would be to use it as a base
    # class for every TYPE of exception you wish to handle to make your engines more robust in error handling.
    class SessionError( Exception ):
        def __init__( self, value ):
            self.value = value


    ## SessionSpec.login
    #
    # The method used to log in to the site your engine module supports.  Self-explanatory.
    #
    # Note:  When implementing in your module, do NOT return a boolean or use any other indicator of success.  Instead,
    # use SessionSpec.Parser.is_logged_in as a conditional in your logic flow for individual actions.  This prevents
    # your contributors from relying on stateful information in a stateless manner.
    @abstractmethod
    def login( self ):
        pass


    ## SessionSpec.Config
    #
    # While the config file can be universal between engines so long as good naming conventions are used by the module
    # implementations, each SessionSpec child class will want to import the whole config file and bind to local values
    # that the module will want to implement.  Here we have some operations related to that which will be common to all
    # modules, providing a common set of values that I'd like the modules to have.
    #
    # You'll want to call the parent class's initialization and expand upon it for module-specific features.
    class Config:
        def __init__( self, config_file ):
            settings = configparser.ConfigParser( allow_no_value=True )
            settings.read( config_file )

            self.useragent = settings.get( "general-client", "user_agent" )

            self.proxy_enabled = settings.getboolean( "proxy", "enabled" )

            if self.proxy_enabled:
                self.proxy = settings.get( "proxy", "proxy" )

    ## SessionSpec.User
    #
    # The User class must be implemented by the module and must be implemented by all modules, as different sites
    # give users different attributes that the module will be interested in.
    class User:
        @abstractmethod
        def __init__(self):
            pass


    ## SessionSpec.Parser
    #
    # Like all good web browsers, you'll need to interpret the code that the browser retrieves with an engine.  Most
    # browsers call this something else, but the concept is the same:  Code goes in that's served by the endpoint, and
    # usable data comes out that the browser decides how to display.  This parser is the component that handles the
    # conversion of that HTTP response into a usable format for the rest of the engine.  The options here are pretty
    # limitless to the point that building structure around it can only limit the scope of the module, so, feel free
    # to experiment.  Efforts were taken to design the structure in a way that allows you to do this.
    #
    # All methods of the Parser class are static, and extract only one datapoint.  As you add more datapoints to
    # extract and identifiers, you will need to implement those abstract methods in your Parser class and bind the
    # identifier for its dedicated datapoint in the dictionary-based router that associates datapoints with static child
    # methods to your Parser.
    class Parser:
        ## SessionSpec.Parser.scrape
        # @type datapoint: string
        # @param datapoint: Identifier representing a datapoint to be extracted from a larger unprocessed body of data.
        #
        # @type text: string
        # @param text: The unprocessed body of data from which the datapoint should be extracted.
        #
        # scrape defines and associates datapoint identifiers with their respective static methods that retrieve them.
        #
        # Returns whatever the helper method returns, which is intended to be either an extracted piece of information
        # from the raw response body or an abstracted piece of data, so long as any points of aggregation are done
        # statelessly.
        @staticmethod
        @abstractmethod
        def scrape( datapoint, text ):
            # this is expected to take in an identifier for the first argument representing a datapoint and the raw page
            # source being interpreted from which the datapoint is extracted
            pass

        ## SessionSpec.Parser.is_logged_in
        # @type text: string
        # @param text: The unprocessed page response to extract information from that identifies whether or not you have
        # an active session.
        #
        # is_logged_in is a vital session management point in the rest of your module.  This is a boolean
        # return that should be checked ad-hoc any time you perform an action that requires a session.
        #
        # The manner in which an active session is validated will vary from site to site, so this must be implemented
        # per-module but will be needed for any module that interfaces with a site that requires a login.
        #
        # Returns a boolean value.
        @staticmethod
        @abstractmethod
        def is_logged_in( text ):
            pass

        ## SessionSpec.Parser.send_message_failed
        # @type text: string
        # @param text: The unprocessed page response to extract information from that identifies whether or not your
        # attempt to send a message failed.
        #
        # Returns a boolean value.
        @staticmethod
        @abstractmethod
        def send_message_failed( text ):
            pass

