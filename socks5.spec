Summary:	Proxy server
Summary(pl):	Serwer Proxy 
Name:		socks5
Copyright:	Copyright (c) 1995,1996 NEC Corporation. Freely Distributable
Version:	1.0r10
Release:	1
Vendor:		Socks5 Team <socks5-comments@socks.nec.com>
Group:		Daemons
Group(pl):	Serwery
# The latest release version of socks5 is only available
# from http://www.socks.nec.com/
Source0:	%{name}-v%{version}.tar.gz
Source1:	socks5.init
Source2:	socks5.sysconfig
Source3:	socks5.sh
Source4:	socks5.csh
Patch0:		http://www.socks.nec.com/patch/socks5-v1.0r10.patch1.txt
Patch1:		http://www.socks.nec.com/patch/socks5-v1.0r10.patch2.txt
Patch2:		http://www.socks.nec.com/patch/socks5-v1.0r10.patch3.txt
Patch3:		http://www.socks.nec.com/patch/socks5-v1.0r10.patch4.txt
Patch4:		http://www.socks.nec.com/patch/socks5-v1.0r10.patch5.txt
# This is modified version of translator patch:	
# http://www.socks.nec.com/translator.html --misiek.
Patch5:		socks-trans-v1.3-PLD-patch.gz
Patch6:		socks5-v1.0r8.archie.diff
Patch7:		socks5-fhs.patch
Patch8:		socks5-DESTDIR.patch
Requires:	rc-scripts
URL:		http://www.socks.nec.com
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Allows hosts behind a firewall to gain full Internet access. Client
programs such as ping, traceroute, ftp, finger, whois, archie, and telnet
that use SOCKS 5.0. Also includes a dynamic link library and script that
allows you to "sockify" programs that don't normally use SOCKS.

%description -l pl
Pakiet pozwalaj±cy komputerom znajduj±cym siê za firewallem na
nieograniczony dostêp do Internetu. Programy takie jak ping, traceroute,
ftp, finger, whois, archie oraz telnet u¿ywaj±ce SOCKS 5.0. Zawiera tak¿e
bibliotekê dynamiczn± i skrypt pozwalaj±cy na "usockowanie" programów, które
normalnie nie u¿ywaj± SOCKS5.

%package server
Summary:	SOCKS 5.0 Server Daemon
Summary(pl):	SOCKS 5.0 Serwer
Group:		Daemons
Group(pl):	Serwery
Requires:	%{name} = %{version}

%description server
SOCKS 5.0 Server - program being run on a host that can communicate
directly to hosts behind the firewall as well as hosts on the Internet at
large. Includes multithreading support via linux threads.

%description -l pl
Serwer SOCKS 5.0 - program który uruchamia siê na serwerze mog±cym
komunikowaæ siê bezpo¶rednio z komputerami za firewallem tak samo jak z
komputerami w Internecie. Zawiera wsparcie dla wielow±tkowo¶ci.

%package devel
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
%setup  -q -T -b 0 -n %{name}-v%{version}
cd lib
%patch0 -p0
%patch2 -p0
%patch3 -p0
cd ../clients/ftp
%patch1 -p0
%patch4 -p0
cd ../..
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

%build
aclocal
autoconf
CFLAGS="$RPM_OPT_FLAGS -I../"
LDFLAGS="-s"
export CFLAGS LDFLAGS
%configure \
	--with-threads \
	--enable-ipv6 \
	--with-ident \
	--with-libconffile=%{_sysconfdir}/socks5/libsocks5.conf \
	--with-srvconffile=%{_sysconfdir}/socks5/socks5.conf \
	--with-srvpwdfile=%{_sysconfdir}/socks5/socks5.passwd \
	--with-srvpidfile=/var/run/socks5.pid \
	--with-srvidtfile=/tmp/.socks5.ident  \
#	--with-krb5=%{_prefix}/athena \
make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig,profile.d,rc.d/init.d,socks5}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/socks5
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/socks5
install %{SOURCE3} %{SOURCE4} $RPM_BUILD_ROOT/etc/profile.d

install examples/socks5.conf.gssapi $RPM_BUILD_ROOT%{_sysconfdir}/socks5/socks5.conf

echo "socks5 - - - - -" > $RPM_BUILD_ROOT%{_sysconfdir}/socks5/libsocks5.conf

touch $RPM_BUILD_ROOT%{_sysconfdir}/socks5/socks5.passwd

rm -f examples/README

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/*
gzip -9nf doc/socks.faq examples/* ChangeLog README.trans

chmod -R u+r $RPM_BUILD_ROOT

%preun -p /sbin/ldconfig
%post  -p /sbin/ldconfig

%post server
/sbin/chkconfig --add socks5
if [ -f /var/lock/subsys/socks5 ]; then
	%{_sysconfdir}/rc.d/init.d/socks5 restart >&2
fi

%preun server
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/socks5 ]; then
		/etc/rc.d/init.d/socks5 stop &>/dev/null
	fi
	/sbin/chkconfig --del socks5
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/socks.faq.gz

%attr(755,root,root) %{_sysconfdir}/profile.d/socks5.*

%attr(755,root,root) %{_libdir}/*.so
%attr(755,root,root) %{_bindir}/*

%dir %{_sysconfdir}/socks5
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/socks5/libsocks5.conf

%{_mandir}/man1/socks5_clients.*
%{_mandir}/man1/runsocks.*
%{_mandir}/man5/libsocks5.conf.*

%files server
%defattr(644,root,root,755)
%doc examples/* ChangeLog.gz README.trans.gz

%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/*

%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/socks5/socks5.conf
%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/socks5/socks5.passwd
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/*

%{_mandir}/man1/stopsocks.*
%{_mandir}/man1/socks5.*
%{_mandir}/man5/socks5.conf.*
%{_mandir}/man5/socks5.passwd.*

%files devel
%defattr(644,root,root,755)
%{_libdir}/libsocks5.a
%{_includedir}/socks.h
