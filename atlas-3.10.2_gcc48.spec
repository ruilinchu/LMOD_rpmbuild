#
# ATLAS-3.9.32.spec, v3.9.32, 2011-02-14 10:23:28 jlockman@tacc.utexas.edu
#
# see http://math-atlas.sourceforge.net/

Summary:    Automatically Tuned Linear Algebra Software
Name:       atlas
Version:    3.10.2
Release:    0
License:    BSD
Vendor:     ATLAS development group
Group:      Libraries/Math
Source:     atlas%{version}.tar.bz2
Packager:   HMS - jimi_chu@hms.harvard.edu
AutoReqProv: no
%define debug_package %{nil}

%description 
The ATLAS (Automatically Tuned Linear Algebra Software) project is an ongoing research effort focusing on applying empirical techniques in order to provide portable performance. At present, it provides C and Fortran77 interfaces to a portably efficient BLAS implementation, as well as a few routines from LAPACK.

%define comp_fam gcc
%define comp_ver 4.8.2
%define mpi_fam openmpi
%define mpi_ver 1.8.4

##do not modify these
%define APPS        /opt/centos/apps
%define MODULES     modulefiles 
%define comp_fam_ver %{comp_fam}-%{comp_ver}
%define mpi_fam_ver %{mpi_fam}-%{mpi_ver}
%define set_tree error
##end do not

## MUST set ONLY one of the three to 1
%define dep_mpi 0
%define dep_comp 0
%define is_core 1

##do not change these
%if "%{is_core}" == "1"
    %define PKG_BASE    %{APPS}/%{name}
    %define INSTALL_DIR %{PKG_BASE}/%{version}
    %define MODULE_DIR  %{APPS}/%{MODULES}/Core/%{name}
    %define set_tree 1
%endif

%if "%{dep_comp}" == "1"
    %define PKG_BASE    %{APPS}/%{comp_fam_ver}/%{name}
    %define INSTALL_DIR %{PKG_BASE}/%{version}                    
    %define MODULE_DIR  %{APPS}/%{MODULES}/Compiler/%{comp_fam}/%{comp_ver}/%{name}
    %define set_tree 1
%endif

%if "%{dep_mpi}" == "1"
    %define PKG_BASE    %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{name}
    %define INSTALL_DIR %{PKG_BASE}/%{version}
    %define MODULE_DIR  %{APPS}/%{MODULES}/MPI/%{comp_fam}/%{comp_ver}/%{mpi_fam}/%{mpi_ver}/%{name}
    %define set_tree 1
%endif

%if "%{set_tree}" == "error"
     %{error: You must set the compiler/mpi/core tree !}
     exit
%endif
##end do not

%prep 
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup  -n ATLAS

%build
# Use mount temp trick
 mkdir -p             %{INSTALL_DIR}
 mkdir -p             $RPM_BUILD_ROOT/%{INSTALL_DIR}
 mkdir -p BUILD
 cd BUILD

module purge
module load gcc/4.8.2

../configure -b 64 -Fa alg -fPIC --with-netlib-lapack-tarfile=%{_sourcedir}/lapack-3.5.0.tgz --prefix=%{INSTALL_DIR} --shared

 make 
 make install

cp    -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
##finish build 

##begin module stuff
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
    
help([[
Module %{name} loads environmental variables defining
the location of the ATLAS libraries: 
HMS_ATLAS_DIR, HMS_ATLAS_LIB, HMS_ATLAS_INC

To use the atlas library, include compilation directives
of the form: -L$HMS_ATLAS_LIB -I$HMS_ATLAS_INC -lsatlas(or -ltatlas)

Here is an example command to compile test.c:
gcc -I\$HMS_ATLAS_INC test.c -L\$HMS_ATLAS_LIB -lsatlas(or -ltatlas)

Use -lsatlas for single threaded job and -ltatlas for multi-threaded job

It also updates the values of the PATH
and the LD_LIBRARY_PATH variables.

Version %{version}
]])

whatis( "ATLAS" )
whatis( "Version: %{version}")
whatis( "Category: libraries, math")
whatis( "Keywords: Linear Algebra, Mathematics, BLAS")
whatis( "Description: Automatically Tuned Linear Algebra Software")

whatis( "URL: http://math-atlas.sourceforge.net/")

-- Export environmental variables
setenv("HMS_ATLAS_DIR", "%{INSTALL_DIR}")
setenv("HMS_ATLAS_INC", "%{INSTALL_DIR}/include")
setenv("HMS_ATLAS_LIB", "%{INSTALL_DIR}/lib")

-- Prepend the Python directories to the adequate PATH variables
prepend_path( "LD_LIBRARY_PATH", "%{INSTALL_DIR}/lib")

EOF

%files 
%defattr(-,rc200,rccg)
%{INSTALL_DIR}
%{MODULE_DIR}

%post

%postun

%clean
rm -rf $RPM_BUILD_ROOT
