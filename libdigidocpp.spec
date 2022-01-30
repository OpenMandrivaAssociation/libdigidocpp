%define _disable_ld_no_undefined 1
%define _disable_lto 1

%define modname digidoc

%define major 1
%define libname %mklibname digidocpp %{major}
%define develname %mklibname digidocpp -d

Name:		libdigidocpp
Version:	3.14.7
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
BuildRequires:  pkgconfig(xalan-c)
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

%prep
%setup -q
%autopatch -p1

%build
%cmake
%make_build

%install
%make_install -C build

%files
%{_bindir}/digidoc-tool
%{_sysconfdir}/digidocpp/schema
%{_sysconfdir}/digidocpp/798.p12
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/digidocpp/digidocpp.conf
%{_mandir}/man1/digidoc-tool.1.*

%files -n %{libname}
%{_libdir}/*.so.%{major}*
%{_libdir}/libdigidocpp.so.%{version}

%files -n %{develname}
%{_includedir}/digidocpp/
%{_libdir}/pkgconfig/lib*.pc
%{_libdir}/*.so
