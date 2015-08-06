#
# plink spec file
#
Summary:   A free, open-source whole genome association analysis toolset
Name:      plink
Version:   1.07
Release:   0
License:   GNU v2 
Vendor:    http://pngu.mgh.harvard.edu/~purcell/plink/
Group:     Genome Association
Source:    plink-1.07-src.zip
Packager:  HMS alex_truong@hms.harvard.edu
AutoReqProv: no

%description
PLINK is a free, open-source whole genome association analysis toolset, designed to perform a range of basic, large-scale analyses in a computationally efficient manner.
The focus of PLINK is purely on analysis of genotype/phenotype data, so there is no support for steps prior to this (e.g. study design and planning, generating genotype or CNV calls from raw data). Through integration with gPLINK and Haploview, there is some support for the subsequent visualization, annotation and storage of results.
PLINK (one syllable) is being developed by Shaun Purcell at the Center for Human Genetic Research (CHGR), Massachusetts General Hospital (MGH), and the Broad Institute of Harvard & MIT, with the support of others.

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

##
## SETUP
##

%setup -n %{name}-%{version}-src
 
##
## BUILD
##

%build
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p %{INSTALL_DIR}/bin

##make sure the modules agree with the parameters!
module purge
module load gcc/4.4.7
module load openblas/0.2.13

sed -i '0,/RE/s/WITH_LAPACK =/WITH_LAPACK = 1/' Makefile
sed -i '0,/RE/s/FORCE_DYNAMIC =/FORCE_DYNAMIC = 1/' Makefile
sed -i '0,/RE/s/LIB_LAPACK = \/usr\/lib\/liblapack.so.3/LIB_LAPACK = -L$(HMS_OPENBLAS_LIB) -lopenblas/' Makefile

make

cp plink %{INSTALL_DIR}/bin
 
cp -rp %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..


##create modulefiles
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help([[
The plink modulefile defines the following environment variable
HMS_PLINK_BIN for the location of the plink binary.

Version %{version}
]])

whatis("Name: plink")
whatis("Version: %{version}")
whatis("Category: Genome Association")
whatis("Keywords: plink, genome, analysis, association, toolkit")
whatis("Description: PLINK is a free, open-source whole genome association analysis toolset, designed to perform a range of basic, large-scale analyses in a computationally efficient manner. ")
whatis("URL: http://pngu.mgh.harvard.edu/~purcell/plink/")

setenv( "HMS_PLINK_DIR", "%{INSTALL_DIR}")
setenv( "HMS_PLINK_BIN", "%{INSTALL_DIR}/bin")

-- Append path
prepend_path("PATH", "%{INSTALL_DIR}/bin")
EOF

%files 
%defattr(775,at237,rccg,-)
%{INSTALL_DIR}
%{MODULE_DIR}

%post

%postun

%clean
rm -rf $RPM_BUILD_ROOT
