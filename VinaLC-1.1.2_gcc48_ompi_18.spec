#
# VinaLC-1.1.2 spec, Feb 3, 2015, Jimi Chu
#
Summary:   VinaLC Parallel Molecular Docking Program
Name:       VinaLC
Version:    1.1.2
Release:    gcc48_openmpi18
License:    GPL
Vendor:     http://mvirdb1.llnl.gov/static_catsid/vina/
Group:      molecule dynamics
Source:     VinaLC-%{version}.tar.gz
Packager:   HMS - jimi_chu@hms.harvard.edu
AutoReqProv: no
%define debug_package %{nil}

%description 
A very popular PC-based molecular docking program, AutoDock Vina, was modified and parallelized, using an MPI and multithreading hybrid scheme, and potentially can be used in the future on exascale machines, without sacrificing accuracy. The resulting program scales up to more than 15K CPUs with a very low overhead cost.

%define comp_fam gcc
%define comp_ver 4.8.2
%define mpi_fam openmpi
%define mpi_ver 1.8.4

##do not modify these
%define APPS        /opt/centos/apps
%define MODULES     modulefiles 
%define comp_fam_ver %{comp_fam}-%{comp_ver}
%define mpi_fam_ver %{mpi_fam}-%{mpi_ver}
%define set_tree error
##end do not

## MUST set ONLY one of the three to 1
%define dep_mpi 1
%define dep_comp 0
%define is_core 0

##do not change these
%if "%{is_core}" == "1"
    %define PKG_BASE    %{APPS}/%{name}
    %define INSTALL_DIR %{PKG_BASE}/%{version}
    %define MODULE_DIR  %{APPS}/%{MODULES}/Core/%{name}
    %define set_tree 1
%endif

%if "%{dep_comp}" == "1"
    %define PKG_BASE    %{APPS}/%{comp_fam_ver}/%{name}
    %define INSTALL_DIR %{PKG_BASE}/%{version}                    
    %define MODULE_DIR  %{APPS}/%{MODULES}/Compiler/%{comp_fam}/%{comp_ver}/%{name}
    %define set_tree 1
%endif

%if "%{dep_mpi}" == "1"
    %define PKG_BASE    %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{name}
    %define INSTALL_DIR %{PKG_BASE}/%{version}
    %define MODULE_DIR  %{APPS}/%{MODULES}/MPI/%{comp_fam}/%{comp_ver}/%{mpi_fam}/%{mpi_ver}/%{name}
    %define set_tree 1
%endif

%if "%{set_tree}" == "error"
     %{error: You must set the compiler/mpi/core tree !}
     exit
%endif
##end do not

%prep 
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup  -n VinaLC

%build
mkdir -p             %{INSTALL_DIR}
mkdir -p             $RPM_BUILD_ROOT/%{INSTALL_DIR}

module purge
module load gcc/4.8.2
module load openmpi/1.8.4
module load boost/1.57.0

./configure --with-boost=$HMS_BOOST_DIR --with-mpi=$HMS_OPENMPI_DIR --prefix=%{INSTALL_DIR}
make
make install

cp    -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
##finish build 

##begin module stuff
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
load("boost/1.57.0")    
help([[
Module %{name} loads environmental variables defining the location of the VINALC libraries: 
HMS_VINALC_DIR, HMS_VINALC_BIN

It also updates the values of the PATH and the LD_LIBRARY_PATH variables to use VinaLC.

Version %{version}
]])

whatis( "VINALC" )
whatis( "Version: %{version}")
whatis( "Category: molecule docking")
whatis( "Keywords: molecule, VinaLC")
whatis( "Description: A very popular PC-based molecular docking program, AutoDock Vina, was modified and parallelized, using an MPI and multithreading hybrid scheme, and potentially can be used in the future on exascale machines, without sacrificing accuracy. The resulting program scales up to more than 15K CPUs with a very low overhead cost.")

whatis( "URL: http://mvirdb1.llnl.gov/static_catsid/vina/")

-- Export environmental variables
setenv("HMS_VINALC_DIR", "%{INSTALL_DIR}")
setenv("HMS_VINALC_BIN", "%{INSTALL_DIR}/bin")

-- Prepend the Python directories to the adequate PATH variables
prepend_path( "PATH", "%{INSTALL_DIR}/bin")
prepend_path( "LD_LIBRARY_PATH", "%{INSTALL_DIR}/lib")

EOF

%files 
%defattr(-,rc200,rccg,-)
%{INSTALL_DIR}
%{MODULE_DIR}

%post

%postun

%clean
rm -rf $RPM_BUILD_ROOT
