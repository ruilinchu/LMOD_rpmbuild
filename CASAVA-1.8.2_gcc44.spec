#
# CASAVA spec file
#
Summary:   CASAVA 1.8.2 (short for "Consensus Assessment of Sequence And VAriation")
Name:      CASAVA
Version:   1.8.2
Release:   0
License:   Copyright 2009-2011 Illumina, Inc. All rights reserved. 
Vendor:    Illumina
Group:     sequencing analysis
Source:    CASAVA_v1.8.2.tar.gz
Packager:  HMS alex_truong@hms.harvard.edu
AutoReqProv: no

%description
CASAVA is the part of Illumina's sequencing analysis software that performs alignment of a sequencing run to a reference genome and subsequent variant analysis and read counting.

## MUST set ONLY one of the three to 1
%define dep_mpi 0
%define dep_comp 1
%define is_core 0

%define comp_fam gcc
%define comp_ver 4.4.7
%define mpi_fam openmpi
%define mpi_ver 1.8.4

%define debug_package %{nil}
##do not modify these
%define APPS        /opt/centos/apps
%define MODULES     modulefiles
%define comp_fam_ver %{comp_fam}-%{comp_ver}
%define mpi_fam_ver %{mpi_fam}-%{mpi_ver}
%define set_tree error
##end do not

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

## SETUP

%setup -n %{name}_v%{version}

## BUILD

%build
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p %{INSTALL_DIR}

##make sure the modules agree with the parameters!
module purge
module load gcc/4.4.7
module load boost/1.44.0

mkdir build
cd build

export BOOST_ROOT=$HMS_BOOST_DIR

../src/configure --prefix=%{INSTALL_DIR}
make
make install prefix=%{INSTALL_DIR}

cp -rp %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..

##Make modulefiles

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help([[
The samtools modulefile defines the following environment variables
HMS_CASAVA_DIR, HMS_CASAVA_BIN, HMS_CASAVA_LXC, HMS_CASAVA_LIB, and HMS_CASAVA_SHARE for resources.

Version %{version}
]])

whatis("Name: CASAVA")
whatis("Version: %{version}")
whatis("Category: sequence analysis")
whatis("Keywords: CASAVA, sequence, analysis, illumina")
whatis("Description: CASAVA 1.8.2 (short for Consensus Assessment of Sequence And VAriation) ")
whatis("URL: http://www.illumina.com")

setenv( "HMS_CASAVA_DIR", "%{INSTALL_DIR}")
setenv( "HMS_CASAVA_BIN", "%{INSTALL_DIR}/bin")
setenv( "HMS_CASAVA_LXC", "%{INSTALL_DIR}/libexec")
setenv( "HMS_CASAVA_LIB", "%{INSTALL_DIR}/lib")
setenv( "HMS_CASAVA_SHARE", "%{INSTALL_DIR}/share")

-- Append path
prepend_path("PATH", "%{INSTALL_DIR}/bin")
EOF

%files 
%defattr(775,at237,rccg,775)
%{INSTALL_DIR}
%{MODULE_DIR}

%post

%postun

%clean
rm -rf $RPM_BUILD_ROOT
