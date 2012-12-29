Title: If Programming is an Art
Date: 2012-12-09 16:30
Author: Admin
Category: Programming

Some of our best and brightest programmers classify programming as an
art ([Donald Knuth][], [Guido van Rossum, and Bjarne Stroustrup][] to
name a few). Depending on who you ask, *art* is skill, craftsmanship,
fine art like painting or sculpture, or perhaps solving problems despite
walking blindly through the realm of the unknown. Donald Knuth says in
[Computer Programming as an Art][Donald Knuth]:

> Science is knowledge which we understand so well that we can teach it
> to a computer; and if we don't fully understand something, it is an
> art to deal with it.

Interesting... intriguing... but useful? When we hear this premise,
*programming is an art*, what argument is it supporting? Or is it simply
an observation devoid of practical value?

## Beautiful code?

When the *common programmer* says *programming is an art* I believe they
usually mean that they strive for *beauty* in their code. I also believe
they are talking about the result, which is the *code*, not the process,
which is the *programming*. I also define *common programmers* as
programmers who are common in their field. They won't be writing any
books and probably not speaking at any conferences but they're smart
folks, have significant experience, and they get a lot done. I would put
myself in this group.

I wrote *beautiful* code years ago. My code would have been tweaked
repeatedly such that all its components seemed to be where they belonged
by the end of my projects. In my gut it *felt* beautiful, but beautiful
really just meant putting like things together. I arrived there without
knowing why I was doing what I was doing, how it was good, and how it
was bad. I was ignorant of just about every other meaningful attribute
of my code.

My ability to compose such *beauty* created an internal illusion of my
own expertise. What I did was working, wasn't it?

## Beauty has no value in code

Try putting a monetary value on the beauty of code. How would you come
up with such a number? Could you measure it without defining beauty in
terms of things like extensibility, testability, readability, or other
objectively measurable attributes? It would seem not. If art and beauty
are simply imprecise terms for a conglomeration of these objective
attributes, does it not detract from our discourse to use them at all?

Beauty is not one thing to all people. It is subjective and as such it
is a terrible attribute for comparison. Is the Mona Lisa more beautiful
than [Jackass 3D][]? I don't know, I'm sick. Really sick.

Since beauty is subjective, anyone could claim that their code is
beautiful and they'd be right and you'd also be right even if you
disagreed. Jackass 3D *is* more beautiful than the Mona Lisa because I
said so. It levels the playing field. Differences in coding practices
become a matter of personal taste with no connection to real world
consequences like expenditure of time and money. That is the true harm
in this kind of thinking.

Maybe you write medical software so testability is extremely important.
Maybe you write embedded software that will never be changed after its
released so maybe you don't care about flexibility or extensibility.
Maybe you need to ship your product in 3 days, or maybe 3 years. Maybe
your team is junior HTML developers or maybe its programming gods who
can flip bits with their minds. Different code attributes will have
different *business value* depending on the changes (or lack there of)
that your code will go through in its lifetime and the team that will
see to those changes. This *business knowledge* should inform your
coding practices, not some misguided quest for *art*.

## Shit, I work with artists

My advice to those out there trying to make the case for less *art* and
more of a practical approach to coding would be to:

-   Analyze the code, coding practices, and tools you use. What makes it
    hard to meet your business needs? Look at specific cases, because
    context matters. No silver bullets. No one size fits all. You want
    to solve a real problem, not sell a religion.
-   Avoid arguing minor details. For example, if you think its
    beneficial to make a big change to your system but you spend all
    your time arguing whether curly braces should be on the same line or
    the next line **no one will listen to you**. Choose your battles.
    Don't gain the reputation of the *code nazi*.
-   **Read about how other people solve problems.**

[Donald Knuth]: http://www.paulgraham.com/knuth.html
[Guido van Rossum, and Bjarne Stroustrup]: http://onlamp.com/pub/a/onlamp/2005/06/30/artofprog.html
[Jackass 3D]: http://www.youtube.com/watch?v=fKwjU_pSSW4
