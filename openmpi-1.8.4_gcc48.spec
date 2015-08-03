#
# Openmpi_gc48 spec file
#
Summary:   Openmpi_gcc48 install
Name:      openmpi
Version:   1.8.4
Release:   0
License:   GNU General Public License
Vendor:    http://www.open-mpi.org
Group:     system/hpc/mpi
Source:    openmpi-1.8.4.tar.gz
Packager:  HMS- jimi_chu@hms.harvard.edu
AutoReqProv: no

%description
The Open MPI Project is an open source Message Passing Interface implementation that is
developed and maintained by a consortium of academic, research, and industry partners. 

%define debug_package %{nil}

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
%define dep_mpi 0
%define dep_comp 1
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
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{name}-%{version}
 
%build

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p %{INSTALL_DIR}

module purge
module load gcc/4.8.2

./configure --prefix=%{INSTALL_DIR} --enable-mpirun-prefix-by-default
make all install
 
cp -rp %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..

##create modulefiles
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}

cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help([[
The openmpi modulefile defines the following environment variables
HMS_OPENMPI_BIN, HMS_OPENMPI_LIB, and HMS_OPENMPI_INC for the location
of the Openmpi distribution, documentation, binaries, libraries, and 
include files, respectively.

To use the openmpi library, include compilation directives
of the form: -L$HMS_OPENMPI_LIB -I$HMS_OPENMPI_INC -lmpi

Here is an example command to compile openmpi_test.c:
gcc -I\$HMS_OPENMPI_INC openmpi_test.c -L\$HMS_OPENMPI_LIB -lmpi

Version %{version}
]])

whatis("Name: OPENMPI")
whatis("Version: %{version}")
whatis("Category: system/hpc/mpi")
whatis("Keywords: MPI ")
whatis("Description: The Open MPI Project is an open source Message Passing Interface implementation.")
whatis("URL: http://www.open-mpi.org")

setenv( "HMS_OPENMPI_DIR", "%{INSTALL_DIR}")
setenv( "HMS_OPENMPI_BIN", "%{INSTALL_DIR}/bin")
setenv( "HMS_OPENMPI_INC", "%{INSTALL_DIR}/include")
setenv( "HMS_OPENMPI_LIB", "%{INSTALL_DIR}/lib")

-- prepend path
prepend_path("PATH", "%{INSTALL_DIR}/bin")
prepend_path("LD_LIBRARY_PATH","%{INSTALL_DIR}/lib")

--setup modulepath for this MPI stack ## only required for gcc, intel, openmpi, mpich, etc
local mroot = os.getenv("MODULEPATH_ROOT")
local mdir = pathJoin(mroot,"MPI", "%{comp_fam}", "%{comp_ver}","%{name}","%{version}")
prepend_path("MODULEPATH", mdir)


EOF

%files 
%defattr(755,rc200,rccg)
%{INSTALL_DIR}
%{MODULE_DIR}

%post

%postun

%clean
rm -rf $RPM_BUILD_ROOT

