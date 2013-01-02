Title: Blogging software:  Blogger, Wordpress, and Pelican
Date: 2012-12-30 19:00
Author: Bob McKee
Category: using-software
Tags: blogging, pelican, python, blogger, wordpress
Keywords: blogging, pelican, python, blogger, wordpress

## What's wrong with Blogger?

In this iteration of my blog I've switched away from Blogger.  At this point in my life Blogger just bummed me out.  A few of my gripes with Blogger:

- Bland *classic* themes
- The newer *dynamic* (ooh aaah!) themes are a bit ridiculous.  I have a blog with basically static content.  I don't need a rich JavaScript app with eight different viewing choices.  The reading experience on blogs that use these themes always felt odd and foreign to me, and the *richness* certainly not at all beneficial.
- Changing themes can change the URLs of your posts (One change added a "_\d{1, 3}" to the end of my post slug).  It obviously isn't good when you change your permalinks.
- The editor for customizing templates is just not good enough.  The code is crammed into one massive, not syntax highlighted, monster document that you can tweak in a little textarea.

On the other side Blogger does have some things going for it:

- Almost zero setup if you go with a premade theme
- Free hosting that can survive high traffic events
- Very easy for non-programmers

## Wordpress as a replacement

When switching from Blogger, the obvious alternative is Wordpress.  I started developing a theme on Wordpress and it wasn't terrible.  For a quick setup I even found a premade Wordpress development environment created using [Vagrant](http://vagrantup.com/).  I took the entire Wordpress installation and checked it into Git.  I removed the default theme and plugins I didn't need.  I added plugins and checked them right into my repo.  Theme development wasn't terrible.  Wordpress is written in PHP so I, along with many many web developers, have tons of PHP experience to leverage.

I could probably have gone live with my Wordpress and been fairly happy.  That said, here are a few things I did not like:

- The theme API is not really like the PHP I'm use to seeing.  Its probably made more for HTML/CSS programmers than someone with a more traditional background.
- Some of the theme API function naming makes me cringe.  the_title().  the_content().  the_ID().  the_facepalm().
- The theme API had that *we know its wrong but we're stuck with it* feel to it.  That doesn't mean it isn't usable, but just makes it a little less enjoyable to work with.
- Without heavy caching tools like [WP Super Cache](http://wordpress.org/extend/plugins/wp-super-cache/) its very slow.
- Theres still a database for mostly static content.  In a high traffic scenario that database is going to be doing a lot of work... but why?
- I realized that I was going to make an *About Me* page for the site in development, but to get that page to production it would involve some sort of export and import which is hardly convenient.

Wordpress has all the benefits I listed for Blogger plus a few more:

- Lots of plugins
- Lots of themes
- Ability to design themes in the tools of your choice, meaning things like editors but also using tools like LESS CSS, Compass, or JQuery

## Pelican, a Python-based static site generator

I had never heard of [Pelican](http://getpelican.com) before.  Pelican is a blogging system written in Python that allows you to write your posts as files with embedded metadata then run a build script which generates your entire site by combining your posts with theme templates.  By default it includes plugins for integration with [Disqus](http://disqus.com/), a popular commenting system with a free plan.  Disqus can be added to a static HTML page using JavaScript.

Creating a theme was pretty easy.  My templates total a little over 150 lines.  I used [SASS](http://sass-lang.com/) to generate CSS.  My theme, custom pages, and articles all get stored in Git (by choice, no VCS is actually required).  Pelican has a Make script which you can easy configure to generate the static content and deploy it in several different ways.

Pelican uses [Jinja](http://jinja.pocoo.org/) for templates; a great choice in my opinion.  The data objects provided to the templates seemed well designed, as did the rest of the Pelican code.

Overall why I like Pelican:

- Good, simple theme API
- Lets me use tools like LESS CSS or SASS
- Local development is stupid-easy to get started with
- Generates static files which leave plenty of options when scaling is a concern
- [All my content is in Git](https://github.com/bywires/bywires-pelican).  No exceptions.
- My content is portable
- I can write posts using whatever I want... they're just files on my computer.  Writing posts on the train with no Wifi - perfectly fine.

I could get into the pitfalls of Pelican but I think the biggest just boil down to small community.  The documentation is still very good, but if you're googling for something don't expect to find much community discussion.  I think it has the right plugins available right now, but if you wanted to do something that wasn't already in Pelican, expect to be writing code.  This of course is a far cry from the experience you'd have with Wordpress and its 20k+ plugin library.

Pelican does have import capabilities from Wordpress.  In my case I exported Blogger content, imported into Wordpress, exported from Wordpress, then imported into Pelican.  I definitely needed to do some cleanup on each article after the fact.

I think Pelican is a great option for a programmer blogger with at least some Python knowledge who wants to make a fairly simple site and wants to have full UI control.

You can see everything I did with Pelican over at [Github](https://github.com/bywires/bywires-pelican).

