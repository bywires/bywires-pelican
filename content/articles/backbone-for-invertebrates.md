Title: Backbone for Invertebrates
Date: 2013-11-17 00:00
Author: Bob McKee
Category: programming
Tags: javascript, backbone, jquery
Keywords: javascript, backbone, jquery

Its 2013 and I'm about to talk about [Backbone.js](http://backbonejs.org/), a four year old library that isn't on the bleeding edge of anything.  This isn't a post about Backbone.js so fans of [AngularJS](http://angularjs.org/), [Knockout](http://knockoutjs.com/), or new M-V-yadda-yadda-yadda framework can settle down.  I want to focus on what we can learn from any system **like** Backbone.js.

Backbone.js is a JavaScript library that separates data from display.  It defines data in terms of Models and Collections [of Models].  UI work is left to Views.  Views generate HTML and react to user-initiated events like button clicks.  Views may change Model and Collection data and they may react to changes to Model and Collection data.  These changes are communicated using custom Events.  [Backbone.js is not an MVC framework, but its close.](http://backbonejs.org/#FAQ-mvc)

As I eluded to earlier, this kind of system is not new and its not unique.  I think most programmers have heard and, to some extent, understand this approach, yet, in my experience, JavaScript is usually not written this way unless a project already uses Backbone or another similar library as part of standard practice.  Why is that?  There are probably a lot of reasons and I'd like to address a couple:

* The idea that this type of structure is not beneficial on small projects
* The idea that you can't have this kind of structure without Backbone.js or a similar system

Lets explore these reasons by building a small photo gallery.

## Evolution of a photo gallery

<iframe width="200" height="300" src="http://jsfiddle.net/9Fbrr/embedded/result/" allowfullscreen="allowfullscreen" frameborder="0" class="jsfiddle float right"></iframe>

Our photo gallery will show three thumbnails and one large photo.  When you click a thumbnail the large photo space shows that photo.  If you asked a typical developer to build this product, how would they implement it?  I might guess something like this...

```javascript
$(function() {
    var photos = [
    	{ thumbnail: '0-thumbnail.jpg', large: '0-large.jpg' },
    	{ thumbnail: '1-thumbnail.jpg', large: '1-large.jpg' },
    	{ thumbnail: '2-thumbnail.jpg', large: '2-large.jpg' }
    ];
    
    var thumbnails = $('#thumbnails'),
    	large = $('#large');    
    
    // add thumbnails
    var imgs = [];
    $.each(photos, function(index, photo) {
    	var thumbnail = $('<img>')
    	    .prop('src', photo.thumbnail)
            .prop('alt', index)
    	    .data(photo);
    	imgs.push(thumbnail);
    });
    thumbnails.append(imgs);
    
    // listen for thumbnail clicks
    thumbnails.on('click', 'img', function() {
    	$('img', large).attr('src', $(this).data().large);
    });
    
    // add large photo
    var img = $('<img>')
        .prop('src', photos[0].large)
        .prop('alt', 'large');
    large.append(img);
});	
```

*See it on [jsfiddle](http://jsfiddle.net/bywires/9Fbrr/)*

Only about 30 lines of code.  We have one type of control, the clickable thumbnails.  One type of data, the photos.  The data is coupled with the thumbnails using jQuery's `.data()` method, which "stores arbitrary data associated with the matched elements".  I use event delegation using jQuery's `.delegate()` method so I only need one listener on my thumbnails container rather than one listeners on each individual thumbnail.  I also benefit from being able to add and remove thumbnails from inside the container without having to re-attach event listeners each time.

My equivalent Backbone.js implementation is below.  You'll notice that its not so terse - about 100 lines of code.  More than three times the code for the same result.

```javascript
$(function() {
    var Photo = Backbone.Model.extend({});
    
    var Photos = Backbone.Collection.extend({
        model: Photo,
        
        initialize: function() {
            this.index = 0;
        },
        
        goTo: function(index) {
            if(index == this.index) return;
            
            this.index = index;
            this.trigger('goto');
        },
        
        current: function() {
            return this.at(this.index);
        }
    });
    
    var LargeView = Backbone.View.extend({
        el: '#large',
        
        initialize: function() {
            this.listenTo(this.collection, 'goto', this.change);
        },
        
        render: function() {
            var photo = this.collection.current();
            
            var img = $('<img>')
                .prop('src', photo.get('large'));
            
            this.$el.append(img);
            
            return this;
        },
        
        change: function() {
            this.$el.empty();
            this.render();
        }
    });
    
    var ThumbnailsView = Backbone.View.extend({
        el: '#thumbnails',
        
        events: {
            'click img': 'click'
        },
        
        render: function() {
            var imgs = [];
            $.each(this.collection.models, function(index, photo) {
                var thumbnail = $('<img>')
                       .prop('src', photo.get('thumbnail'))
                       .data('index', index);
                imgs.push(thumbnail);
            });
            this.$el.append(imgs);
                   
            return this;
        },
        
        click: function(event) {
            this.collection.goTo($(event.currentTarget).data('index'));
        }
    });
    
    var AppView = Backbone.View.extend({
        el: '#gallery',
        
        initialize: function() {
            this.photos = new Photos();
            this.photos.add([
                { thumbnail: '0-thumbnail.jpg', large: '0-large.jpg' },
                { thumbnail: '1-thumbnail.jpg', large: '1-large.jpg' },
                { thumbnail: '2-thumbnail.jpg', large: '2-large.jpg' }
            ]);
            
            this.large = new LargeView({
                collection: this.photos
            });
            
            this.thumbnails = new ThumbnailsView({
                collection: this.photos
            });
        },
  
        render: function() {
            this.thumbnails.render();
            this.large.render();
        }
    });

    new AppView().render();
});
```

*See it on [jsfiddle](http://jsfiddle.net/bywires/NDy9q/)*

This version definitely leaves you with a lot more to soak in, though I think a developer familiar with Backbone.js would know whats going on immediately.  We have a Photo Model for our photos and a Photos Collection which I've modified so it implements a simple Iterator pattern.  Then we have two Views.  One controls the large photo and the other controls the group of thumbnails.  Finally, we have AppView which just ties the whole gallery together.

The ThumbnailsView has an event listener.  If the user clicks an image the Photos Collection is told to go to the clicked image index within the collection.  This fires a "goto" event on the Collection.  The LargeView is listening for this event.  Its event handler gets the current image from the Photo Collection and modifies the DOM to display the image.

## And the winner is?

<iframe width="200" height="335" src="http://jsfiddle.net/bywires/K33Aq/embedded/result/" allowfullscreen="allowfullscreen" frameborder="0" class="jsfiddle float right"></iframe>

If the winner was picked here I'd have to say the first example, the one without Backbone.js, would win.  Its a simple product with a simple solution.  Unfortunately, products rarely seem to be so simple.  Lets add a few features:

* Previous image button which is disabled on the first image
* Next image button which is disabled on the last image
* Border around the active thumbnail

Our non-Backbone code grows to about 70 lines (2.3x increase) and starts looking a little unstructured.  It doesn't exactly offer up a solid pattern for building other similar UI components.

```javascript
$(function() {
    var photos = [
        { thumbnail: '0-thumbnail.jpg', large: '0-large.jpg' },
        { thumbnail: '1-thumbnail.jpg', large: '1-large.jpg' },
        { thumbnail: '2-thumbnail.jpg', large: '2-large.jpg' }
    ];
    
    var thumbnails = $('#thumbnails'),
        large = $('#large'), 
        previous = $('#previous'), 
        next = $('#next'),
        active_index = -1;

    function updateButtons() {
        previous.prop('disabled', active_index == 0);
        next.prop('disabled', active_index == photos.length - 1);
    }
    
    function updateLarge() {
        $('img', large).attr('src', photos[active_index].large);
    }
    
    function updateThumbnails() {
        thumbnails.children().each(function(index) {
            var thumbnail = $(this);
            thumbnail.toggleClass(
                'active', 
                thumbnail.data('index') == active_index
            );
        });
    }
    
    function updateGallery(index) {
        if(index == active_index) return;
        if(index < 0) return;
        if(index >= photos.length) return;
        
        active_index = index;
        
        updateButtons();
        updateLarge();
        updateThumbnails();
    }
        
    // add thumbnails
    var imgs = [];
    $.each(photos, function(index, photo) {
        var thumbnail = $('<img>')
            .prop('src', photo.thumbnail)
            .data(photo)
            .data('index', index);
        imgs.push(thumbnail);
    });
    thumbnails.append(imgs);
    
    // listen for thumbnail clicks
    thumbnails.on('click', 'img', function() {
        updateGallery($(this).data('index'));
    });
    
    // listen for previous and next button clicks
    next.click(function() {
        updateGallery(active_index + 1);
    });
    previous.click(function() {
        updateGallery(active_index - 1);
    });
    
    // add large photo
    large.append($('<img>'));
    
    // initialize gallery state
    updateGallery(0);
});
```

*See it on [jsfiddle](http://jsfiddle.net/bywires/k6mz4/)*

Now to update the Backbone.js version.

```javascript
$(function() {
    var Photo = Backbone.Model.extend({});
    
    var Photos = Backbone.Collection.extend({
        model: Photo,
        
        initialize: function() {
            this.index = 0;
        },
        
        goTo: function(index) {
            if(index == this.index) return;
            if(index < 0) return;
            if(index >= this.length) return;
            
            this.index = index;
            this.trigger('goto');
        },
        
        current: function() {
            return this.at(this.index);
        },
        
        previous: function() {
            this.goTo(this.index - 1);
        },
        
        next: function() {
            this.goTo(this.index + 1);
        },
        
        isFirst: function() {
            return this.index == 0;
        },
        
        isLast: function() {
            return this.index == this.length - 1;
        }
    });
    
    var LargeView = Backbone.View.extend({
        el: '#large',
        
        initialize: function() {
            this.listenTo(this.collection, 'goto', this.change);
        },
        
        render: function() {
            var photo = this.collection.current();
            
            var img = $('<img>')
                .prop('src', photo.get('large'));
            
            this.$el.append(img);
            
            return this;
        },
        
        change: function() {
            this.$el.empty();
            this.render();
        }
    });
    
    var ThumbnailsView = Backbone.View.extend({
        el: '#thumbnails',
        
        events: {
            'click img': 'click'
        },
        
        initialize: function() {
            this.listenTo(this.collection, 'goto', this.change);
        },
        
        render: function() {
            var imgs = [];
            $.each(this.collection.models, function(index, photo) {
                var thumbnail = $('<img>')
                       .prop('src', photo.get('thumbnail'))
                       .data('index', index);
                imgs.push(thumbnail);
            });
            this.$el.append(imgs);
            
            this.change();
            
            return this;
        },
        
        click: function(event) {
            this.collection.goTo($(event.currentTarget).data('index'));
        },
        
        change: function() {
            var active_index = this.collection.index;
            
            this.$el.children().each(function(index) {
                var thumbnail = $(this);
                thumbnail.toggleClass(
                    'active', 
                    thumbnail.data('index') == active_index
                );
            });
        }
    });
    
    var IteratorButtonView = Backbone.View.extend({
        events: {
            'click': 'click'
        },
        
        initialize: function() {
            this.listenTo(this.collection, 'goto', this.render);
        },
        
        render: function() {
            this.$el.prop('disabled', this.isDisabled());
            return this;
        },
        
        isDisabled: function() {
            return false;
        }
    });
    
    var PreviousView = IteratorButtonView.extend({
        el: '#previous',
        
        isDisabled: function() {
            return this.collection.isFirst();
        },
        
        click: function() {
            this.collection.previous();
        }
    });

    var NextView = IteratorButtonView.extend({
        el: '#next',
        
        isDisabled: function() {
            return this.collection.isLast();
        },
        
        click: function() {
            this.collection.next();
        }
    });
    
    var AppView = Backbone.View.extend({
        el: '#gallery',
        
        initialize: function() {
            this.photos = new Photos();
            this.photos.add([
                { thumbnail: '0-thumbnail.jpg', large: '0-large.jpg' },
                { thumbnail: '1-thumbnail.jpg', large: '1-large.jpg' },
                { thumbnail: '2-thumbnail.jpg', large: '2-large.jpg' }
            ]);
            
            this.large = new LargeView({
                collection: this.photos
            });
            
            this.thumbnails = new ThumbnailsView({
                collection: this.photos
            });
            
            this.previous = new PreviousView({
                collection: this.photos
            });
            
            this.next = new NextView({
                collection: this.photos
            });
        },
  
        render: function() {
            this.thumbnails.render();
            this.large.render();
            this.previous.render();
            this.next.render();
        }
    });

    new AppView().render();
}); 
```

*See it on [jsfiddle](http://jsfiddle.net/bywires/fY7YE/)*

My Backbone.js version grows to about 190 lines (1.9x increase), but some interesting things are happening.

First, my Photos Collection became a richer Iterator library and there wasn't anything photo-specific in it so I created the IterableCollection class.  This generic class could undoubtedly be used in other parts of my application.  In our line-of-code comparison we could subtract 35 lines and write this up as a dependency.

Second, I created the IteratorButtonView class which I extend twice.  Its very generic and could definitely be used in other projects since all it does is trigger iteration calls on my new IterableCollection type.  Subtract another 17 lines.

The Backbone.js version has a lot more function and class declarations which, in JavaScript, comes with significantly more boilerplate code.  We're realistically comparing 70 lines to somewhere fairly south of 138 lines (1.3x increase) with the bonus of three new classes that will save you time on future projects.

Backbone.js has other advantages to consider.  To name a few:

* It provides a pattern to follow when building new applications.
* The code is readable and easy to reason about.
* Each class and function has a clear purpose.  This breaking down of responsibilities promotes creation of reusable code.
* The code is very testable as event handlers are exposed though the public interface.  Event triggering can be easily mocked or ignored entirely which leaves you with simpler synchronous tests to write.

For my taste, I think the Backbone.js version wins given the new requirements.  I believe that as the photo gallery's requirements grow the decision to use Backbone.js will become increasingly beneficial as well.

## Make the right decision even without Backbone

Removing the Backbone.js dependency from my last example is extremely simple as you can see below.  Its important to remember that the dependency was very limited.  I was only using Backbone.js for structure and event handling.  That said, Backbone.js isn't doing anything earth-shattering and it gets a lot for free by working on top of [Underscore.js](http://underscorejs.org/).  More importantly - **you are already doing this work somewhere**.  In fact, **you may be doing this work all over your product instead of in just one place**.  

Building a system like Backbone, that standardizes how you model UI components, should reduce the amount of code, code duplication, and complexity you need to worry about on any individual project.

```javascript
$(function() {
    function IterableCollection() {
        this.initialize.apply(this, arguments);
    }
    
    $.extend(IterableCollection.prototype, {
        initialize: function() {
            this.models = [];
            this.index = 0;
        },
        
        add: function(models) {
            this.models = models;
        },
        
        at: function(index) {
            return this.models[index];
        },
        
        on: function() {
            $.fn.on.apply($(this), arguments);            
        },
        
        trigger: function() {
            $.fn.trigger.apply($(this), arguments);
        },
        
        goTo: function(index) {
            if(index == this.index) return;
            if(index < 0) return;
            if(index >= this.models.length) return;
            
            this.index = index;
            this.trigger('goto');
        },
        
        current: function() {
            return this.at(this.index);
        },
        
        previous: function() {
            this.goTo(this.index - 1);
        },
        
        next: function() {
            this.goTo(this.index + 1);
        },
        
        isFirst: function() {
            return this.index == 0;
        },
        
        isLast: function() {
            return this.index == this.models.length - 1;
        }
    });
    
    function LargeView() {
        this.initialize.apply(this, arguments);
    }
    
    $.extend(LargeView.prototype, {
        $el: $('#large'),
        
        initialize: function(options) {
            this.collection = options.collection;
            this.collection.on('goto', this.change.bind(this));
        },
        
        render: function() {
            var photo = this.collection.current();
            
            var img = $('<img>')
                .prop('src', photo.large);
            
            this.$el.append(img);
            
            return this;
        },
        
        change: function() {
            this.$el.empty();
            this.render();
        }
    });
    
    function ThumbnailsView() {
        this.initialize.apply(this, arguments);
    }
    
    $.extend(ThumbnailsView.prototype, {
        $el: $('#thumbnails'),
        
        initialize: function(options) {
            this.collection = options.collection;
            this.$el.on('click', 'img', this.click.bind(this));
            this.collection.on('goto', this.change.bind(this));
        },
        
        render: function() {
            var imgs = [];
            $.each(this.collection.models, function(index, photo) {
                var thumbnail = $('<img>')
                    .prop('src', photo.thumbnail)
                    .data('index', index);
                imgs.push(thumbnail);
            });
            this.$el.append(imgs);
            
            this.change();
            
            return this;
        },
        
        click: function(event) {
            this.collection.goTo($(event.currentTarget).data('index'));
        },
        
        change: function() {
            var active_index = this.collection.index;
            
            this.$el.children().each(function(index) {
                var thumbnail = $(this);
                thumbnail.toggleClass(
                    'active', 
                    thumbnail.data('index') == active_index
                );
            });
        }
    });
    
    function IteratorButtonView() {
        this.initialize.apply(this, arguments);
    }
    
    $.extend(IteratorButtonView.prototype, {
        initialize: function(options) {
            this.collection = options.collection;
            this.$el.bind('click', this.click.bind(this));
            this.collection.on('goto', this.render.bind(this));
        },
        
        render: function() {
            this.$el.prop('disabled', this.isDisabled());
            return this;
        },
        
        isDisabled: function() {
            return false;
        }
    });
    
    function PreviousView() {
        this.initialize.apply(this, arguments);
    }
    
    $.extend(PreviousView.prototype, IteratorButtonView.prototype, {
        $el: $('#previous'),
        
        isDisabled: function() {
            return this.collection.isFirst();
        },
        
        click: function() {
            this.collection.previous();
        }
    });

    function NextView() {
        this.initialize.apply(this, arguments);
    }
    
    $.extend(NextView.prototype, IteratorButtonView.prototype, {
        $el: $('#next'),
        
        isDisabled: function() {
            return this.collection.isLast();
        },
        
        click: function() {
            this.collection.next();
        }
    });
    
    function AppView() {
        this.initialize.apply(this, arguments);
    }
    
    $.extend(AppView.prototype, {
        $el: $('#gallery'),
        
        initialize: function() {
            this.photos = new IterableCollection();
            this.photos.add([
                { thumbnail: '0-thumbnail.jpg', large: '0-large.jpg' },
                { thumbnail: '1-thumbnail.jpg', large: '1-large.jpg' },
                { thumbnail: '2-thumbnail.jpg', large: '2-large.jpg' }
            ]);
            
            this.large = new LargeView({
                collection: this.photos
            });
            
            this.thumbnails = new ThumbnailsView({
                collection: this.photos
            });
            
            this.previous = new PreviousView({
                collection: this.photos
            });
            
            this.next = new NextView({
                collection: this.photos
            });
        },
  
        render: function() {
            this.thumbnails.render();
            this.large.render();
            this.previous.render();
            this.next.render();
        }
    });

    new AppView().render();
});
```

*See it on [jsfiddle](http://jsfiddle.net/bywires/K33Aq/)*