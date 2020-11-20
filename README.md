# LAMPSET Virtual Host Manager

**lampset-vhost-add** is little Python utility script to generate (and activate) a vhost for a development site on localhost

As a full-time web developer I find myself needing to start up a web application on my development machine (*localhost*). I have *Apache2* and the latest *PHP* installed on it and many a time I need to create a *vhost* for the application I will be working with.

I used to use the Wamp *add_vhost.php* file on Windows, but since I dumped Windows more than 12 months ago, I have been doing this via the command line on my [Linux Mint](https://www.linuxmint.com).

Only recently I learnt a bit of Bash scripting and [Python](https://python.org) and I would wondered if it would be a cool idea to write a simple automation script for provisioning a vhost on an Ubuntu-based Apache2 development server.

This is for the fun of it and let's see how it all goes.

## Installation

```
$ cd ~/Downloads
$ git clone https://github.com/gmurambadoro/lampset-vhost-add.git
$ cd lampset-vhost-add
$ chmod +x lampset-vhost-add.py
$ sudo mv lampset.py /usr/local/bin/vhost-add
$ lampset-vhost-add --help
```

## Usage

You can run *lampset-vhost-add* script in one of two modes, namely:

* Interactive mode
* Command-line mode

#### 1. Interactive Mode

```
$ lampset-vhost-add --interactive
```

In this mode, you will be asked a series of questions about the vhost to be created.

#### 2. Command-Line Usage

In this mode you specify all the required parameters needed to create a vhost.

```
$ lampset-vhost-add domain --dir=/path/to/dir [--no-localhost] [--override] [--php-version=7.4]
```

Type in `$ lampset-vhost-add --help` for more usage documentation.

