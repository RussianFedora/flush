Name:			flush
Version:		0.9.10
Release:		7%{?dist}
Summary:		GTK-based BitTorrent client

License:		GPLv3+
Group:			Applications/Internet
URL:			http://%{name}.sourceforge.net/
Source0:		http://downloads.sourceforge.net/project/%{name}/%{name}/%{version}/%{name}-%{version}.tar.bz2
Source1:		%{name}.desktop
Patch0:			%{name}-dbus1.patch
Patch1:			%{name}-dbus2.patch
# https://sourceforge.net/tracker/?func=detail&aid=3231235&group_id=249175&atid=1127117
Patch2:			%{name}-0.9.10-64bit.patch

BuildRequires:		bison-devel
BuildRequires:		flex
BuildRequires:		glibmm24-devel >= 2.16
BuildRequires:		hicolor-icon-theme
BuildRequires:		expat-devel
BuildRequires:		libconfig-devel
BuildRequires:		rb_libtorrent-devel
BuildRequires:		libglademm24-devel
BuildRequires:		libnotify-devel
BuildRequires:		desktop-file-utils
BuildRequires:		libtorrent
BuildRequires:		dbus-c++-devel

Requires:		hicolor-icon-theme

%description
Flush - A GTK-based BitTorrent client. 

Features:
 * Controlling running instance by command line interface.
 * Running many instances with different configs from the same user.
 * Automatic copying finished downloads to specified directory.
 * Setting custom download path for each file of the torrent.
 * Ability to choose torrent file's character set encoding.
 * Automatic torrents loading from specified directory.
 * Automatic pausing and removing old torrents.
 * Temporary pausing and resuming torrents.
 * Overall and current session statistics.
 * Creating your own torrent files.
 * IP filter.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
autoreconf -ivf
%configure

make %{?_smp_mflags}

%install
rm -rf %{buildroot}

iconv -f koi8-r -t utf-8 man/ru/flush.1 > man/ru/flush.1.new
mv -f man/ru/flush.1.new man/ru/flush.1
make install DESTDIR=%{buildroot}
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE1}
rm -f %{buildroot}%{_datadir}/icons/hicolor/icon-theme.cache

install -dD -m 755 %{buildroot}%{_datadir}/pixmaps
install -m644 %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/flush.png \
	%{buildroot}%{_datadir}/pixmaps

%find_lang %{name}

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
	

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING
%{_bindir}/*
%{_datadir}/icons/*/*/apps/*
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/
%{_mandir}/man?/*
%{_mandir}/ru/man?/*



%changelog
* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-7
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> 0.9.10-5
- Rebuild for Boost 1.48

* Fri Sep 09 2011 Adam Jackson <ajax@redhat.com> 0.9.10-4
- Rebuild for boost 1.47

* Sun Apr 17 2011 Kalev Lember <kalev@smartlink.ee> - 0.9.10-3
- Rebuilt for boost 1.46.1 soname bump

* Mon Mar 21 2011 Dan Horák <dan[at]danny.cz> - 0.9.10-2
- fix build on non-x86 64-bit architectures

* Mon Feb 7 2011 Oksana Kurysheva <okurysheva@yahoo.com> - 0.9.10-1
- initial build for Fedora
