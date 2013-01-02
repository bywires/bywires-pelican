Title: PCI DSS compliance and spaghetti code, Part 1
Date: 2011-02-10 22:43
Author: Bob McKee
Category: programming
Tags: command pattern, legacy code, patterns, pci dss
Keywords: command pattern, legacy code, patterns, pci dss

Anyone taking a substantial amount of credit card payments will
eventually stumble onto the [Payment Card Industry Data Security
Standard (PCI DSS)][]. Meeting this standard likely adds significant
complexity to your application, comes at fairly great expense, and will
leave your developers and sysadmins with at least a few head-scratching
moments where as they ask themselves "Why do I have to do this? It has
nothing to do with security." The project I'm working on has been
audited, but the final paperwork is not in yet. Things look good, but
pass or fail, there's still plenty to learn from the experience already.

## Minimizing the PCI DSS burden

My employer's web application has a fundraising module which needed to
become PCI DSS compliant. There are many things we considered when
deciding how to modify our fundraising module. Here are a few of the
larger concerns:

-   Hardware which handles credit card numbers is subject to audit
    (these systems combined are called the Cardholder Data Environment,
    or CDE)
-   CDE hardware changes must be documented
-   CDE code changes are subject to audit
-   CDE code changes must go through a documented security-focused peer
    review
-   Quality testing must be documented for all CDE code changes
-   There are restrictions on who is permitted to deploy CDE code

As you can see, maintenance to a CDE has lots of extra overhead. It
didn't make sense to add that to overhead anything other than our
fundraising module so we decided to separate it from the rest of our
application code as well as serving it from its own cluster of web
servers. This solution also reduces the attack surface area of this
sensitive part of the application.

We would obvious have to make some changes that would cost us this extra
overhead but we realized we could keep that cost low by reducing the
need for change within the CDE code. To do this we tried to keep the CDE
code... well... as dumb as possible. Our application has many
customizable types of fundraising forms used in various workflows, but
we don't want the CDE code to know about that. That stuff is
complicated. It changes, grows, and has a higher bug potential than
something smaller and simpler. All that complexity should continue to
live within our original application which the CDE code can
communication with via a simple API. This sounds great, but how do we
rip our application in two?

## Plotting the course

Segmenting our application this way had huge implications for our
existing fundraising code. The fundraising code had feature after
feature piled on over 5 or 6 years. The user workflow stumbles through a
5000-line top-down PHP file of spaghetti code. Eventually other "helper"
functions and classes might output to browser, redirect, or charge a
credit card and then terminated the request with an exit() call. Eww!
This code was so complex that it was hard to get a good idea of what all
of it did. Without structure or comments it was unreadable and there was
no test coverage.

When I first approached this problem I looked at in a very linear way.
This is roughly how I saw the workflow for a basic fundraising page with
all valid data submitted and no credit card processor errors:

1.  User opens fundraising page on web server (not a CDE web server)
2.  User submits form which posts data to CDE web server
3.  CDE code pulls out credit card number and other sensitive data and
    validates it
4.  CDE passes the validation results and non-sensitive data to a
    validate function on the web server API
5.  Web server validates the rest of the posted data using some
    validation extracted from the spaghetti code
6.  Validation passes so some other extracted code decides to return a
    "sale command" to the CDE (see [Command Pattern][])
7.  CDE executes the command
8.  CDE calls web server API telling it the transaction was successful
9.  Web server uses some extracted code to determine if the user is to
    be shown a "thank you" message or redirected to a "thank you" page
    (each of which could be different depending on the workflow the user
    was executing)

All this code extraction was going to be a real pain. The validation and
form building was tightly coupled using an old Pear library called
[QuickForm][]. The various user workflows were tangled together and
extremely overcomplicated. Making a few huge tears in the middle of the
application seemed high-risk given our relatively short timeline.

## A-ha!

I soon realized this wasn't necessary. I didn't need to do all this
extraction. I didn't need to rip this thing apart with a few huge,
dangerous tears. What I needed to do was encapsulate those end points
which triggered the output of data to the user's browser, a user
redirect, or charging a user's credit card.

These encapsulated end points form Command classes which can be
serialized and returned to the CDE in an API response. These commands
are simple. Its not important *what kind* of page you are outputting,
*what kind* of page you're redirecting to, or *what kind* of fundraising
charge you're doing. The CDE code doesn't need to know. The CDE code
just know how to handle certain sensitive fields, perform a credit card
transaction, and execute these generic commands. All other decision
making is delegated to the web server API.

For our first iteration I created these command classes and took all
that structureless top-down spaghetti code and tossed it into a single
class method (we'll call this class a Controller). I extracted global
variable usage so their values could be passed in through the
Controller's constructor. I also extracted the validation of the
sensitive data and had it run outside the Controller with its results
injected into the Controller (as would eventually happen with the
validation running on the CDE web server). I used several legacy code
refactoring methods described in one of my favorite programming books,
<a hre="http://amzn.com/0131177052">Working Effectively with Legacy
Code</a>. These changes produced something I could release immediately.

Continue to [Part 2](|filename|/articles/pci-dss-compliance-and-spaghetti-code-part-2.md)!

[Payment Card Industry Data Security Standard (PCI DSS)]: http://en.wikipedia.org/wiki/Payment_Card_Industry_Data_Security_Standard
[Command Pattern]: http://en.wikipedia.org/wiki/Command_pattern
[QuickForm]: http://pear.php.net/package/HTML_QuickForm

