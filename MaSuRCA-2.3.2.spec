#
# MaSuRCA spec file
#
Summary:   MaSuRCA assembler  
Name:      MaSuRCA
Version:   2.3.2
Release:   0
License:   GPL
Vendor:    The University of Maryland Genome Assembly Group
Group:     genome assembly
Source:    MaSuRCA-2.3.2.tar.gz
Packager:  HMS jimi_chu@hms.harvard.edu
AutoReqProv: no

%description
MaSuRCA is whole genome assembly software. It combines the efficiency of the de Bruijn graph and Overlap-Layout-Consensus (OLC) approaches. MaSuRCA can assemble data sets containing only short reads from Illumina sequencing or a mixture of short reads and long reads (Sanger, 454).

## MUST set ONLY one of the three to 1
%define dep_mpi 0
%define dep_comp 1
%define is_core 0

%include common.inc

%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

## SETUP

%setup -n %{name}-%{version}

## BUILD

%build
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p %{INSTALL_DIR}

##make sure the modules agree with the parameters!
module purge
module load gcc/4.8.2

DEST=%{INSTALL_DIR} ./install.sh

cp -rp %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..

##Make modulefiles

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help([[
The MaSuRCA modulefile defines the following environment variables:
HMS_MASURCA_DIR, HMS_MASURCA_BIN, HMS_MASURCA_LIB

Version %{version}
]])

whatis("Name: MaSuRCA")
whatis("Version: %{version}")
whatis("Category: genome assembly")
whatis("Keywords: masurca, assembly")
whatis("Description: MaSuRCA is whole genome assembly software. It combines the efficiency of the de Bruijn graph and Overlap-Layout-Consensus (OLC) approaches. MaSuRCA can assemble data sets containing only short reads from Illumina sequencing or a mixture of short reads and long reads (Sanger, 454).")
whatis("URL: http://www.genome.umd.edu/masurca.html")

setenv( "HMS_MASURCA_DIR", "%{INSTALL_DIR}")
setenv( "HMS_MASURCA_BIN", "%{INSTALL_DIR}/bin")
setenv( "HMS_MASURCA_LIB", "%{INSTALL_DIR}/lib")

-- prepend path
prepend_path("PATH", "%{INSTALL_DIR}/bin")
prepend_path("LD_LIBRARY_PATH", "%{INSTALL_DIR}/lib")
EOF

%files 
%defattr(775,rc200,rccg,775)
%{INSTALL_DIR}
%{MODULE_DIR}

%post

%postun

%clean
rm -rf $RPM_BUILD_ROOT
