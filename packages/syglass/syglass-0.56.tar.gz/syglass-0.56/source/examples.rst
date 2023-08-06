Usage Examples
==============

Volumetric Data
---------------

Creating a Project
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Programmatic creation of projects can be useful for rapid viewing of data after collection.

In this example, we'll create a project file from a series of tiffs.

::

	from syglass import pyglass
	import syglass as sy

	# create a project by specifing a path and the name of the project to be created. In this case, we'll call the project autoGenProject.
	project = pyglass.CreateProject(pyglass.path("C:\\syGlassProjects"), "autoGenProject")
	
	# create a DirectoryDescriptor to search a folder for tiff that match a pattern
	dd = pyglass.DirectoryDescription()
	
	# show the directoryDescriptor the first image of the set, and it will create a file list of matching slices
	dd.InspectByReferenceFile("C:\\raw_data\\example0000.tif"))
	
	# create a DataProvider to the dataProvider the file list
	dataProvider = pyglass.OpenTIFFs(dd.GetFileList(), False)

	# indicate which channels to include; in this case, all channels from the file
	includedChannels = pyglass.IntList(range(dataProvider.GetChannelsCount()))
	dataProvider.SetIncludedChannels(includedChannels)
	
	# spawn a ConversionDriver to convert the data
	cd = pyglass.ConversionDriver()
	
	# set the ConversionDriver input to the data provider
	cd.SetInput(dataProvider)
	
	# set the ConversionDriver output to the project previously created
	cd.SetOutput(project)
	
	# start the job!
	cd.StartAsynchronous()

	# report progress
	while cd.GetPercentage() != 100:
		print(cd.GetPercentage())
		time.sleep(1)
	print("Finished!")

Traversing the Volume
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Iterating over the entire volume is a common task. Most projects have multiple resolution levels, where higher levels are split into more and more "blocks".

In this example, we'll determine how many resolution levels are in our volume, select the highest one, and iterate over each of its blocks.

::

	import syglass as sy

	project = sy.get_project("C:/path/to/project_file.syg")

	# Get a dictionary showing the number of blocks in each level
	resolution_map = project.get_resolution_map()

	# Calculate the index of the highest resolution level
	max_resolution_level = len(resolution_map) - 1

	# Determine the number of blocks in this level
	block_count = resolution_map[max_resolution_level]

	# Retrieve a block at each index
	for i in range(block_count):

	  # Because this image volume is static, we'll always use timepoint 0
	  block = project.get_block(0, max_resolution_level, i)

	  # The offset between the volume's origin and the block's origin
	  print(block.offset)

	  # The volumetric data as a numpy array (z, y, x, channel)
	  print(block.data)

Retrieving Volumetric Data Around Points
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You may, in some cases, be interested in analyzing the volumetric data around points. Typically these points come from annotations. For example, the image data 
surrounding some counting points could be used as input for a machine learning model, with the goal of automatically counting the remaining structures.

The function ``get_custom_block()`` can be used to get a block of data of any size, at any location. It is more flexible than ``get_block()`` and ``get_block_by_point()``,
which retrieve blocks of predetermined sizes and positions.

In this example, we retrieve a (100, 100, 100) voxel cube of the volume for each counting point. Each cube is centered around its corresponding annotation.

::

	import syglass as sy
	import numpy as np

	project = sy.get_project("C:/path/to/project_file.syg")

	# Determine the index of the highest resolution level
	resolution = len(project.get_resolution_map()) - 1

	# Define a side length and dimensions for our cube
	side_length = 100
	dimensions = np.full(3, side_length)

	# Iterate over each point in each color series for the default experiment
	counts = project.get_counting_points()
	for color in counts:
		for point in counts[color]:

			# Calculate the offset to each cube based on point position
			offset = np.maximum(point.astype(int) - side_length / 2, np.zeros(3))

			# Retrieve a full-resolution cube from the volume
			block = project.get_custom_block(0, resolution, offset, dimensions)

Counting
--------

Changing Colors of Counting Points
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once retrieved, the color and position of counting points can be changed. Here we change the color of all of the red
counting points in an experiment to green.

::

	import syglass as sy
	import numpy as np

	project = sy.get_project("C:/path/to/project_file.syg")

	# Get counting points for the default experiment
	counts = project.get_counting_points()

	# Copy red points to the green series, clear the red points
	counts["Green"] = np.append(counts["Green"], counts["Red"], axis = 0)
	counts["Red"] = np.empty((0, 3))

	# Save result as the new counting points for the default experiment
	project.set_counting_points(counts)


Get and Set the Multi-tracking Points for a Project
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

	import syglass as sy
	import numpy as np 
	import pprint 

	# get the syGlass project
	project = sy.get_project("C:/path/to/project_file.syg")

	# load the multi tracking points into a dict
	pts = project.get_multitracking_points()

	# add two new points to the dict. One orange point and one violet point 
	pts['Orange'].append([np.array([30.02, 23.02, 19.02]), 235, 3]) # [[z,y,x], frame, series number]
	pts['Violet'].append([np.array([45.02, 22.042, 5.03]), 600, 4]) # [[z,y,x], frame, series number]

	# set the projects new and updated multi tracking points 
	project.set_multitracking_points(pts)

	# retrieve the updated points 
	out = project.get_multitracking_points()
	
	# display the dict with pretty print for organization 
	pp = pprint.PrettyPrinter(indent=4)
	pp.pprint(out)

	
Tracings (SWCs)
---------------

Importing SWC Files
^^^^^^^^^^^^^^^^^^^

Import a series of SWC files for viewing inside of a syGlass project.

::

    import syglass as sy
    import glob
    
    project = sy.get_project("E:/empty/empty.syg")
    l = glob.glob("C:/swcs/*.swc")
    outcome = project.import_swcs(l, "default")


Export and Analyze
^^^^^^^^^^^^^^^^^^

Export tracings as SWC files, and analyze their morphology with the python module NeuroM.

::

	import syglass as sy
	import glob

	# get the syGlass project
	project = sy.get_project("E:/empty/empty.syg")

	# save the tracings (will export each disconnected component as a separate SWC file)
	project.save_tracings()

	# find all the SWC files
	matchingFiles = glob.glob("*.swc")
	print(matchingFiles)
	# output: ['output00000.swc', 'output00001.swc', 'output00002.swc']

	# get first SWC and load into NeuroM
	import neurom as nm
	nrn = nm.load_neuron(matchingFiles[0])
	nrnSegLen = nm.get('segment_lengths', nrn)
	print(sum(nrnSegLen))
	# total length: 111945.68
	
	# calculate Sholl Analysis 
	nrnSholl = nm.get('sholl_frequency', nrn)
	print(nrnSholl)
	# sholl output: [  0.  8.  24.  33.  39.  52.  69.  68.  69.  79.  84.  78.  69.  78.  61. ... ]


Meshes (OBJ)
-------------

Import
^^^^^^^

Import a list of mesh files in the OBJ file format:

::

	import syglass as sy
	import glob

	# get the syGlass project
	project = sy.get_project("C:/syGlass Projects/thor/thorlabs.syg")
	l = glob.glob("C:/meshes/*.obj")
	project.import_meshes(l, "default")


ROIs
----

Importing and Exporting ROI Data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Export ROI data to numpy arrays and import an ROI to syGlass:

::

	import numpy as np
	import tifffile
	import syglass as sy

	# get the syGlass project 
	project = sy.get_project("C:/path/to/project_file.syg")

	roi_index = 1

	# get the raw ROI data block 
	roi_block = project.get_roi_data(roi_index)

	# save the ROI data as a tiff file 
	tifffile.imsave("C:/path/to/roiraw_tiff_file.tiff", roi_block.data)

	# get the mask block of the ROI 
	mask_block = project.get_mask(roi_index)

	# save the mask data as a tiff file 
	tifffile.imsave("C:/path/to/mask_tiff_file.tiff", mask_block.data)

	# import an ROI mask numpy array (z,y,x,channel count)
	incoming_mask = np.ones(100,100,100, 1)
	project.import_mask(incoming_mask, roi_index)