#
# ABySS spec file 
#
Summary:    Assembly By Short Sequences - a de novo, parallel, paired-end sequence assembler
Name:       abyss
Version:    1.5.2
Release:    0
License:    GPL-NC-3+
Vendor:     http://www.bcgsc.ca/platform/bioinfo/software/abyss
Group:      Sequence Assembly
Source:     abyss-%{version}.tar.gz
Packager:   HMS - alex_truong@hms.harvard.edu
AutoReqProv: no
%define debug_package %{nil}

%description 
ABySS is a de novo, parallel, paired-end sequence assembler that is designed for short reads. The single-processor version is useful for assembling genomes up to 100 Mbases in size. The parallel version is implemented using MPI and is capable of assembling larger genomes.

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
    %define _rpmfilename %%{ARCH}/%%{NAME}.%%{VERSION}.%%{RELEASE}.%%{ARCH}.rpm
%endif

%if "%{dep_comp}" == "1"
    %define PKG_BASE    %{APPS}/%{comp_fam_ver}/%{name}
    %define INSTALL_DIR %{PKG_BASE}/%{version}                    
    %define MODULE_DIR  %{APPS}/%{MODULES}/Compiler/%{comp_fam}/%{comp_ver}/%{name}
    %define set_tree 1
    %define _rpmfilename %%{ARCH}/%%{NAME}.%%{VERSION}.%%{RELEASE}.%{com_fam_ver}.%%{ARCH}.rpm
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
rm   -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup  -n %{name}-%{version}

%build
mkdir -p             %{INSTALL_DIR}
mkdir -p             $RPM_BUILD_ROOT/%{INSTALL_DIR}

module purge
module load gcc/4.8.2
module load openmpi/1.8.4
module load boost/1.57.0
module load sparsehash/2.0.2

./configure --prefix=%{INSTALL_DIR} --with-boost=$HMS_BOOST_INC --with-mpi=$HMS_OPENMPI_DIR CPPFLAGS=-I$HMS_SPARSEHASH_INC

make AM_CXXFLAGS=-Wall
make install

cp    -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
##finish build 

##begin module stuff
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help([[
Module %{name} loads environmental variables defining the location of the ABySS resources: 
HMS_ABYSS_DIR, HMS_ABYSS_BIN

Version %{version}
]])

whatis( "ABySS" )
whatis( "Version: %{version}")
whatis( "Category: Sequence Assembly")
whatis( "Keywords: sequence, assembly, abyss")
whatis( "Description: ABySS is a de novo, parallel, paired-end sequence assembler that is designed for short reads.")

whatis( "URL: http://www.bcgsc.ca/platform/bioinfo/software/abyss")

-- Export environmental variables
setenv("HMS_ABYSS_DIR", "%{INSTALL_DIR}")
setenv("HMS_ABYSS_BIN", "%{INSTALL_DIR}/bin")

-- Prepend the Python directories to the adequate PATH variables
prepend_path( "PATH", "%{INSTALL_DIR}/bin")

EOF

%files 
%defattr(775,at237,rccg,-)
%{INSTALL_DIR}
%{MODULE_DIR}

%post

%postun

%clean
rm -rf $RPM_BUILD_ROOT
