# Machapi
## A library engine for connecting to various social networking sites.

Machapi works by the insertion of modules into an engine designed to run them.

Once an engine module is created and inserted, Machapi is able to connect to that site and perform various functions.

# Currently supported modules:
plentyoffish.com


# Why This Exists
This was created after I came across a thread from the POF.com owners saying they won't be creating a 
server-side API, which hinders 3rd party software development.

Hope it helps some developer somewhere get something neat built.

It's pretty easy to use.  Just create a new POFSession object and its methods drive everything.

Most features require you to log in with the object, but it will tell you what you need to do if you miss 
something, and safely manages its own state for any features that are stateful.

## Installation

```
git clone https://github.com/cmpunches/Machapi.git
cd Machapi/
pip3 install -r requirements.txt
```

## Usage
After placing the ./Machapi directory in your project, import the Session object from the corresponding engine module:

```
from Machapi.Engines.POF_com import Session as POFSession

# Create a configuration object from a file.
config = POFSession.Config( config_file_path )

POFobject = POFSession( config )

# start the session by loggin in.
POFobject.login( config.username, config.password )
```

And you're ready to go.  You'll want to, of course, adapt the config.ini file to your needs and adjust paths where
necessary until this engine is a little more polished.

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request.

## History

Run the following after cloning the repo command in the Installation section:
```
git log
```

## Future of this Library

This library is being used as an example use case for all of the additional considerations that go into the
creation of a python library so that other work will be more polished and consumable, and so that other work
that I create will have a higher likelihood of inclusion into other projects.

## TODOs
* Add Proxy Support
* Package as a python wheel or add a setup.py
* Add doxygen documentation generation
* Add unit tests

## License and Authorship

By Chris Punches and owned by same, starting in 2016.  

Released under Apache license with all rights reserved.  See the license file for more details.

You may create derivative works provided that your work references the original author and project.

# Module Legal
Any modules that this engine runes is the property of its respective provider or its licensor and is protected by applicable
copyright law, and their terms of service are applicable, which you must agree to when using this library.

I make no claims of ownership of their content or services.  This is only an interaction engine for use on their respective sites.
