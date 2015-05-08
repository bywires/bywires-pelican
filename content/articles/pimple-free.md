Title: Pimple Free
Date: 
Author: Bob McKee
Category: programming
Tags: silex, symfony, pimple, intellij, phpstorm, php, dependency injection, dependency injection container, php framework
Keywords: 
Description: 

I recently started a new web app project at work.  [Silex](http://silex.sensiolabs.org/) was chosen as the PHP framework we'd be using.  Silex makes heavy use of [Pimple](http://pimple.sensiolabs.org), a very small dependency injection container that allows you to map factories or values to string keys on an object that implements PHP
s [ArrayAccess](http://php.net/manual/en/class.arrayaccess.php) interface.  Here's a quick example of how one might use Pimple:

```php
$pimple = new \Pimple\Container();

$pimple['db.client'] = function($pimple) {
    return new MysqlClient();
};

// elsewhere in project...
$usersDao = new UserDao($pimple['db.client']);
```

Seems innocent enough, but theres a few things wrong.

Does *db.client* exist?  I guess we'll find out at runtime!  If it does exist, where is it defined?  Silex and Pimple promote a *Service Provider* pattern, so the code above would actually look a bit like this:

```php
class DbServiceProvider implements ServiceProviderInterface
{
    public function register(Container $pimple)
    {
        $pimple['db.client'] = function($pimple) {
            return new MysqlClient();
        };
    }
}

class UserServiceProvider implements ServiceProviderInterface
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

This is easy to follow and all the Service Providers in a Silex app live in a single directory so you know where to look.  That said, Silex defines quite a few factories for Pimple.  I came up with a regular expression search to find out roughly how many.  Silex always refers to Pimple as *$app* and always uses array access, so the statement below looks to that with the assignment operator ("=").  The second command is similar except that it looks for keys that have variables in them.  These ones are usually in loops, so the assignments are multiplied by the number of iterations.  It turns out we're looking at a baseline of around 150-200 assignments.  That's a bit of a load on the mind and we haven't even gotten into how the app actually works.

```
ack '\$(this->)?app\[.*?]\s*=' vendor/silex/silex/src | wc -l    
154
ack '\$(this->)?app\[.*?\$.*?]\s*=' vendor/silex/silex/src | wc -l
15
```

Undoubtedly we have lots of Pimple keys and factories to keep in our head.  To further complicate matters the return types from these factories is never explicitly declared.  In my example, what type should we expect for *db.client*?  If you look at the factory that creates it you might think its a *MysqlClient*, but suppose *MysqlClient* implements *DbClient*.  So what is the guaranteed interface of *db.client* - a *DbClient* or *MysqlClient*?   Unfortunately, nothing is guaranteed.  Your best bet is searching for where the key is used and what type is expected there.

An IDE that could interpret this code could offer up tooltips, autocomplete, let you jump to declarations, and much more.  Surely, this would accelerate our understanding of the system.  Sadly, this doesn't seem possible using Pimple.  There could be more than one instance of Pimple, so your IDE would need to know which one you were inspecting and it can't do that without running your code.  Additionally, Pimple's use of *ArrayAccess*, which results in a single method returning mixed values based on a method parameter, cannot be property documented using IDE-supported [PHPDoc](http://www.phpdoc.org/) tags.

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

In this example, *AppContainer* is the base container for your application.  It has one child container, *ApiContainer*.  A user would get an *ApiContainer* instance by calling *AppContainer::api*.  In this simple example there isn't much benefit in using *__get* versus just calling a public *api()* method.  In a full implementation you'd likely have code in *__get* to do thing like provide singleton functionality or maybe other features you see in Pimple's *offsetGet* (we'll see some of this later).

Pimple gets its configuration at runtime.  Until then, our IDEs have no idea what instance of Pimple is being operated on and no idea what configuration it might hold.  This isn't beneficial at all.  Obviously, not all instances of Pimple are the same.  Our application can't just use any instance interchangeably.  Our application needs certain keys to exist and for those keys to return values of certain types.  Our classes have certain type needs and we know what they are **before** runtime.

My example takes advantage of that fact.  *AppContainer* is a distinct class with a distinct interface.  It **always** has an *api* property of type *AppContainer*.  I tell my IDE this using the *property-read* PHPDoc tag.

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

This works.  IDE's like IntelliJ/PHPStorm can use the PHPDoc tags to determine what type of objects you're working with the whole way through.  You get autocomplete.  You can jump to declarations of relevant types.  **MISSION ACCOMPLISHED!**  Uhh, theres just one problem (that I can think of).  Pimple will allow you to easily change out factory methods for use in testing, but my example code will not.  My *Container* class would not let you do this:

```php
$app->api->client = MockApiClient();
var_dump($app->api->client);
```

It won't error out, but *$app->api->client* will still be a *ApiClient* in that *var_dump* call instead of being a *MockApiClient*.  The reason is that after setting the value to *MockApiClient* our instance of *ApiContainer* is no longer referenced.  The next attempt to access *$app->api->client* will generate a new *ApiContainer* with a new *ApiClient* as both are transient objects.

Without too much work we can add support for this.  Below, I've added the concept of *values* and *factories* to *Container*.  I've updated *AppContainer* to register *ApiContainer* as *child* which we now always store as a Singleton Factory.  This means that once *$app->api* is accessed we hold the instance of *ApiContainer* for future accesses, thereby solving the above-mentioned transient object problem.  Finally, I've used the *value* feature to hold and return a reference to the *MockApiClient* object.

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

This simple system should enable the user to take advantage of a powerful IDE and help them understand a system that uses a Dependency Injection Container more easily than a Pimple-based system.  I'll update this post shortly once I've created a Composer package for the code in this article.

**UPDATE**: Check [Pedic](https://github.com/bywires/pedic) out on Github!