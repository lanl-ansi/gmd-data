package gov.lanl.gmd.output;

import ncsa.hdf.object.FileFormat;
import ncsa.hdf.object.h5.H5File;

public class TryHDFJava {
	// The name of the file we'll create.
	private static String fname = "H5FileCreate.h5";

	public static void main(String[] args) {
		// Retrieve an instance of the implementing class for the HDF5 format
		FileFormat fileFormat = FileFormat.getFileFormat(FileFormat.FILE_TYPE_HDF5);

		// If the implementing class wasn't found, it's an error.
		if (fileFormat == null) {
			System.err.println("Cannot find HDF5 FileFormat.");
			return;
		}

		// If the implementing class was found, use it to create a new HDF5 file
		// with a specific file name.
		//
		// If the specified file already exists, it is truncated.
		// The default HDF5 file creation and access properties are used.
		//
		H5File testFile;
		try {
			testFile = (H5File) fileFormat.createFile(fname, FileFormat.FILE_CREATE_DELETE);

			// Check for error condition and report.
			if (testFile == null) {
				System.err.println("Failed to create file: " + fname);
				return;
			}
		} catch (Exception e) {
			e.printStackTrace();
		}

		// End of example that creates an empty HDF5 file named H5FileCreate.h5.


	}

}
