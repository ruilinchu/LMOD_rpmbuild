#
# pdtoolkit spec file
#
Summary:   Program Database Toolkit (PDT) 
Name:      pdtoolkit
Version:   3.20
Release:   0
License:   GNU
Vendor:    University of Oregon Performance Research Lab
Group:     System Environment/Base
Source:    pdt_lite.tar.gz
Packager:  HMS jimi_chu@hms.harvard.edu
AutoReqProv: no

%description
Program Database Toolkit (PDT) is a framework for analyzing source code written in several programming languages and for making rich program knowledge accessible to developers of static and dynamic analysis tools.

## MUST set ONLY one of the three to 1
%define dep_mpi 0
%define dep_comp 0
%define is_core 1

%include common.inc

%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

## SETUP

%setup -n pdtoolkit-3.20
 
## BUILD

%build
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p %{INSTALL_DIR}

##make sure the modules agree with the parameters!
module purge
module load gcc/4.8.2
./configure -GUN -prefix=%{INSTALL_DIR}
make
make install
 
cp -rp %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..

##create modulefiles
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help([[
The pdtoolkit modulefile defines the following environment variables: HMS_PDTOOLKIT_DIR

Version %{version}
]])

whatis("Name: Pdtoolkit")
whatis("Version: %{version}")
whatis("Category: debugger, program analysis")
whatis("Keywords: System, debugger,pdt")
whatis("Description:  Program Database Toolkit (PDT) is a framework for analyzing source code written in several programming languages and for making rich program knowledge accessible to developers of static and dynamic analysis tools.")
whatis("URL: http://www.cs.uoregon.edu/research/tau/pdt/home.php")

setenv( "HMS_PDTOOLKIT_DIR", "%{INSTALL_DIR}")

EOF

%files 
%defattr(775,rc200,rccg,775)
%{INSTALL_DIR}
%{MODULE_DIR}

%post

%postun

%clean
rm -rf $RPM_BUILD_ROOT
