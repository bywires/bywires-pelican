Title: Problems vs Solutions: Putting the cart before the horse
Date: 2013-01-04 22:00
Author: Bob McKee
Category: programming
Tags: patterns, design patterns, decorator pattern, architecture
Keywords: patterns, design patterns, decorator pattern, architecture, tension
Description: In many cases it seems programmers are able to fix problems they don't fully understand.  How do they do it and how well is working?  Is there a better way?

[Design patterns](http://en.wikipedia.org/wiki/Software_design_pattern) are common solutions to common problems.  They are a problem-solution pair.  If you were to ask your programmer friends to describe an [Observer Pattern](http://en.wikipedia.org/wiki/Observer_pattern) solution (implementation) I bet they'd nail it in a matter of seconds.  Yet, if you asked them describe the *problem* it aims to solve I bet even if they got it right the speed and quality of their answer would be less impressive.  The language would be a little fuzzy.  Maybe they'd resort to giving an example of when they used it and work backwards from there.

The *solution* is what we do in code.  We repeat it over and over.  It is deeply engrained in our memories.  Yet, a *solution* cannot exist without its *problem*.  How have we been managing to take full advantage of these solutions without a firm understanding of the problems they aim to solve?

Similarly, have you ever introduced another programmer to unit testing?  These programmers can crank out production code like a pro, yet struggle to write tests before writing the production code to be tested.  They say they don't know what to test, but tests are simply statements of the problem to be solved, so how can that be?  Once again it would seem we are solution experts despite a poor understanding of the problem we're solving.  **How do we do it?**

Answer: **We don't**.

I think programmers often get by with a pinch of luck and a gallon of denial.

* Our general understanding gets us in the ballpark.
* We spend most of our time solving the same problems in slightly different ways so repeating solutions doesn't present us with an immediate burden too large to deny.
* We see bad code as if it were the result of a single disaster rather than a series of small mistakes that we make every day.
* We believe the complexity of our code is [essential](http://en.wikipedia.org/wiki/Essential_complexity), but it is actually [accidental](http://en.wikipedia.org/wiki/Accidental_complexity).
* We judge our code in terms of *beauty* but [we have a poor understanding of how beauty should be measured](|filename|/articles/if-programming-is-an-art.md).

Eventually a problem comes along that doesn't fit neatly into our limited list of solutions and we don't notice until its too late.  We ignore all the signs that something is going wrong.  I call these signs *tension*.

## Tension

My simple definition of *tension* is "Given the existing design, how hard is it to add a new requirement?"  Releasing the tension in a design leaves you with abstractions that have the flexibility you need for the system you must build.

It may seem natural to view tension as an attribute that would be exposed long term as new requirements are added over months and years, but tension is also important in micro-iterations - the ones you might have many of in an hour - as you write code for a larger project.  Sure, you might be given a full list of requirements up front but as you code you are likely adding support for one requirement, or even one piece of one requirement, at a time.  *You* aren't getting new requirements, but *your code* is.  You can begin to sense the tension in your design using this perspective.

If you are sitting alone at your desk quietly cursing "the code is slowing me down", "the code is in my way", or "I'm sick of fighting with this code" you likely have a tense design.  You are frustrated by your code.  You react to your code like it is a teammate who isn't pulling their weight.  These are telltale signs of tension.

## Building tension

A programmer who has invested little time in understanding design patterns but has a high desire to use them is bound to produce some really stellar tension.  Lets follow just such an eager idiot named Eddy Iddy.

Eddy is working on a game where the user can choose their own character and give it a bit of personality.  The characters can introduce themselves and those introductions can be modified at runtime with alternate speech styles.  Internally we also need to get the character ID from any given character object so we can assign it points as it completes different challenges in our game.

Eddy starts with the introduction part.

```php
interface Character {
	public function introduce();
}

class Bob implements Character {
	public function introduce() {
		return "Hi, I'm Bob.";
	}
}
```

Great!  How about those alternate speech styles...

```php
class SlangDecorator implements Character {
	// ...
	public function introduce() {
		return str_replace(
			'Hi', 'Sup',
			$this->_decorated_character->introduce()
		);
	}		
}

class FeignExcitementDecorator implements Character {
	// ...
	public function introduce() {
		return strtoupper(
			$this->_decorated_character->introduce()
		);
	}		
}
```

Its flexible where we need it to be flexible.  OK Edddy, lets get the character's ID.

```php
interface Character {
	public function introduce();
	public function id();
}

class Bob implements Character {
	// ...
	public function introduce() {
		return "Hi, I'm Bob.";
	}
	
	public function id() {
		return this->_id;
	}
}

class SlangDecorator implements Character {
	// ...
	public function introduce() { /* ... */ }

	public function id() {
		return $this->_decorated_character->id();
	}
}

class FeignExcitementDecorator implements Character {
	// ...
	public function introduce() { /* ... */ }

	public function id() {
		return $this->_decorated_character->id();
	}
}
```

Not so hot.  Do you feel the *tension*?  These *decorators* don't really care about `id()`.  They only care about `introduce()`.  If Eddy needs to add more speech styles the problem gets compounded because `id()` gets repeated even more.  If the `Character` interface needs more methods added then all the *decorators* also need to have those methods added.  This is *tension*.  If I want to add something simple its harder than it needs to be with this design and this extra work provides no benefit whatsoever.  More boilerplate.  More waste.

The [Decorator Pattern](http://en.wikipedia.org/wiki/Decorator_pattern) is a solution Eddy has in his tool belt and he uses it whenever he can.  Initially it works out pretty well.  At that point I can see Eddy patting himself on the back saying "You did it, you sly fox."  Next Eddy's autopilot kicks in and he just starts tacking on requirements as if all the designing was done and all the problems were solved.  It was solutions time.  He would have caught the tension immediately if he stopped to think about how the new requirement (the new problem) would play out in the context of the existing design.

Really, this design started to go wrong even before he added `id()`.  He didn't look back at those *decorators* and say "A `Slang` is not a `Character`".  These little language cues give you a subtle hint that something has gone awry.

You can think about how to fix the design, but I won't distract you with a solution.  This article is about seeing problems before solutions.  There is no solution without a problem, so when writing code try to understand the problem first in order to pick the right solution.