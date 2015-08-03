#
# eigen spec file
#
Summary:   Eigen - C++ template library for linear algebra: matrices, vectors, numerical solvers, and related algorithms
Name:      eigen
Version:   3.2.4
Release:   0
License:   MPL2 
Vendor:    http://eigen.tuxfamily.org/
Group:     Linear Algebra Library
Source:    eigen-3.2.4.tar.bz2
Packager:  HMS alex_truong@hms.harvard.edu
AutoReqProv: no

%description
Eigen is a C++ template library for linear algebra: matrices, vectors, numerical solvers, and related algorithms.

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
    %define _rpmfilename %%{ARCH}/%%{NAME}.%%{VERSION}.%%{RELEASE}.%%{COMP_FAM_VER}.%%{ARCH}.rpm
%endif

%if "%{dep_mpi}" == "1"
    %define PKG_BASE    %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{name}
    %define INSTALL_DIR %{PKG_BASE}/%{version}
    %define MODULE_DIR  %{APPS}/%{MODULES}/MPI/%{comp_fam}/%{comp_ver}/%{mpi_fam}/%{mpi_ver}/%{name}
    %define set_tree 1
    %define _rpmfilename %%{ARCH}/%%{NAME}.%%{VERSION}.%%{RELEASE}.%%{COMP_FAM_VER}.%%{MPI_FAM_VER}.%%{ARCH}.rpm
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

%setup -n %{name}-%{name}-10219c95fe65
 
##
## BUILD
##

%build
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p %{INSTALL_DIR}

##make sure the modules agree with the parameters!
module purge
module load gcc/4.8.2

mkdir build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=%{INSTALL_DIR}
make install
 
cp -rp %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..

##create modulefiles
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help([[
The Eigen modulefile defines the environment variable
HMS_EIGEN_DIR for resources.

Version %{version}
]])

whatis("Name: Eigen")
whatis("Version: %{version}")
whatis("Category: library, linear algebra")
whatis("Keywords: System, Library")
whatis("Description: Eigen is a C++ template library for linear algebra: matrices, vectors, numerical solvers, and related algorithms. ")
whatis("URL: http://eigen.tuxfamily.org/")

setenv( "HMS_EIGEN_DIR", "%{INSTALL_DIR}")

-- Append path
prepend_path("PATH", "%{INSTALL_DIR}/bin")
EOF

%files 
%defattr(-,at237,rccg,-)
%{INSTALL_DIR}
%{MODULE_DIR}

%post

%postun

<<<<<<< HEAD
cd %{PKG_BASE}

=======
>>>>>>> 3ddf8c74a76484a89b7af0f37fefaef91440cc6d
%clean
rm -rf $RPM_BUILD_ROOT
