%define name      chipmunk
%define major     6
%define libname   %mklibname %{name} %major
%define develname %mklibname -d %{name}
%define demoname  chipmunk-demo
%define samplname chipmunk-samples

Name:           %{name}
Version:        6.0.3
Release:        %mkrel 2
Summary:        2D physics engine
Group:          Development/C
License:        MIT
URL:            http://chipmunk-physics.net/
Source0:        http://chipmunk-physics.net/release/Chipmunk-%{major}.x/Chipmunk-%{version}.tgz
Source1:        chipmunk-makefile
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}
# opengl is only needed by the demos
BuildRequires:  libmesagl-devel
BuildRequires:  mesaglu-devel
BuildRequires:  freeglut-devel

%description
Chipmunk is a rigid body physics library, designed for 2D video games.

%package -n %{libname}
Summary:        2D physics engine
Group:          Development/C

%description -n %{libname}
Chipmunk is a rigid body physics library, designed for 2D video games.

%package -n %{develname}
Summary:        Development files for %{name}
Group:          Development/C
Requires:       %{libname} = %{version}-%{release}
Provides:       lib%{name} = %{version}-%{release}

%description -n %{develname}
The %{develname} package contains header files for developing
applications that use %{libname}.

%package -n %{demoname}
Summary:        Demos of the library %{name}
Group:          Development/C
Requires:       %{libname} = %{version}-%{release}

%description -n %{demoname}
The %{demoname} package provides some demos of what can be achieved
using the library %{libname}.
Switch the demos using the keyboard keys from [a] to [s].

%package -n %{samplname}
Summary:        Examples of use of the library %{name}
Group:          Development/C
Requires:       %{libname} = %{version}-%{release}

%description -n %{samplname}
The %{samplname} package provides the source code of the demos.

%prep
%setup -q -n Chipmunk-%{version}
cp %{SOURCE1} src/Makefile

%build
pushd src
make clean
make
make cleanobj
make static CFLAGS=-std=c99
popd
pushd Demo
ln -s ../src/libchipmunk.so.* libchipmunk.so
gcc -o chipmunk-demo -std=gnu99 -I../include/chipmunk -L. -lchipmunk -lm -lGL -lGLU -lglut *.c
popd
mkdir samples
cp Demo/*.[ch] samples/

%install
rm -rf %{buildroot}
pushd src
make install \
  INCDIR=%{buildroot}%{_includedir} \
  LIBDEST=%{buildroot}%{_libdir}
popd
pushd Demo
install -d -m 0755 %{buildroot}%{_bindir}
install -m 0755 chipmunk-demo %{buildroot}%{_bindir}
popd

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc LICENSE.txt
%{_libdir}/libchipmunk.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%doc README.textile
%{_libdir}/libchipmunk.so
%{_libdir}/libchipmunk.*a
%{_includedir}/chipmunk

%files -n %{demoname}
%defattr(-,root,root)
%{_bindir}/chipmunk-demo

%files -n %{samplname}
%defattr(-,root,root)
%doc samples


%changelog
* Mon Jan 09 2012 Andrey Bondrov <abondrov@mandriva.org> 6.0.3-2mdv2012.0
+ Revision: 758798
- Set library version to 6.0, update major to 6
- New version 6.0.3, library major is still 5

  + Paulo Ricardo Zanoni <pzanoni@mandriva.com>
    - Add missing -lGLU when compiling with freeglut
    - Add missing GLU BR
    - Require gerneric version of glut (so we can switch to freeglut)

* Tue Jul 13 2010 Florent Monnier <blue_prawn@mandriva.org> 5.2.0-1mdv2011.0
+ Revision: 552628
- fix for /usr/lib64
- import chipmunk


