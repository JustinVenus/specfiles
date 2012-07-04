%define real_version 3.0.2
# laziness mostly
%define tar_version %(%__python -c "import sys; sys.stdout.write('%{real_version}'.replace('.','-'))")
%define major_version %(%__python -c "import sys; sys.stdout.write('%{real_version}'.split('.')[0])")

###############################################################################
# Specfile for Redhat like systems.
#
###############################################################################

Name:		amdlibm
Version:	%{real_version}
Release:	1%{?dist}
Summary:	AMD LibM Optimized for Opteron Processors

Group:		System Environment/Libraries
License:	AMD EULA
URL:		http://developer.amd.com/libraries/LibM/Pages/default.aspx
Source0:	%{name}%{version}lin64.tar.gz
# needed to ensure the 'ar' utility is available
BuildRequires:	binutils
# purely to help setup the macros
BuildRequires:	%__python
# to convert the pdf license to a text file
BuildRequires:	poppler-utils
# for building dynamic library from archive
BuildRequires:  gcc
# for testing new dynamic library 'examples/build_and_run.sh'
BuildRequires:	gcc-c++


%description
AMD LibM is a software library containing a collection of basic math 
functions optimized for x86-64 processor based machines. It provides 
many routines from the list of standard C99 math functions.
This package contains the dynamic shared library.


%package static
Summary:	AMD LibM (static) Optimized for Opteron Processors
Group:		Development/Libraries


%description static
AMD LibM is a software library containing a collection of basic math 
functions optimized for x86-64 processor based machines. It provides 
many routines from the list of standard C99 math functions.
This package contains the static library.


%package devel
Summary:	AMD LibM Headers Optimized for Opteron Processors
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}


%description devel
AMD LibM is a software library containing a collection of basic math 
functions optimized for x86-64 processor based machines. It provides 
many routines from the list of standard C99 math functions.
This package contains the development headers.


%package demo
Summary:	AMD LibM Example Code
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-devel = %{version}-%{release}


%description demo
AMD LibM is a software library containing a collection of basic math 
functions optimized for x86-64 processor based machines. It provides 
many routines from the list of standard C99 math functions.
This package contains demonstration code.


%prep
%setup -q -n %{name}-%{tar_version}


%build
# Convert AMD's PDF license to a text file
pdftotext LICENSE.pdf LICENSE.txt

cd lib/dynamic
%__rm libamdlibm.so
# prepare sources from archive
ar x ../static/libamdlibm.a
# link new dynamic shared library from the archived objects
gcc -s -shared -Wl,-soname,libamdlibm.so.%{major_version} -o libamdlibm.so.%{version} *.o
# so we can run the tests
%__ln_s libamdlibm.so.%{version} libamdlibm.so.%{major_version}
%__ln_s libamdlibm.so.%{version} libamdlibm.so
cd ../../examples
# perform a sort of unit test, by validating that the examples build and run
%__chmod +x build_and_run.sh
# look for errors while running the examples
./build_and_run.sh >&/dev/stdout | %__grep error && exit 1


%install
%__install -m 755 -D lib/dynamic/libamdlibm.so.%{version} %{buildroot}%{_libdir}/libamdlibm.so.%{version}
%__ln_s %{_libdir}/libamdlibm.so.%{version} %{buildroot}%{_libdir}/libamdlibm.so.%{major_version}
%__ln_s %{_libdir}/libamdlibm.so.%{major_version} %{buildroot}%{_libdir}/libamdlibm.so
%__install -m 755 -D lib/static/libamdlibm.a %{buildroot}%{_libdir}/libamdlibm.a
%__install -m 644 -D include/amdlibm.h %{buildroot}%{_includedir}/amdlibm.h

%__rm examples/*.bat ||:
for item in `ls examples`
do
    %__install -m 644 -D examples/${item} %{buildroot}%{_datadir}/%{name}-demo/examples/${item}
done


%post -p %{_sbindir}/ldconfig
%postun -p %{_sbindir}/ldconfig


%clean
%{__rm} -rf %{buildroot}


%files
%doc LICENSE.txt ReleaseNotes.txt
%{_libdir}/libamdlibm.so.%{major_version}
%{_libdir}/libamdlibm.so.%{version}


%files static
%doc LICENSE.txt ReleaseNotes.txt
%{_libdir}/libamdlibm.a


%files devel
%doc LICENSE.txt ReleaseNotes.txt
%{_includedir}/amdlibm.h
%{_libdir}/libamdlibm.so


%files demo
%doc LICENSE.txt ReleaseNotes.txt
%{_datadir}/%{name}-demo/examples/*


%changelog
* Wed Jul  4 2012 Justin Venus <justin.venus@gmail.com>
- packaging an enhanced version of libm for AMD Family 15 Series Processors
