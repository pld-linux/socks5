Summary:	Proxy server
Summary(pl):	Proxy serwer
Name:		socks5
Copyright:	Copyright (c) 1995,1996 NEC Corporation. Freely Distributable
Version:	1.0r8
Release:	2d
Vendor:		Socks5 Team <socks5-comments@socks.nec.com>
Group:		Networking
Group(pl):	Sieci
#########	ftp://ftp.fasta.fh-dortmund.de/pub/linux/
Source0:	%{name}-v%{version}.tar.gz
Source1:	socks5.init
Patch:		%{name}-v1.0r8.archie.diff
URL:		http://www.socks.nec.com/
Prereq:		/sbin/chkconfig
BuildRoot:	/tmp/%{name}-%{version}-root

%description
Allows hosts behind a firewall to gain full Internet access.

Client programs such as ping, traceroute, ftp, finger, whois, archie, and
telnet that use SOCKS 5.0.  Also includes a dynamic link library and script
that allows you to "sockify" programs that don't normally use SOCKS.

%description -l pl
Pakiet pozwalaj±cy komputerom znajduj±cym siê za firewallem
na nieograniczony dostêp do Internetu.

Programy takie jak ping, traceroute, ftp, finger, whois, archie oraz telnet
u¿ywaj±ce SOCKS 5.0. Zawiera tak¿e bibliotekê dynamiczn± i skrypt pozwalaj±cy
na "usockowanie" programów, które normalnie nie u¿ywaj± SOCKS5.

%package	server
Summary:	SOCKS 5.0 Server Daemon
Summary(pl):	SOCKS 5.0 Serwer
Group:		Networking/Daemons
Group(pl):	Sieci/Demony
Requires:	%{name} = %{version}

%description server
SOCKS 5.0 Server - program being run on a host that can communicate directly
to hosts behind the firewall as well as hosts on the Internet at large.
Includes multithreading support via linux threads.

%description -l pl
Serwer SOCKS 5.0 - program który uruchamia siê na serwerze mog±cym komunikowaæ
siê bezpo¶rednio z komputerami za firewallem tak samo jak z komputerami w
Internecie. Zawiera wsparcie dla wielow±tkowo¶ci.

%package	devel
Summary:	SOCKS 5.0 Development header file and libraries.
Summary(pl):	SOCKS 5.0 pliki nag³ówkowe i biblioteki dla developerów.
Group:		Development/Libraries
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
These are the libraries and header files required to develop for NWSL 
(previously CSTC) version 5.0 of SOCKS.

%description -l pl devel
Pakiet zawieraj±cy biblioteki i pliki nag³ówkowe dla developerów
korzystaj±cych z SOCKS w wersji 5.0.

%prep 
%setup -q -T -b 0 -n %{name}-v%{version}
%patch -p1

%build
autoconf
CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s" \
./configure %{_target} \
	--prefix=/usr \
	--with-threads \
	--with-krb5 \
	--with-ident \
	--with-libconffile=/etc/socks5/libsocks5.conf \
	--with-srvconffile=/etc/socks5/socks5.conf \
	--with-srvpwdfile=/etc/socks5/socks5.passwd \
	--with-srvpidfile=/var/run/socks5.pid \
	--with-srvidtfile=/tmp/.socks5.ident
make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{etc/{rc.d/init.d,socks5},usr/sbin}

make install prefix=$RPM_BUILD_ROOT/usr
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/socks5

install examples/socks5.conf.singlehomed $RPM_BUILD_ROOT/etc/socks5/socks5.conf
echo "socks5 - - - - -" > $RPM_BUILD_ROOT/etc/socks5/libsocks5.conf

touch $RPM_BUILD_ROOT/etc/socks5/socks5.passwd

rm -f examples/README

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/*
bzip2 -9 doc/socks.faq examples/* ChangeLog

cd $RPM_BUILD_ROOT/usr/bin
mv rarchie	s5archie
mv rfinger	s5finger
mv rftp		s5ftp
mv rping	s5ping
mv rtelnet	s5telnet
mv rtraceroute	s5traceroute
mv rwhois	s5whois
mv socks5	../sbin

chmod -R u+r $RPM_BUILD_ROOT

%preun -p /sbin/ldconfig
%post  -p /sbin/ldconfig

%post server
/sbin/chkconfig --add socks5
if test -r /var/run/socks5.pid; then
	/etc/rc.d/init.d/socks5 stop >&2
	/etc/rc.d/init.d/socks5 start >&2
fi

%preun server
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del socks5
	/etc/rc.d/init.d/socks5 stop >&2
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/socks.faq.bz2

%attr(755,root,root) /usr/lib/*.so

%attr(755,root,root) /usr/bin/stopsocks
%attr(755,root,root) /usr/bin/runsocks
%attr(755,root,root) /usr/bin/s5*

%dir /etc/socks5
%config(noreplace) %verify(not size mtime md5) /etc/socks5/libsocks5.conf

%{_mandir}/man1/socks5_clients.*
%{_mandir}/man1/runsocks.*
%{_mandir}/man5/libsocks5.conf.*

%files server
%defattr(644,root,root,755)
%doc examples ChangeLog.bz2

%attr(755,root,root) /usr/sbin/socks5
%attr(700,root,root) /etc/rc.d/init.d/socks5

%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/socks5/socks5.conf
%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) /etc/socks5/socks5.passwd

%{_mandir}/man1/stopsocks.*
%{_mandir}/man1/socks5.*
%{_mandir}/man5/socks5.conf.*
%{_mandir}/man5/socks5.passwd.*

%files devel
%defattr(644,root,root,755)
/usr/lib/libsocks5.a
/usr/include/socks.h

%changelog
* Sun Jan 24 1999 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [1.0r8-1d]
- fixed init-script,
- added Group(pl),
- fixed files permissions,
- macro %config(noreplace) %verify(not size mtime md5) in config files,
- minor changes.

* Tue Jan 19 1999 Arkadiusz Mi¶kiewicz <misiek@misiek.eu.org>
  [1.0r8-1d]
- PLD-ized.

* Thu Oct 8 1998 Scott Stone <sstone@turbolinux.com>
- Built for TL 3.0
- Fixed .spec file

* Wed Jul 22 1998 Daniel Deimert <d1dd@dtek.chalmers.se>
- Updated to 1.0r6

* Mon Jul 13 1998 Daniel Deimert <d1dd@dtek.chalmers.se>
- Added Patches for RedHat 5.1
