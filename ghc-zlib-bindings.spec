#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	zlib-bindings
Summary:	Low-level bindings to the zlib package
Summary(pl.UTF-8):	Niskopoziomowe wiązania do pakietu zlib
Name:		ghc-%{pkgname}
Version:	0.1.1.3
Release:	2
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/zlib-bindings
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	d0a535c01d6773e9ef9318e43707601c
URL:		http://hackage.haskell.org/package/zlib-bindings
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 4
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-bytestring >= 0.9.1.4
BuildRequires:	ghc-zlib >= 0.5.2.0
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 4
BuildRequires:	ghc-base-prof < 5
BuildRequires:	ghc-bytestring-prof >= 0.9.1.4
BuildRequires:	ghc-zlib-prof >= 0.5.2.0
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
Requires(post,postun):	/usr/bin/ghc-pkg
%requires_eq	ghc
Requires:	ghc-base >= 4
Requires:	ghc-base < 5
Requires:	ghc-bytestring >= 0.9.1.4
Requires:	ghc-zlib >= 0.5.2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
Provides necessary functions for producing a streaming interface.

%description -l pl.UTF-8
Ten pakiet dostarcza funkcje niezbędne do tworzenia interfejsu
strumieniowego.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC.
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 4
Requires:	ghc-base-prof < 5
Requires:	ghc-bytestring-prof >= 0.9.1.4
Requires:	ghc-zlib-prof >= 0.5.2.0

%description prof
Profiling %{pkgname} library for GHC. Should be installed when GHC's
profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.lhs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs build
runhaskell Setup.lhs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/HSzlib-bindings-%{version}.o
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSzlib-bindings-%{version}.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/*.hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Zlib
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Zlib/*.hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSzlib-bindings-%{version}_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Codec/Zlib/*.p_hi
%endif
