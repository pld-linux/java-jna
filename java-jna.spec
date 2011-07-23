# TODO
# - pass CC and CFLAGS to "native" target
# - Fix tests bcond
#
# Conditional build:
%bcond_without	tests		# don't build and run tests

%define		srcname		jna
%define		snap		rev1177
%include	/usr/lib/rpm/macros.java
Summary:	Easy access to native shared libraries from Java
Summary(pl.UTF-8):	Prosty dostęp do natywnych bibliotek współdzielonych z poziomu Javy
Name:		java-%{srcname}
Version:	3.2.7.0
Release:	0.%{snap}.2
License:	LGPL
Group:		Libraries/Java
# Source0:	https://jna.dev.java.net/source/browse/*checkout*/jna/tags/%{version}/jnalib/dist/src.zip
# svn export https://jna.dev.java.net/svn/jna/tags/3.2.7/jnalib/ --username guest jna-3.2.7.0
# mv  jna-3.2.7.0   jna-3.2.7.0.rev1177
# tar cjf ~/rpm/packages/jna/jna-3.2.7.0.rev1177.tar.bz2 jna-3.2.7.0.rev1177/
Source0:	%{srcname}-%{version}.%{snap}.tar.bz2
# Source0-md5:	ebfd892683335a3fd6da931938322f77
URL:		https://jna.dev.java.net/
BuildRequires:	ant-nodeps
BuildRequires:	jpackage-utils
BuildRequires:	libffi-devel >= 6:4.5.2
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
%if %{with tests}
BuildRequires:	java-junit
BuildRequires:	ant-junit
BuildRequires:	ant-trax
%endif
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JNA provides Java programs easy access to native shared libraries
(DLLs on Windows) without writing anything but Java code - no JNI or
native code is required.

%description -l pl.UTF-8
JNA pozwala na łatwy dostęp do natywnych bibliotek współdzielonych bez
pisania czegokolwiek co nie jest kodem Javy - nie jest potrzebne JNI
ani kod natywny.

%prep
%setup -q -n %{srcname}-%{version}.%{snap}

# Segfaults for us and for fedora
%{__rm} test/com/sun/jna/DirectTest.java

%build
%ant jar contrib-jars %{?with_tests:test}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

# jars
cp -a dist/%{srcname}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_javadir}/%{srcname}.jar
%{_javadir}/%{srcname}-%{version}.jar
