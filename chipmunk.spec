%define major 6.1
%define pkg_major 6
%define libname %mklibname %{name} %{major}
%define devname %mklibname -d %{name}
%define demoname  chipmunk-demo
%define samplname chipmunk-samples

Summary:	2D physics engine
Name:		chipmunk
Version:	6.1.5
Release:	2
License:	MIT
Group:		Development/C
Url:		http://chipmunk-physics.net/
Source0:	http://chipmunk-physics.net/release/Chipmunk-%{pkg_major}.x/Chipmunk-%{version}.tgz
Source1:	chipmunk-makefile
# opengl is only needed by the demos
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(glut)

%description
Chipmunk is a rigid body physics library, designed for 2D video games.

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	2D physics engine shared library
Group:		Development/C
Obsoletes:	%{_lib}chipmunk6 < 6.1.5

%description -n %{libname}
Chipmunk is a rigid body physics library, designed for 2D video games.

%files -n %{libname}
%doc LICENSE.txt
%{_libdir}/libchipmunk.so.%{major}

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
The %{devname} package contains header files for developing
applications that use %{libname}.

%files -n %{devname}
%doc README.textile
%{_libdir}/libchipmunk.so
%{_libdir}/libchipmunk.a
%{_includedir}/chipmunk

#----------------------------------------------------------------------------

%package -n %{demoname}
Summary:	Demos of the library %{name}
Group:		Development/C
Requires:	%{libname} = %{EVRD}

%description -n %{demoname}
The %{demoname} package provides some demos of what can be achieved
using the library %{libname}.
Switch the demos using the keyboard keys from [a] to [s].

%files -n %{demoname}
%{_bindir}/chipmunk-demo

#----------------------------------------------------------------------------

%package -n %{samplname}
Summary:	Examples of use of the library %{name}
Group:		Development/C
BuildArch:	noarch

%description -n %{samplname}
The %{samplname} package provides the source code of the demos.

%files -n %{samplname}
%doc samples

#----------------------------------------------------------------------------

%prep
%setup -q -n Chipmunk-%{version}
cp %{SOURCE1} src/Makefile

%build
pushd src
make clean
make CFLAGS="%{optflags} -std=c99"
make cleanobj
make static CFLAGS="%{optflags} -std=c99"
popd
pushd Demo
ln -s ../src/libchipmunk.so.* libchipmunk.so
gcc -o chipmunk-demo -std=gnu99 -I../include/chipmunk -L. -lchipmunk -lm -lGL -lGLU -lglut *.c
popd
mkdir samples
cp Demo/*.[ch] samples/

%install
pushd src
make install \
  INCDIR=%{buildroot}%{_includedir} \
  LIBDEST=%{buildroot}%{_libdir}
popd
pushd Demo
install -d -m 0755 %{buildroot}%{_bindir}
install -m 0755 chipmunk-demo %{buildroot}%{_bindir}
popd

