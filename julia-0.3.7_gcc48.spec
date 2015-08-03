#
# Julia spec file
#
Summary:   Julia - a high-level, high-performance dynamic programming language for technical computing
Name:      julia
Version:   0.3.7
Release:   0
License:   MIT 
Vendor:    http://julialang.org/
Group:     Programming Language
Source:    julia-0.3.7_cb9bcae93a.tar.gz
Packager:  HMS alex_truong@hms.harvard.edu
AutoReqProv: no

%description
Julia is a high-level, high-performance dynamic programming language for technical computing, with syntax that is familiar to users of other technical computing environments. It provides a sophisticated compiler, distributed parallel execution, numerical accuracy, and an extensive mathematical function library. The library, largely written in Julia itself, also integrates mature, best-of-breed C and Fortran libraries for linear algebra, random number generation, signal processing, and string processing. In addition, the Julia developer community is contributing a number of external packages through Julia’s built-in package manager at a rapid pace. IJulia, a collaboration between the IPython and Julia communities, provides a powerful browser-based graphical notebook interface to Julia.

## MUST set ONLY one of the three to 1
%define dep_mpi 0
%define dep_comp 1
%define is_core 0

%include common.inc

%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

## SETUP

%setup -n %{name}

## BUILD

%build
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p %{INSTALL_DIR}

##make sure the modules agree with the parameters!
module purge
module load gcc/4.8.2
module load openblas/0.2.13
module load fftw/3.3.4

{
echo 'OPENBLAS_TARGET_ARCH=NEHALEM'
echo 'OPENBLAS_DYNAMIC_ARCH=0'
echo 'override USE_SYSTEM_BLAS=1'
echo 'override LIBBLAS = -L/opt/centos/apps/openblas/0.2.13/lib -lopenblas'
echo 'override LIBBLASNAME = libopenblas'
echo 'USE_BLAS64=0'
echo 'override USE_SYSTEM_LAPACK=1'
echo 'override LIBLAPACK = $(LIBBLAS)'
echo 'override LIBLAPACKNAME = $(LIBBLASNAME)'
echo 'override USE_SYSTEM_FFTW=1'
} > Make.user

make -j12
make install prefix=%{INSTALL_DIR}

cp -rp %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..

##Make modulefiles

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

load("openblas","fftw")
help([[
The julia modulefile defines the following environment variables
HMS_JULIA_DIR and HMS_JULIA_BIN for primary resources.

Version %{version}
]])

whatis("Name: Julia")
whatis("Version: %{version}")
whatis("Category: Programming Language")
whatis("Keywords: language, computing, julia")
whatis("Description: Julia - a high-level, high-performance dynamic programming language for technical computing ")
whatis("URL: http://julialang.org/")

setenv( "HMS_JULIA_DIR", "%{INSTALL_DIR}")
setenv( "HMS_JULIA_BIN", "%{INSTALL_DIR}/bin")

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
