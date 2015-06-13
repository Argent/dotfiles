## What's included, and how to customize?

# Synology Diskstation

## Access SFTP with root login

  1. ipkg update
  2. ipkg install openssh-sftp-server
  3. copy sshd_config to /etc/ssh/sshd_config


## Common problems after updating

### Paths

##### Most Diskstation updates will probably delete the root home directory and reset the root `~/.profile` as well as `/etc/profile`

Download them and put them back on the diskstation

  .profile -> /root  
  profile  -> /etc/profile
  
The import parts are to put `/opt/bin` and `/opt/sbin` back into the path. This is where most custom programs and **ipkg** stuff goes. You can use `vi` to manipulate the the files or if you previously installed nano you can call it with it's full path `/opt/bin/nano`.

### Filebot

##### If Filebot doesn't run properly, crashes with a file not found exception or displays the wrong version number, probably executable links to the wrong direktory.

Make sure filebot is linked to the version in the `@appstore` directory:

```bash
$ which filebot
/opt/bin/filebot

$ ls -la /opt/bin/filebot
lrwxrwxrwx    1 root     root            37 Jun 12 23:29 /opt/bin/filebot -> /volume1/@appstore/filebot/filebot.sh
```
If the link is wrong, fix it with:

```bash
$ rm /opt/bin/filebot
$ sudo ln -s /volume1/@appstore/filebot/filebot.sh /opt/bin/filebot
```


##### If Filebot is not able to recognize media data like aspect ratio, codecs, etc, probably it is not able to load the Mediainfo library.

Check with:

```bash
$ filebot -script fn:sysinfo
```

If MediaInfo is not found, download the files manually from [http://sourceforge.net/p/filebot/code/HEAD/tree/trunk/lib/native/linux-i686/](http://sourceforge.net/p/filebot/code/HEAD/tree/trunk/lib/native/linux-i686/) or from the filebot folder and put them into the `/volume1/@appstore/filebot/` without any subdirectories.


### NzbGet

##### After an update usually all custom scripts are gone from the NzbGet directory.

Download the script again and put in the the right directory:

```bash
$ cd /volume1/@appstore/nzbget/share/nzbget/scripts/nzbToMedia
$ wget https://raw.githubusercontent.com/Argent/dotfiles/master/nzbGet/nzbToFilebot.sh
```
