%define api 1.0
%define major 0
%define libname %mklibname %{name} %{major}
%define girname %mklibname %{name}-gir %{api}
%define develname %mklibname -d %{name}

Summary:	D-Bus interfaces for querying and manipulating user account information
Name:		accountsservice
Version:	0.6.43
Release:	1
Group:		System/Libraries
License:	GPLv3+
URL:		http://www.fedoraproject.org/wiki/Features/UserAccountDialog
Source0:	http://www.freedesktop.org/software/accountsservice/%{name}-%{version}.tar.xz
BuildRequires:	intltool
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk-doc)
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(polkit-agent-1)
BuildRequires:	pkgconfig(libsystemd)
Requires:	polkit
Requires:	shadow
Requires:	%{libname} = %{EVRD}

%description
The accountsservice project provides a set of D-Bus interfaces for
querying and manipulating user account information and an implementation
of these interfaces, based on the useradd, usermod and userdel commands.

%package -n %{libname}
Summary:	Client-side library to talk to accountservice
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n %{libname}
This package contains the shared library for %{name}.

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries

%description -n %{girname}
GObject Introspection interface description for %{name}.

%package -n %{develname}
Summary:	Development files for accountsservice-libs
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}

%description -n %{develname}
The accountsservice-devel package contains headers and other
files needed to build applications that use accountsservice-libs.

%prep
%setup -q
%apply_patches

%build
%configure \
    --disable-static \
    --enable-systemd \
    --enable-user-heuristics \
    --with-minimum-uid=1000 \
    --with-systemdsystemunitdir=%{_systemunitdir}

%make LIBS='-lgmodule-2.0'

%install
%makeinstall_std
%find_lang accounts-service

%files -f accounts-service.lang
%doc COPYING README AUTHORS
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.Accounts.conf
%{_libexecdir}/accounts-daemon
%{_datadir}/dbus-1/interfaces/org.freedesktop.Accounts.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.Accounts.User.xml
%{_datadir}/dbus-1/system-services/org.freedesktop.Accounts.service
%{_datadir}/polkit-1/actions/org.freedesktop.accounts.policy
%dir %{_localstatedir}/lib/AccountsService/
%dir %{_localstatedir}/lib/AccountsService/users
%dir %{_localstatedir}/lib/AccountsService/icons
%{_systemunitdir}/accounts-daemon.service

%files -n %{libname}
%{_libdir}/libaccountsservice.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/AccountsService-%{api}.typelib

%files -n %{develname}
%{_includedir}/accountsservice-%{api}
%{_libdir}/libaccountsservice.so
%{_libdir}/pkgconfig/accountsservice.pc
%{_datadir}/gir-1.0/AccountsService-%{api}.gir
%{_datadir}/gtk-doc/html/libaccountsservice/
