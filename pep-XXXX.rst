PEP: XXXX
Title: Explicit Unicode Literal for Python 3.3
Version: XXXX
Author: Armin Ronacher <armin.ronacher@active-4.com>
Status: Draft
Type: Standards Track
Content-Type: text/x-rst
Created: 15-Feb-2012


Abstract
========

This document proposes the reintegration of an explicit unicode literal
from Python 2.x to the Python 3.x language specification to enable
side-by-side support of libraries for both Python 2 and Python 3 without
the need for an explicit 2to3 run.


Rationale and Goals
===================

Python 3 is a major new revision of the language, and it was decided very
early on that breaking backwards compatibility is part of the design, and
the intended move forward is a separate translation tool that converts
the sourcecode to Python 3 syntax.  With more and more libraries
supporting Python 3, however, it has become clear that 2to3 as a tool is
insufficient and people are now attempting to find ways to make the same
source work in both Python 2.x and Python 3.x with varying levels of
success.

Python 2.6 and Python 2.7 start supporting syntax features from Python 3
which for the most part makes a unified code base possible.  Many thought
that the ``unicode_literals`` future import might make a common source
possible but it turns out that it's doing more harm than good.

With the design of the updated WSGI specification a few new terms for
strings were loosely defined: unicode strings, byte strings and native
strings.  In Python 3 the native string type is unicode, in Python 2 the
native string type is a bytestring.  These native string types are used in
a couple of places.  The native string type can be interned and is
preferably used for identifier names, filenames, sourcecode and a few
other low level interpreter things such as the return value of a
``__repr__`` or exception messages.

In Python 2.7 these string types can be defined explicitly.  Without any
future imports ``b'foo'`` means bytestring, ``u'foo'`` declares a unicode
string and ``'foo'`` a native string which in Python 2.x means bytes.
With the ``unicode_literals`` import the native string type is no longer
available and has to be incorrectly labeled as bytestring.  If such a
codebase is then used in Python 3 the interpreter will start using
byte objects in places where they are no longer accepted (such as
identifiers).  This can be solved by a module that detects 2.x and 3.x and
provides wrapper functions that transcode literals at runtime.  This
unfortunately has the side effect of slowing down the runtime performance
of Python and makes for less beautiful code.  Considering that Python 2
and Python 3 support for most libraries will have to be supported for a
few years to come this means that such modules lose one of Python's nice
properties which is that the code is easy to read and understand.

Proposed Solution
=================

The idea is to support (with Python 3.3) an explicit ``u`` and ``U``
prefix for native strings in addition to the prefix-less variants.  These
would stick around for the entirety of the Python 3 lifetime but might at
one point yield deprecation warnings if deemed appropriate.  This might be 
something for pyflakes or other similar libraries to support.

Python 3.2 and earlier
======================

An argument against this proposal was made on the Python-Dev mailinglist,
mentioning that Ubuntu LTS will ship Python 3.2 and 2.7 only for 5 years.
The counterargument that could be brought up here is that Python 2.7 is
currently the Python version of choice for users that want LTS support.
Python 3 as it stands right now is a bad choice for long term investments
since the ecosystem is not yet properly developed and libraries are still
fighting with their API decisions for Python 3.

A valid point is that this would encourage People to become dependent on
Python 3.3 for their ports.  Fortunately that is not a big problem since
that could be fixed at installation time similar to how many projects are
currently invoking 2to3 as part of their installation process.

For Python 3.1 and Python 3.2 (even 3.0 if necessary) a simple
on-installation hook could be provided that tokenizes all source files and
strips away the otherwise unnecessary ``u`` prefix at installation time.

Who Benefits?
=============

There are a couple of places where decisions have to be made for or
against unicode support almost arbitrarily.  This is mostly the case for
protocols that do not support unicode all the way down or hide it behind
transport encodings that might or might not be unicode themselves.  HTTP,
Email and WSGI are good examples of that.  For certain ambiguous cases
it would be possible to apply the same logic for unicode that Python 3
applies to the Python 2 versions of the library as well but, if those
details were exposed to the user of the API, it would mean breaking
compatibility for existing users of the Python 2 API which is a no-go for
many situations.  The automatic upgrading of binary strings to unicode
strings that would be enabled by this proposal would make it much easier
to port such libraries over.

Not only the libraries but also the users of these APIs would benefit from
that.  For instance, the urllib module in Python 2 is using byte strings,
and the one in Python 3 is using unicode strings.  By leveraging a
native string, users can avoid having to adjust for that.

Modernizing Code
================

The 2to3 tool can be easily adjusted to generate code that runs both on
Python 2 and Python 3.  An experimental extension to 2to3 that just
modernizes Python code to the extent that it runs on Python 2.7 or later
with support for the ``six`` library is available as python-modernize [1]_.
For most cases the runtime impact of ``six`` can be neglected (like a
function that calls ``iteritems()`` on a passed dictionary under 2.x or
``items()`` under 3.x), but to make strings cheap for both 2.x and 3.x it is
nearly impossible.  The way it currently works is by abusing the
``unicode-escape`` codec on Python 2.x native strings.  This is especially
ugly if such a string literal is used in a tight loop.

This proposal would fix this.  The modernize module could easily be
adjusted to just not translate unicode strings at all and the runtime
overhead would disappear.

References
==========

.. [1] Python-Modernize
   (http://github.com/mitsuhiko/python-modernize)


Copyright
=========

This document has been placed in the public domain.



..
   Local Variables:
   mode: indented-text
   indent-tabs-mode: nil
   sentence-end-double-space: t
   fill-column: 70
   End:
