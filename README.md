# Apache2 VHost Maker

This is a little Python utility script to generate (and activate) a vhost for a development site on localhost

As a full-time web developer I find myself needing to start up a web application on my development machine (*localhost*). I have *apache2* and the latest *php* installed on it and many a time I need to create a *vhost* for the application I will be working with.

I used to use the Wamp *add_vhost.php* file on Windows, but since I dumped Windows more than 12 months ago, I have been doing this via the command line on my [Linux Mint](https://www.linuxmint.com).

Only recently I learnt a bit of Bash scripting and [Python](https://python.org) and I would wondered if it would be a cool idea to write a simple automation script for provisioning a vhost on an Ubuntu-based apache2 development server.

This is for the fun of it and let's see how it all goes.

## Installation

```
$ cd ~/Downloads
$ git clone https://github.com/gmurambadoro/apache2-vhost-maker.git
$ cd apache2-vhost-maker
$ chmod +x vhost-activate.py
```

## Usage

```
$ ./vhost-activate.py domain --dir=/path/to/dir [--no-localhost] [--override]
```
