#
# gromacs-5.0.4 spec, Feb 3, 2015, Jimi Chu
#
Summary:   GROningen MAchine for Chemical Simulations
Name:       gromacs
Version:    5.0.4
Release:    gcc48_openmpi18
License:    GPL
Vendor:     The GROMACS development teams at the Royal Institute of Technology and Uppsala University, Sweden
Group:      molecular dynamics
Source:     gromacs-%{version}.tar.gz
Packager:   HMS - jimi_chu@hms.harvard.edu
AutoReqProv: no
%define debug_package %{nil}

%description 
Gromacs is a molecular dynamics package primarily designed for simulations of proteins, lipids and nucleic acids. It was originally developed in the Biophysical Chemistry department of University of Groningen, and is now maintained by contributors in universities and research centers across the world. GROMACS is one of the fastest and most popular software packages available, and can run on CPUs as well as GPUs. It is free, open source released under the GNU General Public License.

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

%setup  -n %{name}-%{version}

%build
mkdir -p             %{INSTALL_DIR}
mkdir -p             $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p BUILD
cd BUILD

module purge
module load gcc/4.8.2
module load openmpi/1.8.4
module load openblas/0.2.13

cmake .. -DCMAKE_C_COMPILER=mpicc -DCMAKE_CXX_COMPILER=mpicxx -DGMX_GPU=off -DGMX_BUILD_OWN_FFTW=ON -DGMX_MPI=on -DCMAKE_INSTALL_PREFIX=%{INSTALL_DIR} -DGMX_BLAS_USER=$HMS_OPENBLAS_LIB/libopenblas.a 
make -j 8
make install

cp    -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
##finish build 

##begin module stuff
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
load("openblas/0.2.13")    
help([[
Module %{name} loads environmental variables defining the location of the GROMACS libraries: 
HMS_GROMACS_DIR, HMS_GROMACS_LIB, HMS_GROMACS_INC

It also updates the values of the PATH and the LD_LIBRARY_PATH variables to use gromacs.

Version %{version}
]])

whatis( "GROMACS" )
whatis( "Version: %{version}")
whatis( "Category: molecular dynamics")
whatis( "Keywords: molecular dynamics, gromacs")
whatis( "Description: GROMACS is a molecular dynamics package primarily designed for simulations of proteins, lipids and nucleic acids. GROMACS is one of the fastest and most popular software packages available.")

whatis( "URL: http://www.gromacs.org")

-- Export environmental variables
setenv("HMS_GROMACS_DIR", "%{INSTALL_DIR}")
setenv("HMS_GROMACS_INC", "%{INSTALL_DIR}/include")
setenv("HMS_GROMACS_LIB", "%{INSTALL_DIR}/lib64")

-- Prepend the Python directories to the adequate PATH variables
prepend_path( "PATH", "%{INSTALL_DIR}/bin")
prepend_path( "LD_LIBRARY_PATH", "%{INSTALL_DIR}/lib64")

EOF

%files 
%defattr(-,rc200,rccg,-)
%{INSTALL_DIR}
%{MODULE_DIR}

%post

%postun

%clean
rm -rf $RPM_BUILD_ROOT
