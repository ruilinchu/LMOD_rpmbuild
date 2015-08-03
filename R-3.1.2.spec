#
# R spec file
#
Summary:   R statistics
Name:      R
Version:   3.1.2
Release:   0
License:   GNU General Public License
Vendor:    http://www.r-project.org/
Group:     statistics/graphics
Source:    R-3.1.2.tar.gz
Packager:  HMS- jimi_chu@hms.harvard.edu
AutoReqProv: no

%description
R is a free software environment for statistical computing and graphics.

## MUST set ONLY one of the three to 1
%define dep_mpi 0
%define dep_comp 1
%define is_core 0

%include common.inc

%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n R-%{version}
 
%build

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p %{INSTALL_DIR}

%if "%{comp_fam}" == "gcc"
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
%endif

%if "%{comp_fam}" == "intel"
cat >> config.site << 'EOF'

F77='ifort'
FC='ifort'
CC='icc'
CXX='icpc'
AR='xiar'
LD='xild'
CFLAGS="-O3 -ipo -openmp -xHost"
BLAS_LIBS="-mkl=parallel -lpthread -lm"

EOF
##make sure the modules agree with the parameters
module purge
module load intel/12.0.5
%endif

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

help([[
The R modulefile defines the following environment variables
HMS_R_DIR for the location of the R distribution,
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

--prepend path
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

