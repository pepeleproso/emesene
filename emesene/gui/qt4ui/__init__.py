# -*- coding: utf-8 -*-

'''
Module containing frontend initialization function, and frontend main loop
'''

import extension

GCONTEXT = None


def qt4_main(controller_cls):
    """ main method for Qt4 frontend
    """

    import os
    import sys
    import gobject
    import PyQt4.QtCore as QtCore
    from PyQt4.QtCore import Qt
    import PyQt4.QtGui as QtGui

    setup()

    os.putenv('QT_NO_GLIB', '1')
    #about_data = KdeCore.KAboutData("emesene", "",
                                   #KdeCore.ki18n("emesene"), "0.001")
    #KdeCore.KCmdLineArgs.init(sys.argv[2:], about_data)
    g_main_loop = gobject.MainLoop()
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('emesene')
    app.setAttribute(Qt.AA_DontShowIconsInMenus, False)
    idletimer = QtCore.QTimer(QtGui.QApplication.instance())
    idletimer.timeout.connect(on_idle)

    controller = controller_cls()
    controller.start()

    if os.name == 'nt':
        # windows hack: instead of processing glib events
        # in Qt's event loop, let's do the opposite because
        # g_main_loop.get_context() makes python executable
        # crashe on windows ... (follows)
        gobject.idle_add(app.processEvents)
        g_main_loop.run()
    else:
        # (follows) ... while processing Qt's events in glib's
        # main loop freezes the application on linux ^_^
        global GCONTEXT
        GCONTEXT = g_main_loop.get_context()
        idletimer.start(10)
        app.exec_()


# pylint: disable=W0612
qt4_main.NAME = "qt4_main"
qt4_main.DESCRIPTION = "This extensions uses Qt to build the GUI"
qt4_main.AUTHOR = "Gabriele Whisky Visconti"
qt4_main.WEBSITE = ""
# pylint: enable=W0612

extension.register('main', qt4_main)

def setup():
    """
    define all the components for a Qt4 environment
    """
    # pylint: disable=W0403
    import AvatarChooser
    import Conversation
    import DebugWindow
    import Dialog
    import PictureHandler
    import Preferences
    import TopLevelWindow
    import TrayIcon
    import menus
    import pages
    import widgets
    import Utils

    extension.category_register('avatar chooser',  AvatarChooser.AvatarChooser)
    extension.category_register('conversation',    Conversation.Conversation)
    extension.category_register('dialog',          Dialog.Dialog)
    extension.category_register('debug window',    DebugWindow.DebugWindow)
    extension.category_register('preferences',     Preferences.Preferences,
                                                   single_instance=True)
    extension.category_register('window frame', TopLevelWindow.TopLevelWindow)
    extension.category_register('tray icon', TrayIcon.TrayIcon)
    #FIXME:
    extension.set_default('tray icon', TrayIcon.TrayIcon)

    extension.category_register('connecting window', pages.ConnectingPage)
    extension.category_register('conversation window', pages.ConversationPage)
    extension.category_register('login window', pages.LoginPage)
    extension.category_register('main window', pages.MainPage)

    extension.category_register('contact list', widgets.ContactList)
    extension.category_register('conversation input', widgets.ChatInput)
    extension.category_register('conversation toolbar', widgets.ConversationToolbar)
    extension.category_register('avatar', widgets.Avatar)
    extension.category_register('image area selector',
                                                    widgets.ImageAreaSelector)
    extension.category_register('nick edit', widgets.NickEdit)
    extension.category_register('smiley chooser', widgets.SmileyPopupChooser)
    extension.category_register('status combo', widgets.StatusCombo)
    extension.category_register('info panel', widgets.UserInfoPanel)
    extension.category_register('user panel', widgets.UserPanel)
    extension.category_register('conversation info', widgets.ContactInfoRotate)
    #extension.category_register('filetransfer widget', widgets.FileTransfer)
    try:
        import PyQt4.QtWebKit
        extension.category_register('conversation output',
                                                  widgets.AdiumChatOutput)
        extension.register('conversation output', widgets.ChatOutput)
    except:
        extension.category_register('conversation output', widgets.ChatOutput)

    extension.category_register('main menu',    menus.MainMenu)
    extension.category_register('menu file',    menus.FileMenu)
    extension.category_register('menu actions', menus.ActionsMenu)
    extension.category_register('menu options', menus.OptionsMenu)
    extension.category_register('menu help',    menus.HelpMenu)

    extension.category_register('menu contact', menus.ContactMenu)
    extension.category_register('menu group',   menus.GroupMenu)
    extension.category_register('menu profile', menus.ProfileMenu)
    extension.category_register('menu status',  menus.StatusMenu)

    extension.category_register('tray main menu',  menus.TrayMainMenu)
    extension.category_register('tray login menu', menus.TrayLoginMenu)

    extension.category_register('picture handler',
                                PictureHandler.PictureHandler)

    extension.category_register('below menu', widgets.EmptyWidget)
    extension.category_register('below panel', widgets.EmptyWidget)
    extension.category_register('below userlist', widgets.EmptyWidget)

    extension.category_register('toolkit tags', Utils.QtTags)

def on_idle():
    '''When there's nothing to do in the Qt event loop
    process events in the gobject event queue'''
    while GCONTEXT.pending():
        GCONTEXT.iteration()

