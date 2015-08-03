#
# Sailfish spec file
#
Summary:   Sailfish is a tool for transcript quantification from RNA-seq data.
Name:      sailfish
Version:   0.6.3
Release:   0
License:   GPL
Vendor:    http://www.cs.cmu.edu/~ckingsf/software/sailfish/
Group:     RNA-seq
Source:    sailfish-0.6.3.zip
Packager:  HMS jimi_chu@hms.harvard.edu
AutoReqProv: no

%description
Threading Building Blocks (TBB) is a C++ template library developed by Intel for writing software programs that take advantage of multi-core processors.

## MUST set ONLY one of the three to 1
%define dep_mpi 0
%define dep_comp 1
%define is_core 0

%include common.inc

%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

## SETUP

%setup -n %{name}-master

## BUILD

%build
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p %{INSTALL_DIR}

##make sure the modules agree with the parameters!
module purge
module load gcc/4.8.2
module load boost/1.55.0
module load atlas/3.10.2
module load tbb/4.3.3

export CC="$(which gcc)"
export CXX="$(which g++)"

sed -i 's+-DBOOST_LIBRARYDIR=${Boost_LIBRARY_DIRS}+-DBOOST_LIBRARYDIR=${Boost_LIBRARY_DIRS} -DATLAS_ROOT:Path=/opt/centos/apps/atlas/3.10.2 -DOPT_ENABLE_ATLAS=ON+g'  CMakeLists.txt
mkdir -p build
cd build
cmake -DBOOST_ROOT=$HMS_BOOST_DIR -DTBB_INSTALL_DIR=$HMS_TBB_DIR -DCMAKE_SHARED_LINKER_FLAGS="-L/opt/centos/apps/atlas/3.10.2/lib -ltatlas" -DCMAKE_INSTALL_PREFIX=%{INSTALL_DIR} ..
make 
make install

cp -rp %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..

##Make modulefiles

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
load("boost/1.55.0","atlas/3.10.2","tbb/4.3.3")

help([[
The sailfish modulefile defines the following environment variables
HMS_SAILFISH_DIR, HMS_SAILFISH_BIN, HMS_SAILFISH_LIB for resources.

This sailfish version is built with boost/1.55.0, tbb/4.3.3 and atlas/3.10.2

Version %{version}
]])

whatis("Name: sailfish")
whatis("Version: %{version}")
whatis("Category: RNA-seq")
whatis("Keywords: sailfish, RNA, RNA-seq")
whatis("Description: Sailfish is a tool for transcript quantification from RNA-seq data.")
whatis("URL: https://github.com/kingsfordgroup/sailfish")

setenv( "HMS_SAILFISH_DIR", "%{INSTALL_DIR}")
setenv( "HMS_SAILFISH_BIN", "%{INSTALL_DIR}/bin")
setenv( "HMS_SAILFISH_LIB", "%{INSTALL_DIR}/lib")

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
