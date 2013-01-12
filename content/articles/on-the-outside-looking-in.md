Title: On the outside looking in
Date: 2013-01-12 12:00
Author: Bob McKee
Category: programming
Tags: outside-in, inside-out, acceptance tests, bdd, abstraction
Keywords: outside-in software development, inside-out software development, outside-in, inside-out, acceptance tests, bdd, abstraction
Description: Programmers tend to look at software design from the inside out, but that approach has many pitfalls.  Looking at software development from the outside in provides us with some real advantages including ease of integration and ease of concurrent development.

> Abstraction captures only those details about an object that are relevant to the current perspective.
> 
> <cite>[http://en.wikipedia.org/wiki/Abstraction_(computer_science)](http://en.wikipedia.org/wiki/Abstraction_\(computer_science\))</cite>

Imagine we are writing code which will have the concept of a car in it somehow.  Our `Car` abstraction isn't a real car, of course.  Our `Car` abstraction might not need tires.  Our `Car` abstraction might not even need to exist - maybe any `Automobile` will do.  If we treat them all the same theres no need to make the distinction.  In fact, maybe we just want to have a car image that is one of many possible images that a user can select from, so the concept of *car* or even *automobile* really isn't something we ever need to actually use in our code.

Now imagine designing this system without knowing the "current perspective" or, as I'll refer to it, the *context*.  Which abstraction is the best one?  It seems impossible to know, but, in my experience, this is how many programmers design their code.

## Feel the pain

We must be aware of the context in which an abstraction exists before we design it.  We won't know how to capture the [essential complexity](http://en.wikipedia.org/wiki/Essential_complexity) without adding [accidental complexity](http://en.wikipedia.org/wiki/Accidental_complexity) until we understand the context.

Consider a couple of all-too-familiar experiences...

* You try to integrate backend abstractions into a frontend UI, which was specified by a product manager at the beginning of the project, but things aren't going well.  Features are missing, or there are extra features you don't need, or your abstraction's interface is really hard to work with in this particular context.
* You tried to replace some messy code with something new and clean.  You haven't really studied the messy code in depth, so you don't really know all of what it does... its just messy.  You take the concept that the messy code represents (like *car* for example) and you just build the *best* one of those, as if that were possible to determine without context.   Its time to integrate your code and things are going badly.  The interface is hard to work with.  Its methods don't answer the queries your client code has. You create mess at your integration points just so your new abstraction is usable.

There are many more scenarios like these, but the result is always the same: Your abstractions come face-to-face with your requirements for the first time and they don't get along.  Your abstractions aren't useful in the context in which they are used.  This mistake costs both time and money.

## Inside-out, meet Outside-in

The previous examples use what is called *Inside-out software development*.  You are starting in the middle of the code and working your way out to the edges of the code, where the integration happens.  The alternative here is *Outside-in software development*.

If you google this phrase you get a lot of random results about [BDD](http://en.wikipedia.org/wiki/Behavior-driven_development) and [Cucumber](http://en.wikipedia.org/wiki/Cucumber_\(software\)) or some Agile practices.  I'm not here to sell you those things.  *Outside-in* is a useful concept even without those tools and practices attached.

The *Outside-in* approach is very basic.  Start at your integration points and work inward from it so you can understand the context in which your abstractions will exist.  You don't necessarily need to write your code in order from outermost to innermost, you just need to start by acknowledging the outermost.  You can do this with or without [acceptance tests](http://en.wikipedia.org/wiki/Acceptance_testing).  The outcome should be obvious - your code integrates cleanly because you had the integration in mind from the very start.

This approach is very beneficial if you're working with other developers who will be creating code that will use your new abstraction even before you've finished implementing it.  Since you started with the outermost part of your abstraction you should have at least an interface that other developers can begin to use as a [stub](http://en.wikipedia.org/wiki/Method_stub). 

Abstractions are soft amorphous things.  Contexts are made of requirements.  They are hard and immovable.  Allowing your context to form your abstraction early on removes the pain of integration and allows your team to easily work around your "piece of the puzzle" while you're building it.  This translates into saved time and opens the door for concurrent work, all of which enhances your ability to deliver your project on time.

I'd recommend reading [Growing Object-Oriented Software, Guided by Tests](http://amzn.com/B002TIOYVW) if you're looking to find a good set of practices using *Outside-in software development*.