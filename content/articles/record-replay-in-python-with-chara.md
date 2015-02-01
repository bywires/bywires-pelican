# Record/Replay in Python using Chara


Last week I released a new Python library called Chara.  Chara is basically a record and replay tool.  Imagine you want to test some code that is coupled with some other code.  You don't want to test that other code.  Maybe the other code hits the database, or an external service, or does something that shouldn't or can't happen when tests are run.  You could use a test double and a library like mock.  What if youdon't even know what the dependency does?  This is often the case when working on existing code.  You end up logging or printing a bunch of inputs and outputs to you can manually define the test double's behavior.  This can be a pretty slow process especially with complex interactions.

Chara aims to speed things up and take away the uncertainty.  The flow is simple:

* Write a passing test that uses the unwanted dependency
* Tell Chara to record the behavior of that dependency
* Tell Chara to replay the behavior of that dependency so your test works the same but the dependency is no longer called

## Test drive

Suppose you wanted to test some code that scraped a website and extracted the headline.  Let's start by creating the production code and passing test (test_scraper.py)::

    def scrape_headline(name):
        url, search = {
            'wired': (
                'http://www.wired.com', 
                '<div class="headline headline1">\s*'
                '<h5>[^<]*</h5>\s*'
                '<h2>\s*<a[^>]*>([^<]*?)</a>\s*</h2>\s*'
                '</div>'
            )
        }[name]

        matches = re.search(search, get_html(url))

        return matches.group(1) if matches else None


    def get_html(url):
        return urllib2.urlopen(url).read()


    class DemoTest(TestCase):
        def test_scraper(self):
            self.assertEqual(
                'This Is What Happens When You Hack and '
                'Extort the \'Bitcoin Jesus\'',
                scrape_headline('wired')
            )

Thats a pretty simple test that I know works even before Chara enteres the picture.  Now, we add chara.record decorator and run the test again::

    class DemoTest(TestCase):
        @chara.record('test_scraper.get_html')
        def test_scraper(self):
            self.assertEqual(
                'This Is What Happens When You Hack and '
                'Extort the \'Bitcoin Jesus\'',
                scrape_headline('wired')
            )

This causes get_html() to be decorated with a *spy* that records behavior.  The spy's recordings are serialized and stored in a file when the test's execution completes.  Finally, we switch to using chara.replay.  Notice that even if you turn get_html() to a no-op function the test still passes, so you know that the function's normal functionality is being bypassed by Chara's replay functionality.::

    def get_html(url):
        pass # nothing even happening here, but the test passes!

    class DemoTest(TestCase):
        @chara.replay('test_scraper.get_html')
        def test_scraper(self):
            self.assertEqual(
                'This Is What Happens When You Hack and '
                'Extort the \'Bitcoin Jesus\'',
                scrape_headline('wired')
            )

### Feature incomplete

A quick heads up.  Chara isn't done.  It can spy on functions, instance methods, class methods, and static methods.  Other object attributes like properties, slot wrappers