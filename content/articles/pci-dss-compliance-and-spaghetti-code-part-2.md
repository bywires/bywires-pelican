Title: PCI DSS compliance and spaghetti code, Part 2
Date: 2011-08-01 13:19
Author: Admin
Category: programming
Tags: composite pattern, gateway pattern, legacy code, patterns, pci dss

(Be sure to read [Part 1](|filename|/articles/pci-dss-compliance-and-spaghetti-code-part-1.md) first!)

The first iteration of my [Command objects][] could continue to use our
existing [payment gateway][] code, but this would not be acceptable by
the end of this project. This old payment gateway code relied heavily on
[global state][] to get configuration options and it executed database
queries. If that were allowed the database servers which our CDE web
server accessed would also be subject to audit. On top of that this code
was poorly structured and lacked much of the functionality needed to
complete the project.

Completely replacing a fairly large chunk of code is often a bad choice,
but we had a mound of reasons for making the move.

## Structuring payment gateway code

I worked on this project in parallel with one other teammate, Xiao.
While I was tearing through legacy code and building command objects
Xiao, wrote all of the new payment gateway code I'm about to describe. I
helped him with up-front architecture consulting, code review throughout
the development process, and some pieces of refactoring.

Each payment gateway we needed to support had a name-value-pair API
([such as PayPal's][]) or an XML API ([such as Authorize.net's][]). The
data used to create each request was usually a combination of several
complex objects: merchant account information, name information,
addresses, "payment profile" information, etc. These objects created a
[Composite pattern][]. We used a [Visitor pattern][] to descend into the
Composite and build our final object in the format in which it would be
send to the payment gateway.

This might seem counterintuitive because the structure we area creating
didn't match their API structure at all. For example, an API that used
name-value pairs might include an address. This address wouldn't be a
separate structure that, as a whole, is part of our name-value pairs.
The address parts (city, state, zip, etc) would be individually mixed up
with name, credit card number, expiration date, and so on, because the
name-value pair structure is completely flat.

The benefit to having a composite structure with strong typing is that
it makes it impossible to make an invalid request. Each structure, like
the address, has a set of fields you can define. Every place an address
can be added, its specified by type. Passing an object of the wrong type
causes an error instantly - do not pass GO, do not collect \$200. This
kind of defensiveness seems pretty important for a system as critical as
this one (one that receives money).

Continue to [Part 3](|filename|/articles/pci-dss-compliance-and-spaghetti-code-part-3.md)!

[Command objects]: http://en.wikipedia.org/wiki/Command_pattern
[payment gateway]: http://en.wikipedia.org/wiki/Payment_gateway
[global state]: http://misko.hevery.com/code-reviewers-guide/flaw-brittle-global-state-singletons/
[such as PayPal's]: https://cms.paypal.com/us/cgi-bin/?cmd=_render-content&content_ID=developer/e_howto_api_NVPAPIBasics
[such as Authorize.net's]: http://www.authorize.net/support/ARB_guide.pdf
[Composite pattern]: http://en.wikipedia.org/wiki/Composite_pattern
[Visitor pattern]: http://en.wikipedia.org/wiki/Visitor_pattern
