Summary:	Proxy server
Summary(pl.UTF-8):	Serwer Proxy
Name:		socks5
Version:	1.0r11
Release:	3
License:	non-commercial, not distributable
Vendor:		Socks5 Team <socks5-comments@socks.nec.com>
Group:		Networking/Daemons
# http://archive.socks.permeo.com/cgi-bin/download.pl (requires registration)
Source0:	%{name}-v%{version}.tar.gz
# NoSource0-md5: 4f4f3932bbb9a8d47a63502a6820c948
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Source3:	%{name}.sh
Source4:	%{name}.csh
NoSource:	0
Patch0:		http://www.socks.nec.com/patch/%{name}-v1.0r11.patch1.txt
# This is modified version of translator patch:
# http://archive.socks.permeo.com/60021888/socks-trans-v1.3-patch.gz
Patch1:		http://archive.socks.permeo.com/60021888/socks-trans-v1.3-patch.gz
NoPatch:	1
Patch2:		%{name}-v1.0r8.archie.diff
Patch3:		%{name}-fhs.patch
Patch4:		%{name}-DESTDIR.patch
Patch5:		%{name}-shared_libs.patch
Patch6:		%{name}-stdarg.patch
Patch7:		%{name}-nolibs.patch
URL:		http://www.socks.permeo.com/
BuildRequires:	autoconf >= 2.4
BuildRequires:	heimdal-devel
BuildRequires:	libident-devel
BuildRequires:	perl-base
Requires:	setup >= 2.4.6-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Allows hosts behind a firewall to gain full Internet access. Client
programs such as ping, traceroute, ftp, finger, whois, archie, and
telnet that use SOCKS 5.0. Also includes a dynamic link library and
script that allows you to "sockify" programs that don't normally use
SOCKS.

%description -l pl.UTF-8
Pakiet pozwalający komputerom znajdującym się za firewallem na
nieograniczony dostęp do Internetu. Programy takie jak ping,
traceroute, ftp, finger, whois, archie oraz telnet używające SOCKS
5.0. Zawiera także bibliotekę dynamiczną i skrypt pozwalający na
"usockowanie" programów, które normalnie nie używają SOCKS5.

%package server
Summary:	SOCKS 5.0 Server Daemon
Summary(pl.UTF-8):	Serwer SOCKS 5.0
Group:		Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts

%description server
SOCKS 5.0 Server - program being run on a host that can communicate
directly to hosts behind the firewall as well as hosts on the Internet
at large. Includes multithreading support via linux threads.

%description server -l pl.UTF-8
Serwer SOCKS 5.0 - program który uruchamia się na serwerze mogącym
komunikować się bezpośrednio z komputerami za firewallem tak samo jak
z komputerami w Internecie. Zawiera wsparcie dla wielowątkowości.

%package devel
Summary:	SOCKS 5.0 Development header file and libraries
Summary(pl.UTF-8):	SOCKS 5.0 - pliki nagłówkowe i biblioteki dla developerów
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
These are the libraries and header files required to develop for NWSL
(previously CSTC) version 5.0 of SOCKS.

%description devel -l pl.UTF-8
Pakiet zawierający biblioteki i pliki nagłówkowe dla developerów
korzystających z SOCKS w wersji 5.0.

%package static
Summary:	SOCKS 5.0 Static libraries
Summary(pl.UTF-8):	SOCKS 5.0 - biblioteki statyczne
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
These are the static libraries of NWSL (previously CSTC) version 5.0
of SOCKS.

%description static -l pl.UTF-8
Biblioteki statyczne NWSL (poprzednio CSTC) wersji 5.0 SOCKS.

%prep
%setup -q -n %{name}-v%{version}
cd include
%patch0 -p0
cd ..
# trans patch is for v1.0r10
%{__perl} -pi -e 's/Socks5 v1\.0r11/Socks5 v1.0r10/' include/defs.h
%{__perl} -pi -e 's/ranges from 1 to 255/ranges from 1 to 254/' lib/hostname.c
%patch1 -p0
%{__perl} -pi -e 's/Socks5 v1.0r10/Socks5 v1.0r11/' include/defs.h
%{__perl} -pi -e 's/ranges from 1 to 254/ranges from 1 to 255/' lib/hostname.c
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
# aclocal.m4 is local only, don't use aclocal
%{__autoconf}
CFLAGS="%{rpmcflags} -I.."
%configure \
	--with-threads \
	--enable-ipv6 \
	--with-ident \
	--with-krb5=/usr \
	--with-libconffile=%{_sysconfdir}/socks5/libsocks5.conf \
	--with-srvconffile=%{_sysconfdir}/socks5/socks5.conf \
	--with-srvpwdfile=%{_sysconfdir}/socks5/socks5.passwd \
	--with-srvpidfile=/var/run/socks5.pid \
	--with-srvidtfile=/tmp/.socks5.ident
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{sysconfig,shrc.d,rc.d/init.d},%{_sysconfdir}/socks5}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/socks5
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/socks5
install %{SOURCE3} %{SOURCE4} $RPM_BUILD_ROOT/etc/shrc.d

install examples/socks5.conf.gssapi $RPM_BUILD_ROOT%{_sysconfdir}/socks5/socks5.conf

echo "socks5 - - - - -" > $RPM_BUILD_ROOT%{_sysconfdir}/socks5/libsocks5.conf

touch $RPM_BUILD_ROOT%{_sysconfdir}/socks5/socks5.passwd

rm -f examples/README

chmod -R u+r $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post server
/sbin/chkconfig --add socks5
if [ -f /var/lock/subsys/socks5 ]; then
	/etc/rc.d/init.d/socks5 restart >&2
fi

%preun server
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/socks5 ]; then
		/etc/rc.d/init.d/socks5 stop &>/dev/null
	fi
	/sbin/chkconfig --del socks5
fi

%files
%defattr(644,root,root,755)
%doc doc/socks.faq
%attr(755,root,root) /etc/shrc.d/socks5.*
%attr(755,root,root) %{_libdir}/*.so
%attr(755,root,root) %{_bindir}/*
%dir %{_sysconfdir}/socks5
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/socks5/libsocks5.conf
%{_mandir}/man1/socks5_clients.*
%{_mandir}/man1/runsocks.*
%{_mandir}/man5/libsocks5.conf.*

%files server
%defattr(644,root,root,755)
%doc examples/* ChangeLog README.trans
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/socks5/socks5.conf
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/socks5/socks5.passwd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/*
%{_mandir}/man1/stopsocks.*
%{_mandir}/man1/socks5.*
%{_mandir}/man5/socks5.conf.*
%{_mandir}/man5/socks5.passwd.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/socks.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libsocks5.a
