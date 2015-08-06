#
# gsl spec file
#
Summary:   Gnu GSL library
Name:      gsl
Version:   1.16
Release:   0
License:   GPLv2
Vendor:    http://www.gnu.org/software/gsl/
Group:     library
Source:    gsl-1.16.tar.gz
Packager:  HMS jimi_chu@hms.harvard.edu
AutoReqProv: no

%description
The GNU Scientific Library (GSL) is a numerical library for C and C++ programmers. It is free software under the GNU General Public License.The library provides a wide range of mathematical routines such as random number generators, special functions and least-squares fitting. There are over 1000 functions in total with an extensive test suite.

## MUST set ONLY one of the three to 1
%define dep_mpi 0
%define dep_comp 0
%define is_core 1

%include common.inc

%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

## SETUP -n the actual folder name

%setup -n %{name}-%{version}
 
## BUILD

%build
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/
mkdir -p %{INSTALL_DIR}/lib
mkdir -p %{INSTALL_DIR}/include

##make sure the modules agree with the parameters!
module purge
./configure --prefix=%{INSTALL_DIR}
make
make install

cp -rp %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..

##create modulefiles
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help([[
The gsl modulefile defines the following environment variables
HMS_GSL_LIB, and HMS_GSL_INC for the location of the Gnu GSL module.

Version %{version}
]])

whatis("Name: gsl")
whatis("Version: %{version}")
whatis("Category: library")
whatis("Keywords: gnu, gsl, library")
whatis("Description: The GNU Scientific Library (GSL) is a numerical library for C and C++ programmers. The library provides a wide range of mathematical routines such as random number generators, special functions and least-squares fitting. There are over 1000 functions in total with an extensive test suite.")
whatis("URL: http://www.threadingbuildingblocks.org")

setenv( "HMS_GSL_DIR", "%{INSTALL_DIR}")
setenv( "HMS_GSL_LIB", "%{INSTALL_DIR}/lib")
setenv( "HMS_GSL_INC", "%{INSTALL_DIR}/include")

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
