Title: PCI DSS compliance and spaghetti code, Part 3
Date: 2011-08-09 13:15
Author: Bob McKee
Category: programming
Tags: builder pattern, factory patten, legacy code, patterns, pci dss
Keywords: builder pattern, factory patten, legacy code, patterns, pci dss

(Be sure to read [Part 1](|filename|/articles/pci-dss-compliance-and-spaghetti-code-part-1.md) and [Part 2](|filename|/articles/pci-dss-compliance-and-spaghetti-code-part-2.md) first!)

When writing new code I find its a good idea to start at your
integration point and then write that client code, whether just by
psuedo-coding or writing some test cases. For my payment gateway code I
need code that takes user input, builds a request from that input, sends
that request to the payment gateway, and gets a response back so we can
act accordingly.

<div class="code php" markdown="1">
    <?$factory = new RequestFactory(); // get sale builder

    $builder = $factory->buildSaleRequest(); // get credit card, so we can set it

    $builder->withCreditCard()
        ->setCardType($_POST['cardType'])
        ->setCardNumber($_POST['cardNumber'])
        ->setExpirationDate($_POST['expirationDate']); // get address, so we can set it

    $builder->withBillingAddress()
        ->setCity($_POST['city'])
        ->setState($_POST['state']); // send request to payment gateway

    $response = $builder->execute();
</div>

This seems pretty simple. I have objects to accept my user input which
execute the request and get the response. Marvellous. Under the hood its
slightly less simple if you aren't particularly familiar with the
[Factory pattern][], [Builder pattern][], [Gateway pattern][],
[Composite pattern][], and [Visitor pattern][].

Today I'll start at the surface with our [creational patterns][] being
used here, the Factory and Builder pattern.

## Factory pattern

[Factories][Factory pattern], like all other creational patterns, create
new objects. At first they are often understood as a way to make its
consumer get different *types* of object, which is correct, but people
fail to see that they are places to return differently configured
objects (potentially of the same type) as well. Factories are *the*
place to stowaway configuration information. In Factories the
configuration can be centralized, rather than forcing the consumer code
to have to repeat configuration each time. For example:

<div class="code php" markdown="1">
    <?class CarFactory {
        public function create() {
            $car = new Car();
            if($this->config->useElectricCars()) {
                $car->setEngine(new ElectricEngine());
            } else {
                $car->setEngine(new EnvironmentDestroyingBeastEngine());
            }
            return $car;
        }
    }
</div>

We encapsulate the querying of the "config" object into this Factory
method so we don't need to have other parts of the system be aware of
this "config" or aware of any configuration of this object at all.

In the case of the payment gateway RequestFactory, we'll be grabbing the
payment gateway credentials, which get used in each request, and passing
them onto the Request object that gets returned for consumption. This
way other code need not worry about where those come from. We've made
that decision and we've encapsulated it in a Factory.

## Builder pattern

Most people I've seen learning about the [Builder pattern][] don't
really get it for a while. This was true for myself as well. We know
what it is basically - a class with a bunch of methods you can call to
configure an object and then a method to return the newly created and
configured object - but don't know when to use it. A quick look at the
pattern summary talks about varying complex creation processes. Yea, it
can do that, but you have good reason to create those Builders even if
you need only one implementation now.

Here are a few indicators to help you know when its time to use a
Builder.

### Indicator \#1: Wiring together collaborators in application code

Are you doing this in your application code? You've written a library to
create cars and car parts and everywhere you use this library you're
repeating this process...

<div class="code php" markdown="1">
    <?$carPartFactory = new CarPartFactory();
    $carFactory = new CarFactory();
    $car = $carFactory->create();

    $car->setEngine($carPartFactory->createElectricEngine())
        ->setWheels($carPartFactory->createGoodYearTires(4))
        ->setStereo($carPartFactory->createBadAssStereo());
</div>
You're creating more than one factory to wire together collaborators.
Its Builder time, bitches.

<div class="code php" markdown="1">
    <?$carBuilder = new CarBuilder();
    $car = $carBuilder->addElectricEngine()
                      ->addGoodYearTires(4)
                      ->addBadAssStereo()
                      ->build();
</div>

Its easier to use, less duplication, easier to read, *and* if you ever
need to vary that creation process its already in place.

### Indicator \#2: Factory method with optional parameters

Optional parameters are terrible. I think thats a whole post al by
itself. For now, if you find yourself doing this...

<div class="code php" markdown="1">
    <?public function create($first, $last, $middle = '', $prefix = '', $suffix = '')
</div>

...do this instead...

<div class="code php" markdown="1">
    <?$builder->first($first)
              ->last($last)
              ->middle($middle);
</div>

### Builders in Builders

Final note of the day on Builders. Object chaining can make usage pretty
easy. We get use to returning $this in each method. Sometimes though we
want the Builder to return another Builder which can configure its
collaborator. In this case we return the Builder instead of $this, but
its also good to have a method naming convention to let developers know
instinctively which they'll get back.

Personally, and I think I picked this up from a book though I can't
remember which one, I use "set" or "add", whichever reads best, when
I'll be returning $this, and "with" when I'll be returning another
Builder. Sometimes I might even have a "set/add" method and a "with"
method for configuring the same option, where the "set/add" just uses
default settings and the "with" method lets you dig in, but only if you
want to.

<div class="code php" markdown="1">
    <?// using "add"
    $builder->addGoodYearTires();

    // using "with"
    $builder->withGoodYearTires() // returns TireBuilder
        ->setFancyRims()
        ->setSnowTires();
    
    class CarBuilder {
        public function withGoodYearTires() {
            // keep reference to builder so we can get its "product"
            // and add it to the Car we're building
            $this->_tireBuilder = new TireBuilder();
            return $this->_tireBuilder;
        }
    }
</div>

[Factory pattern]: http://en.wikipedia.org/wiki/Factory_method_pattern
[Builder pattern]: http://en.wikipedia.org/wiki/Builder_pattern
[Gateway pattern]: http://martinfowler.com/eaaCatalog/gateway.html
[Composite pattern]: http://en.wikipedia.org/wiki/Composite_pattern
[Visitor pattern]: http://en.wikipedia.org/wiki/Visitor_pattern
[creational patterns]: http://en.wikipedia.org/wiki/Creational_pattern
  