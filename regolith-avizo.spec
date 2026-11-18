Name:           regolith-avizo
Version:        0.1.5
Release:        1%{?dist}
Summary:        Notification daemon for the volume and brightness keys
License:        GPL-3.0-or-later
URL:            https://github.com/regolith-linux/avizo
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  vala
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gtk+-3.0) >= 3.22
# --pkg=GtkLayerShell-0.1 reads the GIR from gtk-layer-shell-devel
BuildRequires:  pkgconfig(gtk-layer-shell-0)
# avizo.gresource.xml preprocesses its images with to-pixdata
BuildRequires:  /usr/bin/gdk-pixbuf-pixdata

# volumectl runs pactl, which talks to PipeWire's pulse server
Requires:       pulseaudio-utils
Requires:       playerctl
# lightctl prefers brightnessctl, which changes the backlight through logind.
# Debian depends on light instead and makes it setuid in its postinst; this
# package has no scriptlets and doesn't touch light.
Requires:       brightnessctl

Provides:       avizo = %{version}-%{release}
Conflicts:      avizo

%description
Regolith's build of avizo, a simple notification daemon that shows volume
and brightness changes. It is mainly meant for the multimedia keys of a
Wayland session. Two helper scripts change the volume or the screen
brightness and show the notification.

%prep
%autosetup

%build
%meson
%meson_build

%install
%meson_install

%check
# The helper scripts are POSIX sh
for f in volumectl lightctl; do sh -n %{buildroot}%{_bindir}/$f; done

%files
%license LICENSE
%doc README.md
%{_bindir}/avizo-client
%{_bindir}/avizo-service
%{_bindir}/lightctl
%{_bindir}/volumectl
%dir %{_sysconfdir}/xdg/avizo
%config(noreplace) %{_sysconfdir}/xdg/avizo/config.ini

%changelog
* Wed Nov 18 2026 Regolith Fedora Port <port@regolith.invalid> - 0.1.5-1
- Initial package
