#
# sharek spec file
#
Summary:   shark machine learning library
Name:      shark
Version:   3.0
Release:   0
License:   GPL
Vendor:    http://image.diku.dk/
Group:     library
Source:    Shark-3.0.tar.gz
Packager:  HMS jimi_chu@hms.harvard.edu
AutoReqProv: no

%description
SHARK is a fast, modular, feature-rich open-source C++ machine learning library. I

## MUST set ONLY one of the three to 1
%define dep_mpi 0
%define dep_comp 0
%define is_core 1

%include common.inc

%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

## SETUP -n the actual folder name

%setup -n Shark-%{version}
 
## BUILD

%build
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/

##make sure the modules agree with the parameters!
module purge
module load gcc/4.8.2
module load boost/1.49.0
module load atlas

mkdir -p build
cd build
CC=gcc
CXX=g++
cmake -DCMAKE_INSTALL_PREFIX=%{INSTALL_DIR} -DBoost_NO_SYSTEM_PATHS=TRUE -DBOOST_INCLUDEDIR=$HMS_BOOST_INC -DBOOST_LIBRARYDIR=$HMS_BOOST_LIB -DATLAS_ROOT:Path=$HMS_ATLAS_DIR -DOPT_ENABLE_ATLAS=ON -DOPT_DYNAMIC_LIBRARY=ON ..
make -j8
make install
 
cp -rp %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..

##create modulefiles
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help([[
The shark modulefile defines the following environment variables
HMS_SHARK_LIB, and HMS_SHARK_INC for the location of the Intel SHARK module.

This shark version is build with gcc/4.8.2, boost/1.49.0 and atlas/3.10
Version %{version}
]])

whatis("Name: shark")
whatis("Version: %{version}")
whatis("Category: programming")
whatis("Keywords: intel, shark, threading")
whatis("Description: Threading Building Blocks (SHARK) is a C++ template library developed by Intel for writing software programs that take advantage of multi-core processors.")
whatis("URL: http://www.threadingbuildingblocks.org")

setenv( "HMS_SHARK_DIR", "%{INSTALL_DIR}")
setenv( "HMS_SHARK_LIB", "%{INSTALL_DIR}/lib")
setenv( "HMS_SHARK_INC", "%{INSTALL_DIR}/include")

-- Append path
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
