# Watchmaker postinstall

## Before
Make yourself root:
```bash
su
```
## Package sources
```bash
cat << 'EOF' | sudo tee /etc/apt/sources.list
deb http://ftp.pl.debian.org/debian/ buster main contrib non-free

deb http://security.debian.org/debian-security buster/updates main contrib non-free

deb http://ftp.pl.debian.org/debian/ buster-updates main contrib non-free

# Backports are recompiled packages from testing and unstable in a stable environment so that they will run without new libraries
# It is recommended to select single backported packages that fit your needs, and not use all available backports
# Use with care!
deb http://ftp.pl.debian.org/debian buster-backports main contrib non-free

# oldstable is a codename for the previous Debian stable repository, as long as security updates are provided
deb http://ftp.pl.debian.org/debian oldstable main contrib non-free

EOF
```

## Install Packages
```bash
apt update
apt install \
	git gitk gitg \
	vim nano mc gedit \
	bless meld \
	htop iotop dstat \
	libgtop2-dev \
	nmap net-tools network-manager traceroute rfkill \
	isolinux syslinux extlinux squashfs-tools grub2-common debootstrap \
	python python-pip python3 python3-pip \
	audacity audacious \
	numix-gtk-theme numix-icon-theme oxygencursors \
	dirmngr apt-transport-https gnupg \
	gimp vlc mplayer youtube-dl mpg123 \
	firmware-linux-nonfree firmware-iwlwifi firmware-linux firmware-linux-free firmware-misc-nonfree wireless-tools \
	sudo gksu seahorse bash-completion \
	openjdk-8-jdk maven \
	okular kid3 \
	ssh openssh-server openssl \
	baobab gnome-disk-utility gparted testdisk \
	bluez bluez-tools blueman \
	conky pavucontrol ydpdict adb \
	samba smbclient cups \
	aptitude build-essential p7zip-full tar zip gzip tree curl httpie \
	task-laptop task-desktop task-cinnamon-desktop live-task-cinnamon live-task-recommended \

apt install \
	acpid \
	adb \
	apt-transport-https \
	apt-utils \
	aptitude \
	audacious \
	audacity \
	baobab \
	base-files \
	bash-completion \
	binutils \
	bless \
	blueman \
	bluez \
	bluez-tools \
	bsdmainutils \
	bsdutils \
	build-essential \
	ca-certificates \
	conky \
	coreutils \
	cpio \
	cron \
	cups \
	curl \
	dash \
	dbus \
	debconf \
	debian-archive-keyring \
	debianutils \
	deborphan \
	diffutils \
	dirmngr \
	dkms \
	dmidecode \
	dmsetup \
	dosfstools \
	dstat \
	e2fslibs \
	e2fsprogs \
	extlinux \
	fatsort \
	findutils \
	firefox-esr \
	firefox-esr-l10n-en-gb \
	firefox-esr-l10n-pl \
	firmware-iwlwifi \
	firmware-linux \
	firmware-linux-free \
	firmware-linux-nonfree \
	firmware-misc-nonfree \
	gcc \
	gedit \
	gimp \
	git \
	gitk \
	gksu \
	gnome-disk-utility \
	gnupg \
	gnupg-agent \
	gnupg2 \
	gparted \
	gpgv \
	grep \
	grub2-common \
	grub-common \
	gzip \
	hostname \
	hplip \
	htop \
	httpie \
	ifupdown \
	inetutils-ping \
	init \
	init-system-helpers \
	initramfs-tools \
	initramfs-tools-core \
	iotop \
	iproute2 \
	iptables \
	ipython3 \
	isc-dhcp-client \
	isc-dhcp-common \
	isolinux \
	kid3 \
	klibc-utils \
	kmod \
	less \
	libreoffice-calc \
	libreoffice-writer \
	live-boot \
	live-config \
	live-task-base \
	live-task-localisation \
	live-task-localisation-desktop \
	llvm \
	make \
	maven \
	mawk \
	mc \
	meld \
	mpg123 \
	mplayer \
	multiarch-support \
	nano \
	ncurses-base \
	ncurses-bin \
	net-tools \
	netbase \
	network-manager \
	nmap \
	numix-gtk-theme \
	numix-icon-theme \
	okular \
	openjdk-8-jdk \
	openssh-client \
	openssh-server \
	oxygencursors \
	p7zip-full \
	parted \
	pavucontrol \
	pulseaudio-module-bluetooth \
	python \
	python3 \
	python3-pip \
	python3-virtualenv \
	qnapi \
	readline-common \
	rfkill \
	rsyslog \
	rsync \
	samba \
	seahorse \
	sed \
	sensible-utils \
	smbclient \
	software-properties-common \
	sqlitebrowser \
	squashfs-tools \
	ssh \
	sublime-text \
	sudo \
	syslinux \
	tar \
	task-english \
	task-laptop \
	tasksel \
	tasksel-data \
	tcpdump \
	tcpreplay \
	testdisk \
	time \
	traceroute \
	tree \
	tzdata \
	udev \
	util-linux \
	unzip \
	vim \
	vlc \
	wget \
	wireless-tools \
	xserver-xorg-core \
	xxd \
	xz-utils \
	ydpdict \
	youtube-dl \
	zip \

```

## Remove redundant packages
```bash
apt purge \
	firefox-esr-l10n-ach \
	firefox-esr-l10n-af \
	firefox-esr-l10n-all \
	firefox-esr-l10n-an \
	firefox-esr-l10n-ar \
	firefox-esr-l10n-as \
	firefox-esr-l10n-ast \
	firefox-esr-l10n-az \
	firefox-esr-l10n-bg \
	firefox-esr-l10n-bn-bd \
	firefox-esr-l10n-bn-in \
	firefox-esr-l10n-br \
	firefox-esr-l10n-bs \
	firefox-esr-l10n-ca \
	firefox-esr-l10n-cak \
	firefox-esr-l10n-cs \
	firefox-esr-l10n-cy \
	firefox-esr-l10n-da \
	firefox-esr-l10n-de \
	firefox-esr-l10n-dsb \
	firefox-esr-l10n-el \
	firefox-esr-l10n-en-za \
	firefox-esr-l10n-eo \
	firefox-esr-l10n-es-ar \
	firefox-esr-l10n-es-cl \
	firefox-esr-l10n-es-es \
	firefox-esr-l10n-es-mx \
	firefox-esr-l10n-et \
	firefox-esr-l10n-eu \
	firefox-esr-l10n-fa \
	firefox-esr-l10n-ff \
	firefox-esr-l10n-fi \
	firefox-esr-l10n-fr \
	firefox-esr-l10n-fy-nl \
	firefox-esr-l10n-ga-ie \
	firefox-esr-l10n-gd \
	firefox-esr-l10n-gl \
	firefox-esr-l10n-gn \
	firefox-esr-l10n-gu-in \
	firefox-esr-l10n-he \
	firefox-esr-l10n-hi-in \
	firefox-esr-l10n-hr \
	firefox-esr-l10n-hsb \
	firefox-esr-l10n-hu \
	firefox-esr-l10n-hy-am \
	firefox-esr-l10n-id \
	firefox-esr-l10n-is \
	firefox-esr-l10n-it \
	firefox-esr-l10n-ja \
	firefox-esr-l10n-ka \
	firefox-esr-l10n-kab \
	firefox-esr-l10n-kk \
	firefox-esr-l10n-km \
	firefox-esr-l10n-kn \
	firefox-esr-l10n-ko \
	firefox-esr-l10n-lij \
	firefox-esr-l10n-lt \
	firefox-esr-l10n-lv \
	firefox-esr-l10n-mai \
	firefox-esr-l10n-mk \
	firefox-esr-l10n-ml \
	firefox-esr-l10n-mr \
	firefox-esr-l10n-ms \
	firefox-esr-l10n-nb-no \
	firefox-esr-l10n-nl \
	firefox-esr-l10n-nn-no \
	firefox-esr-l10n-or \
	firefox-esr-l10n-pa-in \
	firefox-esr-l10n-pt-br \
	firefox-esr-l10n-pt-pt \
	firefox-esr-l10n-rm \
	firefox-esr-l10n-ro \
	firefox-esr-l10n-ru \
	firefox-esr-l10n-si \
	firefox-esr-l10n-sk \
	firefox-esr-l10n-sl \
	firefox-esr-l10n-son \
	firefox-esr-l10n-sq \
	firefox-esr-l10n-sr \
	firefox-esr-l10n-sv-se \
	firefox-esr-l10n-ta \
	firefox-esr-l10n-te \
	firefox-esr-l10n-th \
	firefox-esr-l10n-tr \
	firefox-esr-l10n-uk \
	firefox-esr-l10n-uz \
	firefox-esr-l10n-vi \
	firefox-esr-l10n-xh \
	firefox-esr-l10n-zh-cn \
	firefox-esr-l10n-zh-tw \
	libreoffice-help-ca \
	libreoffice-help-cs \
	libreoffice-help-da \
	libreoffice-help-de \
	libreoffice-help-dz \
	libreoffice-help-el \
	libreoffice-help-es \
	libreoffice-help-et \
	libreoffice-help-eu \
	libreoffice-help-fi \
	libreoffice-help-fr \
	libreoffice-help-gl \
	libreoffice-help-hi \
	libreoffice-help-hu \
	libreoffice-help-it \
	libreoffice-help-ja \
	libreoffice-help-km \
	libreoffice-help-ko \
	libreoffice-help-nl \
	libreoffice-help-om \
	libreoffice-help-pt \
	libreoffice-help-pt-br \
	libreoffice-help-ru \
	libreoffice-help-sk \
	libreoffice-help-sl \
	libreoffice-help-sv \
	libreoffice-help-tr \
	libreoffice-help-vi \
	libreoffice-help-zh-cn \
	libreoffice-help-zh-tw \
	libreoffice-l10n-af \
	libreoffice-l10n-am \
	libreoffice-l10n-ar \
	libreoffice-l10n-as \
	libreoffice-l10n-ast \
	libreoffice-l10n-be \
	libreoffice-l10n-bg \
	libreoffice-l10n-bn \
	libreoffice-l10n-br \
	libreoffice-l10n-bs \
	libreoffice-l10n-ca \
	libreoffice-l10n-cs \
	libreoffice-l10n-cy \
	libreoffice-l10n-da \
	libreoffice-l10n-de \
	libreoffice-l10n-dz \
	libreoffice-l10n-el \
	libreoffice-l10n-en-za \
	libreoffice-l10n-eo \
	libreoffice-l10n-es \
	libreoffice-l10n-et \
	libreoffice-l10n-eu \
	libreoffice-l10n-fa \
	libreoffice-l10n-fi \
	libreoffice-l10n-fr \
	libreoffice-l10n-ga \
	libreoffice-l10n-gd \
	libreoffice-l10n-gl \
	libreoffice-l10n-gu \
	libreoffice-l10n-gug \
	libreoffice-l10n-he \
	libreoffice-l10n-hi \
	libreoffice-l10n-hr \
	libreoffice-l10n-hu \
	libreoffice-l10n-id \
	libreoffice-l10n-in \
	libreoffice-l10n-is \
	libreoffice-l10n-it \
	libreoffice-l10n-ja \
	libreoffice-l10n-ka \
	libreoffice-l10n-kk \
	libreoffice-l10n-km \
	libreoffice-l10n-kmr \
	libreoffice-l10n-kn \
	libreoffice-l10n-ko \
	libreoffice-l10n-ku \
	libreoffice-l10n-lt \
	libreoffice-l10n-lv \
	libreoffice-l10n-mk \
	libreoffice-l10n-ml \
	libreoffice-l10n-mn \
	libreoffice-l10n-mr \
	libreoffice-l10n-nb \
	libreoffice-l10n-ne \
	libreoffice-l10n-nl \
	libreoffice-l10n-nn \
	libreoffice-l10n-nr \
	libreoffice-l10n-nso \
	libreoffice-l10n-oc \
	libreoffice-l10n-om \
	libreoffice-l10n-or \
	libreoffice-l10n-pa-in \
	libreoffice-l10n-pt \
	libreoffice-l10n-pt-br \
	libreoffice-l10n-ro \
	libreoffice-l10n-ru \
	libreoffice-l10n-rw \
	libreoffice-l10n-si \
	libreoffice-l10n-sk \
	libreoffice-l10n-sl \
	libreoffice-l10n-sr \
	libreoffice-l10n-ss \
	libreoffice-l10n-st \
	libreoffice-l10n-sv \
	libreoffice-l10n-ta \
	libreoffice-l10n-te \
	libreoffice-l10n-tg \
	libreoffice-l10n-th \
	libreoffice-l10n-tn \
	libreoffice-l10n-tr \
	libreoffice-l10n-ts \
	libreoffice-l10n-ug \
	libreoffice-l10n-uk \
	libreoffice-l10n-uz \
	libreoffice-l10n-ve \
	libreoffice-l10n-vi \
	libreoffice-l10n-xh \
	libreoffice-l10n-za \
	libreoffice-l10n-zh-cn \
	libreoffice-l10n-zh-tw \
	libreoffice-l10n-zu \
	aspell-am \
	aspell-ar \
	aspell-ar-large \
	aspell-bg \
	aspell-bn \
	aspell-br \
	aspell-ca \
	aspell-cs \
	aspell-cy \
	aspell-da \
	aspell-de \
	aspell-de-1901 \
	aspell-de-alt \
	aspell-doc \
	aspell-el \
	aspell-eo \
	aspell-eo-cx7 \
	aspell-es \
	aspell-et \
	aspell-eu \
	aspell-eu-es \
	aspell-fa \
	aspell-fo \
	aspell-fr \
	aspell-ga \
	aspell-gl-minimos \
	aspell-gu \
	aspell-he \
	aspell-hi \
	aspell-hr \
	aspell-hsb \
	aspell-hu \
	aspell-hy \
	aspell-is \
	aspell-it \
	aspell-kk \
	aspell-kn \
	aspell-ku \
	aspell-lt \
	aspell-lv \
	aspell-ml \
	aspell-mr \
	aspell-nl \
	aspell-no \
	aspell-or \
	aspell-pa \
	aspell-pt \
	aspell-pt-br \
	aspell-pt-pt \
	aspell-ro \
	aspell-ru \
	aspell-sk \
	aspell-sl \
	aspell-sv \
	aspell-ta \
	aspell-te \
	aspell-tl \
	aspell-uk \
	aspell-uz \
	task-albanian-desktop \
	task-amharic \
	task-amharic-desktop \
	task-arabic \
	task-arabic-desktop \
	task-asturian \
	task-asturian-desktop \
	task-basque \
	task-basque-desktop \
	task-belarusian \
	task-belarusian-desktop \
	task-bengali \
	task-bengali-desktop \
	task-bosnian \
	task-bosnian-desktop \
	task-brazilian-portuguese \
	task-brazilian-portuguese-desktop \
	task-british-desktop \
	task-bulgarian \
	task-bulgarian-desktop \
	task-catalan \
	task-catalan-desktop \
	task-chinese-s \
	task-chinese-s-desktop \
	task-chinese-t \
	task-chinese-t-desktop \
	task-croatian \
	task-croatian-desktop \
	task-cyrillic \
	task-cyrillic-desktop \
	task-czech \
	task-czech-desktop \
	task-danish \
	task-danish-desktop \
	task-dutch \
	task-dutch-desktop \
	task-dzongkha-desktop \
	task-esperanto \
	task-esperanto-desktop \
	task-estonian \
	task-estonian-desktop \
	task-finnish \
	task-finnish-desktop \
	task-french \
	task-french-desktop \
	task-galician \
	task-galician-desktop \
	task-georgian-desktop \
	task-german \
	task-german-desktop \
	task-greek \
	task-greek-desktop \
	task-gujarati \
	task-gujarati-desktop \
	task-hebrew \
	task-hebrew-desktop \
	task-hindi \
	task-hindi-desktop \
	task-hungarian \
	task-hungarian-desktop \
	task-icelandic \
	task-icelandic-desktop \
	task-indonesian-desktop \
	task-irish \
	task-irish-desktop \
	task-italian \
	task-italian-desktop \
	task-japanese \
	task-japanese-desktop \
	task-kazakh \
	task-kazakh-desktop \
	task-khmer \
	task-khmer-desktop \
	task-korean \
	task-korean-desktop \
	task-kurdish \
	task-kurdish-desktop \
	task-latvian \
	task-latvian-desktop \
	task-lithuanian \
	task-lithuanian-desktop \
	task-macedonian \
	task-macedonian-desktop \
	task-malayalam \
	task-malayalam-desktop \
	task-marathi \
	task-marathi-desktop \
	task-nepali-desktop \
	task-northern-sami \
	task-northern-sami-desktop \
	task-norwegian \
	task-norwegian-desktop \
	task-persian \
	task-persian-desktop \
	task-portuguese \
	task-portuguese-desktop \
	task-punjabi \
	task-punjabi-desktop \
	task-romanian \
	task-romanian-desktop \
	task-russian \
	task-russian-desktop \
	task-serbian \
	task-serbian-desktop \
	task-sinhala-desktop \
	task-slovak \
	task-slovak-desktop \
	task-slovenian \
	task-slovenian-desktop \
	task-south-african-english-desktop \
	task-spanish \
	task-spanish-desktop \
	task-swedish \
	task-swedish-desktop \
	task-tagalog \
	task-tamil \
	task-tamil-desktop \
	task-telugu \
	task-telugu-desktop \
	task-thai \
	task-thai-desktop \
	task-turkish \
	task-turkish-desktop \
	task-ukrainian \
	task-ukrainian-desktop \
	task-uyghur-desktop \
	task-vietnamese-desktop \
	task-welsh \
	task-welsh-desktop \
	task-xhosa-desktop \
	fonts-beng-extra \
	fonts-deva-extra \
	fonts-gujr-extra \
	fonts-guru-extra \
	fonts-lohit-knda \
	fonts-lohit-taml-classical \
	fonts-smc \
	fonts-telu-extra \
	apache2 \
	apache2-bin

apt autoremove
```

## Upgrade packages
```bash
apt upgrade
```

## visudo config
add lines after
`sudo visudo`:
```bash
user ALL=(ALL) NOPASSWD:ALL
%sudo  ALL=(ALL) NOPASSWD:ALL
```

## System settings
```bash
cat << 'EOF' | sudo tee /etc/hostname
watchmaker
EOF
```

```bash
cat << 'EOF' | sudo tee /etc/motd

Welcome to the machine...
EOF
```

## Set Passwords
```bash
passwd
passwd user
```

## Locales
Uncomment pl_PL.UTF-8 UTF-8, en_US.UTF-8 UTF-8 or:
```bash
cat << 'EOF' | sudo tee /etc/locale.gen
# This file lists locales that you wish to have built. You can find a list
# of valid supported locales at /usr/share/i18n/SUPPORTED, and you can add
# user defined locales to /usr/local/share/i18n/SUPPORTED. If you change
# this file, you need to rerun locale-gen.

# en_GB ISO-8859-1
# en_GB.ISO-8859-15 ISO-8859-15
# en_GB.UTF-8 UTF-8
# en_US ISO-8859-1
# en_US.ISO-8859-15 ISO-8859-15
en_US.UTF-8 UTF-8
# pl_PL ISO-8859-2
pl_PL.UTF-8 UTF-8
EOF

sudo /usr/sbin/locale-gen
```

## user bash profiles
execute as user:
```bash
cat << 'EOF' > ~/.bashrc
# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# If set, the pattern "**" used in a pathname expansion context will
# match all files and zero or more directories and subdirectories.
#shopt -s globstar

# make less more friendly for non-text input files, see lesspipe(1)
#[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color|*-256color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
#force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
    # We have color support; assume it's compliant with Ecma-48
    # (ISO/IEC-6429). (Lack of such support is extremely rare, and such
    # a case would tend to support setf rather than setaf.)
    color_prompt=yes
    else
    color_prompt=
    fi
fi

# if [ "$color_prompt" = yes ]; then
#    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
#else
#    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
#fi
unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    #alias dir='dir --color=auto'
    #alias vdir='vdir --color=auto'

    #alias grep='grep --color=auto'
    #alias fgrep='fgrep --color=auto'
    #alias egrep='egrep --color=auto'
fi

# colored GCC warnings and errors
#export GCC_COLORS='error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01'

# some more ls aliases
#alias ll='ls -l'
#alias la='ls -A'
#alias l='ls -CF'

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi

alias ls='ls --color=auto'
alias ll='ls -al --color=auto'
alias l='ls -CF --color=auto'
alias pax='ps ax | grep '

alias python3=python3.6

# colours
force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
    # We have color support; assume it's compliant with Ecma-48
    # (ISO/IEC-6429). (Lack of such support is extremely rare, and such
    # a case would tend to support setf rather than setaf.)
    color_prompt=yes
    else
    color_prompt=
    fi
fi

# [BOLD][BLUE]username[DIM]@host workdir[RESET][BOLD][BLUE]$[RESET]
PS1="\[\033[1;34m\]\u\[\033[2m\]@\h \W\[\033[0;1;34m\]\$\[\033[0m\] "

JAVA_HOME=/usr/lib/jvm/default-java
export JAVA_HOME

#export GREP_OPTIONS='--color=always'

# ~/bin
if [ -d $HOME/bin ]; then
    export PATH="$HOME/bin:$PATH"
fi
if [ -d /mnt/win/ext/opt/android/sdk/platform-tools ]; then
    export PATH="/mnt/win/ext/opt/android/sdk/platform-tools:$PATH"
fi

# locale
export LC_CTYPE="pl_PL.UTF-8"
export LC_NUMERIC="pl_PL.UTF-8"
export LC_TIME="pl_PL.UTF-8"
export LC_COLLATE="pl_PL.UTF-8"
export LC_MONETARY="pl_PL.UTF-8"
#export LC_MESSAGES="pl_PL.UTF-8"
export LC_PAPER="pl_PL.UTF-8"
export LC_NAME="pl_PL.UTF-8"
export LC_ADDRESS="pl_PL.UTF-8"
export LC_TELEPHONE="pl_PL.UTF-8"
export LC_MEASUREMENT="pl_PL.UTF-8"
export LC_IDENTIFICATION="pl_PL.UTF-8"
#export LC_ALL="pl_PL.UTF-8"
export LOCALE="pl_PL.UTF-8"

EOF

cat << 'EOF' > ~/.bash_profile
#
# ~/.bash_profile
#

[[ -f ~/.bashrc ]] && . ~/.bashrc

EOF

cat << 'EOF' > ~/.profile
# ~/.profile: executed by the command interpreter for login shells.
# This file is not read by bash(1), if ~/.bash_profile or ~/.bash_login
# exists.
# see /usr/share/doc/bash/examples/startup-files for examples.
# the files are located in the bash-doc package.

# the default umask is set in /etc/profile; for setting the umask
# for ssh logins, install and configure the libpam-umask package.
#umask 022

# if running bash
if [ -n "$BASH_VERSION" ]; then
    # include .bashrc if it exists
    if [ -f "$HOME/.bashrc" ]; then
    . "$HOME/.bashrc"
    fi
fi

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/bin" ] ; then
    PATH="$HOME/bin:$PATH"
fi
if [ -d "/mnt/win/ext/opt/android/sdk/platform-tools" ] ; then
    PATH="/mnt/win/ext/opt/android/sdk/platform-tools:$PATH"
fi

# locale
export LC_CTYPE="pl_PL.UTF-8"
export LC_NUMERIC="pl_PL.UTF-8"
export LC_TIME="pl_PL.UTF-8"
export LC_COLLATE="pl_PL.UTF-8"
export LC_MONETARY="pl_PL.UTF-8"
#export LC_MESSAGES="pl_PL.UTF-8"
export LC_PAPER="pl_PL.UTF-8"
export LC_NAME="pl_PL.UTF-8"
export LC_ADDRESS="pl_PL.UTF-8"
export LC_TELEPHONE="pl_PL.UTF-8"
export LC_MEASUREMENT="pl_PL.UTF-8"
export LC_IDENTIFICATION="pl_PL.UTF-8"
#export LC_ALL="pl_PL.UTF-8"
export LOCALE="pl_PL.UTF-8"

EOF
```

## root bash profiles
execute as root:
```bash
cat << 'EOF' | sudo tee /root/.bashrc
# ~/.bashrc: executed by bash(1) for non-login shells.

# Note: PS1 and umask are already set in /etc/profile. You should not
# need this unless you want different defaults for root.
# PS1='${debian_chroot:+($debian_chroot)}\h:\w\$ '
# umask 022

# You may uncomment the following lines if you want `ls' to be colorized:
# export LS_OPTIONS='--color=auto'
# eval "`dircolors`"
# alias ls='ls $LS_OPTIONS'
# alias ll='ls $LS_OPTIONS -l'
# alias l='ls $LS_OPTIONS -lA'
#
# Some more alias to avoid making mistakes:
# alias rm='rm -i'
# alias cp='cp -i'
# alias mv='mv -i'

alias ls='ls --color=auto'
alias ll='ls -al --color=auto'
alias l='ls -CF --color=auto'

force_color_prompt=yes

# [BOLD][RED]username[DIM]@host workdir[RESET][BOLD][RED]$[RESET]
PS1="\[\033[1;31m\]\u\[\033[2m\]@\h \W\[\033[0;1;31m\]#\[\033[0m\] "

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if ! shopt -oq posix; then
    if [ -f /usr/share/bash-completion/bash_completion ]; then
        . /usr/share/bash-completion/bash_completion
    elif [ -f /etc/bash_completion ]; then
        . /etc/bash_completion
    fi
fi


export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

EOF

cat << 'EOF' | sudo tee /root/.profile
# ~/.profile: executed by Bourne-compatible login shells.

if [ "$BASH" ]; then
  if [ -f ~/.bashrc ]; then
    . ~/.bashrc
  fi
fi

mesg n || true

alias ls='ls --color=auto'
alias ll='ls -al --color=auto'

force_color_prompt=yes

# [BOLD][RED]username[DIM]@host workdir[RESET][BOLD][RED]$[RESET]
PS1="\[\033[1;31m\]\u\[\033[2m\]@\h \W\[\033[0;1;31m\]#\[\033[0m\] "

EOF
```

## Packages apart from official repos
```bash
cd /tmp
```
### Sublime text
```bash
wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -
echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list
apt update
apt install sublime-text
```
### Spotify
Install No-ads deb
```bash
wget -O spotify.deb --no-check-certificate 'https://drive.google.com/uc?export=download&id=1Qi2vb0L4Vsf9R4Yy2-j3sR9ZdJqrNuEW'
sudo dpkg -i spotify.deb
```
### Google Chrome
```bash
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
apt update
apt install google-chrome-stable
```
### Teamviewer
```bash
wget https://download.teamviewer.com/download/linux/teamviewer_amd64.deb
sudo dpkg -i teamviewer_amd64.deb
```

## chrome config
Log in, sync, log out

## wine install
```bash
cd /tmp
dpkg --add-architecture i386
wget -nc https://dl.winehq.org/wine-builds/Release.key
apt-key add Release.key
echo "deb https://dl.winehq.org/wine-builds/debian/ buster main" | sudo tee /etc/apt/sources.list.d/wine.list
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 76F1A20FF987672F
apt update
apt install --install-recommends winehq-stable winetricks
```
as a normal user:
```bash
winetricks directplay
```

## enable sysrq magic key
```bash
# uncomment kernel.sysrq=1
cat /etc/sysctl.conf | sed -e "s/#\\? *kernel\\.sysrq=[01]/kernel.sysrq=1/" > /tmp/sysctl.conf
sudo mv /tmp/sysctl.conf /etc/sysctl.conf
sudo sysctl -p /etc/sysctl.conf
```

## cinnamon panels
Applets:
* Menu
* Panel launchers: nemo, sublime, google-chrome, terminal, ydpdict
* Window list
* Workspace switcher: 1,2
* Multi-Core System Monitor
* Sound with apps volume
* Calendar: Date format: %H:%M:%S, %a %d.%m.%y

## cinnamon themes
* Window borders: Numix
* Icons: Numix
* Controls: Numix
* Mouse Pointer: oxy-white
* Desktop: Mint-Y-Yltra-Dark
* Settings: show icons in menus, show icons in buttons, use a dark theme variant when available in certain applications

## nemo terminal here
Alt + T shortcut
```bash
mkdir -p ~/.gnome2/accels
cat << 'EOF' > ~/.gnome2/accels/nemo
(gtk_accel_path "<Actions>/DirViewActions/OpenInTerminal" "<Alt>t")
EOF
```

## ssh keys
Watchmaker SSH keys
```bash
mkdir -p ~/.ssh
ssh-keygen
```

## gitconfig
```bash
cat << 'EOF' > ~/.gitconfig
# This is Git's per-user configuration file.
[user]
# Please adapt and uncomment the following lines:
    name = watchmaker
    email = igrek51.dev@gmail.com


# GIT KURWA
[branch]
    autosetupmerge = true

[push]
    default = upstream
[rerere]
    enabled = true
[rebase]
    autosquash = true

[color]
    ui = auto
[color "branch"]
    current = yellow reverse
    local = yellow
    remote = green
[color "diff"]
    meta = yellow bold
    frag = magenta bold
    old = red bold
    new = green bold
[color "status"]
    added = yellow
    changed = green
    untracked = cyan

[alias]
    #LAZY VERSIONS OF BASIC COMMANDS

    co = checkout
    br = branch
    ci = commit
    st = status

    #BETTER VERSIONS OF BASIC COMMANDS

    purr = pull --rebase
    puff = pull --ff-only
    difff = diff --color-words #just words
    bbranch = branch -v
    branches = branch -avvl
    sth = stash -u
    unstage = reset HEAD --
    alias = !git config --list | grep 'alias\\.' | sed 's/alias\\.\\([^=]*\\)=\\(.*\\)/\\1 => \\2/' | grep -v 'alias'| awk 'BEGIN { FS = \"=>\" }{ printf(\"%-20s=>%s\\n\", $1,$2)}'|sort
    makegitrepo = !git init && git add . && git commit -m \"initial commit\"

    #BASIC HISTORY VIEWING

    hist = log --pretty=format:'%Cred%h%Creset %C(bold blue)<%an>%Creset%C(yellow)%d%Creset %Cgreen(%cr)%Creset%n%w(80,8,8)%s' --graph
    histfull = log --pretty=format:'%Cred%h%Creset %C(bold blue)<%an>%Creset%C(yellow)%d%Creset %Cgreen(%cr)%Creset%n%w(80,8,8)%s%n' --graph --name-status
    llog = log --pretty=format:'%C(yellow)%h %Cred%ad %Cblue%an%Cgreen%d %Creset%s' --date=iso
    changelog = log --pretty=format:'%Cgreen%d %Creset%s' --date=iso
    ls = log --pretty=format:'%C(yellow)%p..%h %C(white dim)%cd %<|(49,trunc)%an %C(reset)%s' --date=short --abbrev=8 --no-merges

    #BASIC REPO INFORMATION

    whois = "!sh -c 'git log -i -1 --pretty=\"format::%an <%ae>\n\" --author=\"$1\"' -"
    whatis = show -s --pretty='tformat::%h (%s, %ad)' --date=short
    howmany = "!sh -c 'git log -a --pretty=oneline | wc -l'"
    howmanybywhom = shortlog -sn

    #WHAT WAS GOING ON, WHILE YOU WERE AWAY

    anychanges = !sh -c 'git fetch' && git log --oneline HEAD..origin/$1
    anychangesonmaster = !sh -c 'git fetch' && git log --oneline HEAD..origin/master
    whoischanging = !sh -c 'git shortlog HEAD..origin/$0'
    whoischangingmaster = !sh -c 'git shortlog HEAD..origin/master'

    #what branches you have on origin, with info on who is guilty and how long ago. Useful for gitflow and feature branches in general. Requires fetch up-front.
    showorigin = "!sh -c 'for branch in `git branch -r | grep -v HEAD`;do echo `git show -s --format=\"%Cred%ci %C(green)%h %C(yellow)%cr %C(magenta)%an %C(blue)\" $branch | head -n 1` \\\t$branch; done | sort -r'"

    #get remote branches
    trackallbranches = !sh -c "for branchname in `git branch -r `; do git branch --track $branchname; done"
    updateallbranches = !sh -c "for branchname in `git branch -r `; do git checkout $branchname ; git pull; done"

    #TAGS

    showtags = show-ref --tags
    pushtags = push --tags
    tagwithdate = !sh -c 'git tag "$0"_$(date "+%y-%m-%d_%H-%M-%S")'
    lasttag = describe --abbrev=0 --tags
    checkoutlasttag = !sh -c 'git checkout `git describe --abbrev=0 --tags`'
    # Pushes given tag to remote 'origin' repo (or the remote passed as the second parameter)
    publishtag = "!sh -c 'git push ${2:-origin} $1' -"
    # Removes given tag from remote 'origin' repo (or the remote passed as the second parameter)
    unpublishtag = "!sh -c 'git push ${2:-origin} :refs/tags/$1' -"

    #IGNORING

    # fix .gitignore
    fixgitignore = !git rm -r --cached . && git add . && git commit -m \"Just a .gitignore fix \"

    # Ignore files only locally
    hide = update-index --assume-unchanged
    unhide = update-index --no-assume-unchanged

    #OTHER

    #Finds a filename in the git repository. Gives absolute location (from the git root).
    find = !sh -c 'git ls-tree -r --name-only HEAD | grep --color $1' - 

    #Deletes all branches that were safely merged into the master. All other are skipped (no worries).
    #on osx xargs does not have -r argument, so it fail. If you remove -r, it will run at least once, making this not safe operation
    cleanup = !git branch --merged=master | grep -Ev '^\\* | master$' | xargs -r git branch -d

    #Deletes orphaned remote branches (.git/refs/remotes/origin), clean up reflog and remove all untracked files
    cleanuplocal = !git remote prune origin && git gc && git clean -df

    # Check if any file in repo has whitespace errors
    # As described in http://peter.eisentraut.org/blog/2014/11/04/checking-whitespace-with-git/
    check-whitespace = !git diff-tree --check $(git hash-object -t tree /dev/null) HEAD

    # Check if any file in repo has windows line endings
    #Currently do not work as alias, works from comand line directly. There is a problem with \r
    #check-eol = grep -I --files-with-matches --cached $'\r' HEAD

    #Jira tickets (from: http://blogs.atlassian.com/2014/08/whats-new-git-2-1/)
    issues = "!f() { : git log ; echo 'Printing issue keys'; git log --oneline $@ | egrep -o [A-Z]+-[0-9]+ | sort | uniq; }; f"
    #version for git below 2.1
    #issues = !sh -c 'git log --oneline $@ | egrep -o [A-Z]+-[0-9]+ | sort | uniq' -

    # Gets the current branch name (not so useful in itself, but used in other aliases)
    branch-name = "!git rev-parse --abbrev-ref HEAD"
    # Pushes the current branch to the remote "origin" (or the remote passed as the parameter) and set it to track the upstream branch
    publish = "!sh -c 'git push -u ${1:-origin} $(git branch-name)' -"
    # Deletes the remote version of the current branch from the remote "origin" (or the remote passed as the parameter)
    unpublish = "!sh -c 'set -e; git push ${1:-origin} :$(git branch-name);git branch --unset-upstream $(git branch-name)' -"

    # Fetch PR from GitHub by number/id
    fetchpr = "!sh -c 'git fetch origin pull/$0/head:pr/$0'"

[apply]
    whitespace = nowarn
[core]
    pager = less -R
    editor = vim
#[help]
#    autocorrect = 1 #fucking magic!

#Kudos for (copied from):
#http://git-scm.com/book/en/Customizing-Git-Git-Configuration
#http://robots.thoughtbot.com/post/4747482956/streamline-your-git-workflow-with-aliases
#http://oli.jp/2012/git-powerup/#conclusion
#http://blog.blindgaenger.net/advanced_git_aliases.html
#https://gist.github.com/robmiller/6018582 (branch-name, publish, unpublish)

# GIT KURWA PL
[color]
    ui = auto
[color "branch"]
    current = yellow reverse
    local = yellow
    remote = green
[color "diff"]
    meta = yellow bold
    frag = magenta bold
    old = red bold
    new = green bold
[color "status"]
    added = yellow
    changed = green
    untracked = cyan

[alias]
    drzewokurwa = log --pretty=format:'%Cred%h%Creset %C(bold blue)<%an>%Creset%C(yellow)%d%Creset %Cgreen(%cr)%Creset%n%w(80,8,8)%s' --graph
    duzedrzewokurwa = log --pretty=format:'%Cred%h%Creset %C(bold blue)<%an>%Creset%C(yellow)%d%Creset %Cgreen(%cr)%Creset%n%w(80,8,8)%s%n' --graph --name-status
    komitykurwa = log --pretty=format:'%C(yellow)%h %Cred%ad %Cblue%an%Cgreen%d %Creset%s' --date=iso

    ktotokurwa = "!sh -c 'git log -i -1 --pretty=\"format::%an <%ae>\n\" --author=\"$1\"' -"
    cotokurwa = show -s --pretty='tformat::%h (%s, %ad)' --date=short

    cotamkurwa = !sh -c 'git fetch' && git log --oneline HEAD..origin/$1
    cotammistrzukurwa = !sh -c 'git fetch' && git log --oneline HEAD..origin/master
    ktotamkurwa = !sh -c 'git shortlog HEAD..origin/$0'
    ktotammistrzukurwa = !sh -c 'git shortlog HEAD..origin/master'

    tagikurwa = show-ref --tags
    pchajtagikurwa = push --tags
    tagujzdatakurwa = !sh -c 'git tag "$0"_$(date "+%y-%m-%d_%H-%M-%S")'

    pojebalosiekurwa = reset --hard

    ktonajebalkurwa = blame

    kurwa = status
    cokurwa = status
    cojestkurwa = diff
    howcanikurwa = help
    nabokkurwa = stash
    zbokukurwa = stash apply
    sprzatajkurwa = clean
    sprzatajwszystkokurwa = !sh -c 'git clean -x' && git reset --hard
    wyjebzrobionekurwa = !sh -c 'git branch --merged' | grep -v "\\*" | grep -v master | grep -v dev | xargs -n 1 git branch -d

    dodajkurwa = add
    takkurwa = commit
    sciagajkurwa = pull
    sciagajtegokurwa = !sh -c 'git pull origin $(git rev-parse --abbrev-ref HEAD)'
    dalejkurwa = push
    dalejnowociotokurwa = push -u origin master
    pchajkurwa = push
    pchajkurwayolo = push --force
    sorrykurwa = commit --amend -m

    cofnijwchuj = reset HEAD~100
    wypierdolwchuj = reset HEAD~100 --hard
    acomitamkurwa = push origin --force
    walictokurwa = rm .* -rF

    palisiekurwa = !sh -c 'git add . && git commit -m \"palilo sie\" && git push --force && echo \"Ok, now RUN!\"'

	lg = log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit --

[apply]
    whitespace = nowarn

[mergetool]
    keepBackup = false

[credential]
	helper = cache

EOF
```

## git repos
Linux-helpers, py-tools:
```bash
mkdir -p ~/live-dev
git clone https://igrek51@bitbucket.org/igrek51/linux-helpers.git ~/live-dev/linux-helpers
git clone https://github.com/igrek51/py-tools.git ~/live-dev/py-tools
```

## ydpdict db
```bash
sudo mkdir -p /usr/local/share/ydpdict/
sudo cp ~/live-dev/linux-helpers/ydpdict/usr-local-share-ydpdict/* /usr/local/share/ydpdict/
```

## tab bell disable
in file `/etc/inputrc`, uncomment:
```
set bell-style none
```

## cinnamon keyboard shortcuts
Disable Sound and Media Volume down/up shortcuts.
Add custom shortcuts:
* shutdown dialog: ```cinnamon-session-quit --power-off```, alt + shift + f4
* volumen up: ```/home/user/live-dev/py-tools/volumen/volumen.py up```, Audio raise volume
* volumen down: ```/home/user/live-dev/py-tools/volumen/volumen.py down```, Audio lower volume

## fstab
mount rwx options:
```bash
cat << 'EOF' | sudo tee /etc/fstab
proc /proc proc defaults 0 0
/dev/sda1 / ext4 errors=remount-ro 0 1
overlay / overlay rw 0 0
tmpfs /tmp tmpfs nosuid,nodev 0 0
/dev/disk/by-label/persistence /mnt/persistence auto nosuid,nodev,nofail,x-gvfs-show 0 0
/dev/disk/by-label/watchmodules /mnt/watchmodules auto rw,users,exec,nosuid,nodev,nofail,x-gvfs-show 0 0
EOF
```

## sublime config
* install package manager
* install git, brogrammer
* settings:
```bash
cat << 'EOF' > "$HOME/.config/sublime-text-3/Packages/User/Preferences.sublime-settings"
{
	"always_show_minimap_viewport": true,
	"auto_close_tags": false,
	"auto_match_enabled": false,
	"color_scheme": "Packages/Theme - Brogrammer/brogrammer.tmTheme",
	"draw_minimap_border": true,
	"fallback_encoding": "Windows 1250",
	"font_size": 12,
	"highlight_line": true,
	"highlight_modified_tabs": true,
	"hot_exit": true,
	"ignored_packages":
	[
		"Vintage"
	],
	"remember_full_screen": true,
	"scroll_past_end": false,
	"shift_tab_unindent": true,
	"show_encoding": true,
	"show_line_endings": true,
	"theme": "Brogrammer.sublime-theme",
	"update_check": false,
	"word_wrap": true
}
EOF
```
* Key bindings:
```bash
cat << 'EOF' > "$HOME/.config/sublime-text-3/Packages/User/Default (Linux).sublime-keymap"
[
    { "keys": ["ctrl+d"], "command": "duplicate_line" },
    { "keys": ["ctrl+shift+d"], "command": "find_under_expand" },
    { "keys": ["ctrl+t"], "command": "new_file" },
    { "keys": ["ctrl+o"], "command": "show_overlay", "args": {"overlay": "goto", "text": "@"} },
    { "keys": ["ctrl+l"], "command": "show_overlay", "args": {"overlay": "goto", "text": ":"} },
    { "keys": ["shift+enter"], "command": "run_macro_file", "args": {"file": "res://Packages/Default/Add Line.sublime-macro"} },
    { "keys": ["ctrl+shift+s"], "command": "save_all" },
    { "keys": ["tab"], "command": "insert", "args": {"characters": "\t"},
        "context":
        [
            { "key": "selection_empty", "operator": "equal", "operand": true, "match_all": true },
        ]
    },
]

EOF
```

## conky
```bash
cat << 'EOF' > ~/.conkyrc
-- vim: ts=4 sw=4 noet ai cindent syntax=lua
--[[
Conky, a system monitor, based on torsmo

Any original torsmo code is licensed under the BSD license

All code written since the fork of torsmo is licensed under the GPL

Please see COPYING for details

Copyright (c) 2004, Hannu Saransaari and Lauri Hakkarainen
Copyright (c) 2005-2012 Brenden Matthews, Philip Kovacs, et. al. (see AUTHORS)
All rights reserved.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
]]

conky.config = {
    alignment = 'top_left',
    background = false,
    border_width = 1,
    cpu_avg_samples = 2,
default_color = 'white',
    default_outline_color = 'white',
    default_shade_color = 'white',
    draw_borders = false,
    draw_graph_borders = true,
    draw_outline = false,
    draw_shades = false,
    use_xft = true,
    font = 'DejaVu Sans Mono:size=12',
    gap_x = 5,
    gap_y = 5,
    minimum_height = 5,
minimum_width = 5,
    net_avg_samples = 2,
    no_buffers = true,
    out_to_console = false,
    out_to_stderr = false,
    extra_newline = false,
    own_window = true,
    own_window_class = 'Conky',
    own_window_type = 'desktop',
    own_window_transparent = true,
    own_window_argb_visual = true,
    own_window_argb_value = 0,
    stippled_borders = 0,
    update_interval = 2.0,
    uppercase = false,
    use_spacer = 'none',
    show_graph_scale = false,
    show_graph_range = false,
double_buffer = true,
    short_units = true
}

conky.text = [[
Watchmaker ${execi 600 cat ~/.osversion}
${color grey}$color$sysname $kernel on $machine
${color grey}$nodename ${execi 3600 grep -q persistence /proc/cmdline && echo 'persistence' || echo 'live'}${execi 3600 grep -q toram /proc/cmdline && echo ' RAM'} - ${execi 3600 [ -d /sys/firmware/efi ] && echo 'UEFI' || echo 'BIOS'} boot
CPU $hr
${color grey}CPU Usage:$color $cpu% ${cpubar 4}
${color grey}Frequency:$color $freq MHz
${color grey}Load AVG (1m):$color ${loadavg 1}
${color grey}CPU temperature: $color${hwmon temp 1}°C
${color grey}CPU cores: $color${hwmon 1 temp 2}°C, ${hwmon 1 temp 3}°C, ${hwmon 1 temp 4}°C, ${hwmon 1 temp 5}°C
${color grey}ACPI temperatures: $color${hwmon 0 temp 1}°C, ${hwmon 0 temp 2}°C, ${hwmon 0 temp 3}°C
${cpugraph}
Memory $hr
${color grey}RAM Usage:$color $mem/$memmax - $memperc% ${membar 4}
${color grey}Free:$color $memfree
${color grey}Buffered:$color $buffers
${color grey}Cached:$color $cached
${color grey}Swap:$color $swap/$swapmax - $swapperc% ${swapbar 4}
${color grey}Dirty:$color ${exec grep -e Dirty: /proc/meminfo | sed -E 's/Dirty: +//g'}
${color grey}Writeback:$color ${exec grep -e Writeback: /proc/meminfo | sed -E 's/Writeback: +//g'}
Disk usage $hr
 ${color grey}/        $color${fs_used /}/${fs_size /} ${fs_bar 6 /}
 ${color grey}persistence $color${fs_used /mnt/persistence}/${fs_size /mnt/persistence} ${fs_bar 6 /mnt/persistence}
 ${color grey}watchmodules $color${fs_used /mnt/watchmodules}/${fs_size /mnt/watchmodules} ${fs_bar 6 /mnt/watchmodules}
Networking $hr
${color lightgrey}Ethernet:
${color grey}IP address: $color${addr enp3s0}
${color grey}Up: $color${upspeedf enp3s0} Kb/s $alignr${color grey}Down: $color${downspeedf enp3s0} Kb/s
${color lightgrey}Wi-Fi:
${color grey}IP address: $color${addr wlp2s0}
${color grey}Up: $color${upspeedf wlp2s0} Kb/s $alignr${color grey}Down: $color${downspeedf wlp2s0} Kb/s
$hr
${color grey}Time:$color ${time %H:%M:%S, %a %d.%m.%Y}
${color grey}Uptime:$color $uptime
$hr
${color grey}Processes:$color $processes  ${color grey}Running:$color $running_processes
${color grey}Name              PID   CPU%   MEM%
${color lightgrey} ${top name 1} ${top pid 1} ${top cpu 1} ${top mem 1}
${color lightgrey} ${top name 2} ${top pid 2} ${top cpu 2} ${top mem 2}
${color lightgrey} ${top name 3} ${top pid 3} ${top cpu 3} ${top mem 3}
${color lightgrey} ${top name 4} ${top pid 4} ${top cpu 4} ${top mem 4}
]]

EOF
```
Add to Cinnamon Startup applications:
```bash
conky -d -p 5
```

## Initializer service
```bash
cat << 'EOF' | sudo tee /etc/systemd/system/watchmaker-live-initializer.service
[Unit]
Description=Watchmaker live initializer running after fstab
Requires=local-fs.target
After=local-fs.target
RequiresMountsFor=/mnt/watchmodules

[Service]
Type=simple        
ExecStart=/bin/bash -c "/home/user/init.sh"

[Install]
WantedBy=multi-user.target

EOF

cat << 'EOF' | tee /home/user/init.sh
#!/bin/bash
#
# Watchmaker live initializer script
# launched from /etc/systemd/system/watchmaker-live-initializer.service
#

if [ -f "/mnt/watchmodules/init/init.sh" ]; then
	. "/mnt/watchmodules/init/init.sh"
fi
EOF

sudo chmod +x /etc/systemd/system/watchmaker-live-initializer.service
sudo systemctl daemon-reload
sudo systemctl enable watchmaker-live-initializer
sudo systemctl start watchmaker-live-initializer
```

# Update kernel
update vmlinuz, initrd.img on boot/live
```bash
update-initramfs -u
```

# Install hamachi, haguichi
```bash
cd /tmp
# hamachi
wget https://www.vpn.net/installers/logmein-hamachi_2.1.0.203-1_amd64.deb
sudo dpkg -i logmein-hamachi_2.1.0.203-1_amd64.deb
# haguichi
sudo sh -c 'echo "deb http://ppa.launchpad.net/webupd8team/haguichi/ubuntu bionic main" > /etc/apt/sources.list.d/haguichi.list'
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys C2518248EEA14886
sudo apt update
sudo apt install -y haguichi
```
disable in cinnamon startup applications

# Install docker, configure device mapper
```bash
cd /tmp
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/debian \
   $(lsb_release -cs) \
   stable"
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
sudo usermod -aG docker user

sudo systemctl stop docker
sudo systemctl disable docker
sudo rm -rf /var/lib/docker
```
Change `/lib/systemd/system/docker.service`:
Set `ExecStart=/usr/bin/dockerd --storage-driver=vfs -H fd://`

# Instal pip3 packages
```bash
pip3 install \
	requests \
	ipython \
	youtube-dl \
	cliglue

```

# Create .osversion
```bash
cat << 'EOF' | tee /home/user/.osversion
v2.21
EOF
```
