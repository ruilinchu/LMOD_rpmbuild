#
# gcc spec file
#
Summary:   GNU compiler
Name:      gcc
Version:   5.1.0
Release:   0
License:   GPL
Vendor:    GNU
Group:     compiler
Source:    gcc-5.1.0.tar.gz
Packager:  HMS jimi_chu@hms.harvard.edu
AutoReqProv: no

%description
The GNU Compiler Collection (GCC) is a compiler system produced by the GNU Project supporting various programming languages.

## MUST set ONLY one of the three to 1
%define dep_mpi 0
%define dep_comp 0
%define is_core 1

%include common.inc

%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

## SETUP -n the actual folder name
%setup -n gcc-5.1.0
 
## BUILD

%build
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/

##make sure the modules agree with the parameters!
module purge
module load gcc/4.8.2

mkdir build
cd build

../configure --enable-shared --prefix=%{INSTALL_DIR} --disable-multilib  --disable-bootstrap
make -j12
make install
 
cp -rp %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..

##create modulefiles
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help([[
The gcc modulefile defines the following environment variables
HMS_GCC_LIB, and HMS_GCC_INC for the location of the Intel GCC module.

Version %{version}
]])

whatis("Name: gcc")
whatis("Version: %{version}")
whatis("Category: compiler")
whatis("Keywords: compiler, gcc, g++, c++, c, fortran")
whatis("Description: GNU compiler include gcc, g++, gfortran, etc")
whatis("URL: http://www.threadingbuildingblocks.org")

setenv( "HMS_GCC_DIR", "%{INSTALL_DIR}")
setenv( "HMS_GCC_LIB", "%{INSTALL_DIR}/lib64")
setenv( "HMS_GCC_INC", "%{INSTALL_DIR}/include")

-- prepend path
prepend_path("LD_LIBRARY_PATH", "%{INSTALL_DIR}/lib64")
prepend_path("PATH", "%{INSTALL_DIR}/bin")

-- Setup Modulepath for packages built by this GCC
local mroot = os.getenv("MODULEPATH_ROOT")
local mdir = pathJoin(mroot,"Compiler/gcc", "%{version}")
prepend_path("MODULEPATH", mdir)

EOF

%files 
%defattr(775,rc200,rccg,775)
%{INSTALL_DIR}
%{MODULE_DIR}

%post

%postun

%clean
rm -rf $RPM_BUILD_ROOT
