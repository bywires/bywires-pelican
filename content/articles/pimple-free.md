Title: Pimple Free
Date: 
Author: Bob McKee
Category: programming
Tags: silex, symfony, pimple, intellij, phpstorm, php, dependency injection, dependency injection container, php framework
Keywords: 
Description: 

This month I started on a new project at work - a totally greenfield web app.  [Silex](http://silex.sensiolabs.org/) was chosen as the tool we'd be using to create the web app.  Silex makes heavy use of [Pimple](http://pimple.sensiolabs.org), a *very* small dependency injection container that allows you to map factories or values to string keys on an object that implements [ArrayAccess](http://php.net/manual/en/class.arrayaccess.php).

Here's a quick example of how one might use Pimple:

```php
$pimple = new \Pimple\Container();;

$pimple['db.client'] = function($pimple) {
    return new MysqlClient();
};
```

Simple enough, but the problem arises rather quickly.  Somewhere else in the project there will be code like this:

```php
$usersDao = new UserDao($pimple['db.client']);
```

So whats wrong?  Possibly a few things.

Does *db.client* exist?  I guess we'll find out at runtime!  If it does exist, where is it defined?  Silex and Pimple promote a *Service Provider* pattern, so the code above would actually look a bit like this...

```php
class DbServiceProvider implement ServiceProviderInterface
{
    public function register(Container $pimple)
    {
        $pimple['db.client'] = function($pimple) {
            return new MysqlClient();
        };
    }
}

class UserServiceProvider implement ServiceProviderInterface
{
    public function register(Container $pimple)
    {
        $pimple['data.user'] = function($pimple) {
            return new UserDao($pimple['db.client']);
        };
    }
}

$pimple->register(new DbServiceProvider());
$pimple->register(new UserServiceProvider());
```

You can follow this. I can follow this.  Its two classes.  No big deal.  All the Service Providers in a Silex app live in a single directory so you know where to look.  That said, Silex defines quite a few factories for Pimple.  Silex always refers to the Pimple (actually a Pimple subclass) as *$app* and always uses array access, so the statement below looks to that with the assignment operator ("=").  The second command is similar except that it looks for keys that have variables in them.  These ones are usually in loops so the assignments are multiplied by the number of iterations.  We're looking at a baseline of 150-200 assignments.  That a bit of a load on the mind and we haven't into how the app actually works.

```
ack '\$(this->)?app\[.*?]\s*=' vendor/silex/silex/src | wc -l    
154
ack '\$(this->)?app\[.*?\$.*?]\s*=' vendor/silex/silex/src | wc -l
15
```

Theres a bit of ambiguity regarding the types resulting from these factories.  In my example, what type should we expect for *db.client*?  If you look at the factory that creates it you might think its a MysqlClient, but suppose MysqlClient implements DbClient, but MysqlClient has a superset of methods than those in DbClient.  So what is the gauranteed interface of *db.client* - a DbClient or MysqlClient?   Unfortuntely, nothing is guaranteed.  Your best bet is searching for where the key is used and what type is expected there.  Some people set the key in Pimple to be the name of an interface to remove this ambiguity, but Silex unfortunately does not.

One thing that could help navigate all this code is allowing for an IDE to jump to the declaration of a given key, but, alas, theres a few more hurdles.  First, there could be more than one instance of Pimple, so your IDE would need to know which one you were inspecting and it can't do that without running your code.  Second, [PHPDoc](http://www.phpdoc.org/) does not allow for a parameterized return value so the Pimple using ArrayAccess is a problem.  Telling your IDE what the return type is using PHPDoc is out.

Given my complaints about Pimple I wondered what an alternative implementation might be.  There are other PHP Dependency Injection Containers but most are not nearly as simple as Pimple (one file, couple hundred lines).  Here's what I've come up with.  The *Container* class is really the only library code.

```php
class Container
{
    /** @var null|Container */
    protected $rootContainer = null;

    public function __get($name)
    {
        return $this->{'_' . $name}();
    }

    protected function child(Container $container)
    {
        $container->rootContainer = $this->rootContainer ?: $this;
        return $container;
    }
}

/**
 * @property-read ApiContainer $api
 */
class AppContainer extends Container
{
    protected function _api()
    {
        return $this->child(new ApiContainer());
    }
}
```

In this example, *AppContainer* is the base container for your application.  It has one child container, *ApiContainer*.  A user would get an *ApiContainer* instance by calling *$appContainer->api*.  The magic *__get* method would call the *AppContainer::_api()* method which would return the *ApiContainer*.  In my simple example there isn't much benefit in using *__get* versus just calling a public *api()* method.  In a full implementation you'd likely have code in *__get* to do thing like provide singleton functionality or maybe some of the other functionality you see in Pimple's *offsetGet* (we'll see some of this later).

Pimple gets its configuration by executing its methods at runtime.  Our IDEs have no idea what instance of Pimple is being operated on and no idea what configuration it might hold.  This isn't beneficial at all.  Obviously, not all instances of Pimple are the same.  Our application can't just use any ol' instance interchangeably.  Our application needs certain keys to exist and for those keys to return values of certain types.  Our classes have certain type needs and we know what they are **before** runtime.

In my example, AppContainer is a distinct class with a distinct interface.  It **always** has an *api* property of type *AppContainer*.  I tell my IDE this using the *property-read* PHPDoc tag.

Here's an expanded usage example:

```php
/**
 * @property-read ApiContainer $api
 * @property-read HttpDriver $httpDriver
 */
class AppContainer extends Container
{
    protected function _api()
    {
        return $this->child(new ApiContainer());
    }

    protected function _httpDriver()
    {
        return new CurlDriver();
    }
}

/**
 * @property AppContainer $rootContainer
 * @property-read ApiClient $client
 */
class ApiContainer extends Container
{
    protected function _client() {
        return new ApiClient($this->rootContainer->httpDriver);
    }
}

interface HttpDriver {}

class CurlDriver implements HttpDriver {}

class ApiClient
{
    public function __construct(HttpDriver $httpDriver)
    {
        $this->httpDriver = $httpDriver;
    }

    public function get($url) {
        // ...
    }
}

$app = new AppContainer();
$app->api->client->get('http://www.google.com');
```

This works.  Your IDE uses the PHPDoc tags to determine what type of objects you're working with the whole way through.  You can have autocomplete.  You can jump to declarations of relevant types.  MISSION ACCOMPLISHED!  Uhh, theres just one problem (that I can think of).  Pimple will all you to easily change out factory methods for use in testing, but this will not.  For example the above code would not let you do this:

```php
$app->api->client = MockApiClient();
var_dump($app->api->client);
```

It won't error out, but *$app->api->client* will still be a *ApiClient* in that *var_dump* instead of *MockApiClient*.  The reason is that after setting the value to *MockApiClient* our instance of *ApiContainer* is no longer referenced.  The next attempt to access *$app->api->client* will generate a new *ApiContainer* with a new *ApiClient* as both are transient objects.

Without too much work we can add support for this.  Below I've added the concept of *values* and *factories* to *Container*.  I've updated *AppContainer* to register *ApiContainer* as *child* which we now internally store as a singleton factory.  This means that once *$app->api* is accessed we hold the instance of *ApiContainer* for future accesses, thereby solving the above-mentioned transient object problem.  Finally, I've used the *value* feature to hold and return a reference to the *MockApiClient* object.

```php
class Container
{
    /** @var null|Container */
    protected $rootContainer = null;

    /** @var callable[] */
    protected $factories = [];

    /** @var mixed[] */
    protected $values = [];

    public function __get($name)
    {
        if (isset($this->values[$name])) {
            return $this->values[$name];
        } elseif (isset($this->factories[$name])) {
            return $this->factories[$name]();
        }

        $result = $this->{'_' . $name}();

        if ($result instanceof Singleton) {
            $this->factories[$name] = $result;
            $result = $result();
        }

        return $result;
    }

    public function __set($name, $value)
    {
        if (is_callable($value)) {
            $this->factories[$name] = $value;
        } else {
            $this->values[$name] = $value;
        }
    }

    protected function child(Container $container)
    {
        $container->rootContainer = $this->rootContainer ?: $this;
        return new Singleton($container);
    }
}

class Singleton
{
    public function __construct($instance)
    {
        $this->instance = $instance;
    }

    public function __invoke()
    {
        return $this->instance;
    }
}

$app->api->client = MockApiClient();
```