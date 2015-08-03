#
# git spec file
#
Summary:   A distributed version control system 
Name:      git
Version:   2.3.0
Release:   0
License:   Copyright © 1994-2008 Lua.org, PUC-Rio. 
Vendor:    lua.org
Group:     System Environment/Base
Source:    git-2.3.0.tar.gz
Packager:  HMS alex_truong@hms.harvard.edu
AutoReqProv: no

%description
Git is a free and open source distributed version control system designed to handle everything from small to very large projects with speed and efficiency.

Git is easy to learn and has a tiny footprint with lightning fast performance. It outclasses SCM tools like Subversion, CVS, Perforce, and ClearCase with features like cheap local branching, convenient staging areas, and multiple workflows.

## MUST set ONLY one of the three to 1
%define dep_mpi 0
%define dep_comp 0
%define is_core 1

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

make configure
./configure --prefix=%{INSTALL_DIR}
make all doc
make install install-doc install-html
 
cp -rp %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..

##create modulefiles
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help([[
The git modulefile defines the following environment variables
HMS_GIT_BIN, HMS_GIT_LIB, HMS_GIT_LXC, and HMS_GIT_SHR for the location of the Lua distribution,
documentation, binaries, libraries, and include files, respectively.

Version %{version}
]])

whatis("Name: git")
whatis("Version: %{version}")
whatis("Category: version control system")
whatis("Keywords: git, project, version control")
whatis("Description: Git is a free and open source distributed version control system designed to handle everything from small to very large projects with speed and efficiency. ")
whatis("URL: http://git-scm.com/")

setenv( "HMS_GIT_DIR", "%{INSTALL_DIR}")
setenv( "HMS_GIT_BIN", "%{INSTALL_DIR}/bin")
setenv( "HMS_GIT_LIB", "%{INSTALL_DIR}/lib64")
setenv( "HMS_LUA_LXC", "%{INSTALL_DIR}/libexec")
setenv( "HMS_GIT_SHR", "%{INSTALL_DIR}/share")

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
