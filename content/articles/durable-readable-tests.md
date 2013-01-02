Title: Durable, readable tests
Date: 2010-07-29 23:10
Author: Bob McKee
Category: programming
Tags: testing
Keywords: testing

Anyone who has written tests is familiar with our friend the setUp()
fixture method. We use setUp() to do all that work that's common across
all our tests. It can be used to reduce repetition within our tests,
making them simpler, and more readable. Unfortunately testing can get a
little more complicated when you need to sense behavior through a
dependency.

Take this class below which decides which developer is on-call using a
[Chain of Responsibility pattern][].

<div class="code php" markdown="1">
    <?class DeveloperOnCall_Bob implements DeveloperOnCall {
        public function getOnCallDeveloper() {
            if($this->_date->inRange('2010-07-19', '2010-07-26')) {
                return 'Bob';
            }
            return $this->_nextLinkInChain->getOnCallDeveloper();
        }
    }
</div>

A lot of people would just load their test methods with mock object
declarations and probably end up with something like this:

<div class="code php" markdown="1">
    <?class DeveloperOnCall_BobTest extends TestCase {
        public function testShouldReturnBobWhenHeIsOnCall() {
            $date = new Date('2010-07-21'); // date in range!
            $nextLinkInChain = $this->getMock('DeveloperOnCall ',
                 array('getDeveloperOnCall'));
            $nextLinkInChain->expects($this->never())
                ->method('getDeveloperOnCall');
            $actual = $this->_getClassUnderTest($date,
                 $nextLinkInChain)->getDeveloperOnCall();
            $this->assertEquals('Bob', $actual,
                 'Bob should be on call!');
        }

        public function testShouldNotReturnBobWhenHeIsOnNotCall() {
            $date = new Date('2010-07-30'); // date not in range!
            $nextLinkInChain = $this->getMock('DeveloperOnCall ',
                 array('getDeveloperOnCall'));
            $nextLinkInChain->expects($this->once())
                ->method('getDeveloperOnCall');
            $actual = $this->_getClassUnderTest($date,
                 $nextLinkInChain)->getDeveloperOnCall();
        }

        private function _getClassUnderTest(Date $date,
             DeveloperOnCall $nextLinkInChain) {
            return new DeveloperOnCall_Bob($date, $nextLinkInChain);
        }
    }
</div>

How good is this test? Lots of setup in those test methods. A bit hard
to read. The two tests are very similar yet given this design its very
hard to reuse that similar code. If the way those dependencies work
changes (as they often do during development) both these tests break and
need to be fixed separately.

There is another way though. Lets configure our dependencies somewhat
lazily. Consider this alternative:

<div class="code php" markdown="1">
    <?class DeveloperOnCall_BobTest extends TestCase {
        public function setUp() {
            $this->_date =  $this->getMock('Date', array('inRange')),
            $this->_nextLinkInChain = $this->getMock('DeveloperOnCall',
                 array('getDeveloperOnCall'));
             $this->_classUnderTest = new DeveloperOnCall_Bob(
                $this->_date,
                $this->_nextLinkInChain
            );
        }

        public function testShouldReturnBobWhenHeIsOnCall() {
            $this->whenDateIs($this->duringBobsOnCallTime())
                ->theNextLinkShould($this->neverBeCalled())
                ->andTheDeveloperOnCallShouldBe('Bob');
        }

        public function testShouldNotReturnBobWhenHeIsOnNotCall() {
            $this->whenDateIs($this->notDuringBobsOnCallTime())
                ->theNextLinkShould($this->beCalledOnce())
                ->andTheDeveloperOnCallShouldBe('Adam');
        }

        private function whenDateIs($inRange) {
            $this->_date->expects($this->any())
                ->method('inRange')
                ->will($this->returnValue($inRange));
            return $this;
        }

        private duringBobsOnCallTime() {
            return true;
        }

        private notDuringBobsOnCallTime() {
            return false;
        }

        private function theNextLinkShould($expects) {
            $this->_nextLinkInChain->expects($expects)
                ->method('getDeveloperOnCall')
                ->will($this->returnValue('Adam'));
            return $this;
        }

        private neverBeCalled() {
            return $this->never();
        }

        private beCalledOnce() {
            return $this->once();
        }

        private function andTheDeveloperOnCallShouldBe($dev) {
            $this->assertEquals(
                $dev,
                 $this->_classUnderTest->getDeveloperOnCall(),
                "Wrong developer is on call!"
            );
        }
    }
</div>

This last example may be a but longer than the previous but it seems
almost like comparing paragraphs and bullet points in terms of
readability. This test is extremely expressive. It is clear and to the
point. A person who has never worked with this library can easily see
the author's intent.

Finally, if the dependencies change the code that mocks those
dependencies is only in setUp() and private methods so the test methods
themselves will not need to change.

[Chain of Responsibility pattern]: http://en.wikipedia.org/wiki/Chain-of-responsibility_pattern
