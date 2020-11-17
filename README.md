# Lapset Virtual Host Manager

**lapset-vhost-add** is little Python utility script to generate (and activate) a vhost for a development site on localhost

As a full-time web developer I find myself needing to start up a web application on my development machine (*localhost*). I have *apache2* and the latest *php* installed on it and many a time I need to create a *vhost* for the application I will be working with.

I used to use the Wamp *add_vhost.php* file on Windows, but since I dumped Windows more than 12 months ago, I have been doing this via the command line on my [Linux Mint](https://www.linuxmint.com).

Only recently I learnt a bit of Bash scripting and [Python](https://python.org) and I would wondered if it would be a cool idea to write a simple automation script for provisioning a vhost on an Ubuntu-based Apache2 development server.

This is for the fun of it and let's see how it all goes.

## Installation

```
$ cd ~/Downloads
$ git clone https://github.com/gmurambadoro/lapset-vhost-add.git
$ cd lapset-vhost-add
$ chmod +x main.py
$ ln -s main ~/.local/bin/lapset-vhost-add
```

## Usage

You can run this *lapset-vhost-add* script in one of two modes, namely:

* Interactive mode
* Command-line mode

### Interactive Mode

```
$ lapset-vhost-add --interactive
```

In this mode, you will be asked a series of questions about the vhost to be created.

### Command-Line Usage

In this mode you specify all the required parameters needed to create a vhost.

```
$ lapset-vhost-add domain --dir=/path/to/dir [--no-localhost] [--override] [--php-version=7.4]
```

Type in `$ lapset-vhost-add --help` for more usage documentation.
