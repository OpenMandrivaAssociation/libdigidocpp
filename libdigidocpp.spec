%define _disable_ld_no_undefined 1
%define _disable_lto 1

%define modname digidoc

%define major 1
%define libname %mklibname digidocpp %{major}
%define develname %mklibname digidocpp -d

Name:		libdigidocpp
Version:	3.14.5
Release:	1
Summary:	Library for creating and validating BDoc and DDoc containers

Group:		System/Libraries
License:	LGPLv2+
URL:		https://github.com/open-eid/libdigidocpp
Source:		https://github.com/open-eid/libdigidocpp/releases/download/v%{version}/libdigidocpp-%{version}.tar.gz

BuildRequires:	cmake
BuildRequires:  vim-common
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libp11)
BuildRequires:	pkgconfig(xml-security-c)
BuildRequires:	xsd-devel
Requires:	opensc

%description
libdigidocpp is a C++ library for reading, validating, and creating BDoc and
DDoc containers. These file formats are widespread in Estonia where they are
used for storing legally binding digital signatures.

%package	-n %{libname}
Group:		System/Libraries
Summary:	Library for creating and validating bdoc and ddoc containers
Requires:	%{name} >= %{version}-%{release}

%description	-n %libname
libdigidocpp is a C++ library for reading, validating, and creating BDoc and
DDoc containers. These file formats are widespread in Estonia where they are
used for storing legally binding digital signatures.

%package	-n %{develname}
Summary:	Development files for %{name}
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Requires:	pkgconfig(libp11)
Requires:	pkgconfig(openssl)
Requires:	pkgconfig(xml-security-c)
Requires:	xsd-devel
Provides:	%{name}-devel = %{version}-%{release}

%description	-n %{develname}
This package contains libraries and header files for
developing applications that use %{name}.

%package	-n perl-%{modname}
Summary:	Perl bindings for %{name}
Group:		Development/Perl
BuildRequires:	perl-devel
BuildRequires:	swig
Requires:	%{libname} = %{version}-%{release}

%description	-n perl-%{modname}
The perl-%{modname} package provides access to
%{name} features from Perl programs.

%package	-n python-%{modname}
Summary:	Python bindings for %{name}
Group:		Development/Python
BuildRequires:	python-devel
BuildRequires:	swig
Requires:	%{libname} = %{version}-%{release}

%description	-n python-%{modname}
The python-%{modname} package provides access to
%{name} features from Python programs.

%package	-n php-%{modname}
Summary:	PHP bindings for %{name}
Group:		Development/PHP
BuildRequires:	php-devel
BuildRequires:	swig
Requires:	%{libname} = %{version}-%{release}

%description	-n php-%{modname}
The php-%{modname} package provides access to
%{name} features from PHP programs.

%prep
%setup -q
%autopatch -p1

%build
%cmake
%make_build

%install
%make_install -C build
#mv %{buildroot}%{_sysconfdir}/php.d/digidoc.ini %{buildroot}%{_sysconfdir}/php.d/90_digidoc.ini


%post -n php-%{modname}
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun -n php-%{modname}
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%files
#{_sysconfdir}/digidocpp/certs
%{_sysconfdir}/digidocpp/schema
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/digidocpp/digidocpp.conf

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%{_includedir}/digidocpp/
%{_libdir}/pkgconfig/lib*.pc
%{_libdir}/*.so

%files -n perl-%{modname}
#{perl_vendorarch}/auto/digidoc.so
#{perl_vendorlib}/digidoc.pm

%files -n python-%{modname}
#{py_platsitedir}/*

%files -n php-%{modname}
%{_datadir}/php/*
%attr(0755,root,root) %{_libdir}/php/extensions/*
#config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/90_digidoc.ini

