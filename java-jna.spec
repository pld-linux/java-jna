# TODO: Renema to java-jna ?
# Conditional build:
# %bcond_without	javadoc		# don't build javadoc
%bcond_without	source		# don't build source jar
%bcond_without	tests		# don't build and run tests

%include	/usr/lib/rpm/macros.java

# To force building with specific JDK implementation
# without replacing currently installed /usr/bin/javac, etc.
#%%define	use_jdk	java-gcj-compat
#%%buildrequires_jdk
#BuildRequires:	rpmbuild(macros) >= 1.556

# Name without java- prefix. If it is application, not a library,
# just do s/srcname/name/g
%define		srcname		jna
Summary:	Easy access to native shared libraries from Java
Summary(pl.UTF-8):	Prosty dostęp do natywnych bibliotek dzielonych z poziomu Javy.

Name:		jna
Version:	3.2.7.0.rev1177
Release:	0.1
License:	LGPL
# for random java packages (applications?)
Group:		Development/Languages/Java
# for java-XXX packages
Group:		Libraries/Java
# Source0:	https://jna.dev.java.net/source/browse/*checkout*/jna/tags/%{version}/jnalib/dist/src.zip
# svn export https://jna.dev.java.net/svn/jna/tags/3.2.7/jnalib/ --username guest jna-3.2.7.0
# mv  jna-3.2.7.0   jna-3.2.7.0.rev1177
# tar cjf ~/rpm/packages/jna//jna-3.2.7.0.rev1177.tar.bz2 jna-3.2.7.0.rev1177/
Source0:	%{name}-%{version}.tar.bz2
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
# for %%undos macro
BuildRequires:	rpmbuild(macros) >= 1.553
%if %{with source}
BuildRequires:	rpmbuild(macros) >= 1.555
%endif
BuildRequires:	sed >= 4.0
# for %{_javadir}
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



%package source
Summary:	Source code of %{srcname}
Summary(pl.UTF-8):	Kod źródłowy %{srcname}
Group:		Documentation
Requires:	jpackage-utils >= 1.7.5-2

%description source
Source code of %{srcname}.

%description source -l pl.UTF-8
Kod źródłowy %{srcname}.

%prep
%setup -q -n %{srcname}-%{version}
#%%undos build.xml
# %patch2 -p1 -b .tests-headless

# Segfaults for us and for fedora
rm test/com/sun/jna/DirectTest.java

%build
export JAVA_HOME="%{java_home}"

required_jars="jaxp_parser_impl"
CLASSPATH=$(build-classpath $required_jars)
export CLASSPATH

export LC_ALL=en_US # source code not US-ASCII

%ant

# %{__make}
cd src
%javac -cp $CLASSPATH $(find -name '*.java')
%jar cf ../%{srcname}.jar $(find -name '*.class')
%if %{with source}
%jar cf ../%{srcname}.src.jar $(find -name '*.java')
%endif
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

# jars
cp -a dist/%{srcname}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# for jakarta packages:
#for a in dist/*.jar; do
#	jar=${a##*/}
#	cp -a dist/$jar $RPM_BUILD_ROOT%{_javadir}/${jar%%.jar}-%{version}.jar
#	ln -s ${jar%%.jar}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/$jar
#done


# source
install -d $RPM_BUILD_ROOT%{_javasrcdir}
cp -a %{srcname}.src.jar $RPM_BUILD_ROOT%{_javasrcdir}/%{srcname}.src.jar

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(644,root,root,755)
%{_javadir}/%{srcname}.jar
%{_javadir}/%{srcname}-%{version}.jar


%if %{with source}
%files source
%defattr(644,root,root,755)
%{_javasrcdir}/%{srcname}.src.jar
%endif
