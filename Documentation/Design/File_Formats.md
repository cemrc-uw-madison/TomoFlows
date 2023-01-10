## File Formats:

### MRC
MRC is a common micrograph image format, with different implementations provided by software packages.  The header for the format has slight differences based on the software developer and it has been overloaded with many different uses.  
- Can represent a single image
- Can represent a "stack" of multiple images.
- Can represent volumetric data (tomogram or 3D volume from single particle data).

### TIF
TIF is another common micrograph image format.  Also can have LZW compression and a much reduced data footprint compared to MRC files.  We try to collect all data in TIF-LZW format with a separate gain reference image.  The gain reference is subtracted from each image during preprocessing to correct for defects in the camera or projection not provided from sample.

### DM4
Proprietary image format from Gatan for K3 cameras on microscopes.

### MTF
Material Transfer Function 

### .star
.star formats are data files used by RELION (single particle analysis) software. These describe input and output metadata for a project.

### PDB
PDB is a common format describing atom coordinates and molecular descriptions.  

### mmCIF
mmCIF is a newer common format describing atom coordinates and molecular descriptions.  It has largely replaced PDB (except for convience, as PDB is easy editable and mmCIF is not).  

### MTZ
a crystallographic format describing intensities, structure factors, and phases.  Fourier transform converts back from this "reciprocal space" to "real space" volumes and maps.

### XML
Commonly used format for describing data and avoid custom file formats.  Was preferred format early in 2000s for web use to be less proprietary.  Example use in MAPS software for describing project metadata.

### JSON
Commonly used format for describing data and avoid custom file formats.  Many web applications now make use of this.

