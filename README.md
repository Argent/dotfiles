## What's included, and how to customize?

## Access SFTP with root login

  1. ipkg update
  2. ipkg install openssh-sftp-server
  3. copy sshd_config to /etc/ssh/sshd_config


## Common problems after updating

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

