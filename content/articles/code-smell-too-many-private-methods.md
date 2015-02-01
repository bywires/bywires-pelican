Title: Code smell: Too many private methods
Date: 2010-07-21 12:46
Author: Bob McKee
Category: programming
Tags: anti-patterns, code smell
Keywords: anti-patterns, code smell

I mentioned this in my last post so I figured I'd add some examples to
clarify. Consider the following code:

```php
class Cache {
    public function set($key, $data) {
        if($this->_useMemcache()) {
            $this->_setInMemcache($key, $data);
        } elseif($this->_useFilesystem()) {
            $this->_setInFilesystem($key, $data);
        } else {
            $this->_setInMemory($key, $data);
        }
    }
}
```

Its part of a class that would be used for caching data. If you had a
view of all the methods on this class there would be groups of similar
methods: those with "memcache" in the name, "filesystem" in the name,
and "memory" in the name. On any given operation when one "memcache"
method would be used other "memcache" methods are used with it. The same
would be true for the "filesystem" and "memory" methods.

If this class were around for a while eventually you'd find yourself
saying "Damn, I want to reuse this functionality for writing to
memcache, but I don't want the whole Cache system."

If this class was built without tests and you ended up with the task to
add them you'd be saying "Holy fucking shit of shit, this is fuckin hard
to test" in a Lewis Black voice as you wildly shook from side to side.
This is your Minnesota winter (google it).

What we really want is separate classes for caching in memcache, the
filesystem, and in memory. You could probably wire these together using
a [Chain of Responsibility patttern][]. The Chain of Responsibility
essentially lets you create a series of fallbacks.

Client: "I need to cache this data."  

Memcache: "I don't want to cache this data but I know someone who might.
Do you want to cache this data?"  

Filesystem: "I'm watching my show, fuck off. Memory, get the fuck in
here? Cache this for me."  

Memory: "I have no feeling of self-worth and will grow up to be an
unsuccessful empty shell of a man, so I may as well comply. OK,
filesystem, I'll cache it."

Anyways, once you understand the [Single Responsibility Principle][]
you'd never write this Cache class in the first place. Its obviously
flawed. Clear as day. Sometime you don't find out until you're already
coding though.

## The less obvious case

About a year and a half ago I was writing a class that could read and
write language translations from a excel file. The class was going to be
used to import it into a database or export what was in the database
into a spreadsheet. I already had an interface I used to access
translations from other sources so I started implementing it. I used a
3rd-party library, [PHPExcel][], for traversing the grid, reading, and
writing.

I was learning PHPExcel's API as I went. We also had somewhat complex
schema that the spreadsheet needed to fit. There could be a variable
number of columns depending on how many languages were translated, and
any number of rows because new strings were always being added or
removed.

I got it working but was left with lots of private methods that did what
I needed to conveniently on the spreadsheet. I had a good tool to work
with (PHPExcel) but I needed more. I should have had a class which used
PHPExcel but traversed the data in the way I needed.

Since then our translation files have grown and we found that PHPExcel
is a memory hog. Exporting a few hundred (maybe up to a thousand) rows
takes several minutes. I've profiled the code and the problem is
PHPExcel (FWIW, I hear there are some newer features in later versions
that may fix this). Unfortunately, if we wanted to replace PHPExcel with
a faster library we have to tear apart the class I wrote because its all
cooked in there, hiding complexities in private methods.

Had I separated my concerns properly replacing the underlying Excel
reader/writer would be simply a matter of writing a new class with the
interface needed to work with my translation importer/exporter class.

[Chain of Responsibility patttern]: http://en.wikipedia.org/wiki/Chain-of-responsibility_pattern
[Single Responsibility Principle]: http://en.wikipedia.org/wiki/Single_responsibility_principle
[PHPExcel]: http://phpexcel.codeplex.com/
