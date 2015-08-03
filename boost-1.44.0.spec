#
# boost-1.44.0 spec, Feb 3, 2015, Jimi Chu
#
Summary:   Boost c++ library
Name:       boost
Version:    1.44.0
Release:    0
License:    Boost Software License
Vendor:     boost.org
Group:      library, c++
Source:     boost_1_44_0.tar.gz
Packager:   HMS - alex_truong@hms.harvard.edu
AutoReqProv: no
%define debug_package %{nil}

%description 
Boost is a set of libraries for the C++ programming language that provide support for tasks and structures such as linear algebra, pseudorandom number generation, multithreading, image processing, regular expressions, and unit testing. It contains over eighty individual libraries.

## MUST set ONLY one of the three to 1
%define dep_mpi 0
%define dep_comp 0
%define is_core 1

%include common.inc

%prep 
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup  -n boost_1_44_0

%build
mkdir -p             %{INSTALL_DIR}
mkdir -p             $RPM_BUILD_ROOT/%{INSTALL_DIR}

module purge
module load gcc/4.4.7

cat > tools/build/v2/user-config.jam << 'EOF'
using mpi ;
EOF

./bootstrap.sh --prefix=%{INSTALL_DIR} --with-python=python
./bjam install

cp    -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
##finish build 

##begin module stuff
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help([[
Module %{name} loads environmental variables defining the location of the BOOST libraries: 
HMS_BOOST_DIR, HMS_BOOST_LIB, HMS_BOOST_INC.

This boost version is built with system python (2.6.6).

It also updates the values of the PATH and the LD_LIBRARY_PATH variables to use boost.

Version %{version}
]])

whatis( "BOOST" )
whatis( "Version: %{version}")
whatis( "Category: library, c++")
whatis( "Keywords: c++, boost")
whatis( "Description: Boost is a set of libraries for the C++ programming language that provide support for tasks and structures such as linear algebra, pseudorandom number generation, multithreading, image processing, regular expressions, and unit testing. It contains over eighty individual libraries.")

whatis( "URL: http://www.boost.org")

-- Export environmental variables
setenv("HMS_BOOST_DIR", "%{INSTALL_DIR}")
setenv("HMS_BOOST_INC", "%{INSTALL_DIR}/include")
setenv("HMS_BOOST_LIB", "%{INSTALL_DIR}/lib")

-- Prepend the Python directories to the adequate PATH variables
prepend_path( "LD_LIBRARY_PATH", "%{INSTALL_DIR}/lib")

EOF

%files 
%defattr(775,at237,rccg,775)
%{INSTALL_DIR}
%{MODULE_DIR}

%post

%postun

%clean
rm -rf $RPM_BUILD_ROOT
