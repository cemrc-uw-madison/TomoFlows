## Gain Reference Conversions

A gain image is one taken on the camera in absence of the sample.  It can be used to correct for defects that would be visible on all sample images (inherent to either camera or optics path to the camera).

The Gatan K3 camera will acquire images with a proprietary format (DM4).  This can be converted to the common MRC format with `dm2mrc` (provided by IMOD software suite).  The Gatan K3 camera will acquire its image in a higher resolution than the physical pixel dimensions of the camera, aka super-resolution mode.

### Steps

We typically convert and then rescale from 11520 x 8184 to 5760 x 4092.  

`dm2mrc <input> <output>`
`newstack -shrink 2 <input> <output>`

### Notes

We currently do this manually after start of collections with EPU software and staff provide the gain file.  We should automate this, and it is a requirement for preprocessing to correctly run for RELION and CryoSPARC.  

GUI will need to collect the filename/path for the Gain file and trigger a task to convert.  The task which runs above steps will need to put the gain reference in a standard location -or- *better* that preprocessing should be able to query metadata from this job type to get the final output MRC file.

### Visual Output

We should be able to show an image of the output gain reference MRC on the UI. This might require creating a thumbnail in a format like JPG or PNG.