#
# tbb spec file
#
Summary:   Intel TBB library
Name:      tbb
Version:   4.3.3
Release:   0
License:   GPLv2
Vendor:    http://www.threadingbuildingblocks.org/
Group:     programming
Source:    tbb-4.3.3.tgz
Packager:  HMS jimi_chu@hms.harvard.edu
AutoReqProv: no

%description
Threading Building Blocks (TBB) is a C++ template library developed by Intel for writing software programs that take advantage of multi-core processors.

## MUST set ONLY one of the three to 1
%define dep_mpi 0
%define dep_comp 0
%define is_core 1

%include common.inc

%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

## SETUP -n the actual folder name

%setup -n tbb43_20150209oss
 
## BUILD

%build
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/
mkdir -p %{INSTALL_DIR}/lib
mkdir -p %{INSTALL_DIR}/include

##make sure the modules agree with the parameters!
module purge
gmake
cp build/linux_intel64_gcc_cc4.4.7_libc2.12_kernel2.6.32_debug/libtbb*  %{INSTALL_DIR}/lib
cp build/linux_intel64_gcc_cc4.4.7_libc2.12_kernel2.6.32_release/libtbb* %{INSTALL_DIR}/lib
cp -r include %{INSTALL_DIR}/
 
cp -rp %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..

##create modulefiles
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help([[
The tbb modulefile defines the following environment variables
HMS_TBB_LIB, and HMS_TBB_INC for the location of the Intel TBB module.

Version %{version}
]])

whatis("Name: tbb")
whatis("Version: %{version}")
whatis("Category: programming")
whatis("Keywords: intel, tbb, threading")
whatis("Description: Threading Building Blocks (TBB) is a C++ template library developed by Intel for writing software programs that take advantage of multi-core processors.")
whatis("URL: http://www.threadingbuildingblocks.org")

setenv( "HMS_TBB_DIR", "%{INSTALL_DIR}")
setenv( "HMS_TBB_LIB", "%{INSTALL_DIR}/lib")
setenv( "HMS_TBB_INC", "%{INSTALL_DIR}/include")

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
