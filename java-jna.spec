#
# Conditional build:
%bcond_without	tests		# unit test
%bcond_without	system_libffi	# system libffi (upstream 3.0.12 or gcc >= 4.8)

Summary:	Easy access to native shared libraries from Java
Summary(pl.UTF-8):	Prosty dostęp do natywnych bibliotek współdzielonych z poziomu Javy
Name:		java-jna
Version:	5.10.0
Release:	1
License:	LGPL v2.1 or Apache v2.0
Group:		Libraries/Java
#Source0Download: https://github.com/java-native-access/jna/tags
Source0:	https://github.com/java-native-access/jna/archive/%{version}/jna-%{version}.tar.gz
# Source0-md5:	c11ee374a7e665ab18294751f2e9c835
# Note: by default jna.jar contains versions of native libjnidispatch
# for many systems/architectures; this patch disables such packaging;
# we package libjnidispatch.so as normal native library instead
Patch0:		jna-nonative.patch
Patch1:		jna-soname.patch
Patch2:		jna-tmpdir.patch
Patch3:		jna-x32.patch
Patch4:		jna-no-aar.patch
URL:		https://github.com/java-native-access/jna/
%if %(locale -a | grep -q '^en_US$'; echo $?)%(locale -a | grep -q '^en_US\.utf8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
BuildRequires:	ant >= 1.9.0
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.745
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
%if %{with system_libffi}
# upstream version
BuildRequires:	libffi-devel >= 3.0.12
# gcc version (gcc 4.7.3 is not sufficient - missing ffi_prep_cif_var added in libffi 3.0.12)
BuildRequires:	libffi-devel >= 6:4.8
BuildRequires:	pkgconfig
%endif
%if %{with tests}
BuildRequires:	java-junit
BuildRequires:	ant-junit
%endif
Requires:	jpackage-utils
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
%setup -q -n jna-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%{__rm} -r dist/* lib/native/*.jar

%if %{with system_libffi}
# use system libffi
%{__sed} -i -e '/property name="dynlink\.native"/s/value="false"/value="true"/' build.xml
%endif
# optflags
%{__sed} -i -e '/property name="cflags_extra\.native"/s@value=""@value="%{rpmcflags}"@' build.xml

# ELFAnalyserTest fails when foreign native libraries are not present
%{__rm} test/com/sun/jna/ELFAnalyserTest.java

%build
# build seems to need iso-8859-1 locale (there are some 8bit-encoded characters in win32 sources)
export LC_ALL=en_US
%ant \
	-DCC="%{__cc}" \
	-Drelease=1 \
	-Dbuild-native=true \
	-Ddynlink.native=true \
	dist

%if %{with tests}
# but tests require UTF-8
export LC_ALL=en_US.UTF-8
%ant \
	-Drelease=1 \
	test
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javadir},%{_libdir}}

# jars
cp -p dist/jna.jar $RPM_BUILD_ROOT%{_javadir}/jna-%{version}.jar
ln -s jna-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/jna.jar
cp -p dist/jna-platform.jar $RPM_BUILD_ROOT%{_javadir}/jna-platform-%{version}.jar
ln -s jna-platform-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/jna-platform.jar
# native stub library
install build/native-linux-*/libjnidispatch.so $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.md LICENSE OTHERS README.md TODO
%attr(755,root,root) %{_libdir}/libjnidispatch.so
%{_javadir}/jna-%{version}.jar
%{_javadir}/jna.jar
%{_javadir}/jna-platform-%{version}.jar
%{_javadir}/jna-platform.jar
