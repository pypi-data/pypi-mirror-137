
# ------------------------------------------------------------------------------
#  Local Functions
# ------------------------------------------------------------------------------

def get_filename(absolute_pathfile):
	'''
	This function takes in the absolute path of a file and returns the filename.
	:param absolute_pathfile: The absolute path of the file.
	:return: The filename.
	'''
	return absolute_pathfile.split("/")[-1].split("""\\""")[-1].split(".")[0]
