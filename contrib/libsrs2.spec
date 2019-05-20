#
# $Id: aterm.spec,v 1.4 2003/09/24 04:23:47 heinlein Exp $
# $Source: /home/heinlein/projects/specs/RCS/aterm.spec,v $
#
# rpm spec file for aterm
#

Summary: SRS email address rewriting engine
Name: libsrs2
Version: 1.0.18
Release: 50%{?dist}
License: GPL
Group: System Environment/Libraries
Packager: Shevek <srs@anarres.org>
URL: http://www.libsrs2.org/
Source: http://www.libsrs2.org/srs/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: gcc-c++

%description
libsrs2 is the next generation SRS library. SPF verifies that the
Sender address of a mail matches (according to some policy) the
client IP address which submits the mail. When a mail is forwarded,
the sender address must be rewritten to comply with SPF policy. The
Sender Rewriting Scheme, or SRS, provides a standard for this
rewriting which is not vulnerable to attacks by spammers.

%package devel
Summary: Development tools needed to build programs that use libsrs2
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The libsrs2-devel package contains the header files necessary for
developing programs using the libsrs2 (Sender Rewriting Framework)
library.

If you want to develop programs that will rewrited mail envelope
according SRS you should install libsrs2-devel.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags} CFLAGS="%{optflags} -fno-strict-aliasing"


%install
make \
        DESTDIR=%{buildroot} \
        INSTALL="install -p" \
        install


%files
%defattr(-,root,root)
%doc ChangeLog INSTALL README NEWS AUTHORS COPYING
%{_libdir}/libsrs2.so.*
%{_bindir}/srs

%files devel
%{_includedir}/srs2.h
%{_libdir}/libsrs2.so
%{_libdir}/libsrs2.a
%{_libdir}/libsrs2.la

%changelog
* Mon May 20 2019 Petr Vokac <vokac@fedoraproject.org> 1.0.18-50
- update spec file and split into main + devel package
