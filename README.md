Cromlech ZODB & SQL Demo
========================

Installation instructions are in INSTALL.md

Cromlech is a offshoot  of Grok, written by one of 
the original Grok contributors, Souheil Chelfouh.  It is in daily
production use in a big company in Germany, and in
daily development use by its author Souheil.

Why use Cromlech instead of Grok? There seeral reasons.  Cromlech is already
ported to Python 3.  It uses Zeam instead of zope.formli and z3c.form.  It has the more modern security on views model. 


For me the biggest reason is that cromlech
is already running in Python 3, while Grok has some
15-24 packages which need to be ported.  

The other reason is that we are now much smarter than when grok was written.
zope.formlib and z3c.form had way way too many adapters.  Zeam.form is much
better designed.   Grok is really tied in with the a single root ZODB, Cromlech
can optionally use one ore more ZODBs. Cromlech can also do traversal or
dispatch.  In my case I intend to do the simple thing, and just ahve a
single ZODB app using traversal.

How does Cromlech differ from Grok?   Both are based on the ZTK.
The big difference is that Cromlech uses the more modern WebOb,
while grok/zope are still using the older ?????.

The next big difference is  in the security model.  The
modern way to do security is security on views.
ZTK also does security on object access.
So Grok has to patch that leading to a lot of additional complexity.
Cromlech takes the simpler approach of directly downg security on views.

The next big difference is that Cromlech uses Zeam.form, while Grok uses
zope.formlib and Z3c.form.  The problem with the later two is that they
have a lot of extra adaptors, leading to unnecessary complexity.  Even
Jim Fulton said something like: “We used way too many adaptors.”  And of
course zeam.form can also be used with Grok or Plone.


The final big difference is that  Cromlech has a new component registry.
While it is plug compatible with the old registry, it allows for chaining of
registries.  Think a tree of registries.



So why not just use Pyramid?  The reason that I like Grok or Cromlech is
that they are rich environments.  They give you a lot of concepts to build
on.  In contrast Pyramid is quite stripped down.  Optimized for computer speed,
rather than ease of development.

And while I do not fully understand the following, it is said that Pyramid
is another bulky framework, whereas Cromlech is more a collection of
separate tools.

Martian Vs Venusian.
Grok does configuration using martian.  Cromlech
uses gentian.  What is the difference?

Martian  uses declarations.   Here is an example.

```
class AuditAccount(grok.View):
   grok.context(IAccount)
   grok.name ("audit")
   grok.require("banking.auditAccount")
```

Venutian uses decorators  Here is an example from the Pyramid documentation.
Although I believe the cromlech decorators are a bit different.


```
@view_config()
def my_view(request):
    """ My view “""
    return Response()
```

The senior developers prefer decorators.  Simpler to implement and do no 
inherit.  The junior developers prefer martian.  Easier to understand.  
Does inheritance properly.  In many cases you do not have to do anything, 
inheritance does it for you.  It looks just like regular code.  But of 
course open source is written by the senior developers, for the senior 
developers, so martian has sadly mostly passed out of use.  
For those who do prefer martian, the good news is that it is already running on
Python 3.  But there are many special grokkers in Grok, and reportedly as of 
middle 2017, not all of them work  with Martian on Python 3. 


As for Grok?  Cromlech is built on top of Zope, so mostly they should be 
compatible.  Once I figure out the Cromlech libraries, it should not be that 
hard to port a Grok application over.  My hope is that porting a Grok 
application to cromlech will only require upgrading a few grok packages to 
Python 3.  
