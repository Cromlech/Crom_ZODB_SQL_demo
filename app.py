# -*- coding: utf-8 -*-

import os
from loader import Configuration


def populate_db(db):
    """We create what we want here. We get the DB connection object.
    We need to open and to close it. It doesn't need to return anything.
    Make sure to use a transaction manager to have it correctly persisted.
    """
    pass


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

    # We read the zodb conf and initialize it
    from cromlech.zodb import init_db
    with open(config['zodb']['config'], 'r') as fd:
        db = init_db(fd.read())
    populate_db(db)

    # Creating the applications and routing them
    from rutter import urlmap
    from cromdemo.wsgi import demo1, demo2

    router = urlmap.URLMap()
    router['/demo1'] = demo1
    router['/demo2'] = demo2

    # Wrapping the router in the ZODB middleware
    # It will create the ZODB connection object in the environ
    # at the given key
    from cromlech.zodb.middleware import ZODBApp
    application = ZODBApp(router, db, key="zodb.connection")
