#
# bamtools spec file
#
Summary:   BamTools provides both a programmer's API and an end-user's toolkit for handling BAM files.
Name:      bamtools
Version:   2.3.0
Release:   0
License:   LGPLv3
Vendor:    https://github.com/pezmaster31/bamtools
Group:     File Manipulation
Source:    bamtools-2.3.0.tar.gz
Packager:  HMS lingsheng_dong@hms.harvard.edu
AutoReqProv: no

%description
BamTools provides both a programmer's API and an end-user's toolkit for handling BAM files.

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

mkdir build
cd build
export CC=gcc
export CXX=g++
cmake ..
make
cp -r ../bin %{INSTALL_DIR}
cp -r ../include %{INSTALL_DIR}
cp -r ../lib %{INSTALL_DIR}
 
cp -rp %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..

##create modulefiles
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help([[
The bamtools modulefile describes the environmental variables HMS_BAMTOOLS_BIN and HMS_BAMTOOLS_LIB for resources. 

Version %{version}
]])

whatis("Name: bamtools")
whatis("Version: %{version}")
whatis("Category: file manipulation")
whatis("Keywords: file, files, bamtools, tools")
whatis("Description: BamTools provides both a programmer's API and an end-user's toolkit for handling BAM files. ")
whatis("URL:  https://github.com/pezmaster31/bamtools")

setenv( "HMS_BAMTOOLS_DIR", "%{INSTALL_DIR}")
setenv( "HMS_BAMTOOLS_BIN", "%{INSTALL_DIR}/bin")
setenv( "HMS_BAMTOOLS_LIB", "%{INSTALL_DIR}/lib")


-- Append path
prepend_path("PATH", "%{INSTALL_DIR}/bin")
EOF

%files 
%defattr(755,ld32,rccg,775)
%{INSTALL_DIR}
%{MODULE_DIR}

%POst

%postun

%clean
rm -rf $RPM_BUILD_ROOT
