#!/usr/local/Cellar/python3/3.6.3/bin/python3
# coding: utf-8
#
# Copyright © 2017 LazyGroot <matthias.david.974@gmail.com>
#
# Distributed under terms of the MIT license.

# ██████             ██████   ██   ██
#░██░░░██  █████    ░██░░░██ ░░██ ██
#░██  ░██ ██░░░██   ░██  ░██  ░░███
#░██████ ░███████   ░██████    ░██
#░██░░░  ░██░░░░  ██░██░░░     ██
#░██     ░░██████░██░██       ██
#░░       ░░░░░░ ░░ ░░       ░░


from bs4 import BeautifulSoup
import requests
from prompt_toolkit import prompt
from tabulate import tabulate
# pip install lxml
from pyfiglet import Figlet
import urwid
import webbrowser
import logging


logging.basicConfig(filename='test_log.log',level=logging.DEBUG, format='%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s')

palette = [
    ('body',            '',                     '',         'standout'),
    ('header',          'light cyan,bold',      'black'),
    ('footer',          'light gray',           'black'),
    ('button normal',   'dark green',           '',         'standout'),
    ('button waiting',  '',                     '',         'standout'),
    ('button downloading','dark blue',          '',         'standout'),
    ('button checking', 'yellow',               '',         'standout'),
    ('button failed',   'dark red',             '',         'standout'),
    ('button select',   'white',                'dark green'),
    ('button disabled', 'dark gray',            'dark blue'),
    ('exit',            'white',                'dark cyan'),
    ('key',             'light cyan',           'black',    'underline'),
    ('title',           'white',                'black',),
    ('focus',           'black',                'dark cyan','standout')
    ]

class PEapp(object):
    def __init__(self):

        self.footer_text = [
              ('key', "UP"), ", ", ('key', "DOWN"), " Haut & Bas | ",
              ('key', "ENTER"), " Acceder a l'offre | ",
              ('key', "Q"), ", ",('key', "ESC"),    " Quitter",
        ]

        # IMPORTATION DES DONNES
        l = self.getPEData()

        self.listbox = urwid.AttrWrap(ScrollableListBox(l, offset=1) , 'body')
        #self.listbox = ScrollableListBox(l, offset=1)

        hdr = urwid.AttrWrap( urwid.Text("TPES - Tui Pole Emploi Search"), 'header')
        self.footer = urwid.AttrWrap(urwid.Text(self.footer_text),'footer')

        self.listframe = urwid.Frame(self.listbox, header=self.listheader, footer=self.footer)
        self.w = urwid.Frame(self.listframe, header=hdr)
        self.loop = urwid.MainLoop(self.w, palette, unhandled_input=self.keyHandler)



    def run(self):
        self.loop.run()



    def keyHandler(self, input):
        pass
    #    """We leave if user press a quit char"""
    #    if input in ('esc','q','Q'):
    #        raise urwid.ExitMainLoop()

    #    if input == 'enter':
    #        self.listframe.set_focus('footer')

    #    else:
    #        pass
            #return self.menu.checkShortcuts(input) #needed to manage shortcuts






    def getPEData(self):
        payload = {'lieux': '97411', 'offresPartenaires': 'true', 'motsCles': '', 'rayon': '10', 'tri': '0'}

        r = requests.get('https://candidat.pole-emploi.fr/offres/recherche', params=payload, timeout=5)

        html = r.text.encode("utf-8")
        soup = BeautifulSoup(html, 'lxml')


        poste = []

        l = []


        for res in soup.find_all('li', 'result'):
            p = res.h2.a.get_text()
            entreprise = res.find('p',{'class': 'subtext'}).get_text()
            description = res.find('p',{'class': 'description'}).get_text()
            type_contrat = res.find('p',{'class': 'contrat'}).get_text()
            lien = 'https://candidat.pole-emploi.fr%s' %  (res.find('a',{'class': 'btn-reset'}).attrs['href'])
            poste.append( [ p, entreprise, type_contrat, lien ] )

        self.listheader = urwid.AttrMap(
            urwid.Columns([
                ('weight', 1, urwid.Text('Poste')),
                ( urwid.Text('entreprise')),
                ( 'fixed', 15, urwid.Text('Type')),
                ( urwid.Text('Lien')),
            ], dividechars=1), 'header')

        for p, entreprise, type_contrat, lien in poste:
            # DEFINITION DES COLONNES (largeur, fixe ou pas ...)
            w = urwid.Columns( [
                ('weight', 1,urwid.Text(p)),
                (urwid.Text(entreprise)),
                ('fixed', 15, urwid.Text(type_contrat)),
                urwid.Text(lien)], dividechars=1)

            # ON REMPLI LA LISTE AVEC DECO
            logging.info(w)
            l.append( urwid.AttrWrap(w, None,'focus') )
            #l.append(w)
        
        #logging.info(l)
        return l




class ScrollableListBox(urwid.ListBox):
    """
    A `ListBox` subclass with additional methods for scrolling the
    focus up and down, to the bottom and to the top.
    """
    def __init__(self, contents, offset=1):
        """
        Arguments:
        `contents` is a list with the elements contained in the
        `ScrollableListBox`.
        `offset` is the number of position that `scroll_up` and `scroll_down`
        shift the cursor.
        """
        self.offset = offset
        
        urwid.ListBox.__init__(self, urwid.SimpleListWalker(contents))

    def focus_previous(self):
        """Sets the focus in the previous element (if any) of the listbox."""
        focus_status, pos = self.get_focus()
        if pos is None:
            return

        new_pos = pos - self.offset
        if new_pos < 0:
            new_pos = 0
        self.set_focus(new_pos)

    def focus_next(self):
        """Sets the focus in the next element (if any) of the listbox."""
        focus_status, pos = self.get_focus()
        if pos is None:
            return

        new_pos = pos + self.offset
        if new_pos >= len(self.body):
            new_pos = len(self.body) - 1
        self.set_focus(new_pos)

    def focus_first(self):
        """Sets the focus in the first element (if any) of the listbox."""
        if len(self.body):
            self.set_focus(0)

    def focus_last(self):
        """Sets the focus in the last element (if any) of the listbox."""
        last = len(self.body) - 1
        if last:
            self.set_focus(last)

    def keypress(self, size, key):
        if key == 'up':
            focus_widget, idx = self.get_focus()
            if idx > 0:
                idx = idx-1
                self.set_focus(idx)

        elif key == 'down':
            focus_widget, idx = self.get_focus()
            if idx < len(self.body)-1:  # pour eviter l'erreur de depasser le focus au dela du content  
                idx = idx+1
                self.set_focus(idx)

        elif key in ('esc','q','Q'):
            # TODO reallyAdd = urwid.AttrWrap(urwid.Overlay(urwid.LineBox('Etes vous sure de vouloir quiter ? Y/N', title='|** Confirm **|'), self.parent, 'center', 40, 'middle', None), 'PopupMessageBg')

            raise urwid.ExitMainLoop()

        elif key == 'enter':
            wb = webbrowser.get('chromium')
            wb.open('https://google.com')

    def _quit(self, widget=None):
        raise urwid.ExitMainLoop()





if '__main__'==__name__:

    try:
  
        PEapp().run()
    except KeyboardInterrupt:
        print (" exit now.")
        sys.exit(2)
