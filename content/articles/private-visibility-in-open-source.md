Title: Private visibility in open-source
Date: 2010-07-20 21:43
Author: Bob McKee
Category: programming

The statement in question: ["Private has absolutely no useful role in
open-source code."][]

There's already lots of drawn out discussion about this so I'll keep it
short.

-   Lots of private methods are bad, but not because of OSS. Its a code
    smell that usually means too many responsibilities (thereby
    violating the [Single Responsibility Principle][]). If you don't
    believe me look at the classes in your code base with the most
    private methods - ugly right?
-   Private methods are a good way to keep methods short by dividing up
    work into small well-described chunks. These well-described methods
    and can be used in place of more heavy-weight documentation in some,
    but certainly not all, cases. I haven't seen any large scale project
    with perfect documentation, so its important that the code speaks to
    you. Self-describing code won't degrade like documentation.
    (Excellent examples of this in the book [Clean Code][])
-   Code that relies on the internals of 3rd-party code is fragile. If
    the package author changes the internal implementation of a class
    that you depend on then your shit is going to break. Technically
    speaking, of course. If you want to extend code for other OSS
    projects use inheritance or a form of delegate to use the underlying
    package without having to modify it or depend on its internals.
-   Plenty of successful programming languages do no have private
    methods. It can be done. It just requires discipline and technical
    expertise.

At the end of the day its almost a silly point. Public or private, when
talking about these internal-use-only methods programmers should avoid
mucking with them. What are you trying to get at anyways? If its
something significant it should be extracted into a new class which is
in turn made a dependency of the original.

["Private has absolutely no useful role in open-source code."]: http://twitter.com/mtabini/status/18867470296
  [Single Responsibility Principle]: http://en.wikipedia.org/wiki/Single_responsibility_principle
  [Clean Code]: http://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882
