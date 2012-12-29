Title: Categorizing exceptions: Subtypes vs Error codes
Date: 2010-08-25 03:10
Author: Admin
Category: programming
Tags: anti-patterns, exceptions

Today's problematic pattern: Catching a single, usually per-package,
exception and then using an associated error code in a conditional
statement to determine what else to do. I've seen several colleague
programmers do it and they never seemed to think about doing it any
other way. Its an oddly unconscious decision.

Consider the following code:

<div class="code php" markdown="1">
    <?try {
        $http->get('/~bob');
        // do something} catch (Http_Exception $e) {
        if($e->getCode() == 404) {
            // do something else
        }
    }
</div>

When you use things like well-established HTTP status codes this almost
seems reasonable. It gets a little weirder when you're talking about
some internal code defined in some package no one knows anything about.
Take this bank account withdrawal example:

<div class="code php" markdown="1">
    <?try {
        $customerBankAccount->withdraw(100);} catch (CustomerBankAccount_Exception $e) {
        if($e->getCode() == 123) {
            // 123 means they overcharged their account, SHIT!
        }
    }
</div>

My problem with this is that we're using two tools for a single purpose.
What is the purpose of an Exception subtype, Http\_Exception or
CustomerBankAccount\_Exception, in these examples? Exception type
categorization. What is the purpose of an exception code in these
examples? Exception type categorization. Why are we categorizing the
same exception using two different systems? Additionally, why would
caller code be left to interpret magic numbers like 404 or some other
constant value a programmer in your office came up with?

It can get worse. People create their own custom exception error codes
with pre-specified ranges like code 100 to 200 are set aside for account
balance errors and 200 to 300 are for "the bank spent all your money"
-related errors. Once again, can't exception subtypes be used for this?
The ranges are essentially more API for a developer to remember.

Better example time - GO!

This is more descriptive...

<div class="code php" markdown="1">
    <?} catch (Http_Exception_NotFound $e) {
</div>

Sure, we all know what a 404 is anyway, but what about a 402 or a 203 or
a 912 (Glenn Beck Logic Not Found)? If you're writing this code you're
gonna need to figure out what you want to catch. The next guy reading
through it probably doesn't want to figure it out and he'd appreciate it
if was just looking at some plain English exception class names.

If you want to catch all those 4xx-class exceptions why not...

<div class="code php" markdown="1">
    <?} catch (Http_Exception_ClientError $e) {
</div>

(The official category of 4xx errors is "Client Error")

I bet a lot of developers see this kind of problem and say "OH SHIT OH
SHIT OH SHIT!!! I need to write a one line class with no body at all for
like 20 exceptions, that's like 20 lines... OH SHIT OH SHIT OH SHIT!!!"
I never quite get that. They would rather spend the time writing
catch-blocks with if-blocks inside them that each duplicate some
evaluation on a magic error code. It won't take very long for that
try/catch/if/else boilerplate nonsense to make those 20 lines of
exception definition code look mighty appealing.

## Look what I found!

During my research for this post I stumbled upon discussions in many
programming language communities about this idea that error codes can be
used for exception message translations. "That sounds interesting," I
thought. I've never considered that use before but as I read through a
plan proposed to the [Zend Framework][] I quickly began to dismiss the
notion.

[Thoroughly enjoy this proposal.][]

> Currently, exceptions can only be handled on a per-class basis, or
> possibly by string comparison against the message.
>
> Instead, we propose that exception codes be used throughout the
> framework, using a 4-byte hexadecimal format.
>
> This has at least four obvious benefits.
>
> First, it's now possible to distinguish exceptions based on the type
> of error instead of only by class. This allows users to handle them
> intelligently.
>
> Second, codes let us do some interesting things with exception
> handling. Users would now be able to call a method such as:
>
>     if ($e->stringTooShort()) {
          ... } if ($e->stringTooShort()) { ... }
>
> thereby making exception special-casing easy.
>
> Third, this gives us the ability to translate error messages using
> Zend\_Translate (loaded only when an exception occurs) and using
> separate translation files (for example, .mo format). Not all
> developers speak English; those that do generally prefer to see
> exception messages in their native language.
> 
> <cite>[http://framework.zend.com/wiki/pages/viewpage.action?pageId=22134][Thoroughly
> enjoy this proposal.]</cite>

Who cares about point 4, I'm already gagging. Even the language irks me
a bit. Just being able to do something doesn't make it "beneficial". A
magical genie could come and grant me my one wish; the ability to shit
dead baby seagulls. Its certainly something I couldn't do before, but is
it beneficial? Maybe. I really hate baby seagulls.

I don't think I have to re-explain my feelings on Point 1 and 2, but
whats the deal with lucky number 3? Oh, number 3. If you checked out the
article you probably saw that each package in the whole framework has
its own error code range preallocated. Its like preemptive namespacing
for codes. No, it IS namespacing for codes. Yes, there's already a way
to namespace exceptions; the same way we namespace any other class.

If the goal is to be able to translate any exception then we can't
really do that with this approach. Other packages using the same
error-code-to-string mapping scheme could overlap in code ranges, so
we're at least going to have to catch each different base exception type
for each package that has its own defined error code ranges. Then we're
going to have to somehow map those to different translation files.

I'm not saying its necessarily easier to just map class names to
exceptions, but I can't imagine it being harder. This new approach
doesn't seem to be solving any problems and its creating a few new ones.

The proposal has tons of user comments. Some people pushed back. One
user asked why PHP's Exception class took an error code in its
constructor at all (a very good question). One of the proposal's authors
answered:

> The error code parameter is intended to be used exactly how we're
> using it: differentiating exceptions within exception "namespaces"
> (classes).

Sigh.

Finally, translations are for presentation. Are these presentation layer
exceptions? No sir, sadly they are not. We're prepping our business
layer exceptions with some data that is meaningless everywhere except
the presentation layer assuming the presentation layer knows how to
interpret the codes in the first place.

I don't know how to end this. I'd like to be shown something that throws
my conclusions on its head, but from my reading thus far, I'm not seeing
it. Feedback welcome.

[Zend Framework]: http://framework.zend.com/
  [Thoroughly enjoy this proposal.]: http://framework.zend.com/wiki/pages/viewpage.action?pageId=22134
