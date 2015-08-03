#
# Tophat spec file
#
Summary:   A fast splice junction mapper for RNA-Seq reads
Name:      tophat
Version:   2.0.13
Release:   0
License:   Boost 1.0 
Vendor:    http://ccb.jhu.edu/software/tophat/index.shtml
Group:     Sequence mapping
Source:    tophat-2.0.13.tar.gz
Packager:  HMS jimi_chu@hms.harvard.edu
AutoReqProv: no

%description
TopHat is a fast splice junction mapper for RNA-Seq reads. It aligns RNA-Seq reads to mammalian-sized genomes using the ultra high-throughput short read aligner Bowtie, and then analyzes the mapping results to identify splice junctions between exons. 

TopHat is a collaborative effort among Daehwan Kim and Steven Salzberg in the Center for Computational Biology at Johns Hopkins University, and Cole Trapnell in the Genome Sciences Department at the University of Washington. TopHat was originally developed by Cole Trapnell at the Center for Bioinformatics and Computational Biology at the University of Maryland, College Park.

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
module load boost/1.49.0
module load python/2.7.9
./configure --prefix=%{INSTALL_DIR} --with-boost=$HMS_BOOST_DIR
make
make install

cp -rp %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..

##Make modulefiles

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

load("python/2.7.9")
load("bowtie/1.1.1")
load("bowtie2/2.2.4")

help([[
The tophat modulefile defines the following environment variables
HMS_TOPHAT_DIR, HMS_TOPHAT_BIN for resources. This version of tophat was built with Boost v.1.49.0.

Version %{version}
]])

whatis("Name: tophat")whatis("Version: %{version}")
whatis("Category: Sequence mapping")
whatis("Keywords: tophat, bowtie, bowtie2, mapping")
whatis("Description: TopHat is a fast splice junction mapper for RNA-Seq reads. ")
whatis("URL: http://ccb.jhu.edu/software/tophat/index.shtml")

setenv( "HMS_TOPHAT_DIR", "%{INSTALL_DIR}")
setenv( "HMS_TOPHAT_BIN", "%{INSTALL_DIR}/bin")

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
