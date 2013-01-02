Title: Configurable return types kill puppies
Date: 2010-07-20 02:33
Author: Bob McKee
Category: programming
Tags: anti-patterns, patterns
Keywords: anti-patterns, patterns

Here's some code you could see using [PHP's Adodb][] library. The
library isn't the point but its demonstrates a pattern I see a fair
amount.

<div class="code php" markdown="1">
    <?$oldFetchMode = $conn->setFetchMode(ADODB_FETCH_ASSOC);
    $recordSet = $conn->execute("SELECT * FROM table");
    $objectThatDoesWork->work($recordSet);
    $conn->setFetchMode($oldFetchMode);
</div>

To me this is a multi-fail.

1.  If an exception is thrown before the fetch mode is reset it doesn't
    get reset unless you catch it. That can add up to a lot of
    boiler-plate try/catch blocks.
2.  If the next call to execute() doesn't set the fetch mode first in
    order to guarantee you get the return type you expect bad things can
    happen. I've seen plenty of code that doesn't explicitly set the
    fetch mode every time and it works... until it doesn't. Code
    somewhere else in your system changes the fetch mode. The error is
    coming from code that source control tells you hasn't changed
    recently. Your tests prove to you that the code works. Your query
    logs show you that the query you expected to be run was actually
    run. It sends you in the wrong direction every time.
3.  Setting the fetch mode every time with this long method and verbose
    constant adds a bunch of boilerplate.
4.  $objectThatDoesWork-\>work() should also have its first parameter
    be typed or you'll only know something went wrong when it tries to
    access that first row the wrong way rather than failing immediately.
    I'd prefer it to [fail fast (pdf)][].

At first glance it could look flexible and convinient. You don't need to
set the fetch mode ever in theory. You can just use the default, and
that's pretty simple right? I'd be happy to rip this method out and
pretend it never existed, but it does and its scaring the kids.

Luckily, there is actually a easy enough solution to this problem. Take
a look at this rewrite.

<div class="code php" markdown="1">
    <?$recordSetFactory = $conn->execute("SELECT * FROM table");
    $objectThatDoesWork->work($recordSetFactory->asAssoc());
</div>

$recordSetFactory has the underlying record set resource stored
privately.

$recordSetFactory object might have different ways to access the data
such as asAssoc(), which would return an iterator where the current row
is returned as an associative array. It could have another that returns
an iterator which returns row data with numeric indexes (asList()
maybe). There are plenty of ways to access this data conveniently.

Best of all that configuration is explicitly requested every time. Its
used and it gets thrown away when the object's lifecycle ends. Done and
done.

[PHP's Adodb]: http://phplens.com/lens/adodb/docs-adodb.htm
[fail fast (pdf)]: http://martinfowler.com/ieeeSoftware/failFast.pdf
