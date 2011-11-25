# -*- coding: utf-8 -*-

#    This file is part of emesene.
#
#    emesene is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    emesene is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with emesene; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import time
import calendar
import xml.sax.saxutils

import e3

class MessageFormatter(object):
    '''a class that holds the state of a conversation and
    format the messages according to the state and the
    format provided

    tag list:

    %ALIAS%: the alias of the account
    %DISPLAYNAME%: the alias if exist otherwise the nick if exist
        otherwise the account
    %TIME%: the time of the message
    %SHORTTIME%: the time of the message in format HH:MM:SS
    %MESSAGE%: the message with format
    %RAWMESSAGE%: the message without format
    %STATUS%: the status of the account
    %NL%: new line

    some basic formating is allowed as html tags:
    b: bold
    i: italic
    u: underline
    br: new line
    '''

    def __init__(self, new_line='<br/>'):
        '''constructor'''

        self.new_line = new_line

        # default formats
        self.incoming = '<div class="message-incomming">'\
            '<b>%DISPLAYNAME%</b>:%NL%    [%SHORTTIME%] %MESSAGE%%NL%</div>'
        self.outgoing = '<div class="message-outgoing">'\
            '<b>%DISPLAYNAME%</b>:%NL%    [%SHORTTIME%] %MESSAGE%%NL%</div>'
        self.consecutive_incoming = '<div class="consecutive-incomming">'\
            '    [%SHORTTIME%] %MESSAGE%%NL%</div>'
        self.consecutive_outgoing = '<div class="consecutive-outgoing">'\
            '    [%SHORTTIME%] %MESSAGE%%NL%</div>'
        self.offline_incoming = \
            '<i>(offline message)</i><b>%DISPLAYNAME%</b>:%NL%    [%SHORTTIME%] %MESSAGE%%NL%'
        self.information = '<i>%MESSAGE%</i>%NL%'
        self.history = '<div class="message-history">'\
            '<b>%TIME% %DISPLAYNAME%</b>: %MESSAGE%%NL%</div>'

    def format_message(self, template, message):
        '''format a message from the template, include new line
        if new_line is True'''
        template = template.replace('%NL%', self.new_line)
        template = template.replace('%MESSAGE%', escape(message))

        return template

    def format_information(self, message):
        '''format an info message from the template, include new line
        if new_line is True'''
        return self.format_message(self.information, message)

    def format(self, msg):
        '''format the message according to the template'''
        if msg.type is None:
            msg.type = e3.Message.TYPE_MESSAGE

        if not msg.timestamp is None:
            timestamp = calendar.timegm(msg.timestamp.timetuple())
        else:
            timestamp = time.time()

        if msg.type == e3.Message.TYPE_MESSAGE:
            if msg.first:
                if msg.incoming:
                    template = self.incoming
                else:
                    template = self.outgoing
            else:
                if msg.incoming:
                    template = self.consecutive_incoming
                else:
                    template = self.consecutive_outgoing

        if msg.type == e3.Message.TYPE_OLDMSG:
            template = self.history

        if msg.type == e3.Message.TYPE_FLNMSG:
            template = self.offline_incoming

        formated_time = time.strftime('%c', time.gmtime(timestamp))
        formated_short_time = time.strftime('%X', time.localtime(timestamp))

        template = template.replace('%ALIAS%',
            escape(msg.alias))
        template = template.replace('%DISPLAYNAME%',
            escape(msg.display_name))
        template = template.replace('%TIME%',
            escape(formated_time))
        template = template.replace('%SHORTTIME%',
            escape(formated_short_time))
        template = template.replace('%STATUS%',
            escape(msg.status))
        template = template.replace('%NL%', self.new_line)

        is_raw = False

        if '%MESSAGE%' in template:
            (first, last) = template.split('%MESSAGE%')
        elif '%RAWMESSAGE%' in template:
            (first, last) = template.split('%RAWMESSAGE%')
            is_raw = True
        else:
            first = template
            last = ''

        if not is_raw:
            middle = e3.common.add_style_to_message(msg.message, msg.style, False)

        msg.message = first + middle + last

        return msg.message

dic = {
    '\"'    :    '&quot;',
    '\''    :    '&apos;'
}

dic_inv = {
    '&quot;'    :'\"',
    '&apos;'    :'\''
}

def escape(string_):
    '''replace the values on dic keys with the values'''
    return xml.sax.saxutils.escape(string_, dic)

def unescape(string_):
    '''replace the values on dic_inv keys with the values'''
    return xml.sax.saxutils.unescape(string_, dic_inv)

