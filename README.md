# Pofapi
## A fully functional python API library for POF.com

This was created after I came across a thread from the POF.com owners saying they won't be creating a 
server-side API, which hinders 3rd party software development.

Hope it helps some developer somewhere get something neat built.

It's pretty easy to use.  Just create a new POFSession object and its methods drive everything.

Most features require you to log in with the object, but it will tell you what you need to do if you miss 
something, and safely manages its own state for any features that are stateful.

## Installation

```
git clone https://github.com/cmpunches/Pofapi.git
cd Pofapi/
pip install -r requirements.txt
```

## Usage
After placing the ./pofapi directory in your project, import the POFSession object: 

```
from pofapi import POFSession
POFobject = POFSession()
```

And you're ready to go.

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

# POF Legal
The site POF.com is the property of its respective provider or its licensor and is protected by applicable 
copyright law as set forth below.  I make no claims of ownership of their content or services.  This is only
an interaction API for use on their site.
