$ cd ~/projects/hispug/poe/web/app
$ ~/Downloads/Python-3.9.5/Tools/i18n/pygettext.py -a -v -d messages -o i18n/messages.po views/\*.html
$ cp messages.po i18n/fr/LC_MESSAGES/messages.po 

cd i18n/fr/LC_MESSAGES
## make the necessary language translations
~/Downloads/Python-3.9.5/Tools/i18n/msgfmt.py -o messages.mo messages.po

