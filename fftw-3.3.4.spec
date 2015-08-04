#
# Fftw spec file
#
Summary:   fftw – Utilities for the Sequence Alignment/Map (SAM) format
Name:      fftw
Version:   3.3.4
Release:   0
License:   GPL
Vendor:    FFTW
Group:     performance, fftw
Source:    fftw-3.3.4.tar.gz
Packager:  HMS jimi_chu@hms.harvard.edu
AutoReqProv: no

%description

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
    %define _rpmfilename %%{ARCH}/%%{NAME}.%%{VERSION}.%%{RELEASE}.%%{ARCH}.rpm
%endif

%if "%{dep_comp}" == "1"
    %define PKG_BASE    %{APPS}/%{comp_fam_ver}/%{name}
    %define INSTALL_DIR %{PKG_BASE}/%{version}                    
    %define MODULE_DIR  %{APPS}/%{MODULES}/Compiler/%{comp_fam}/%{comp_ver}/%{name}
    %define set_tree 1
    %define _rpmfilename %%{ARCH}/%%{NAME}.%%{VERSION}.%%{RELEASE}.%{comp_fam_ver}.%%{ARCH}.rpm
%endif

%if "%{dep_mpi}" == "1"
    %define PKG_BASE    %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{name}
    %define INSTALL_DIR %{PKG_BASE}/%{version}
    %define MODULE_DIR  %{APPS}/%{MODULES}/MPI/%{comp_fam}/%{comp_ver}/%{mpi_fam}/%{mpi_ver}/%{name}
    %define set_tree 1
    %define _rpmfilename %%{ARCH}/%%{NAME}.%%{VERSION}.%%{RELEASE}.%{comp_fam_ver}.%{mpi_fam_ver}.%%{ARCH}.rpm
%endif

%if "%{set_tree}" == "error"
     %{error: You must set the compiler/mpi/core tree !}
     exit
%endif
##end do not

%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

##
## SETUP
##

%setup -n fftw-%{version}
 
##
## BUILD
##

%build
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p %{INSTALL_DIR}

##make sure the modules agree with the parameters!
module purge
module load gcc/4.8.2
module load openmpi/1.8.4

export CC="$(which gcc)"
export CXX="$(which g++)"
export MPICC="$(which mpicc)"
export MPICXX="$(which mpicxx)"

./configure --prefix=%{INSTALL_DIR} --enable-shared=yes CFLAGS='-fPIC' --enable-float --enable-mpi --enable-openmp --enable-threads CFLAGS=-march=native CPPFLAGS=-march=native
make -j8
make install

cp -rp %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..

##create modulefiles
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help([[
The fftw modulefile defines the following environment variables
HMS_FFTW_DIR, HMS_FFTW_BIN, HMS_FFTW_INC, HMS_FFTW_LIB for resources.

This FFTW is built with gcc-4.8.2 and openmpi-1.8.4.

Version %{version}
]])

whatis("Name: FFTW")
whatis("Version: %{version}")
whatis("Category: FFTW")
whatis("Keywords: fftw, mpi")
whatis("Description: fftw – is a C subroutine library for computing the discrete Fourier transform (DFT) in one or more dimensions,.")
whatis("URL: http://www.fftw.org")

setenv( "HMS_FFTW_DIR", "%{INSTALL_DIR}")
setenv( "HMS_FFTW_BIN", "%{INSTALL_DIR}/bin")
setenv( "HMS_FFTW_INC", "%{INSTALL_DIR}/include")
setenv( "HMS_FFTW_LIB", "%{INSTALL_DIR}/lib")

-- Append path
prepend_path("PATH", "%{INSTALL_DIR}/bin")
prepend_path("LD_LIBRARY_PATH", "%{INSTALL_DIR}/lib")

EOF

%files 
%defattr(775,rc200,rccg,775)
%{INSTALL_DIR}
%{MODULE_DIR}

%post

%postun

%clean
rm -rf $RPM_BUILD_ROOT
