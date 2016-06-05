%define api 1.0
%define major 0
%define libname %mklibname %{name} %{major}
%define girname %mklibname %{name}-gir %{api}
%define develname %mklibname -d %{name}

Summary:	D-Bus interfaces for querying and manipulating user account information
Name:		accountsservice
Version:	0.6.40
Release:	8
Group:		System/Libraries
License:	GPLv3+
URL:		http://www.fedoraproject.org/wiki/Features/UserAccountDialog
Source0:	http://www.freedesktop.org/software/accountsservice/%{name}-%{version}.tar.xz
Patch0:		accountsservice-0.6.37-filter-bin-true-login-shell-users-from-user-list.patch
# (tpg) patches from upstream git
Patch1:		0001-lib-add-language-to-SetLanguage-failure.patch
Patch2:		0002-daemon-remove-dead-code.patch
Patch3:		0003-lib-Copy-password-hint-instead-of-user-s-real-name.patch
Patch4:		0004-lib-clean-up-debug-message.patch
Patch5:		0005-accountsservice-Add-SetPasswordHint-function.patch
Patch6:		0006-lib-Use-G_PARAM_STATIC_STRINGS.patch
Patch7:		0007-lib-fix-misleading-debug-message.patch
Patch8:		0008-wtmp-fix-wtmp-file-on-solaris-and-netbsd.patch
Patch9:		0009-systemd-check-for-libsystemd-instead-of-libsystemd-l.patch
Patch10:	0010-Makefile-Move-to-AM_DISTCHECK_CONFIGURE_FLAGS.patch
Patch11:	0011-Allow-remote-inactive-users-to-change-their-own-data.patch
Patch12:	0012-systemd-disable-GVFS-support.patch
BuildRequires:	intltool
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gtk-doc)
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(polkit-agent-1)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	systemd
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
