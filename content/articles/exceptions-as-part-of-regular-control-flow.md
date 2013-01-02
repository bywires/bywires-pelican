Title: Exceptions as part of "regular" control flow
Date: 2010-08-31 03:38
Author: Bob McKee
Category: programming
Tags: exceptions
Keywords: exceptions

I've heard this rule a lot: "Never use exception for control flow." Its
an interesting statement to parse. We know what an exception is, but the
definition of control flow is a little fuzzy, so lets clarify things a
bit.

> In computer science, control flow (or alternatively, flow of control)
> refers to the order in which the individual statements, instructions,
> or function calls of an imperative or a declarative program are
> executed or evaluated.
>
> <cite><a href="http://en.wikipedia.org/wiki/Control\_flow">http://en.wikipedia.org/wiki/Control\_flow</a></cite>

Immediately I'm confused. Is it possible to use an exception and not
effect control flow? Nope. Exceptions *are* a means of controlling flow.
Sometimes people making this point specify that its "normal" or
"regular" control flow. "Normal" and "regular" are delightfully relative
and unhelpful. Normal? Compared to what? What they're trying to get at
is that they don't believe exceptions should be used unless there is an
application error.

This seems odd considering that business layer classes aren't
necessarily made for only one code path or even one application and
therefore lack context to determine the exceptionality of the condition.
I touch on this a bunch in my 
[Exceptions vs Null](|filename|/articles/exceptions-vs-null.md) article.

There are lots of "crazy" things you can do with exceptions and if
you're interested in seeing more check out [this article][] on
[c2.com][]. Here I will only be discussing three usages I found
particularly interesting.

## Exceptions as return values

This example comes from [c2.com][]. I think even people who have never
thought deeply about exception usage would never dream up this code.
Still, I believe this might be the perfect example of what people are
talking about when they say not to use exceptions for control flow.

<div class="code java" markdown="1">
    void search( TreeNode node, Object data ) throws ResultException {
        if (node.data.equals( data ))
            throw new ResultException( node );
        else {
            search( node.leftChild, data );
            search( node.rightChild, data );
        }
    }
</div>

Get it now? As a starting point I think we can all agree that this it
batty. Its a search algorithm that throws an exception upon *success*.
Really? The article correctly points out that this is a violation of the
[Principle of Least Astonishment][]. I know this code make me feel
violated.

## Exceptions as commands to the caller

<div class="code php" markdown="1">
    <?} catch(MyService_Exception_CouldNotBeReached $e) {
        throw new MyOtherService_Exception_Retry("Couldn't reach my service, retry!");
    }
</div>

This exception seems to be commanding the caller to retry something.
Like the previous example, this also breaks the [Principle of Least
Astonishment][]. In order to benefit from the full functionality of the
method you need to be setup to catch exception commands that it throws
and follow out some other action to continue. This is a
application-agnostic service making application-specific decisions
(whether or not to retry). No thank you.

## Exceptions as loop termination conditions

[c2.com][] offers us another gem, and I don't mean that negatively.

<div class="code java" markdown="1">
    try {
        for (int i = 0; /*wot no test?*/ ; i++)
            array[i]++;
    } catch (ArrayIndexOutOfBoundsException e) {}
</div>

The first thing when I thought when I saw this was "What about things
like Python's StopIteration?" One line later its mentioned. Yay! This
article may be reading my mind. I do wonder if the fact that
StopIteration exist in [Python][], [Ruby][], and [Javascript][] now
might start to carve away at [exception/null failure/absence debate](|filename|/articles/exceptions-vs-null.md).
I'd like to know more about the decision making that went into the the
design of feature but so far have failed to find any discussions on the
matter.

All that said, I'm not sure how I feel about the name - "stop"
iteration. Sounds like the service commanding its caller. If I were to
use a exception-terminated loop I'd prefer to explicitly specify the
exception type rather than using a language generic exception with a
name that is a command. Maybe something like this (which I would not be
surprised to find already exists somewhere):

<div class="code php" markdown="1">
    <?until(RecordNotFoundException $e) {
        print $recordSet->getNext()->getLabel() . "\n";
    }
</div>

[http://en.wikipedia.org/wiki/Control\_flow]: http://en.wikipedia.org/wiki/Control_flow
[Exceptions vs Null]: http://blog.bywires.com/2010/08/exceptions-vs-null.html
[this article]: http://c2.com/cgi/wiki?DontUseExceptionsForFlowControl
[c2.com]: http://c2.com/
[Principle of Least Astonishment]: http://c2.com/cgi/wiki?PrincipleOfLeastAstonishment
[Python]: http://docs.python.org/library/exceptions.html#exceptions.StopIteration
[Ruby]: http://books.google.com/books?id=jcUbTcr5XWwC&pg=PA138&lpg=PA138&dq=stopiteration+in+ruby&source=bl&ots=fHIjsb4sdD&sig=6TYYoWQX9zw-un9WPZMa4qk-UrA&hl=en&ei=1-N6TOefCIaKlwfT7bSzCg&sa=X&oi=book_result&ct=result&resnum=8&ved=0CDsQ6AEwBw#v=onepage&q=stopiteration%20in%20ruby&f=false
[Javascript]: https://developer.mozilla.org/en/JavaScript/Guide/Iterators_and_Generators
