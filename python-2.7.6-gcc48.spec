#
# python spec file
#
Summary:   python install
Name:      python
Version:   2.7.6
Release:   0
License:   GNU General Public License
Vendor:    http://www.python.org/
Group:     statistics/graphics
Source:    Python-2.7.6.tgz
Packager:  HMS- jimi_chu@hms.harvard.edu
AutoReqProv: no

%description
Python is a widely used general-purpose, high-level programming language.

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

%setup -n Python-%{version}
 
%build

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p %{INSTALL_DIR}

##make sure the modules agree with the parameters
module purge
module load gcc/4.8.2

./configure --prefix=%{INSTALL_DIR} --with-cxx-main=g++
make
make altinstall
ln -s %{INSTALL_DIR}/bin/python2.7 %{INSTALL_DIR}/bin/python

##create modulefiles
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help([[
The python modulefile defines the following environment variables
HMS_PYTHON_DIR for the location of the R distribution.

Version %{version}
]])

whatis("Name: python")
whatis("Version: %{version}")
whatis("Category: programming,scripting")
whatis("Keywords: python,programming")
whatis("Description: Python is a widely used general-purpose, high-level programming language.")
whatis("URL: http://www.python.org/")

setenv( "HMS_PYTHON_DIR", "%{INSTALL_DIR}")

-- Append/prepend path
prepend_path("PATH", "%{INSTALL_DIR}/bin")

EOF

%files 
%defattr(775,rc200,rccg,775)
%{INSTALL_DIR}
%{MODULE_DIR}

%post

%postun

%clean
rm -rf $RPM_BUILD_ROOT

