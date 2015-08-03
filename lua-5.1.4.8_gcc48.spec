#
# lua spec file
#
Summary:   Local Lua binary install
Name:      lua
Version:   5.1.4.8
Release:   0
License:   Copyright © 1994-2008 Lua.org, PUC-Rio. 
Vendor:    lua.org
Group:     System Environment/Base
Source:    lua-5.1.4.8.tar.gz
Packager:  HMS jimi_chu@hms.harvard.edu
AutoReqProv: no

%description
Lua is a powerful, fast, light-weight, embeddable scripting language.
Lua combines simple procedural syntax with powerful data description
constructs based on associative arrays and extensible semantics. Lua
is dynamically typed, runs by interpreting bytecode for a
register-based virtual machine, and has automatic memory management
with incremental garbage collection, making it ideal for
configuration, scripting, and rapid prototyping.
"Lua" (pronounced LOO-ah) means "Moon" in Portuguese. As such, it is
neither an acronym nor an abbreviation, but a noun. More specifically,
"Lua" is a name, the name of the moon of the Earth and the name of the
language. Like most names, it should be written in lower case with an
initial capital, that is, "Lua". Please do not write it as "LUA",
which is both ugly and confusing, because then it becomes an acronym
with different meanings for different people. So, please, write "Lua"
right!

%define debug_package %{nil}

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
%define dep_mpi 0
%define dep_comp 0
%define is_core 1

##do not change these
%if "%{is_core}" == "1"
    %define PKG_BASE    %{APPS}/%{name}
    %define INSTALL_DIR %{PKG_BASE}/%{version}
    %define MODULE_DIR  %{APPS}/%{MODULES}/Core/%{name}
    %define set_tree 1
%endif

%if "%{dep_comp}" == "1"
    %define PKG_BASE    %{APPS}/%{comp_fam_ver}/%{name}
    %define INSTALL_DIR %{PKG_BASE}/%{version}                    
    %define MODULE_DIR  %{APPS}/%{MODULES}/Compiler/%{comp_fam}/%{comp_ver}/%{name}
    %define set_tree 1
%endif

%if "%{dep_mpi}" == "1"
    %define PKG_BASE    %{APPS}/%{comp_fam_ver}/%{mpi_fam_ver}/%{name}
    %define INSTALL_DIR %{PKG_BASE}/%{version}
    %define MODULE_DIR  %{APPS}/%{MODULES}/MPI/%{comp_fam}/%{comp_ver}/%{mpi_fam}/%{mpi_ver}/%{name}
    %define set_tree 1
%endif

%if "%{set_tree}" == "error"
     %{error: You must set the compiler/mpi/core tree !}
     exit
%endif
##end do not

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
CC=gcc ./configure --prefix=%{INSTALL_DIR}
make
make install
 
cp -rp %{INSTALL_DIR}/ $RPM_BUILD_ROOT/%{INSTALL_DIR}/..

##create modulefiles
rm -rf $RPM_BUILD_ROOT/%{MODULE_DIR}
mkdir -p $RPM_BUILD_ROOT/%{MODULE_DIR}
cat > $RPM_BUILD_ROOT/%{MODULE_DIR}/%{version}.lua << 'EOF'

help([[
The lua modulefile defines the following environment variables
HMS_LUA_BIN, HMS_LUA_LIB, and HMS_LUA_INC for the location of the Lua distribution,
documentation, binaries, libraries, and include files, respectively.

To use the Lua library, include compilation directives
of the form: -L$HMS_LUA_LIB -I$HMS_LUA_INC -llua

Here is an example command to compile lua_test.c:
gcc -I\$HMS_LUA_INC lua_test.c -L\$HMS_LUA_LIB -llua

Version %{version}
]])

whatis("Name: Lua")
whatis("Version: %{version}")
whatis("Category: library, scripting language")
whatis("Keywords: System, Library, Scripting Language")
whatis("Description: Lua is a powerful, fast, light-weight, embeddable scripting language. ")
whatis("URL: http://www.lua.org")

setenv( "HMS_LUA_DIR", "%{INSTALL_DIR}")
setenv( "HMS_LUA_BIN", "%{INSTALL_DIR}/bin")
setenv( "HMS_LUA_LIB", "%{INSTALL_DIR}/lib")
setenv( "HMS_LUA_INC", "%{INSTALL_DIR}/include")

-- Append path
prepend_path("PATH", "%{INSTALL_DIR}/bin")
EOF

%files 
%defattr(-,rc200,rccg,-)
%{INSTALL_DIR}
%{MODULE_DIR}

%post
cd %{PKG_BASE}
if [ -d  %{name} ]; then
  rm -f %{name}
fi
ln -s %{version} %{name}

%postun

cd %{PKG_BASE}
if [ -h %{name} ]; then
  lv=`readlink %{name}`
  if [ ! -f $lv ]; then
    rm %{name} 
  fi
fi

%clean
rm -rf $RPM_BUILD_ROOT
