#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#

%define without_java 1
%define without_python 1
%define without_ruby 1
%define without_php 1
%define without_qt4 1
%define without_qt5 1
%define without_tests 0

%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           thrift
%if %{defined fedora}
License:        ASL 2.0
%else
License:        Apache-2.0
%endif
Group:          Development
Summary:        RPC and serialization framework
Version:        1.0.0~dev
Release:        0
URL:            http://thrift.apache.org
Source0:        %{name}-%{version}.tar.bz2
BuildRequires:  gcc45
BuildRequires:  gcc45-c++
BuildRequires:  libtool
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  boost-devel
%if %{defined fedora}
BuildRequires:  pkgconfig
BuildRequires:  openssl-devel
%else
BuildRequires:  pkg-config
BuildRequires:  libopenssl-devel
%endif

%if 0%{!?without_java:1}
BuildRequires:  java-devel >= 0:1.5.0
BuildRequires:  ant >= 0:1.6.5
%endif

%if 0%{!?without_python:1}
BuildRequires:  python-devel
%endif

%if 0%{!?without_ruby:1}
%define gem_name %{name}
BuildRequires:  ruby-devel
BuildRequires:  rubygems-devel
%endif

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-build

%description
Thrift is a software framework for scalable cross-language services
development. It combines a powerful software stack with a code generation
engine to build services that work efficiently and seamlessly between C++,
Java, C#, Python, Ruby, Perl, PHP, Objective C/Cocoa, Smalltalk, Erlang,
Objective Caml, and Haskell.

%files
%defattr(-,root,root)
%{_bindir}/thrift


%package lib-cpp
Summary: Thrift C++ library
Group:   Libraries

%description lib-cpp
C++ libraries for Thrift.

%files lib-cpp
%defattr(-,root,root)
%{_libdir}/libthrift*.so.*
%{_libdir}/libthrift*.so


%package lib-cpp-devel
Summary:   Thrift C++ library development files
%if %{defined fedora}
Group:     Development/Libraries
%else
Group:     Development/Libraries/C and C++
%endif
Requires:  %{name} = %{version}-%{release}
%if %{defined fedora}
BuildRequires:  openssl-devel
%else
BuildRequires:  libopenssl-devel
%endif
Requires:  boost-devel
Requires:  libopenssl-devel
%if 0%{!?without_libevent:1}
Requires:  libevent-devel >= 1.2
%endif
%if 0%{!?without_zlib:1}
Requires:  zlib-devel
%endif

%description lib-cpp-devel
C++ static libraries and headers for Thrift.

%files lib-cpp-devel
%defattr(-,root,root)
%{_includedir}/thrift/
%{_libdir}/libthrift*.*a
%{_libdir}/pkgconfig/thrift*.pc


%if 0%{!?without_java:1}
%package lib-java
Summary:   Thrift Java library
Group:     Libraries
Requires:  java >= 0:1.5.0

%description lib-java
Java libraries for Thrift.

%files lib-java
%defattr(-,root,root)
%{_javadir}/*
%endif


%if 0%{!?without_python:1}
%package lib-python
Summary: Thrift Python library
Group:   Libraries

%description lib-python
Python libraries for Thrift.

%files lib-python
%defattr(-,root,root)
%{python_sitearch}/*
%endif


%if 0%{!?without_ruby:1}
%package -n rubygem-%{gem_name}
Summary: Thrift Ruby library
Group:   Libraries
Obsoletes: %{name}-lib-ruby

%description -n rubygem-%{gem_name}
Ruby libraries for Thrift.

%files -n rubygem-%{gem_name}
%defattr(-,root,root)
%{gem_dir}/*
%endif


%if 0%{!?without_php:1}
%package lib-php
Summary: Thrift PHP library
Group:   Libraries

%description lib-php
PHP libraries for Thrift.

%files lib-php
%defattr(-,root,root)
/usr/lib/php/*
%endif


%prep
%setup -q

%build
[[ -e Makefile.in ]] || ./bootstrap.sh
export GEM_HOME=${PWD}/.gem-home
export RUBYLIB=${PWD}/lib/rb/lib
export CC=gcc-4.5
export CXX=g++-4.5
%configure \
  --with-pic \
  %{?without_libevent: --without-libevent } \
  %{?without_zlib:     --without-zlib     } \
  %{?without_tests:    --without-tests    } \
  %{?without_java:     --without-java     } \
  %{?without_python:   --without-python   } \
  %{?without_ruby:     --without-ruby     } \
  %{?without_php:      --without-php      } \
  %{?without_qt4:      --without-qt4      } \
  %{?without_qt5:      --without-qt5      } \
  %{!?without_php:     PHP_PREFIX=${RPM_BUILD_ROOT}/usr/lib/php } \
  --without-csharp \
  --without-erlang \
  --without-haxe \
  --without-c_glib \
  --without-haskell \
  --without-go \
  --without-d

make 

%if 0%{!?without_java:1}
cd lib/java
%ant
cd ../..
%endif

%if 0%{!?without_python:1}
cd lib/py
CFLAGS="%{optflags}" %{__python} setup.py build
cd ../..
%endif

%if 0%{!?without_ruby:1}
%gem_install -n lib/rb/thrift*.gem
%endif

%install
export GEM_HOME=${PWD}/.gem-home
export RUBYLIB=${PWD}/lib/rb/lib
%makeinstall
ln -s libthrift-%{version}.so ${RPM_BUILD_ROOT}%{_libdir}/libthrift.so.0
ln -s libthriftnb-%{version}.so ${RPM_BUILD_ROOT}%{_libdir}/libthriftnb.so.0
ln -s libthriftz-%{version}.so ${RPM_BUILD_ROOT}%{_libdir}/libthriftz.so.0

%if 0%{!?without_java:1}
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p lib/java/build/*.jar $RPM_BUILD_ROOT%{_javadir}
%endif

%if 0%{!?without_python:1}
cd lib/py
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
cd ../..
%endif

%if 0%{!?without_ruby:1}
mkdir -p %{buildroot}%{gem_dir}
cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/
%endif

%clean
rm -rf ${RPM_BUILD_ROOT}


%post
umask 007
/sbin/ldconfig > /dev/null 2>&1


%postun
umask 007
/sbin/ldconfig > /dev/null 2>&1

%changelog
* Tue May 24 2016 Bernhard Miklautz <bernhard.miklautz@thincast.com> - 1.0.0~dev-0
- update package to 1.0.0~dev
* Wed Oct 10 2012 Thrift Dev <dev@thrift.apache.org> 
- Thrift 0.9.0 release.
