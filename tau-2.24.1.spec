#
# tau-2.24.1 spec, May 25, 2015, Jimi Chu
#
Summary:   Tuning and Analysis Utilities: TAU
Name:       tau
Version:    2.24.1
Release:    0
License:    GPL
Vendor:     Department of Computer and Information Science, University of Oregon
Group:      debugger, profiler, parallel
Source:     tau.tgz
Packager:   HMS - jimi_chu@hms.harvard.edu
AutoReqProv: no
%define debug_package %{nil}

%description
TAU provides a suite of static and dynamic tools that provide graphical user interaction and inter-operation to form an integrated analysis environment for parallel Fortran, C++, C, Java, and Python applications. 

## MUST set ONLY one of the three to 1
%define dep_mpi 1
%define dep_comp 0
%define is_core 0

%include common.inc

%prep 
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup  -n %{name}-%{version}

%build
mkdir -p %{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

module purge
module load gcc/4.8.2
module load openmpi/1.8.4
module load pdtoolkit/3.20

./configure -c++=mpicxx -cc=mpicc -fortran=mpif90 -mpi -ompt=download -bfd=download -unwind=download -pdt=$HMS_PDTOOLKIT_DIR -prefix=%{INSTALL_DIR}

make install

cp -rp %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..

##Make module file
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help([[
Module %{name} loads environmental variables defining the location of the TAU Portable Profiling Package: 
HMS_TAU_DIR, HMS_TAU_BIN TAU_MAKEFILE

to use:
> tau_cxx.sh foo.cpp -o foo
> mpirun -np 4 ./foo
or
> mpirun -np 12 tau_exec foo

> pprof

or

> paraprof (needs X11)
Version %{version}
]])

whatis( "TAU" )
whatis( "Version: %{version}")
whatis( "Category: debugger, profiler")
whatis( "Keywords: debugger, profiler, parallel, tau")
whatis( "Description: TAU provides a suite of static and dynamic tools that provide graphical user interaction and inter-operation to form an integrated analysis environment for parallel Fortran, C++, C, Java, and Python applications.")

whatis( "URL: http://www.cs.uoregon.edu/research/tau/about.php")

-- Export environmental variables
setenv("HMS_TAU_DIR", "%{INSTALL_DIR}")
setenv("HMS_TAU_BIN", "%{INSTALL_DIR}/x86_64/bin")
setenv("TAU_MAKEFILE", "%{INSTALL_DIR}/x86_64/lib/Makefile.tau-ompt-mpi-pdt-openmp")

-- Prepend the Python directories to the adequate PATH variables
prepend_path( "PATH", "%{INSTALL_DIR}/x86_64/bin")

EOF

%files 
%defattr(775,rc200,rccg,775)
%{INSTALL_DIR}
%{MODULE_DIR}

%post

%postun

%clean
rm -rf $RPM_BUILD_ROOT
