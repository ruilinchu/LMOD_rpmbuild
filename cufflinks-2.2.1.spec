#
# cufflinks spec file
#
Summary:   cufflinks
Name:      cufflinks
Version:   2.2.1
Release:   0
License:   GPL
Vendor:    cufflinks
Group:     RNA-Seq
Source:    cufflinks-2.2.1.tar.gz
Packager:  HMS jimi_chu@hms.harvard.edu
AutoReqProv: no

%description
Cufflinks assembles transcripts, estimates their abundances, and tests for differential expression and regulation in RNA-Seq samples.

## MUST set ONLY one of the three to 1
%define dep_mpi 0
%define dep_comp 1
%define is_core 0

%include common.inc
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
module load eigen
module load samtools/1.2
module load boost/1.49.0

sed -i 's+-lbam+$HMS_SAMTOOLS_LIB/libbam.a $HMS_SAMTOOLS_LIB/libhts.a+g' configure
sed -i 's+-L$ac_bam_path_tmp/lib+ +g' configure
sed -i 's+ac_bam_path_tmp/include+HMS_SAMTOOLS_INC+g' configure
./configure --prefix=%{INSTALL_DIR} --with-boost=$HMS_BOOST_DIR --with-eigen=$HMS_EIGEN_DIR
make
make install
 
cp -rp %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..

##create modulefiles
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'
load("boost/1.49.0")
help([[
The cufflinks modulefile defines the following environment variables
HMS_CUFFLINKS_DIR for the location of the cufflinks distribution.

Version %{version}
]])

whatis("Name: Cufflinks")
whatis("Version: %{version}")
whatis("Category: RNA-Seq,seq")
whatis("Keywords: RNA-Seq,cufflinks")
whatis("Description: Cufflinks Cufflinks assembles transcripts, estimates their abundances, and tests for differential expression and regulation in RNA-Seq samples")
whatis("URL: http://cole-trapnell-lab.github.io/cufflinks/")

setenv( "HMS_CUFFLINKS_DIR", "%{INSTALL_DIR}")
setenv( "HMS_CUFFLINKS_BIN", "%{INSTALL_DIR}/bin")

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
