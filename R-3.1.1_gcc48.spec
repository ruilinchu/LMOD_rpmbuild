#
# R spec file
#
Summary:   R install
Name:      R
Version:   3.1.1
Release:   gcc48
License:   GNU General Public License
Vendor:    http://www.r-project.org/
Group:     statistics/graphics
Source:    R-3.1.1.tar.gz
Packager:  HMS- jimi_chu@hms.harvard.edu
AutoReqProv: no

%description
R is a free software environment for statistical computing and graphics.

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
%define dep_comp 1
%define is_core 0

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

%setup -n R-%{version}
 
%build

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p %{INSTALL_DIR}

cat >> config.site << 'EOF'

CFLAGS='-g -O3'
FFLAGS='-g -O3' 
CXXFLAGS='-g -O3'
FCFLAGS='-g -O3'
BLAS_LIBS="-L${HMS_OPENBLAS_LIB} -lopenblas"

EOF

##make sure the modules agree with the parameters
module purge
module load gcc/4.8.2
module load openblas/0.2.13

./configure --prefix=%{INSTALL_DIR} --with-blas --with-lapack --with-x=no
make
make install

##make the R_LIB built-in
sed -i.old '1s;^;rlibname <- paste0(Sys.getenv("HOME"),"/R/library/",getRversion(),"_","%{comp_fam_ver}")\ninvisible(system(paste("mkdir","-p",rlibname), intern = TRUE))\nSys.setenv("R_LIBS" = rlibname)\nSys.setenv("R_LIBS_USER" = rlibname)\n;' %{INSTALL_DIR}/lib64/R/library/base/R/Rprofile
 
cp -rp %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..

##create modulefiles
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
load("openblas/0.2.13")
help([[
The R modulefile defines the following environment variables
HMS_R_BIN, HMS_R_LIB, and HMS_R_INC for the location of the R distribution,
documentation, binaries, libraries, and include files, respectively.

Version %{version}
]])

whatis("Name: R")
whatis("Version: %{version}")
whatis("Category: statistics")
whatis("Keywords: statistics, graphics, ")
whatis("Description: R is a language and environment for statistical computing and graphics.")
whatis("URL: http://www.r-project.org/")

setenv( "HMS_R_DIR", "%{INSTALL_DIR}")

-- Append/prepend path
prepend_path("PATH", "%{INSTALL_DIR}/bin")

EOF

%files 
%defattr(-,rc200,rccg,-)
%{INSTALL_DIR}
%{MODULE_DIR}

%post

%postun

%clean
rm -rf $RPM_BUILD_ROOT

