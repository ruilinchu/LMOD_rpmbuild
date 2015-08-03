#
# BLAST (BLAST+) spec file
#
Summary:   BLAST finds regions of similarity between biological sequences.
Name:      BLAST+
Version:   2.2.30+
Release:   0
License:   BLAST is a registered Trademark of the National Library of Medicine. 
Vendor:    http://blast.ncbi.nlm.nih.gov/
Group:     Sequence Alignment
Source:    ncbi-blast-2.2.30+-src.tar.gz
Packager:  HMS alex_truong@hms.harvard.edu
AutoReqProv: no

%description
The Basic Local Alignment Search Tool (BLAST) is the most widely used sequence similarity tool. There are versions of BLAST that compare protein queries to protein databases, nucleotide queries to nucleotide databases, as well as versions that translate nucleotide queries or databases in all six frames and compare to protein databases or queries. PSI-BLAST produces a position-specific-scoring-matrix (PSSM) starting with a protein query, and then uses that PSSM to perform further searches. It is also possible to compare a protein or nucleotide query to a database of PSSM’s. The NCBI supports a BLAST web page at blast.ncbi.nlm.nih.gov as well as a network service. The NCBI also distributes stand-alone BLAST applications for users who wish to run BLAST on their own machines or with their own databases. 

## MUST set ONLY one of the three to 1
%define dep_mpi 0
%define dep_comp 1
%define is_core 0

%include common.inc

%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

## SETUP

%setup -n ncbi-blast-%{version}-src

## BUILD

%build
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p %{INSTALL_DIR}

##make sure the modules agree with the parameters!
module purge
module load gcc/4.8.2
module load boost/1.57.0

cd c++

sed -i '0,/RE/s/--with-mt/--with-mt --with-boost=$HMS_BOOST_DIR/' configure

./configure

cd ReleaseMT/build

make -j8 all_r

mkdir -p %{INSTALL_DIR}/inc
mkdir -p %{INSTALL_DIR}/lib
mkdir -p %{INSTALL_DIR}/bin
mkdir -p %{INSTALL_DIR}/status

cp -r ../inc/* %{INSTALL_DIR}/inc
cp -r ../lib/* %{INSTALL_DIR}/lib
cp -r ../bin/* %{INSTALL_DIR}/bin
cp -r ../status/* %{INSTALL_DIR}/status

cp -rp %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..

##Make modulefiles

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help([[
The BLAST(+) modulefile defines the following environment variables
HMS_BLASTPLUS_DIR, HMS_BLASTPLUS_BIN and HMS_BLASTPLUS_LIB for resources.

Version %{version}
]])

whatis("Name: BLAST+")whatis("Version: %{version}")
whatis("Category: Sequence Alignment")
whatis("Keywords: blast, blast+, sequence, alignment")
whatis("Description: BLAST finds regions of similarity between biological sequences. ")
whatis("URL: http://blast.ncbi.nlm.nih.gov/")

setenv( "HMS_BLASTPLUS_DIR", "%{INSTALL_DIR}")
setenv( "HMS_BLASTPLUS_BIN", "%{INSTALL_DIR}/bin")
setenv( "HMS_BLASTPLUS_INC", "%{INSTALL_DIR}/inc")
setenv( "HMS_BLASTPLUS_LIB", "%{INSTALL_DIR}/lib")
setenv( "HMS_BLASTPLUS_STATUS", "%{INSTALL_DIR}/status")

-- Append path
prepend_path("PATH", "%{INSTALL_DIR}/bin")
prepend_path("LD_LIBRARY_PATH", "%{INSTALL_DIR}/lib")
EOF

%files 
%defattr(775,at237,rccg,775)
%{INSTALL_DIR}
%{MODULE_DIR}

%post

%postun

%clean
rm -rf $RPM_BUILD_ROOT
