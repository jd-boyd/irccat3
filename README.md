# Intro

I liked the idea of last.fm's irccat (https://github.com/RJ/irccat), but
I didn't like the installation or setup and I continually had trouble with
it on low resource VPS services.

So, I decided to make my own in Python.  I found reference to a
program call irccat2, which doesn't really do the same thing as
irccat, so I called this one irccat3.

# Comparison to irccat

Aside, from being in a new language, this also leaves out the ability
to run external commands, as well as the ability to direct messages by
prefixing them with #channel or @private_nick at the beginning.  At
some point, I'd like to add the destination control, but I'm unlikely to
implement running external commands.  It seems that if you want that, use
a more full featured but like willie or hubot.

# Usage.

Install, then run with the following options:

```
usage: irccat3 [-h] [--verbosity VERBOSITY] [--irc-server IRC_SERVER]
               [--irc-port IRC_PORT] [--irc-channel IRC_CHANNEL]
               [--listen-interface LISTEN_INTERFACE]
               [--listen-port LISTEN_PORT]

optional arguments:
  -h, --help            show this help message and exit
  --verbosity VERBOSITY
                        increase output verbosity
  --irc-server IRC_SERVER
                        IRC server to connect to.
  --irc-port IRC_PORT   Port for irc server
  --irc-channel IRC_CHANNEL
                        IRC channel to publish to
  --listen-interface LISTEN_INTERFACE
                        network interface to listen on. Defaults to all of
                        them.
  --listen-port LISTEN_PORT
                        Port to listen on (default 12345)
```