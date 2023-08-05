import os


# -----------------------------------------------------------------------------------
# Stencil functions
# ------------------------------------------------------------------------------
def get_list_of_stencils(folder, devices_data):
	default_stencil = devices_data.default_stencil
	stencil_col = devices_data.stencil
	if not stencil_col in devices_data.df:
		print(f"column information incorrect, check column existance `{stencil_col}`") 
		devices_data.df[stencil_col] = ""

	used_stn = set(devices_data.df[stencil_col])
	try:
		used_stn.remove("")
	except: pass
	found_stn = []
	stn_file = set()
	for file in os.listdir(folder):
		if file.startswith("~$$"): continue
		if default_stencil and file.startswith(default_stencil):
			found_stn.append(folder+file)
			stn_file.add(".".join(file.split(".")[:-1]))
			continue
		for stn in used_stn:
			if file.find(stn) > -1 :
				found_stn.append(folder+file)
				stn_file.add(".".join(file.split(".")[:-1]))
				break
	if len(used_stn) == len(stn_file):
		return found_stn
	elif len(used_stn) == 0:
		return found_stn
	else:
		print("Below mentioned stencil(s) are missing; ",
		"Kindly update/correct data before re-run.\n",
		used_stn.difference(stn_file), "\n")
		raise ValueError("Stencil is/are Missing or Invalid")


