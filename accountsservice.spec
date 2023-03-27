%define api 1.0
%define major 0
%define libname %mklibname %{name}
%define girname %mklibname %{name}-gir %{api}
%define develname %mklibname -d %{name}

Summary:	D-Bus interfaces for querying and manipulating user account information
Name:		accountsservice
Version:	22.08.8
Release:	2
Group:		System/Libraries
License:	GPLv3+
URL:		http://www.fedoraproject.org/wiki/Features/UserAccountDialog
Source0:	http://www.freedesktop.org/software/accountsservice/%{name}-%{version}.tar.xz
# (crazy) use our defaults so all GUIs etc do the same.
# only drop if upstream implements something about these.
Patch10:	default-distro-groups.patch
BuildRequires:	intltool
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(polkit-agent-1)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	vala vala-tools
BuildRequires:	systemd-rpm-macros
BuildRequires:	meson
Requires:	polkit
Requires:	shadow
Requires:	%{libname} = %{EVRD}
%systemd_requires

%description
The accountsservice project provides a set of D-Bus interfaces for
querying and manipulating user account information and an implementation
of these interfaces, based on the useradd, usermod and userdel commands.

%package -n %{libname}
Summary:	Client-side library to talk to accountservice
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	%{mklibname %{name} %{major}} < %{EVRD}

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

%package vala
Summary:	Vala language bindings for %{name}
Group:		Development/Vala
Requires:	%{develname} = %{EVRD}

%description vala
Vala language bindings for %{name}

%prep
%autosetup -p1
%meson -Dsystemdsystemunitdir="%{_unitdir}" -Dminimum_uid=1000

%build
%meson_build

%install
%meson_install

mkdir -p %{buildroot}%{_datadir}/accountsservice/interfaces/

%find_lang accounts-service

%post
%systemd_post accounts-daemon.service

%preun
%systemd_preun accounts-daemon.service

%postun
%systemd_postun accounts-daemon.service

%files -f accounts-service.lang
%doc COPYING AUTHORS
%{_datadir}/dbus-1/system.d/org.freedesktop.Accounts.conf
%{_libexecdir}/accounts-daemon
%{_datadir}/dbus-1/interfaces/org.freedesktop.Accounts.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.Accounts.User.xml
%{_datadir}/dbus-1/system-services/org.freedesktop.Accounts.service
%{_datadir}/polkit-1/actions/org.freedesktop.accounts.policy
%{_datadir}/accountsservice
%dir %{_localstatedir}/lib/AccountsService/
%dir %{_localstatedir}/lib/AccountsService/users
%dir %{_localstatedir}/lib/AccountsService/icons
%{_unitdir}/accounts-daemon.service

%files -n %{libname}
%{_libdir}/libaccountsservice.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/AccountsService-%{api}.typelib

%files -n %{develname}
%{_includedir}/accountsservice-%{api}
%{_libdir}/libaccountsservice.so
%{_libdir}/pkgconfig/accountsservice.pc
%{_datadir}/gir-1.0/AccountsService-%{api}.gir

%files vala
%{_datadir}/vala/vapi/*
