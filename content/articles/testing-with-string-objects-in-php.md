Title: Testing with string objects in PHP
Date: 2010-07-29 23:56
Author: Bob McKee
Category: programming
Tags: php, testing
Keywords: php, testing

As shown in the last post there are benefits to instantiating the class
under test in setUp(). With objects its simple to create them and
maintain reference to them so you can change them, but what about things
like strings? Unlike in many other modern languages, strings are not
objects in PHP. They are not passed by reference. The good news is while
strings are not objects, objects can be stings.

<div class="code php" markdown="1">
    <?class String {
        public function set($str) {
            $this->_str = $str;
        }
        public function __toString() {
            return $this->_str;
        }
    }
</div>

This class can be used as a string. It can work in PHP's string
functions and any other place a string is desired. So pass this to the
class you're testing and then change it later. It works all the same.

Its important to note that if you are using these in your test setUp()
that you can't do work using that string object during the construction
process of the class under test. Initially this slipped my mind as its
part of my standard practices. I believe you should [never do any work
in your constructor at all][].

[never do any work in your constructor at all]: http://misko.hevery.com/code-reviewers-guide/flaw-constructor-does-real-work/
