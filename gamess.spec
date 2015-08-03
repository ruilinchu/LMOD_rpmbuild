#
# gromacs-2015 spec, Jul 8, 2015, Jimi Chu
#
Summary:  The General Atomic and Molecular Electronic Structure System (GAMESS)
Name:       gamess
Version:    2015
Release:    0
License:    GPL
Vendor:     Gordon research group at Iowa State University
Group:      quantum chemistyr
Source:     gamess-current.tar.gz
Packager:   HMS - jimi_chu@hms.harvard.edu
AutoReqProv: no
%define debug_package %{nil}

%description 
The General Atomic and Molecular Electronic Structure System (GAMESS) is a general ab initio quantum chemistry package. 

## MUST set ONLY one of the three to 1
%define dep_mpi 1
%define dep_comp 0
%define is_core 0

%include common.inc

%prep 
rm -rf $RPM_BUILD_ROOT/%{INSTALL_DIR}

%setup -n %{name}

%build
mkdir -p             %{INSTALL_DIR}
mkdir -p             $RPM_BUILD_ROOT/%{INSTALL_DIR}

module purge
module load gcc/4.8.2
module load openmpi/1.8.4
module load MKL

cat > input << 'EOF'
enter
linux64
EOF

echo $PWD >> input
echo $PWD >> input
cat >> input << 'EOF'
00
gfortran
4.8
enter
mkl
/opt/centos/apps/intel/12.0.5/mkl
skip
enter
enter
mpi
openMPI
/opt/centos/apps/gcc-4.8.2/openmpi/1.8.4/
no
EOF

./config < input

sed -i 's+set COMM = $GMS_DDI_COMM+set COMM = mixed +g' ddi/compddi
sed -i 's+set MPI_INCLUDE_PATH = \x27\x27+set MPI_INCLUDE_PATH = \x27/opt/centos/apps/gcc-4.8.2/openmpi/1.8.4/include\x27+g' ddi/compddi

make 

cp rungms rungms_bak

cat > rungms << 'EOF'
#!/bin/csh
set MPIRUN=$1
set JOB=$2
set SCR=.
set USERSCR=.
set GMSPATH=%{INSTALL_DIR}
rm -fr $SCR/$JOB.F*
rm -fr $SCR/$JOB.dat
rm -fr $USERSCR/$JOB.r* 
rm -fr $USERSCR/$JOB.dat
cp $JOB.inp $SCR/$JOB.F05
setenv OUTPUT $SCR/$JOB.F06
setenv PUNCH $SCR/$JOB.F07
setenv TRAJECT     $SCR/$JOB.F04
setenv RESTART $USERSCR/$JOB.rst
setenv REMD $USERSCR/$JOB.remd
source %{INSTALL_DIR}/gms-files.csh
EOF

echo setenv LD_LIBRARY_PATH $LD_LIBRARY_PATH >> rungms
cat >> rungms << 'EOF'
$MPIRUN %{INSTALL_DIR}/gamess.00.x $JOB.inp
EOF
chmod +x rungms

cp * %{INSTALL_DIR}/
cp -fr %{INSTALL_DIR} $RPM_BUILD_ROOT/%{INSTALL_DIR}/..

##finish build 

##Make module file
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help([[
Module %{name} loads environmental variables defining the location of the GAMESS: 
HMS_GAMESS_DIR

usage example: rungms mpirun.v1.8.4 test
where test.inp is your input file. Launch even number of mpi tasks per node.

Version %{version}
]])

whatis( "GAMESS" )
whatis( "Version: %{version}")
whatis( "Category: quantum chemistry")
whatis( "Keywords: quantum, chemistry, gamess")
whatis( "Description: The General Atomic and Molecular Electronic Structure System (GAMESS)is a general ab initio quantum chemistry package.")

whatis( "URL: http://www.msg.ameslab.gov/gamess")

-- Export environmental variables
setenv("HMS_GAMESS_DIR", "%{INSTALL_DIR}")

-- Prepend the Python directories to the adequate PATH variables
prepend_path( "PATH", "%{INSTALL_DIR}")

EOF

%files 
%defattr(775,rc200,rccg,775)

%{INSTALL_DIR}
%{MODULE_DIR}

%post

%postun

%clean
rm -rf $RPM_BUILD_ROOT
