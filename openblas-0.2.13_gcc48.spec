#
# openblas spec file
#
Summary:   openblas install
Name:      openblas
Version:   0.2.13
Release:   0
License:   BSD
Vendor:    http://www.openblas.net
Group:     Libraries/Math
Source:    openblas-0.2.13.tar.gz
Packager:  HMS jimi_chu@hms.harvard.edu
AutoReqProv: no
%description
OpenBLAS is an optimized BLAS library based on GotoBLAS2 1.13 BSD version.

%define debug_package %{nil}

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
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n OpenBLAS-%{version}
 
%build

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p %{INSTALL_DIR}

make USE_OPENMP=1
make PREFIX=%{INSTALL_DIR} install
 
cp -rp %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..

##create modulefiles
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help([[
The openblas modulefile defines the following environment variables
HMS_OPENBLAS_DIR, HMS_OPENBLAS_LIB, and HMS_OPENBLAS_INC for the location of 
the openblas distribution, libraries, and include files, respectively.

To use the openblas library, include compilation directives
of the form: -L$HMS_OPENBLAS_LIB -I$HMS_OPENBLAS_INC -lopenblas

Here is an example command to compile test.c:
gcc -I\$HMS_OPENBLAS_INC test.c -L\$HMS_OPENBLAS_LIB -lopenblas

Version %{version}
]])

whatis("Name: OpenBlas")
whatis("Version: %{version}")
whatis("Category: library, math")
whatis("Keywords: Library, Math, Performance, Linear Algebra")
whatis("Description: OpenBLAS is an optimized BLAS library based on GotoBLAS2 1.13 BSD version.")
whatis("URL: http://www.openblas.net")

setenv( "HMS_OPENBLAS_DIR", "%{INSTALL_DIR}")
setenv( "HMS_OPENBLAS_LIB", "%{INSTALL_DIR}/lib")
setenv( "HMS_OPENBLAS_INC", "%{INSTALL_DIR}/include")

-- Append path
prepend_path("LD_LIBRARY_PATH", "%{INSTALL_DIR}/lib")

EOF

%files 
%defattr(755,rc200,rccg)
%{INSTALL_DIR}
%{MODULE_DIR}

%post

%postun

%clean
rm -rf $RPM_BUILD_ROOT

