#
# Gatk spec file
#
Summary:   gatk – Genome Analysis Toolkit 
Name:      gatk
Version:   3.3
Release:   0
License:   MIT/Expat 
Vendor:    Broad Institute
Group:     genome analysis
Source:    gatk-3.3.tar.gz
Packager:  HMS jimi_chu@hms.harvard.edu
AutoReqProv: no

%description
The Genome Analysis Toolkit or GATK is a software package developed at the Broad Institute to analyze high-throughput sequencing data. The toolkit offers a wide variety of tools, with a primary focus on variant discovery and genotyping as well as strong emphasis on data quality assurance. Its robust architecture, powerful processing engine and high-performance computing features make it capable of taking on projects of any size.

## MUST set ONLY one of the three to 1
%define dep_mpi 0
%define dep_comp 1
%define is_core 0

%include common_java.inc

%prep
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

## SETUP

%setup -n %{name}-protected-%{version}

## BUILD

%build
mkdir -p $RPM_BUILD_ROOT/%{INSTALL_DIR}
mkdir -p %{INSTALL_DIR}

##make sure the modules agree with the parameters!
module purge
module load oracle-JDK/1.7.0.71

mvn verify
find . -name '*.jar' | xargs cp -t %{INSTALL_DIR}

cp -rp %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..

##Make modulefiles

rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help([[
The gatk modulefile defines the following environment variables
HMS_GATK_DIR for gatk resources.

Usage:
java -jar $HMS_GATK_DIR/GenomeAnalysisTK.jar -and_other_options ...

Version %{version}
]])

whatis("Name: gatk")
whatis("Version: %{version}")
whatis("Category: Genome Analysis")
whatis("Keywords: gatk, genome, high-throughput, sequencing")
whatis("Description: The Genome Analysis Toolkit or GATK is a software package developed at the Broad Institute to analyze high-throughput sequencing data. The toolkit offers a wide variety of tools, with a primary focus on variant discovery and genotyping as well as strong emphasis on data quality assurance. Its robust architecture, powerful processing engine and high-performance computing features make it capable of taking on projects of any size.")
whatis("URL: https://www.broadinstitute.org/gatk/")

setenv( "HMS_GATK_DIR", "%{INSTALL_DIR}")

EOF

%files 
%defattr(775,rc200,rccg,775)
%{INSTALL_DIR}
%{MODULE_DIR}

%post

%postun

%clean
rm -rf $RPM_BUILD_ROOT
