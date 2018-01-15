# -*- coding: utf-8 -*-

import os
from loader import Configuration


with Configuration('config.json') as config:

    # We setup the cache for Chameleon templates
    os.environ["CHAMELEON_CACHE"] = config['cache']['templates']

    # We ask for the PO files to be compiled,
    # as we don't want to do it by hand
    os.environ["cromlech_compile_mo_files"] = "True"

    # We initialize our Crom registry
    # Here, we would have to "grok" our packages.
    # We can do it with a zcml file or manually.
    # We init it here, just to have the view lookup working.
    from crom import monkey, implicit
    monkey.incompat()  # incompat means it changes the behavior of the iface
    implicit.initialize()  # we create a new registry and make it the default
    
    # we define our publisher
    from cromlech.dawnlight import DawnlightPublisher
    from cromlech.browser.interfaces import IView
    from cromlech.dawnlight import ViewLookup, view_locator
    from cromlech.webob.request import Request
    
    def query_view(request, context, name=""):
        return IView.component(context, request, name=name)

    view_lookup = ViewLookup(view_locator(query_view))
    Publisher = DawnlightPublisher(view_lookup=view_lookup)
    
    # We read the zodb conf and initialize it
    from cromlech.zodb import init_db_from_file
    with open(config['zodb']['config'], 'r') as fd:
        db = init_db_from_file(fd)


    # We create our ZODB connection manager
    import transaction
    from cromlech.zodb.controlled import Connection

    class ZODBApplication(object):

        def __init__(self, db):
            self.db = db

        async def handle(self, request):
            async with Connection(self.db, transaction.manager) as conn:
                with transaction.manager as tm:
                    root = conn.get_connection('demo1').root()
                    response = Publisher.publish(
                        request, root, handle_errors=True)
                    return ''

    # Let serve our async app
    from aiohttp import web
    handle = ZODBApplication(db).handle
    app = web.Application()
    app.router.add_get('/', handle)
    web.run_app(app)
