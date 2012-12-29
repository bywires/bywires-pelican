Title: Faking PHP functions
Date: 2010-07-22 21:28
Author: Admin
Category: Programming
Tags: legacy code, php, testing

Usually when I want to fake some kind of functionality provided by PHP,
I create a new library that maps all that crazy API stuff baked into PHP
to something that makes more sense. Maybe it even uses exceptions rather
than -1/0/false/null. Holy shit. I almost never write something that did
a straight pass-through - no parameter changes, method signature
identical to the underlying function. I'd find myself spending time and
thinking a lot about this library I was building. So PHP does it
“wrong”, what does “right” look like? This can be a time-consuming
exercise, but these kinds of libraries can get reused a lot. Writing
tests for what you've done can be a problem as well. One of these
problems is the inspiration for this post.

Here's a dumbed-down version of some code I was writing for a MySQL
class (Yes, I'm actually writing one of those... in 2010... really!):

<div class="code php" markdown="1">
    <?class Mysql {
        public function execute($query) {
            $result = mysql_query($query);
            if($result === false) {
                if(mysql_errno() === self::LOST_CONNECTION) {
                    throw new MysqlLostConnectionException();
                } else {
                    throw new MysqlException();
                }
            }
        }
    }
</div>

How do I get mysql\_errno() to return the code for a lost connection? I
should write a class to wrap this MySQL functionality... oh wait... I
am. I needed something much simpler. Enter "THE SIMPLEST CLASS
EVER!!!"...

<div class="code php" markdown="1">
    <?class PHP_Functions {
        public function __call($phpFunction, $args) {
            return call_user_func_array($phpFunction, $args);
        }
    }
</div>

Now we can rewrite the other code by taking the PHP\_Functions object in
the constructor of our MySQL class and modify two other lines...

<div class="code php" markdown="1">
    <?class Mysql {
        public function execute($query) {
            $result = $this->_phpFunctions->mysql_query($query);
            if($result === false) {
                if($this->_phpFunctions->mysql_errno() ===self::LOST_CONNECTION) {
                    throw new MysqlLostConnectionException();
                } else {
                    throw new MysqlException();
                }
            }
        }
    }
</div>

In our tests its now easy to mimic these MySQL error conditions. We just
have to mock our PHP\_Functions object.

<div class="code php" markdown="1">
    <?/**
     * @expectedException MysqlLostConnectionException
     */
    public function testShouldThrowLostConnectionException() {
        $phpFunctions = $this->getMock('PHP_Functions',array('mysql_query', 'mysql_errno'));
        $phpFunctions->expects($this->any())
            ->method('mysql_query')
            ->will($this->returnValue(false));
        $phpFunctions->expects($this->any())
            ->method('mysql_errno')
            ->will($this->returnValue(Mysql::LOST_CONNECTION));
        $mysql = new Mysql($phpFunctions);
        $mysql->execute('SELECT 1');
    }
</div>

Generally speaking, if someone shows me a magic method like \_\_call() I
find myself unable to reach their heart through their throat but I keep
trying. My arms are big and their throats are small. It just doesn't
work... I keep “breaking” these people. Anyways, I'm not a fan. I
haven't found them to be the least bit useful except for adapting some
legacy code (like I am sort of doing in my example) and maybe making a
[Decorator][] base class if working with code with no type hints (I
don't like those systems either).

There are other options in this case if you find yourself more upset
about magic methods than I am. You can move calls to the MySQL functions
to protected methods and override them in testing to provide mock
functionality. I use this trick a lot when getting legacy code under
test ([See Working Effectively with Legacy Code. Excellent book.][]).
Write a class like below. Then, for your tests, subclass this, override
the methods to provide mock functionality, then run the test on the
subclass you created.

<div class="code php" markdown="1">
    <?class Mysql {
        public function execute($query) {
            $result = $this->_mysql_query($query);
            if($result === false) {
                if($this->_mysql_errno() === self::LOST_CONNECTION) {
                    throw new MysqlLostConnectionException();
                } else {
                    throw new MysqlException();
                }
            }
        }

        protected function _mysql_query($query) {
            return mysql_query($query);
        }

        protected function _mysql_errno() {
            return mysql_errno();
        }
    }
</div>

I had several cases where I needed to mock consecutive calls so it just
seemed like [PHPUnit][] was ready to go with that, so I opted for that
route. Either approach would work well.

[Decorator]: http://en.wikipedia.org/wiki/Decorator_pattern
[See Working Effectively with Legacy Code. Excellent book.]: http://www.amazon.com/Working-Effectively-Legacy-Michael-Feathers/dp/0131177052
[PHPUnit]: http://www.phpunit.de/
