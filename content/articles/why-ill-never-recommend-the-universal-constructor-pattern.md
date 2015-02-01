Title: Why I'll never recommend the "Universal constructor" pattern
Date: 2010-07-20 12:44
Author: Bob McKee
Category: programming
Tags: anti-patterns, patterns
Keywords: anti-patterns, patterns

I read the [PlanetPHP][] feed every day and honestly it usually leaves
me scratching my head a bit. Recently I saw a post referencing the
["universal constructor" pattern][] in the PHP framework, [Solar][]. I
hadn't heard this pattern name before but I've seen the code a million
times looking through other people's code (and maybe even my own 3+
years ago). The people who use it generally think its the best thing
ever. It solves that way-too-many parameters problem. In my experience,
however, it almost always indicates poor design elsewhere.

The pattern is simple. Constructors take only one parameter ever. That
one parameter contains a hash of option/setting pairs (configuration).
Here's an example of where you might see something like this...

```php
$userImporter = new UserImporter(array(
    'enable_deduping' => true,
    'email_admin_on_failure' => true,
    'import_batch_size' => 1000));
```

Code that uses this pattern is notorious for breaking the [Single
Responsibility Principle][]. Breaking this principle leads to tightly
coupled, hard-to-test code. Its fairly obvious problem to catch when you
think about it. If someone showed you a class with a constructor that
had maybe a few required parameters then 10 optional ones you'd probably
run for the hills.

My example class apparently reads some sort of importable data
structure, knows how to interact with the data's destination, dedupes
users, breaks work into batches, sends alert emails, and probably nailed
Jesus to the cross.

This approach appears to solve one problem: it gets rid of that long
optional parameter list which leads to code like so...

```php
class UserImport {
    public function __construct($enableDeduping = true, $enableEmailOnFailure = false, $batchSize = 1000) {
        // ...
    }
}

$userImport = new UserImport(
                  true,  // default
                  false, // default
                  2000   // custom setting!);
```

You're repeating defaults all over the place to get to that last
optional value. You can never remember which parameter it is without
looking. Is batch size the 5th or 7th param??? Guess I'll go read the
code AGAIN.

We can fix this with a better API. Unfortunately the the UserImport
example I am giving fails at this point. These parameters shouldn't live
together because there are too many responsibilities that correspond to.
Here a slightly modified example that might be a scenario where you'd
actually use setters for your optional parameters.

```php
class UserImport {
    public function __construct(Framework_DatabaseConnection $databaseConnection) {
        $this->_databaseConnection = $databaseConnection;
        // implements logger interface but does not write logs or actually do anything 
        // else.  this is my default logger value.
        $this->_logger = new Framework_Logger_Null();
    }

    public function setLogger(Framework_Logger $logger) {
        $this->_logger = $logger;
    }
}
```

In this case rather than having an optional logger in the constructor
with default value I just set the object's logger to the default, a
[null object][] called Framework\_Logger\_Null. If you want to supply a
real logger just use out setLogger setter method.

In summary, constructors take required parameters. Setters take optional
parameters.

Next, don't think of using types here. Can't be done. You're writing all
your validation in PHP. You could write a base class for that
functionality and waste the one chance of inheritance PHP gives you on
that. You could couple your class to some validation library you
instantiate statically (using "new") or using static method calls.
Granted you're on the hook here for scalar types anyways in PHP since it
does not offer types for integers, strings, and booleans for example.

In a project like Solar you probably always have good documentation
that's kept up-to-date, but for your home-grown PHP project that almost
never the case. These things over time always end up with new
configuration options added making them even more complex and the
documentation more out-of-date. What I am getting to is - how do you
know what options are available? Manual documentation works but decays
over time. Auto-generated documentation isn't going to help you. Users
could just read the implementation of your class to figure it out (I see
this way too much). Essentially you are hiding how to use your class.
This is true both when you are using these configuration hashes in the
constructor and also a method parameter.

The easy way to expose the functionality your classes offer is by
exposing that functionality through the public API.

Lastly, although this is on a required symptom of this pattern, I almost
never see [dependency injection][] used with this pattern. People don't
want to mix simple configuration settings with dependency management
because this pattern is suppose to be all about convenience, and how
convenient is it to instantiate all kinds of dependency objects when
you're creating this object in some client code? Not very. The general
solution Universal-constructor people use is to just instantiate
dependencies right in the same class, thereby tightly coupling it to
those implementations. There are better ways to handle dependency
management but thats another post for another day.

[PlanetPHP]: http://www.planet-php.net/
["universal constructor" pattern]: http://solarphp.com/manual/appendix-standards.constructor
[Solar]: http://solarphp.com/
[Single Responsibility Principle]: http://en.wikipedia.org/wiki/Single_responsibility_principle
[null object]: http://en.wikipedia.org/wiki/Null_Object_pattern
[dependency injection]: http://en.wikipedia.org/wiki/Dependency_injection
