/*
 *  model.c
 *  This file is part of LIME, the versatile line modeling engine
 *
 *  Copyright (C) 2006-2014 Christian Brinch
 *  Copyright (C) 2015-2017 The LIME development team
 *  Copyright (C) 2023      mkirc
 *
 */

#include "lime.h"

/******************************************************************************/
static double model_radius=2.7002512991143854e+18;
static double model_minscale=6.750628247785964e+17;


void
input(inputPars *par, image *img){

  char* vtk_file = getenv("LIME_VTK_FILE");
  char* in_file = getenv("LIME_IN_FILE");
  char* out_file = getenv("LIME_OUT_FILE");
  char* nThreadsChar = getenv("LIME_N_THREADS");
  unsigned long n_threads = strtoul(nThreadsChar, NULL, 10);
  /* long n_threads = strtol(getenv("N_THREADS"), NULL, 10); */

  if (! vtk_file) {
      puts("ERROR: VTK_FILE env var missing, aborting!");
      exit(1);
  }
  if (! in_file) {
      puts("ERROR: IN_FILE env var missing, aborting!");
      exit(1);
  }
  if (! out_file) {
      puts("ERROR: OUT_FILE env var missing, aborting!");
      exit(1);
  }
  if (n_threads == 0) {
      puts("WARNING: N_THREADS env var missing, setting it to 1!");
      n_threads = 1;
  }

  int i;

  /*
   * Basic parameters. See cheat sheet for details.
   */
  par->radius                   = model_radius;
  par->minScale                 = model_minscale;
  par->pIntensity               = 512;
  par->sinkPoints               = 296;

  par->dust                     = "jena_thin_e6.tab";
  par->moldatfile[0]            = "hco+@xpol.dat";
  par->sampling                 = 0; //  uniformly on a sphere.
  par->nSolveIters              = 3;
  par->resetRNG	                = 0;

/* The following are deprecated. Only the VTK output is still considered
 * useful.
  par->outputfile               = "populations.pop";
  par->binoutputfile            = "restart.pop";
*/
  par->gridfile                 = vtk_file;

  /*
    Setting elements of the following three arrays is optional. NOTE
    that, if you do set any of their values, you should set as many as
    the number of elements returned by your function density(). The
    ith element of the array in question will then be assumed to refer
    to the ith element in the density function return. The current
    maximum number of elements allowed is 7, which is the number of
    types of collision partner recognized in the LAMBDA database.

    Note that there is no (longer) a hard connection between the
    number of density elements and the number of collision-partner
    species named in the moldata files. This means in practice that,
    if you set the values for par->collPartIds, you can, if you like,
    set some for which there are no transition rates supplied in the
    moldatfiles. This might happen for example if there is a molecule
    which contributes significantly to the total molecular density but
    for which there are no measured collision rates for the radiating
    species you are interested in.

    You may also omit to mention in par->collPartIds a collision
    partner which is specified in the moldatfiles. In this case LIME
    will assume the density of the respective molecules is zero.

    If you don't set any values for any or all of these arrays,
    i.e. if you omit any mention of them here (we preserve this
    possibility for purposes of backward compatibility), LIME will
    attempt to replicate the algorithms employed in version 1.5, which
    involve guessing which collision partner corresponds to which
    density element. Since this was not exactly a rigorous procedure,
    we recommend use of the arrays.

    par->nMolWeights: this specifies #include "<stdio.h>"
#include "<stdlib.h>"
how you want the number density
    of each radiating species to be calculated. At each grid point a
    sum (weighted by par->nMolWeights) of the density values is made,
    then this is multiplied by the abundance to return the number
    density.

    par->collPartNames: this helps make a firm connection between the density
    functions and the collision par#include "<stdio.h>"
#include "<stdlib.h>"
tner information in the moldatfile.

    par->collPartMolWeights: this now allows control over the calculation of
    the dust opacity.                  ]

    Note that there are convenient macros defined in ../src/collparts.h for
    7 types of collision partner.
                                                 ID column numSpaceDims
    Below is an example of how you might use these parameters:
  */

  par->collPartIds[0]           = CP_H2;
  par->nMolWeights[0]           = 1.0;
  par->collPartNames[0]         = "H2";
  par->collPartMolWeights[0]    = 2.0159;
  /* par->nThreads                 = n_threads; */
  par->nThreads                 = n_threads;
  /* par->polarization             = 1; */ // needed for magfield to be working, and vice versa

  /* Set one or more of the following parameters for full output of the
   * grid-specific data at any of 4 stages during the processing. (See the
   * header of gridio.c for information about the stages.)
  */
  /* par->gridOutFiles[0] = "grid_stage_1.h5"; */
  /* par->gridOutFiles[1] = "grid_stage_2.h5"; */
  /* par->gridOutFiles[2] = "grid_stage_3.h5"; */
  /* par->gridOutFiles[3] = "grid_stage_4.h5"; */
  /* par->gridOutFiles[4] = "grid_stage_5.h5"; */

  /* You can also optionally read in a FITS file stored via the previous
   * parameters, or prepared externally. See the header of grid2fits.c for
   * information about the correct file format. LIME can cope with almost any
   * sensible subset of the recognized columns; it will use the file values if
   * they are present, then calculate the missing ones.
  */
  par->gridInFile = in_file;
  /* par->gridInFile = "grid_stage_4.h5"; */
  /* par->gridInFile = "single_test.h5"; */
  /* par->gridInFile = "all_test.h5"; */
  /* par->gridInFile = "nblocks_test.h5"; */
  /* par->gridInFile = "three_test.h5"; */

  /*
   * Definitions for image #0. Add blocks with successive values of i for additional images.
   */
  i=0;
  img[i].nchan                  = 61;                // Number of channels
  img[i].velres                 = 500.;              // Channel resolution in m/s
  img[i].trans                  = 3;                 // zero-indexed J quantum number
  img[i].pxls                   = 1e3;               // Pixels per dimension
  img[i].imgres                 = 0.1;               // Resolution in arc seconds
  img[i].distance               = 5e2*model_radius;  // source distance in m
  img[i].source_vel             = 0;                 // source velocity in m/s
  img[i].azimuth                = 0.0;
  img[i].incl                   = 0.0;
  img[i].posang                 = 0.0;

  /* For each set of image parameters above, numerous images with different units can be outputted. This is done by
   * setting img[].units to a delimited (space, comma, colon, underscore) string of the required outputs, where:
   *        0:Kelvin
   *        1:Jansky/pixel
   *        2:SI
   *        3:Lsun/pixel
   *        4:tau
   * If multiple units are specified for a single set of image parameters (e.g. "0 1 2") then the unit name is added
   * automatically at the end of the given filename, but before the filename extension if it exists. Otherwise if a
   * single unit is specified then the filename is unchanged.

   * A single image unit can also be specified for each image using img[].unit as in previous LIME versions. Note that
   * only img[].units or img[].unit should be set for each image.
  */
  img[i].units                  = "0 1";
  /* img[i].unit                   = 1; */
  /* img[i].filename               = "image0.fits";   // Output filename */
  img[i].filename               = out_file;   // Output filename
}

/******************************************************************************/
void
density(double x, double y, double z, double *density){
  /*
   * Define variable for radial coordinate
   */
  /*double r, rToUse; */
  /*const double rMin = 0.2*model_radius; /1* This cutoff should be chosen smaller than par->minScale but greater than zero (to avoid a singularity at the origin). *1/ */

  /*/1* */
  /* * Calculate radial distance from origin */
  /* *1/ */
  /*r=sqrt(x*x+y*y+z*z); */
  /*/1* */
  /* * Calculate a spherical power-law density profile */
  /* * (Multiply with 1e6 to go to SI-units) */
  /* *1/ */
  /*if(r>rMin) */
  /*  rToUse = r; */
  /*else */
  /*  rToUse = rMin; /1* Just to prevent overflows at r==0! *1/ */

  /*density[0] = 1.5e6*pow(rToUse/(0.1 * model_radius),-1.5)*1e6; */
    density[0] = 1.5e12;
}
/* void */
/* density(double x, double y, double z, double *density){ */
/*     /1* calculates distance to nearest point of input model, */
/*      * returning its density */
/*      *1/ */
/*     double mindist = model_minscale; */
/*     double dist, dx, dy, dz; */
/*     double best_dens = 0.; */
/*     printf("[%f, %f, %f]\n", x, y, z); */
/*     double r = sqrt(x*x + y*y + z*z); */
/*     if(r > model_radius) { */
/*         printf("huh?\n"); */
/*     } */
/*     for(int i=0; i<model_size; i++){ */
/*         dx = x - model_x[i]; */
/*         dy = y - model_y[i]; */
/*         dz = z - model_z[i]; */
/*         dist = sqrt(dx*dx + dy*dy + dz*dz); */
/*         if(dist < mindist) { */
/*             mindist = dist; */
/*             best_dens = model_density[i]; */
/*         } */
/*     } */
/*     density[0] = best_dens; */
/* } */

/******************************************************************************/

void
temperature(double x, double y, double z, double *temperature){
  /*int i,x0=0; */
  /*double r; */
  /*/1* */
  /* * Array containing temperatures as a function of radial */
  /* * distance from origin (this is an example of a tabulated model) */
  /* *1/ */
  /*double temp[2][10] = { */
  /*    {2.0e13, 5.0e13, 8.0e13, 1.1e14, 1.4e14, 1.7e14, 2.0e14, 2.3e14, 2.6e14, 2.9e14}, */
  /*    {44.777, 31.037, 25.718, 22.642, 20.560, 19.023, 17.826, 16.857, 16.050, 15.364} */
  /*}; */
  /*/1* */
  /* * Calculate radial distance from origin */
  /* *1/ */
  /*r=sqrt(x*x+y*y+z*z); */
  /*/1* */
  /* * Linear interpolation in temperature input */
  /* *1/ */
  /*if(r > temp[0][0] && r<temp[0][9]){ */
  /*  for(i=0;i<9;i++){ */
  /*    if(r>temp[0][i] && r<temp[0][i+1]) x0=i; */
  /*  } */
  /*} */
  /*if(r<temp[0][0]) */
  /*  temperature[0]=temp[1][0]; */
  /*else if (r>temp[0][9]) */
  /*  temperature[0]=temp[1][9]; */
  /*else */
  /*  temperature[0]=temp[1][x0]+(r-temp[0][x0])*(temp[1][x0+1]-temp[1][x0])/(temp[0][x0+1]-temp[0][x0]); */
    temperature[0] = 15.;
}

/******************************************************************************/

void
abundance(double x, double y, double z, double *abundance){
  /*
   * Here we use a constant abundance. Could be a
   * function of (x,y,z).
   */
  abundance[0] = 1.e-9;
}

/******************************************************************************/

void
doppler(double x, double y, double z, double *doppler){
  /*
   * 200 m/s as the doppler b-parameter. This
   * can be a function of (x,y,z) as well.
   * Note that *doppler is a pointer, not an array.
   * Remember the * in front of doppler.
   */
  *doppler = 200.;
}

/******************************************************************************/

void
velocity(double x, double y, double z, double *vel){
  double r, rToUse, ffSpeed;
   /* This cutoff should be chosen smaller than par->minScale but greater than zero (to avoid a singularity at the origin). */
  const double rMin = 0.1*model_minscale;

  /*
   * Calculate radial distance from origin
   */
  r = sqrt(x*x+y*y+z*z);
  if(r>rMin)
    rToUse = r;
  else
    rToUse = rMin;

  /*
   * Free-fall velocity in the radial direction onto a central 
   * mass of 1.0 solar mass
   */  
  ffSpeed = sqrt(2*GRAV*1.989e30/rToUse);

  vel[0] = -x*ffSpeed/rToUse;
  vel[1] = -y*ffSpeed/rToUse;
  vel[2] = -z*ffSpeed/rToUse;
}

/******************************************************************************/

void
magfield(double x, double y, double z, double *B){
  // this is just for getting the hdf5 column names
  B[0] = 3.;
  B[1] = 0.0;
  B[2] = 0.0;
}
