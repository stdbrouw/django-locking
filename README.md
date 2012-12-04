=======================================
Concurrency control with django-locking
=======================================

Django has seen great adoption in the content management sphere, especially among the newspaper crowd. One of the trickier things to get right, is to make sure that nobody steps on each others toes while editing and modifying existing content. Newspaper editors might not always be aware of what other editors are up to, and this goes double for distributed teams. When different people work on the same content, the one who saves last will win the day, while the other edits are overwritten.

`django-locking` provides a system that makes concurrent editing impossible, and informs users of what other users are working on and for how long that content will remain locked. Users can still read locked content, but cannot modify or save it.

``django-locking`` makes sure no two users can edit the same content at the same time, preventing annoying overwrites and lost time. Find the repository and download the code at http://github.com/RobCombs/django-locking

``django-locking`` has only been tested on Django 1.2 and 1.3, but probably works from 1.0 onwards.

Documentation
-------------
Originally forked from the Django Locking plugin at stdbrouw/django-locking, this code is now the new authoritative repository per Stijn Debrouwere the original author of django-locking.
This code features the cream of the crop for django-locking combining features from over 4 repos!

New features added to this fork
===============================
Changes on change list pages
----------------------------
    
Unlock content object from change list page by simply clicking on the lock icon
_______________________________________________________________________________

![unlock prompt](https://github.com/RobCombs/django-locking/raw/master/docs/screenshots/unlock_prompt.png)

Hover over the lock icon to see when the lock expires
_____________________________________________________

![expire status](https://github.com/RobCombs/django-locking/raw/master/docs/screenshots/expire_status.png)

Hover over the username by the lock icon to see the full name of the person who has locked the content object 
_____________________________________________________________________________________________________________

![lock_by_who](https://github.com/RobCombs/django-locking/raw/master/docs/screenshots/lock_by_who.png)


Consolidated username and lock icon into one column on change list page
Changes in settings:
----------------------------

Added Lock warning and expiration flags in terms of seconds

Lock messages:
----------------------------

Added options to reload or save the object when lock expiration message is shown

![reload or bust](https://github.com/RobCombs/django-locking/raw/master/docs/screenshots/reload_or_bust.png)

Improved look and feel for the lock messages
Lock messages fade in and out seamlessly
Added much more detail to let users know who the content object was locked by providing the username, first name and last name
Added lock expiration warnings
Shows how much longer the object is locked for in minutes

Locking:
----------------------------

 Added hard locking support using Django's validation framework

![hard lock](https://github.com/RobCombs/django-locking/raw/master/docs/screenshots/hard_lock.png)

 Set hard and soft locking as the default to ensure the integrity of locking
 Added seamless unlocking when lock expires

![auto unlock](https://github.com/RobCombs/django-locking/raw/master/docs/screenshots/auto_unlock.png)


Architecture:
----------------------------

1 model tracks lock information and that's it!  No messy migrations for each model that needs locking.
Refactored and cleaned up code for easier maintainability
 Simplified installation by coupling common functionality into base admin/form/model classes


10 Minute Install
-----------------

1) Get the code:

    git clone git@github.com:RobCombs/django-locking.git

2) Install the django-locking python egg:
    
    cd django-locking
    sudo python setup.py install

3) Add locking to the list of INSTALLED_APPS in project settings file:

    INSTALLED_APPS = ('locking',)
    
4) Add the following url mapping to your urls.py file:

    urlpatterns = patterns('',
    (r'^admin/ajax/', include('locking.urls')),
    )

5) Add locking to the admin files that you want locking for:

    from locking.admin import LockableAdmin
    class YourAdmin(LockableAdmin):
       list_display = ('get_lock_for_admin')

6) Add warning and expiration time outs to your Django settings file:

    LOCKING = {'time_until_expiration': 120, 'time_until_warning': 60}


7) Build the Lock table in the database:

    django-admin.py/manage.py migrate locking (For south users. Recommended approach) OR
    django-admin.py/manage.py syncdb (For non south users)

8) Install django-locking media:

    cp -r django-locking/locking/media/locking $your static media directory

Note: This is the step where people usually get lost.  
Just start up your django server and look for the 200/304s http responses when the server attempts to load the media 
as you navigate to a model change list/view page where you've enabled django-locking. If you see 404s, you put the media in the wrong directory! 

You should see something like this in the django server console:

[02/May/2012 15:33:20] "GET /media/static/locking/css/locking.css HTTP/1.1" 304 0

[02/May/2012 15:33:20] "GET /media/static/web/common/javascript/jquery-1.4.4.min.js HTTP/1.1" 304 0

[02/May/2012 15:33:20] "GET /media/static/locking/js/jquery.url.packed.js HTTP/1.1" 304 0

[02/May/2012 15:33:21] "GET /admin/ajax/variables.js HTTP/1.1" 200 114

[02/May/2012 15:33:21] "GET /media/static/locking/js/admin.locking.js?v=1 HTTP/1.1" 304 0

[02/May/2012 15:33:21] "GET /admin/ajax/redirects/medleyobjectredirect/14/is_locked/?_=1335987201245 HTTP/1.1" 200 0

[02/May/2012 15:33:21] "GET /admin/ajax/redirects/medleyobjectredirect/14/lock/?_=1335987201295 HTTP/1.1" 200 0


You can also hit the media directly for troubleshooting your django-locking media installation: 
http://www.local.wsbradio.com:8000/media/static/locking/js/admin.locking.js
If the url resolves, then you've completed this step correctly!  
Basically, the code refers to the media like so.  That's why you needed to do this step.

    class Media:
    js = ( 'http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js', 
         'static/locking/js/jquery.url.packed.js',
         "/admin/ajax/variables.js",
         "static/locking/js/admin.locking.js?v=1")
    css = {"all": ("static/locking/css/locking.css",)
    }

That's it!

Checking the installation
-------------------------
Simulate a lock situation -> Open 2 browsers and hit your admin site with one user logged into the 1st browser and
other user logged into the other.  Go to the model in the admin that you've installed locking for with one browser.  
On the other browser, go to the change list/change view pages of the model that you've installed django-locking for.
You'll see locks in the interface similar to the screen shots above.

You can also look at your server console and you'll see the client making ajax calls to the django server checking for locks like so:

    [04/May/2012 15:15:09] "GET /admin/ajax/redirects/medleyobjectredirect/14/is_locked/?_=1336158909826 HTTP/1.1" 200 0
    [04/May/2012 15:15:09] "GET /admin/ajax/redirects/medleyobjectredirect/14/lock/?_=1336158909858 HTTP/1.1" 200 0

Optional
--------
If you'd like to enforce hard locking(locking at the database level), then add the LockingForm class to the same admin pages

Example:

    from locking.forms import LockingForm
    class YourAdmin(LockableAdmin):
     list_display = ('get_lock_for_admin')
     form = LockingForm
     
Note: if you have an existing form and clean method, then call super to invoke the LockingForm's clean method

Example:

    from locking.forms import LockingForm
    class YourFormForm(LockingForm):
      def clean(self):
        self.cleaned_data = super(MedleyRedirectForm, self).clean()
        ...some code
        return self.cleaned_data

CREDIT
------
This code is basically a composition of the following repos with a taste of detailed descretion from me. Credit goes out to the following authors and repos for their contributions
and my job for funding this project:
https://github.com/stdbrouw/django-locking
https://github.com/runekaagaard/django-locking
https://github.com/theatlantic/django-locking
https://github.com/ortsed/django-locking