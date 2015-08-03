#
# BWA spec file
#
Summary:   Installation of BWA
Name:      bwa
Version:   0.7.12
Release:   gcc48
License:   GNU General Public License
Vendor:    https://github.com/lh3/bwa
Group:     seq/align
Source:    bwa-0.7.12.tgz
Packager:  HMS- nam_pho@hms.harvard.edu
AutoReqProv: no

%description
Burrow-Wheeler Aligner for pairwise alignment between DNA sequences 

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

%setup -n bwa-%{version}
 
%build

mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}/bin
mkdir -p %{INSTALL_DIR}/bin

# no special configurations req'd
cat >> config.site << 'EOF'

EOF

##make sure the modules agree with the parameters
module purge
module load gcc/4.8.2
#module load openblas/0.2.13

#./configure --prefix=%{INSTALL_DIR} --with-blas --with-lapack --with-x=no
make PREFIX=%{INSTALL_DIR}/bin/ bwa
make PREFIX=%{INSTALL_DIR}/bin/ bwamem-lite
#make install

cp -rp %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..

##create modulefiles
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help([[
This is the bwa modulefile.

Version %{version}
]])

whatis("Name: %{program}")
whatis("Version: %{version}")
whatis("Category: statistics")
whatis("Keywords: seq, align, ")
whatis("Description: Burrow-Wheeler Aligner for pairwise alignment between DNA sequences ")
whatis("URL: %{vendor}")

-- Append/prepend path
prepend_path("PATH", "%{INSTALL_DIR}/bin")

EOF

%files 
%defattr(-,np106,rccg,-)
%{INSTALL_DIR}
%{MODULE_DIR}

%post

%postun

%clean
rm -rf $RPM_BUILD_ROOT

