#
# mpiBLAST spec file 
#
Summary:    A freely available, open-source, parallel implementation of NCBI BLAST
Name:       mpiblast
Version:    1.6.0
Release:    0
License:    GNUv2
Vendor:     http://www.mpiblast.org/
Group:      Sequence Alignment
Source:     mpiBLAST-%{version}.tgz
Packager:   HMS - alex_truong@hms.harvard.edu
AutoReqProv: no
%define debug_package %{nil}

%description 
mpiBLAST is a freely available, open-source, parallel implementation of NCBI BLAST. By efficiently utilizing distributed computational resources through database fragmentation, query segmentation, intelligent scheduling, and parallel I/O, mpiBLAST improves NCBI BLAST performance by several orders of magnitude while scaling to hundreds of processors. mpiBLAST is also portable across many different platforms and operating systems. Lastly, a renewed focus and consolidation of the many codebases has positioned mpiBLAST to continue to be of high utility to the bioinformatics community.

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

./configure --prefix=%{INSTALL_DIR} --with-mpi=$HMS_OPENMPI_DIR 

make ncbi
make
make install

cp    -r %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..
##finish build 

##begin module stuff
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
help([[
Module %{name} loads environmental variables defining the location of the mpiBLAST resources: 
HMS_MPIBLAST_DIR, HMS_MPIBLAST_BIN

Version %{version}
]])

whatis( "mpiBLAST" )
whatis( "Version: %{version}")
whatis( "Category: Sequence Alignment")
whatis( "Keywords: sequence, alignment, mpi, blast, mpiblast")
whatis( "Description: mpiBLAST is a freely available, open-source, parallel implementation of NCBI BLAST.")

whatis( "URL: http://www.mpiblast.org/")

-- Export environmental variables
setenv("HMS_MPIBLAST_DIR", "%{INSTALL_DIR}")
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
