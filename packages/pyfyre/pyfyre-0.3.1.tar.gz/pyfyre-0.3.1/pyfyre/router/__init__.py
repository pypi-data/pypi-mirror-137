from pyfyre.globals import Globals
from pyfyre.globals.events import Events
from pyfyre.pyfyre import runApp

from browser import document, window, bind

class Router:
    """Router v0.2-alpha.
    
    Creates a wrapper object with window location
    history listener that when it's changed,
    the whole app rerenders and get the provided
    routes and map it correctly.

    Attributes
    ----------
    routes : dict
        A dictionary of object routes. Every value
        must inherit the [UsesState] object.

        For instance:
            Router(
                routes={
                    "/": Home(),
                    "/about": About()
                }
            )
    """

    def __init__(self, routes):
        self.routes = routes

        if not Globals.PATH_INITIALIZED:
            Globals.__LOC__ = window.location.pathname
            Globals.PATH_INITIALIZED = True

        if not "change_route" in Globals.__EVENTS__:
            Events.add("change_route")

            self.listenRoute()
        
    def dom(self):
        return self.routes[Globals.__LOC__].dom()

    def listenRoute(self):
        def changeRoute():
            runApp(Globals.__PARENT__)

        Events.addListener("change_route", changeRoute)

    @staticmethod
    def push(location):
        Globals.__LOC__ = location

        Events.broadcast("change_route")
        window.history.pushState(None, None, location)

        @bind(window, 'popstate')
        def popState(e):
            Globals.__LOC__ = window.location.pathname
            Events.broadcast("change_route")
            e.preventDefault()