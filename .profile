if [ "$ZSH_VERSION" = "" ] && which zsh >/dev/null 2>&1 ; then 
    case $- in
        # only for interactive shells
        # (just to be safe but not really needed)
        *i*)
            echo >&2 "exec'ing zsh"
            exec zsh --login
            ;;
    esac
fi

umask 022

PATH=$PATH:/sbin:/bin:/usr/sbin:/usr/bin:/usr/syno/sbin:/usr/syno/bin:/usr/local/sbin:/usr/local/bin
export PATH

#This fixes the backspace when telnetting in.
#if [ "$TERM" != "linux" ]; then
#        stty erase
#fi

HOME=/root
export HOME

TERM=${TERM:-cons25}
export TERM

PAGER=more
export PAGER

PS1="`hostname`> "

alias dir="ls -al"
alias ll="ls -la"
PATH=$PATH:/var/packages/JavaManager/target/Java/bin # Synology Java Manager Package
PATH=$PATH:/var/packages/JavaManager/target/Java/jre/bin # Synology Java Manager Package
PATH=$PATH://volume1/@appstore/compressionutils/utils/bin # Compression Utils (par2, unzip, unrar, ... )
export PATH # Synology Java Manager Package
