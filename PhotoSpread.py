#!/usr/bin/env python3

from pofapi.POFSession import POFSession
from yattag import Doc, indent
from lxml import html
import os

class UserGalleyDataEntry():
    def __init__(self, user, photo_set):
        self.profile_url = user.profile_url
        self.uid = user.uid
        self.online = user.online

        self.photos = photo_set

def generate_html_gallery( person_suite ):
    doc, tag, text = Doc().tagtext()

    doc.asis('<!DOCTYPE html>')
    with tag('html', lang="en"):
        with tag('head'):
            doc.asis('<meta charset="utf-8">')
            doc.asis('<meta name="viewport" content="width=device-width, initial-scale=1">')
            doc.asis('<link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">')
            with tag('script', src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"):
                pass
            with tag('script', src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"):
                pass
            with tag('body'):
                with tag('div', klass="container-fluid"):
                    for person in person_suite:
                        print("Adding photos for user {0}".format(person.uid))
                        with tag('div', klass='row'):
                            for photo in person.photos:
                                with tag('div', klass="col-xs-1", style="padding-left: 5px; padding-right: 5px; padding-top: 5px; padding-bottom: 5px;"):
                                   with tag('p'):
                                       with tag('a', href=person.profile_url, target="_blank"):
                                           doc.stag('img', src=photo, height="175", width="175")
    return indent(doc.getvalue())

def save_gallery_to_file( filename, html_doc ):
    fh = open(filename, 'w')
    # Clean up...
    fh.truncate()

    fh.write( html_doc )
    fh.close()


def open_gallery( filename ):
    os.system('xdg-open "{0}"'.format(filename))

def Main():
    output_path = "lol.html"
    config_file = "config.ini"

    config = POFSession.Config( config_file )

    testSession = POFSession(config)
    testSession.login(config.username, config.password)

    galleryData = list()
    users = testSession.searchUsers(config, 100, online_only=True)
    print("Search complete.")
    for user in users:
        photos = testSession.getPhotos(user)
        galleryDataEntry = UserGalleyDataEntry(user, photos)
        galleryData.append(galleryDataEntry)

    html_doc = generate_html_gallery( galleryData )

    save_gallery_to_file( output_path, html_doc )

    open_gallery( output_path )


if __name__ == '__main__':
    Main()
