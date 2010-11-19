%define version 0.3.0
%define rel 2
%define release %mkrel %rel
%define name libdigidocpp
%define modname digidoc

%define major 0
%define libname %mklibname digidocpp %major
%define develname %mklibname digidocpp -d

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Library for creating and validating BDoc and DDoc containers

Group:		System/Libraries
License:	LGPLv2+
URL:		http://code.google.com/p/esteid
Source:		http://esteid.googlecode.com/files/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	cmake
BuildRequires:	libdigidoc-devel
BuildRequires:	libp11-devel
BuildRequires:	openssl-devel
BuildRequires:	xml-security-c-devel
BuildRequires:	xsd-devel
Requires:	opensc

%description
libdigidocpp is a C++ library for reading, validating, and creating BDoc and
DDoc containers. These file formats are widespread in Estonia where they are
used for storing legally binding digital signatures.


%package	-n %libname
Group:		System/Libraries
Summary:	Library for creating and validating bdoc and ddoc containers
Requires:	%{name} >= %{version}-%{release}

%description	-n %libname
libdigidocpp is a C++ library for reading, validating, and creating BDoc and
DDoc containers. These file formats are widespread in Estonia where they are
used for storing legally binding digital signatures.

%package	-n %develname
Summary:	Development files for %{name}
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Requires:	libdigidoc-devel
Requires:	libp11-devel
Requires:	openssl-devel
Requires:	xml-security-c-devel
Requires:	xsd-devel
Provides:	%{name}-devel = %{version}-%{release}

%description	-n %develname
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

%build
%cmake
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std -C build
mv $RPM_BUILD_ROOT/etc/php.d/digidoc.ini $RPM_BUILD_ROOT/etc/php.d/90_digidoc.ini


%clean
rm -rf $RPM_BUILD_ROOT


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
%defattr(-,root,root,-)
%{_sysconfdir}/digidocpp/
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/digidocpp/digidocpp.conf


%files -n %libname
%defattr(-,root,root,-)
%doc AUTHORS COPYING NEWS README
%{_libdir}/*.so.*


%files -n %develname
%defattr(-,root,root,-)
%{_includedir}/digidocpp/
%{_libdir}/pkgconfig/lib*.pc
%{_libdir}/*.so


%files -n perl-%{modname}
%defattr(-,root,root,-)
%{perl_vendorarch}/auto/digidoc.so
%{perl_vendorlib}/digidoc.pm


%files -n python-%{modname}
%defattr(-,root,root,-)
%{py_platsitedir}/*


%files -n php-%{modname}
%defattr(-,root,root)
%{_datadir}/php/*
%attr(0755,root,root) %{_libdir}/php/extensions/*
%config(noreplace) %attr(0644,root,root) %{_sysconfdir}/php.d/90_digidoc.ini


