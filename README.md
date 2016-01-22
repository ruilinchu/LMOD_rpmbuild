# LMOD_rpmbuild
```

#----------------------
Apps category definition:
Core: 
1. compiler itself, like gcc, intel, etc;
2. no compile options, like java, matlab, mathematica, etc;
3. purely library, like boost, atlas, eigen, etc;
4. header files;

Compiler:
1. need to be compiled
2. and is not core;
most of our apps are in this category, openmpi, R, bwa, samtools, sailfish ...

MPI:
1. need to be compiled 
2. and is not core 
3. and depend on MPI stack when running, like Gromacs, VinaLC, mpiblast, etc;
#-----------------------

```
