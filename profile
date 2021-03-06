#/etc/profile: system-wide .profile file for ash.

umask 022

PATH=/opt/bin:/opt/sbin:/sbin:/bin:/usr/sbin:/usr/bin:/usr/syno/sbin:/usr/syno/bin:/usr/local/sbin:/usr/local/bin
export PATH

#This fixes the backspace when telnetting in.
#if [ "$TERM" != "linux" ]; then
#        stty erase
#fi
PGDATA=/var/services/pgsql
export PGDATA

TERMINFO=/usr/share/terminfo
export TERMINFO

TERM=${TERM:-cons25}
export TERM

PAGER=more
export PAGER

export LC_ALL=en_US.utf8
export LANG=en_US.utf8

PS1="`hostname`> "

alias dir="ls -al"
alias ll="ls -la"

ulimit -c unlimited
PATH=$PATH:/var/packages/JavaManager/target/Java/bin # Synology Java Manager Package
PATH=$PATH:/var/packages/JavaManager/target/Java/jre/bin # Synology Java Manager Package
JAVA_HOME=/var/packages/JavaManager/target/Java/jre # Synology Java Manager Package
CLASSPATH=.:/var/packages/JavaManager/target/Java/jre/lib # Synology Java Manager Package
LANG=en_US.utf8 # Synology Java Manager Package
export CLASSPATH PATH JAVA_HOME LANG # Synology Java Manager Package
