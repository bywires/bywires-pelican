Title: Template Method Trap
Date: 2013-06-06 19:30
Author: Bob McKee
Category: programming
Tags: template method pattern, inheritance
Keywords: template method pattern, inheritance

Inheritance is often a trap.  Its starts off like an adorable lion cub but grows up to be a man-eater.  One common use of inheritance is within the [Template Method Pattern](http://sourcemaking.com/design_patterns/template_method).  It is the Jekyll and Hyde of patterns; half pattern, half anti-pattern.

## What is Template Method?

Let me step back for a moment.  What is Template Method?  In the example below, a base class (`CurrencyConverter`) has one or more invariant methods (`convert()`) which wire together other variant methods (`sourceCurrencyCode()` and `targetCurrencyCode()`).  These variant methods are available to be implemented in subclasses (like `UsdToCadConverter`).  The variant methods may be abstract or null in the base class.  These invariant method stubs form a template for subclasses, hence the name Template Method.

```python
class CurrencyConverter():
	def sourceCurrencyCode(self):
		raise NotImplementedError()
		
	def targetCurrencyCode(self):
		raise NotImplementedError()

	def convert(self, units):
		return units * get_exchange_rate(self.sourceCurrencyCode(),
			self.targetCurrencyCode())
		
class UsdToCadConverter(CurrencyConverter):
	def sourceCurrencyCode(self):
		return 'USD'
		
	def targetCurrencyCode(self):
		return 'CAD'
```

Template Method implementations usually attempt to accomplish one or more of these goals:  

* Vary configuration values
* Vary behavior
* Trigger events using Hooks

There may be other goals but these are the ones I see most in the wild.  The example above is varying configuration values.

Behavior-modifying template methods don't just return static value; they perform an action for the invariant method.  Below you can see that the `crop()` method varies in `SimpleProfilePictureCreator` and `FaceFindingProfilePictureCreator`.

```python
class ProfilePictureCreator():
    def crop(self, image, width, height):
    	raise NotImplementedError()

	def getProfilePicture(self, image, width, height):
		self.crop(image, width, height)
		sharpen(image)
		saturate(image)
		add_sweet_mustache_even_on_ladies_dont_judge_me(image)
		
def SimpleProfilePictureCreator(ProfilePictureCreator):
	def crop(self, image, width, height):
		crop(image, 0, 0, width, height)
		
def FaceFindingProfilePictureCreator(ProfilePictureCreator):
	def crop(self, image, width, height):
		center = locate_face(image)
		crop(image, center.x - (width/2), 
			center.y - (height/2), width, height)
```

Hooks are frequently seen in MVC framework Controller classes.  The below should look familiar.  Subclasses like `MyController` can vary the behavior of `beforeRender()` which is called from `render()`.

```python
class Controller():
    def __init__(self):
        self.view = View()
        
    def beforeRender(self):
        pass
        
    def render(self, action):
        self.beforeRender()
        getattr(self, action)()
        result = self.view.render(action + ".html")
        return result

class MyController(Controller):
    def beforeRender(self):
        self.view.set('is_logged_in', Authorization().isLoggedIn())

    def doSomething(self):
        self.view.set('message', 'Hello World!')
		
```

The Template Method Pattern may indeed save time in some basic cases, but it comes at an immediate cost, and potentially more growing pains as complexity and variation increase.  Lets talk about these weaknesses and possible alternatives.

## Injecting configuration

The subclasses in a Template Method Pattern either expose those variant methods in the public interface, when they are implementation details not meant for public consumption, or hide them from the interface making them hard or impossible to test in isolation.

This can easily be taken care of by injecting the configuration.  The currency example is dead simple.  The two configuration variables are passed into the constructor.  No implementation details spill into the public interface.

```python
class CurrencyConverter():
	def __init__(self, source_currency, target_currency):
		self.source_currency = source_currency
		self.target_currency = target_currency

	def convert(self, units):
		return units * get_exchange_rate(self.source_currency,
			self.target_currency)
```

You could argue that the constructors took no parameters in the earlier currency example so you just instantiate the class and you're ready to go.  However, imagine supporting 20 currencies with this approach!  This code clearly would not grow well.

## Strategy pattern

Testing of the variant methods cannot be done without instantiating the class which, depending on what the base class does, may not be desirable and may be overcomplicated.  Ever try testing one controller method and all of a sudden you're loading an *entire* framework?

Injecting methods to modify behavior or define hooks is a bit different.  In languages like Python you can inject functions.  In stricter object-oriented languages you might make an interface for `cropper`'s and create multiple implementations of it.  This injecting of interchangeable objects or functions is the [Strategy Pattern](http://sourcemaking.com/design_patterns/strategy) in action.  In the example below `simple_profile_picture_cropper` and `face_finding_profile_picture_cropper` are both strategies.

I created a [Factory](http://sourcemaking.com/design_patterns/factory_method) to handle wiring together the pieces, but, were there more pieces, one could use a [Builder Pattern](http://sourcemaking.com/design_patterns/builder).

```python
class ProfilePictureCreator():
	def __init__(self, cropper):
		self.cropper = cropper

	def getProfilePicture(self, image, width, height):
		self.cropper(image, width, height)
		sharpen(image)
		saturate(image)
		
def simple_profile_picture_cropper(image, width, height):
	crop(image, 0, 0, width, height)
		
def face_finding_profile_picture_cropper(image, width, height):
	center = locate_face(image)
	crop(image, center.x - (width/2), 
		center.y - (height/2), width, height)
		
class Factory():
	def createSimpleCreator(self):
		return ProfilePictureCreator(simple_profile_picture_cropper)
		
	def createFaceFindingCreator(self):
		return ProfilePictureCreator(face_finding_profile_picture_cropper)
```

In the first profile picture example the constructor had no parameters so you could easily instantiate the profile picture creator of your choosing and be off to the races.  In this one you need to call a factory method before you start to work.  The first example requires slightly less typing to use the code.  The second example is more testable, more flexible in its creation (consider if more options exist, or *will* exist), and hides its implementation details.  So it's a choice, and the choice is yours.

## Common variant methods

With a Template Method implementation you may need to share the behavior of some of the variant methods in multiple subclasses.  The typical way to handle this problem is to create a new class with those common variant methods and subclass it.  Below is an example illustrating this approach.

```python
class CurrencyConverter():
	def sourceCurrencyCode(self):
		raise NotImplementedError()
		
	def targetCurrencyCode(self):
		raise NotImplementedError()

	def convert(self, units):
		return units * get_exchange_rate(self.sourceCurrencyCode(),
			self.targetCurrencyCode())

class UsdConverter(CurrencyConverter):
	def sourceCurrencyCode(self):
		return 'USD'
			
class UsdToCadConverter(UsdConverter):
	def targetCurrencyCode(self):
		return 'CAD'
		
class UsdToGbpConverter(UsdConverter):
	def targetCurrencyCode(self):
		return 'GBP'
```

Notice the `UsdConverter` class isn't to be used alone.  Its just a means for `UsdTo*` classes to get their `sourceCurrencyCode()` methods for free.  So whats the problem?  Well, there are a few...

* Depending on the size of your system there may unnecessarily be lots of common-method classes and they be multiple levels of inheritance deep.
* Naming common-method classes also becomes difficult since the grouping of methods might not have a logical relationship or single purpose.  One consequence of this problem is that your outermost subclasses inherit from common-method classes that give little indication of what they do.
*  At some point a change in the common-method class may be undesirable in some of its subclasses since they may lack that true [is-a relationship](http://en.wikipedia.org/wiki/Is-a).

If you don't couple your configuration options, you don't really have this problem.  You can vary your more complicated situations using Strategies, Decorators, Chains Of Responsibility - all kinds of patterns depending on what you are trying to build.  You can, if needed, wire them all together with Builders.  If you find you're repeating a lot of your construction process by calling the same set of methods on your Builder, then perhaps you can combine those calls into a new method on your Builder, or create a Factory which pre-configures your Builder with a set of method calls.

This approach makes you create some really powerful and flexible Builders.  Your construction process reads top-down like a recipe rather than a shuffled stack of common-method classes.  

My advice is to always consider inheritance as a last option when that is-a relationship is not present.  This is much easier if you have a firm grasp on the other patterns which do not rely on inheritance.