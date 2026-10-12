%define _disable_ld_no_undefined 1
%define _disable_lto 1

%define modname digidoc

%define major 1
%define libname %mklibname digidocpp %{major}
%define develname %mklibname digidocpp -d

Name:		libdigidocpp
Version:	4.4.0
Release:	2
Summary:	Library for creating and validating BDoc and DDoc containers

Group:		System/Libraries
License:	LGPLv2+
URL:		https://github.com/open-eid/libdigidocpp
Source:		https://github.com/open-eid/libdigidocpp/releases/download/v%{version}/libdigidocpp-%{version}.tar.gz
Patch0:		libdigidocpp-openssl-4.patch

BuildSystem:	cmake
BuildRequires:	vim-common
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libp11)
BuildRequires:	pkgconfig(xml-security-c)
BuildRequires:	pkgconfig(xmlsec1-openssl)
BuildRequires:	pkgconfig(xalan-c)
BuildRequires:	pkgconfig(minizip)
BuildRequires:	pkgconfig(python)
BuildRequires:	swig
BuildRequires:	doxygen
# Implicit dep of xmlsec1-openssl
BuildRequires:	libltdl-devel
BuildRequires:	xsd-devel
Requires:	opensc

%prep -a
# Patch0 is applied by cmake prep. OpenSSL 4 hides the ASN.1 structures.
# clang no longer injects nullptr_t into the global namespace.
sed -i 's/make_unique_ptr(nullptr_t)/make_unique_ptr(std::nullptr_t)/' src/util/memory.h
# The SWIG typemap still calls the Python 2 string API. Bytes are enough.
sed -i '/PyString_Check/,+2d' libdigidocpp.i

%patchlist
# dropped (no longer applies): libdigidocpp-compile.patch

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

%files
%{_bindir}/digidoc-tool
%{_sysconfdir}/digidocpp/schema
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/digidocpp/digidocpp.conf
%{_mandir}/man1/digidoc-tool.1*
%{py_sitedir}/digidoc.py
%{py_sitedir}/_digidoc_python.so

%files -n %{libname}
%{_libdir}/*.so.%{major}*
%{_libdir}/libdigidocpp.so.%{version}

%files -n %{develname}
%doc %{_docdir}/libdigidocpp
%{_includedir}/digidocpp
%{_includedir}/digidocpp_csharp
%{_libdir}/pkgconfig/lib*.pc
%{_libdir}/*.so
