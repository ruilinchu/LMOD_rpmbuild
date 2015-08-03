#
# vcftools spec file
#
Summary:   vcftools − Utilities for the variant call format (VCF) and binary variant call format (BCF)
Name:      vcftools
Version:   0.1.12b
Release:   0
License:   LGPLv3
Vendor:    vcftools.sourceforge.net
Group:     File Manipulation
Source:    vcftools_0.1.12b.tar.gz
Packager:  HMS alex_truong@hms.harvard.edu
AutoReqProv: no

%description
vcftools is a suite of functions for use on genetic variation data in the form of VCF and BCF files. The tools provided will be used mainly to summarize data, run calculations on data, filter out data, and convert data into other useful file formats.

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

%setup -n %{name}_%{version}
 
##
## BUILD
##

%build
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p %{INSTALL_DIR}

##make sure the modules agree with the parameters!
module purge
module load gcc/4.8.2

make PREFIX=%{INSTALL_DIR}
 
cp -rp %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..

##create modulefiles
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help([[
The vcftools modulefile describes the environmental variables HMS_VCFTOOLS_BIN and HMS_VCFTOOLS_LIB for resources. 

Version %{version}
]])

whatis("Name: vcftools")
whatis("Version: %{version}")
whatis("Category: file manipulation")
whatis("Keywords: file, files, vcftools tools")
whatis("Description: vcftools is a suite of functions for use on genetic variation data in the form of VCF and BCF files. The tools provided will be used mainly to summarize data, run calculations on data, filter out data, and convert data into other useful file formats. ")
whatis("URL: http://vcftools.sourceforge.net")

setenv( "HMS_VCFTOOLS_DIR", "%{INSTALL_DIR}")
setenv( "HMS_VCFTOOLS_BIN", "%{INSTALL_DIR}/bin")
setenv( "HMS_VCFTOOLS_LIB", "%{INSTALL_DIR}/lib")


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
