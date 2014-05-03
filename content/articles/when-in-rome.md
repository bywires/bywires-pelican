Title: When in Rome
Date: 2014-05-03 09:00
Author: Bob McKee
Category: programming
Tags: coding conventions, coding standards
Keywords: coding conventions, coding standards

There is something about programming conventions that gets everyone riled up.  Everyone has an opinion and no one agrees.  Today, I got a little riled up.  I'd like to lay on your couch and tell you about it while you sit attentively taking notes with a quizzical expression on your face.  You'll ask me about my recurring dreams and my relationship with my father.

Um, right.  My employer's product has a Python component that I've been working on more and more recently.  In it, I wrote some code like this:

```python
'I like to eat %s' % food
```

I was told that this is the wrong way and the better way is...

```python
'I like to eat {}'.format(food)
```

Why is the second way better than the first?  I was told that the reason is *readability* and also that it was part of the company's Python coding standard.  Hmmm.  I care a lot about readability, but... really?  If I had multiple replacement arguments I'd switch to *format()* and provide some nicely named tokens, though you could still do it using the *%* operator.

```python
'I like to eat {food} for {meal}'.format(food='bacon', meal='all meals')
'I like to eat %(food)s for %(meal)s'. % {'food': 'bacon', 'meal': 'all meals'}
```

It turns out that *format()* is Python's recommendation ([str.format... is the new standard in Python 3, and should be preferred to the % formatting](https://docs.python.org/2/library/stdtypes.html#str.format)) and thats good enough for me.  My coworker was right, but for the wrong reason.  Readability isn't a good reason here and neither is the company standard.

## The value of decisions

In an earlier article I wrote that [programming isn't an art](/articles/programming/if-programming-is-an-art/), and the value of our decisions is not subjective.  So, what is the value of this decision?  Keep in mind this is proprietary software, its forever-bound to Python 2 unless some epic refactoring is performed, and, lets be honest, any python developer could read either version very quickly.

There is another important distinction: This is implementation not interface, meaning it will never be reused (unlike an interface), so even if it had a defect its effect would not be multiplied.

Hopefully, I've convinced you that in this context the value of this decision is about $0.  It doesn't add technical debt and it also doesn't save us money later.  Its a wash.

Another coworker, having witnessed my little scuff, kindly commiserated with me.  He had gotten a slap on the wrists for not following the company's PHP class naming standard.  We use camelcase and when the class name contains acronyms we only capitalize their first letter (ex. Http, not HTTP).

It was a Friday around 4pm and our project was ready on schedule (high five!), so I had time and maybe I was in a disagreeable mood, but I had to argue again.  His decision could be a cause for error for many future developers.

In PHP, how many times have you forgotten which order $needle and $haystack are in in the array functions (its inconsistent)?  In Python, do you find that after writing some tests are you creating method names like getById instead of get_by_id (because *unittest.TestCase* methods use camelcase, unlike most other python functions)?

Conventions allow us to create mental shortcuts.  One can assume things about a well designed piece of code without even looking at it.  When you correctly assume things you save time, and saving time is saving money.

The language of design patterns has a similar time-saving effect.  If I see *window.decorator.Scrollbar* or *storage.adapter.Redis* being used, I already know something about the class, maybe even a lot about it if I've used other *window.decorator*'s or *storage.adapter*'s.  I know the problem the code needed to solve and how it was solved.  I can make a lot of assumptions and save a lot of time.

Using HTTP versus Http in a class name in this context isn't an expensive defect.  Its cost is not $0, but I'd say it's pretty low.  It is multiplied though.  This class name will be referenced in multiple places by multiple developers and each will have a chance to fall victim to this inconsistency.  There is an advantage to following the established convention and no disadvantage, so... when in Rome...

## Fiddle while Rome burns

There's one more aspect of this experience that burns a little more than the others.  Coding standards can provide some value, but they don't imply code quality one bit.  Spend a few minutes on github and I'm sure you can find a plethora of [PEP8](http://legacy.python.org/dev/peps/pep-0008/)-compliant garbage.

Its easy for these low-value matters of style to dominate code reviews, which really is a shame.  What about the high-value decisions?  If [all code is bad](http://stilldrinking.org/programming-sucks), how could this possibly be part of the solution?  If you care about a standard like PEP8, set up a PEP8 validator in your build process and be done with it.  Knowing the ins and outs of these standard shouldn't make anyone feel useful.  Knowing how to take a software design and evaluate it based on the business needs you've identified... thats value.