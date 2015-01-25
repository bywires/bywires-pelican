Title: Remote PHPUnit execution using Intellij or PHPStorm
Date: 2015-01-25 18:00
Author: Bob McKee
Category: using-software
Tags: intellij, phpstorm, virtualbox, php, phpunit, vagrant, xdebug, vmware, nginx, php fpm, apache mod_php
Keywords: intellij, phpstorm, virtualbox, php, phpunit, vagrant, xdebug, vmware, nginx, php fpm, apache mod_php
Description: Step by step setup of remote PHPUnit execution using Intellij or PHPStorm with Xdebug support.  Nginx and PHP-FPM are used to support this integration.

Trying to get [Intellij](https://www.jetbrains.com/idea/) or [PHPStorm](https://www.jetbrains.com/phpstorm/) setup to remotely run [PHPUnit](https://phpunit.de/) with [Xdebug](http://xdebug.org/) can be a bit of a beast.  The tools used to run PHPUnit remotely seem to make the assumption that your web accessible directory is also where your tests and the rest of your code lives.  This assumption is often false and leads to problems when mapping local paths to remote paths.  Additionally, Intellij's configuration can be a bit daunting.  All of my notes below came after much trial and error.

## Prerequisites 

* Installed Intellij or PHPStorm
* Installed [PHP Remote Interpreter](https://plugins.jetbrains.com/plugin/7511?pr=phpStorm) Intellij plugin (may not be required with PHPStorm?)
* Remote host with web server with [PHP](Intellij or PHPStorm) and Xdebug support. [Nginx](http://nginx.org/en/) with [PHP-FPM](http://php-fpm.org/) are used in these examples, though the strategy should easily port to [Apache](http://httpd.apache.org/) with mod_php.
* PHPUnit installed on the same remote host.  PHPUnit can be installed globally or per-project using [Composer](https://getcomposer.org/).  My examples take the later approach.
* PHPUnit tests to run in your project

The following steps worked for me using Intellij IDEA 14.0.2.  My project files are in a directory mounted by the remote host.  Other means of deploying the files may be used but that may require you to vary from this setup.  Though personally I am just using a manually setup virtual machine running in [Virtualbox](https://www.virtualbox.org/), this is still applicable if you manage you virtual machine using [Vagrant](https://www.vagrantup.com/) other development environment manager.

## Overview

Here is the basic flow of the remote execution of PHPUnit tests triggered by Intellij and subsequent debugging of that request:

* User tells Intellij to listen for Xdebug connections
* User triggers a unit test run from Intellij
* Intellij deploys a file named *_intellij_phpunit_launcher.php* to the remote host at a path that is accessible via HTTP
* Intellij requests *_intellij_phpunit_launcher.php* over HTTP, passing along configuration in the query string
* *_intellij_phpunit_launcher.php* triggers your test code until a debugger breakpoint is hit (the first executed line of PHP may be the debugger breakpoint)
* XDebug determines where the debugger client is using the *$_SERVER['REMOTE_ADDR']* value from the web request and the configured *xdebug.remote_port* value (this is assuming you're using *xdebug.remote_connect_back*)
* Intellij, which is still listening for connection, recieves a request from Xdebug to initiate a debugging session
* As the user walks through code using the Intellij debugger client, Intellij sends commands to Xdebug using the [DBGp protocol](http://xdebug.org/docs-dbgp.php) (details on the communication and the roles of Intellij and Xdebug can be seen here - [Xdebug 2 Remote Debugging Communication Set-up](http://xdebug.org/docs/remote#communication))
* The user completes their debugging session
* Unit test results are returned as the body of the original HTTP request

## Xdebug

First, the easiest part - configuring Xdebug.  Remember, this is set on your remote host, not locally.  Setting up PHPUnit with Xdebug locally is possible, but done differently, and I won't be covering it here.

```ini
zend_extension=xdebug.so
xdebug.remote_enable=1
xdebug.remote_connect_back=1
xdebug.remote_port=9000
xdebug.remote_handler="dbgp"
xdebug.remote_autostart=1
xdebug.idekey="PHPSTORM"
```

The interesting options here are...

* *xdebug.remote_connect_back* - This tells Xdebug to connect to the host that initiated the HTTP request which   triggered Xdebug
* *xdebug.remote_port* - This is the port at which your IDE  will listen for Xdebug to initiate a session
* *xdebug.idekey* - Needs to match the key set in your IDE

More on [Xdebug settings](http://xdebug.org/docs/all_settings) can be found [here](http://xdebug.org/docs/all_settings).

## Nginx

The Nginx configuration isn't bad either, but requires some explanation.  Add this code as an Nginx *site* (Usually in the *sites-enabled* directory that the main *nginx.conf* file includes).  Remember this configuration is for access to your project for testing only.  You likely only want to use this configuration in your development environment and not in your production environment.

```nginx
server {
    listen 81;
    server_name foo;
    root /foo;        

    location = /_intellij_phpdebug_validator.php {
        fastcgi_pass unix:/var/run/php5-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }

    location = /_intellij_phpunit_launcher.php {
        set $args $args&load_mode=l&load_path=$document_root/vendor/autoload.php;
        fastcgi_pass unix:/var/run/php5-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param PHP_VALUE "display_errors=1\nhtml_errors=0";
        fastcgi_read_timeout 3600;
        include fastcgi_params;
    }
}
```

* Lets say your web accessible directory of you project is */foo/web*, served at port 80, so in this example your project root is just */foo*, served at port 81.
* *_intellij_phpdebug_validator.php* works similarly to how *_intellij_phpunit_launcher.php* but instead of returning unit test results its for supporting Intellij's "Validate remote evironment" feature, which checks for the existance of a php.ini file with Xdebug configured.
* For the *_intellij_phpunit_launcher.php* location block first we're adding some extra query parameters.  Setting *load_mode* to *l* and *load_path* to *vendor/autoload.php* causes PHPUnit to be loaded based on your composer autoloader configuration rather than just using a globally installed version.  There might be another way to do this, but I couldn't find it.
* Enabling display_errors will cause any error messages to show up in the Run output panel rather than failing silently.
* You may have configred Xdebug to override normal error output with HTML formatted out which in this context makes it completely unreadable, so disable it.
* Unit test execution will timeout after 30 seconds by default.  You'll easily exceed 30 seconds in most debugging sessions, so we set the timeout to an hour instead.

If you want to know exactly how Intellij is interacting with your web server check your Nginx access and error logs.  If you want to know what code its executing just comment out the *_intellij_phpunit_launcher.php* location block, restart nginx, and run your tests from Intellij (using the configuration I'll get to later).  The file will be served as a plain text file and show in your Run panel output.

## Intellij

### Interpreter configuration

* In your Intellij preferences go to Language & Frameworks > PHP > PHPUnit > Interpreter > "..."
* Enter in server settings and use the "Test connection..." button to verify your settings are correct

### Xdebug client configuration

* In your Intellij preferences go to Language & Frameworks > PHP > Debug
* In the Xdebug section enter port 9000 and check "Can accept external connections"

### Run configuration, deployment server, debug server

* In Intellij go to Run > Edit configurations... > "+" > PHPUnit on Server
* Name your configuration - I call mine "All tests"
* Set Test to "XML file"
* Check "User alternate configuration file" and select your phpunit.xml or phpunit.xml.dist file
* * Click Server > "..." > "+"
* Name your deployment server - Following my examples here I'd call mine "foo:81"
* Set Type to "Local or mounted folder" and set the Web server root URL to "http://foo:81"
* Click the Mappings tab
* Select the local project root path that is mounted to */foo* on the remote host
* Set Deployment path on server to "." and Web path on server to "/"
* Click OK
* Make sure your new server is selected on the Servers menu back on the Run/Debug configurations window
* Click the Remote tab > Debug server > "..." > "+"
* Set name to something like "foo:81", Host to "foo", Port to "81"
* Add a path mapping from your local project root to your remote project root
* Click Validate remote environment > Validate, validation should succeed and list some information about the configuration of the remote host.  If it fails the server configuration for *_intellij_phpdebug_validator.php* did not work, so check your web server logs to find out what went wrong.
* Close the Validate Remote Environment window
* Click OK

### Run it!

* In Intellij go to Run > Start Listening for PHP Debug Connections
* Run > Run... > "All tests"
* Accept the incoming connection
* Hit the play button on the Debug panel, as it likely is on the first line of the *_intellij_phpunit_launcher.php* file.  You might be able to add a mapping for the file, but it doesn't always work for me and I likely don't care about debugging from their anyways.

## Other resources

* [The definitive remote debug and unittest with PHPStorm guide: part 4](https://dutchweballiance.nl/techblog/the-definitive-remote-debug-and-unittest-with-phpstorm-guide-part-4/)
