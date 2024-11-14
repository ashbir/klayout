#
# spec file for package klayout
#
%global debug_package %{nil}

Name:           klayout
Version:        0.29.8
Release:        3%{?dist}
Summary:        KLayout, viewer and editor for mask layouts
License:        GPL-2.0+
Group:          Productivity/Scientific/Electronics
Url:            https://www.klayout.de
Source0:        https://www.klayout.de/downloads/%{name}-%{version}.tar.gz
# BuildRoot:      %{_tmppath}/%{name}-%{version}-build

# Disable auto-detection of dependencies (to prevent including the
# so's of klayout itself)
AutoReqProv: 	no

BuildRequires:  make
BuildRequires:  clang 
BuildRequires:  qt5-qtbase-devel 
BuildRequires:  qt5-qtmultimedia-devel 
BuildRequires:  qt5-qtxmlpatterns-devel 
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qttools-devel
BuildRequires:  ruby-devel
BuildRequires:  zlib-devel
BuildRequires:  python3-devel
%if 0%{?rhel} == 8 
BuildRequires:  libgit2_1.7-devel
%else
BuildRequires:  libgit2-devel
%endif
Requires: ruby 
Requires: python3
Requires: qt5-qtbase 
Requires: qt5-qtmultimedia 
Requires: qt5-qtxmlpatterns 
Requires: qt5-qtsvg 
Requires: qt5-qttools 
# NOTE: this package is required for libQt5Designer and pulls in a lot of devel stuff.
# Maybe it's worth considering to drop designer support and replace by QUiLoader.
Requires: qt5-qttools-devel 
# Needed by something else (still?)
Requires: http-parser 
%if 0%{?rhel} == 8 
Requires:  libgit2_1.7
%else
Requires:  libgit2
%endif

%description
Mask layout viewer and editor for the chip design engineer.

For details see README.md

%prep

%setup -q	

%build

TARGET="linux-release"

cd %{_builddir}/%{name}-%{version}
# clean bin dir
rm -rf %{_builddir}/bin.$TARGET

# do the actual build
./build.sh -rpath %{_libdir}/klayout \
           -bin %{_builddir}/bin.$TARGET \
           -build %{_builddir}/build.$TARGET

cp -p LICENSE Changelog CONTRIB %{_builddir}
strip %{_builddir}/bin.$TARGET/*.so
strip %{_builddir}/bin.$TARGET/*/*.so
strip %{_builddir}/bin.$TARGET/*/*/*.so
strip %{_builddir}/bin.$TARGET/klayout
strip %{_builddir}/bin.$TARGET/strm*

%install

TARGET="linux-release"

# create and populate libdir
mkdir -p %{buildroot}%{_libdir}/klayout
mkdir -p %{buildroot}%{_libdir}/klayout/db_plugins
mkdir -p %{buildroot}%{_libdir}/klayout/lay_plugins
mkdir -p %{buildroot}%{_libdir}/klayout/pymod
cp -pd %{_builddir}/bin.$TARGET/lib*.so* %{buildroot}%{_libdir}/klayout
cp -pd %{_builddir}/bin.$TARGET/db_plugins/lib*.so* %{buildroot}%{_libdir}/klayout/db_plugins
cp -pd %{_builddir}/bin.$TARGET/lay_plugins/lib*.so* %{buildroot}%{_libdir}/klayout/lay_plugins
cp -rpd %{_builddir}/bin.$TARGET/pymod/* %{buildroot}%{_libdir}/klayout/pymod
%if %{defined copylibs}
  cp -pd %{copylibs} %{buildroot}%{_libdir}/klayout
%endif
chmod 644 %{buildroot}%{_libdir}/klayout/*.so*
chmod 644 %{buildroot}%{_libdir}/klayout/db_plugins/*.so*
chmod 644 %{buildroot}%{_libdir}/klayout/lay_plugins/*.so*
find %{buildroot}%{_libdir}/klayout/pymod -type f -exec chmod 644 {} +
find %{buildroot}%{_libdir}/klayout/pymod -type d -exec chmod 755 {} +

# create and populate bindir
mkdir -p %{buildroot}%{_bindir}
cp -pd %{_builddir}/bin.$TARGET/klayout %{_builddir}/bin.$TARGET/strm* %{buildroot}%{_bindir}
chmod 755 %{buildroot}%{_bindir}/*

# other files
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/pixmaps
install -Dm644 %{_builddir}/%{name}-%{version}/etc/%{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
install -Dm644 %{_builddir}/%{name}-%{version}/etc/logo.png %{buildroot}%{_datadir}/pixmaps/%{name}.png


%files
%defattr(-,root,root)
%doc LICENSE
%doc Changelog
%doc CONTRIB
%{_bindir}/klayout
%{_bindir}/strm*
%{_libdir}/klayout/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png

%changelog
%autochangelog/*
