# Pofapi
## A fully functional python API library for POF.com

This was created after I came across a thread from the POF.com owners saying they won't be
creating a server-side API, which hinders 3rd party software development.

Hope it helps some developer somewhere get something neat built.

It's pretty easy to use.  Just create a new POFSession object and its methods drive everything.

Most features require you to log in with the object, but it will tell you what you need to do if you miss 
something, and safely manages its own state for any features that are stateful.

## Installation

```
git clone https://github.com/cmpunches/Pofapi.git
```

## Usage

```
from pofapi import POFSession
```

And you're there.

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## History

Run the following after cloning the repo command in the Installation section:
```
git log
```


## TODOs
* Add Proxy Support
* Create a requirements.txt for more automatic installation

## License and Authorship

By Chris Punches and owned by same, starting in 2016.  
Released under Apache license with all rights reserved.  See the license file for more details.

