#
# Samtools spec file
#
Summary:   samtools – Utilities for the Sequence Alignment/Map (SAM) format
Name:      samtools
Version:   1.2
Release:   0
License:   MIT/Expat 
Vendor:    htslib.org
Group:     file manipulation
Source:    samtools-1.2.tar.bz2
Packager:  HMS jimi_chu@hms.harvard.edu
AutoReqProv: no

%description
Samtools is a set of utilities that manipulate alignments in the BAM format. It imports from and exports to the SAM (Sequence Alignment/Map) format, does sorting, merging and indexing, and allows to retrieve reads in any regions swiftly.

Samtools is designed to work on a stream. It regards an input file `-' as the standard input (stdin) and an output file `-' as the standard output (stdout). Several commands can thus be combined with Unix pipes. Samtools always output warning and error messages to the standard error output (stderr).

Samtools is also able to open a BAM (not SAM) file on a remote FTP or HTTP server if the BAM file name starts with `ftp://' or `http://'. Samtools checks the current working directory for the index file and will download the index upon absence. Samtools does not retrieve the entire alignment file unless it is asked to do so.


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
make
make install prefix=%{INSTALL_DIR}

mkdir -p %{INSTALL_DIR}/include/bam
mkdir -p %{INSTALL_DIR}/lib

cp *.h %{INSTALL_DIR}/include/bam
cp -r htslib-1.2.1/htslib %{INSTALL_DIR}/include

cp *.a %{INSTALL_DIR}/lib
cp htslib-1.2.1/*.a %{INSTALL_DIR}/lib

cp -rp %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..

##Make modulefiles

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help([[
The samtools modulefile defines the following environment variables
HMS_SAMTOOLS_DIR, HMS_SAMTOOLS_BIN, HMS_SAMTOOLS_INC, HMS_SAMTOOLS_LIB, and HMS_SAMTOOLS_SHARE for resources.

Version %{version}
]])

whatis("Name: samtools")
whatis("Version: %{version}")
whatis("Category: File Manipulation")
whatis("Keywords: samtools, file, files")
whatis("Description: samtools – Utilities for the Sequence Alignment/Map (SAM) format ")
whatis("URL: http://www.htslib.org")

setenv( "HMS_SAMTOOLS_DIR", "%{INSTALL_DIR}")
setenv( "HMS_SAMTOOLS_BIN", "%{INSTALL_DIR}/bin")
setenv( "HMS_SAMTOOLS_INC", "%{INSTALL_DIR}/include")
setenv( "HMS_SAMTOOLS_LIB", "%{INSTALL_DIR}/lib")
setenv( "HMS_SAMTOOLS_SHARE", "%{INSTALL_DIR}/share")

-- Append path
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
