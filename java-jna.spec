# TODO
# - allow disable tests
#
# Conditional build:
%bcond_without	tests		# don't build and run tests

%define		srcname		jna
%define		snap		rev1177
%include	/usr/lib/rpm/macros.java
Summary:	Easy access to native shared libraries from Java
Summary(pl.UTF-8):	Prosty dostęp do natywnych bibliotek dzielonych z poziomu Javy.
Name:		java-%{srcname}
Version:	3.2.7.0
Release:	0.%{snap}.1
License:	LGPL
Group:		Libraries/Java
# Source0:	https://jna.dev.java.net/source/browse/*checkout*/jna/tags/%{version}/jnalib/dist/src.zip
# svn export https://jna.dev.java.net/svn/jna/tags/3.2.7/jnalib/ --username guest jna-3.2.7.0
# mv  jna-3.2.7.0   jna-3.2.7.0.rev1177
# tar cjf ~/rpm/packages/jna/jna-3.2.7.0.rev1177.tar.bz2 jna-3.2.7.0.rev1177/
Source0:	%{srcname}-%{version}.%{snap}.tar.bz2
# Source0-md5:	ebfd892683335a3fd6da931938322f77
URL:		https://jna.dev.java.net/
%if %(locale -a | grep -q '^en_US$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
BuildRequires:	ant-nodeps
BuildRequires:	jpackage-utils
BuildRequires:	libffi-devel >= 4.5.2
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	sed >= 4.0
Requires:	jpackage-utils
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JNA provides Java programs easy access to native shared libraries
(DLLs on Windows) without writing anything but Java code No JNI or
native code is required.

%description -l pl.UTF-8
JNA pozwala na łatwy dostęp do natywnych bibliotek dzielonych bez
pisania czegokolwiek co nie jest kodem Javy. Nie potrzebne jest ani
JNI ani fragmentu kodu natywnego.

%prep
%setup -q -n %{srcname}-%{version}.%{snap}

# Segfaults for us and for fedora
rm test/com/sun/jna/DirectTest.java

%build
export JAVA_HOME="%{java_home}"

required_jars="jaxp_parser_impl"
CLASSPATH=$(build-classpath $required_jars)
export CLASSPATH
export LC_ALL=en_US # source code not US-ASCII

%ant

cd src
%javac -cp $CLASSPATH $(find -name '*.java')
%jar cf ../%{srcname}.jar $(find -name '*.class')

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
