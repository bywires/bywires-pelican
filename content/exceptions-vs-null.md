Title: Exceptions vs Null
Date: 2010-08-24 19:41
Author: Admin
Category: Programming
Tags: anti-patterns, exceptions

Plenty of developers agree that returning mixed-type results is not a
good practice. It leads to conditional statements wherever the method
returning the result is used. Everbody agrees thats bad, and then Null
walks in, and we're not sure anymore.

Null is suppose to be magical value which can passed as any type of
object and represent "no object". Usually methods return Null when the
thing we want to get is absent, and that absence is considered normal
for our particular application. Maybe the caller asked for a row that
doesn't exist in a table or the next line of a file when you've already
reached the end.

If the method you are calling may return Null then you must (almost?)
always check for Null. Isn't this why we dislike mixed-type return
values? This is only the beginning of the problem with Null.

Personally, I've chosen this rule: "In OOP never return Null and instead
always use exceptions".

## Absence vs Failure

Those whom I disagree with seem to draw the line at "absence versus
failure". They interpret the absence of something as being unexceptional
and return Null. The failure to be able to do something within a method
call is seen as being exceptional so they throw an exception (or maybe
they return some other magic value because they think they're
mother-fuckin' David Blane, and by that I mean talentless and
insignificant).

This excitingly-named article - [When To Use Exceptions][] - asks one
question that seems rather compelling and butts heads with the "absence
versus failure" rule:

> "Who exactly are [library programmers] to decide that not finding
> [something] is a non-exceptional event for my application?"

I like everything about that statement including the touch of anger.
Business layer classes, or libraries, shouldn't be making application
layer decisions. Its like a business layer class triggering a fatal
error rather than throwing an exception. I determine whats a fatal
error, not the tools I'm using to build with. I always separate my
application layer from my business layer, but until recently never
considered determining exceptional conditions as part of that division.

Suppose we had a web app for managing blog entries. The app chooses a
search-engine-friendly /english-words-dashed-together/ URL for the blog
post based on the blog post title you entered. This gives us two obvious
times were we want to lookup URLs:

-   We want to use the URL in a new blog post but need to make sure its
    not already in use (absence is not exceptional)
-   A blog post URL has been requested and we need to find the blog post
    and serve it (absence is exceptional)

Both of these scenarios could call upon the same method -
\$blogPostGateway-\>getPostByUrl(\$url). The exceptionality of this
scenario depends on the context within the application, yet, as a
business class, this gateway knows (or should know) nothing about the
application which it lives in.

This does not mean that a method call lacks any context. There are still
post-conditions for the method even absent an application context. A
method call's post-condition is that it returns a value of a
pre-specified type. If an object of the proper type cannot be returned
because of absent data then we have an exceptional case. We don't need a
new tool, Null, to sit in place of that object because we already have a
tool to say "I failed!" - an exception.

## Null = repetition

Suppose \$blogPostGateway-\>getPostByUrl(\$url) does return Null. Now
the caller is left to interpret these magic values. Should callers be
left to duplicate those conditionals everywhere? That's not good design.

Preferably the "absence scenario" here would be handled on the blog post
gateway in a method like \$blogPostGateway-\>blogPostExists(\$url) which
returns a boolean. No Null. No new exceptions necessary. This decision
not to use Null also forces the developer to make the right choice and
write these extra methods which check for existence.

## Whats the difference, really?

This issue is seen by some as a matter of style. Exceptions with
try/catch blocks seen as being identical to Nulls with if/else blocks.
Is there a difference? I think so the previously mentioned points are
huge, but there are functional differences as well.

Exceptions can be handled immediately, eventually, or allowed to go
uncaught and [fail fast][]. Null values may not cause problem until much
later in a program's execution. That means cryptic error messages and
more tracing to get back to where the Null originated.

## Is there anyone else who knows a lot about Null that doesn't like Null?

It seems the [guy who invented it][] calls it his ["Billion Dollar
Mistake"][].

## Summary

Don't use Null. Don't. Do not.

[When To Use Exceptions]: http://barelyenough.org/blog/2007/11/when-to-use-exceptions/
  [fail fast]: http://www.martinfowler.com/ieeeSoftware/failFast.pdf
  [guy who invented it]: http://qconlondon.com/london-2009/presentation/Null+References%3A+The+Billion+Dollar+Mistake
  ["Billion Dollar Mistake"]: http://www.infoq.com/presentations/Null-References-The-Billion-Dollar-Mistake-Tony-Hoare
