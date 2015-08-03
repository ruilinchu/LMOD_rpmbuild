#
# NAMD-2.10 with openmpi 1.8.4 May 13, 2015, Jimi Chu
#
Summary:   NAMD scalable molecular dynamics
Name:       NAMD
Version:    2.10
Release:    0
License:    GPL
Vendor:     Beckman Institute for Advanced Science and Technology 
Group:      molecular dynamics
Source:     NAMD_CVS-2015-05-12_Source.tar.gz
Packager:   HMS - jimi_chu@hms.harvard.edu
AutoReqProv: no
%define debug_package %{nil}

%description 
NAMD, recipient of a 2002 Gordon Bell Award and a 2012 Sidney Fernbach Award, is a parallel molecular dynamics code designed for high-performance simulation of large biomolecular systems.

## MUST set ONLY one of the three to 1
%define dep_mpi 1
%define dep_comp 0
%define is_core 0

%include common.inc

%prep 
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup  -n NAMD_CVS-2015-05-12_Source

%build
mkdir -p             %{INSTALL_DIR}
mkdir -p             $RPM_BUILD_ROOT/%{INSTALL_DIR}

module purge
module load gcc/4.8.2
module load openmpi/1.8.4

tar xf charm-6.6.1.tar
cd charm-6.6.1
env MPICXX=mpicxx ./build charm++ mpi-linux-x86_64 --with-production --build-shared
cd ..
wget http://www.ks.uiuc.edu/Research/namd/libraries/fftw-linux-x86_64.tar.gz
  tar xzf fftw-linux-x86_64.tar.gz
  mv linux-x86_64 fftw
  wget http://www.ks.uiuc.edu/Research/namd/libraries/tcl8.5.9-linux-x86_64.tar.gz
  wget http://www.ks.uiuc.edu/Research/namd/libraries/tcl8.5.9-linux-x86_64-threaded.tar.gz
  tar xzf tcl8.5.9-linux-x86_64.tar.gz
  tar xzf tcl8.5.9-linux-x86_64-threaded.tar.gz
  mv tcl8.5.9-linux-x86_64 tcl
  mv tcl8.5.9-linux-x86_64-threaded tcl-threaded
./config Linux-x86_64-g++ --charm-arch mpi-linux-x86_64
sed -i 's+-module CkLoop+ +g' Makefile
sed -i 's+-DUSE_CKLOOP=1+ +g' Makefile

  cd Linux-x86_64-g++
  gmake -j12
rm Make*
rm src
rm sb
rm plugins
cp -r * %{INSTALL_DIR}

cp    -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
##finish build 

##Make module file
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help([[
Module %{name} loads environmental variables defining the location of the NAMD libraries: HMS_NAMD_DIR

Version %{version}
]])

whatis( "NAMD" )
whatis( "Version: %{version}")
whatis( "Category: molecular dynamics")
whatis( "Keywords: molecular dynamics, namd")
whatis( "Description: NAMD, recipient of a 2002 Gordon Bell Award and a 2012 Sidney Fernbach Award, is a parallel molecular dynamics code designed for high-performance simulation of large biomolecular systems.")

whatis( "URL: http://www.ks.uiuc.edu/Research/namd/")

-- Export environmental variables
setenv("HMS_NAMD_DIR", "%{INSTALL_DIR}")

-- Prepend the Python directories to the adequate PATH variables
prepend_path( "PATH", "%{INSTALL_DIR}")

EOF

%files 
%defattr(775,rc200,rccg,775)
%{INSTALL_DIR}
%{MODULE_DIR}

%post

%postun

%clean
rm -rf $RPM_BUILD_ROOT
