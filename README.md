![TravisCI Status](https://travis-ci.org/jd-boyd/irccat3.png)
# IRCCat3

`netcat` stuff to IRC. 

IRCcat3 does one thing:

1) Listen on a specific ip:port and write incoming data to an IRC channel.
   This is useful for sending various announcements and log messages to irc.

IRCCat3 was inspired by irccat (https://github.com/RJ/irccat).  IRCcat
removes features I don't care about and requires fewer resources.  Also, 
I just don't have good luck with Java applications running in OpenVZ with
venet networking, common to many VPSs.

BTW, googling for irccat2 turned up a python example that isn't really
like irccat.

# Usage.

Install (`pip install irccat3`), then run with the following options:

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

Once it is running connected to the IRC server, send messages to IRC by:
```
echo "Something just happened" | nc -q0 somemachine 12345
```