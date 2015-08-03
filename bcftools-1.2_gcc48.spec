#
# bcftools spec file
#
Summary:   bcftools — utilities for variant calling and manipulating VCFs and BCFs.
Name:      bcftools
Version:   1.2
Release:   0
License:   MIT/Expat or GNU
Vendor:    htslib.org
Group:     file manipulation
Source:    bcftools-1.2.tar.bz2
Packager:  HMS alex_truong@hms.harvard.edu
AutoReqProv: no

%description
BCFtools is a set of utilities that manipulate variant calls in the Variant Call Format (VCF) and its binary counterpart BCF. All commands work transparently with both VCFs and BCFs, both uncompressed and BGZF-compressed.

Most commands accept VCF, bgzipped VCF and BCF with filetype detected automatically even when streaming from a pipe. Indexed VCF and BCF will work in all situations. Un-indexed VCF and BCF and streams will work in most, but not all situations.

BCFtools is designed to work on a stream. It regards an input file "-" as the standard input (stdin) and outputs to the standard output (stdout). Several commands can thus be combined with Unix pipes.

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

%setup -n %{name}-%{version}
 
##
## BUILD
##

%build
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p %{INSTALL_DIR}

##make sure the modules agree with the parameters!
module purge
module load gcc/4.8.2
make
make install prefix=%{INSTALL_DIR}
 
cp -rp %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..

##create modulefiles
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help([[
The bcftools modulefile defines the following environment variables
HMS_BCFTOOLS_DIR, HMS_BCFTOOLS_BIN, and HMS_BCFTOOLS_SHARE for resources.

Version %{version}
]])

whatis("Name: bcftools")whatis("Version: %{version}")
whatis("Category: File Manipulation")
whatis("Keywords: samtools, bcftools, file, files")
whatis("Description: bcftools — utilities for variant calling and manipulating VCFs and BCFs")
whatis("URL: http://www.htslib.org")

setenv( "HMS_BCFTOOLS_DIR", "%{INSTALL_DIR}")
setenv( "HMS_BCFTOOLS_BIN", "%{INSTALL_DIR}/bin")
setenv( "HMS_BCFTOOLS_SHARE", "%{INSTALL_DIR}/share")

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
