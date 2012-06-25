import directorytools as dt
from shutil import copyfile
from csv import DictWriter

REPORT_DIRECTORY = "reports/"

def report_summary(feed_details, valid_files, invalid_files, invalid_sections):
	dt.create_directory(REPORT_DIRECTORY)
	fname = "report_summary_" + feed_details["file_time_stamp"] + ".txt"

	if "vip_id" not in feed_details:
		directory = REPORT_DIRECTORY + "unknown"
		dt.create_directory(directory)
		with open(fname, "w") as w:
			summary_header(feed_details, w)
			file_summary(valid_files, invalid_files, invalid_sections, w)
			w.write("Missing source information, could not process feed")
	else:
		directory = REPORT_DIRECTORY + str(feed_details["vip_id"]) + "/"
		dt.create_directory(directory)
		dt.create_directory(directory + "archives/")
		dt.clear_or_create(directory + "current/")
		with open(directory + "current/" + fname, "w") as w:
			if "election_id" not in feed_details:
				summary_header(feed_details, w)
				file_summary(valid_files, invalid_files, invalid_sections, w)
				w.write("Missing election information, could not process feed")
			else:
				summary_header(feed_details, w)
				election_summary(feed_details, w)
				file_summary(valid_files, invalid_files, invalid_sections, w)
		copyfile(directory + "current/" + fname, directory + "archives/" + fname)

def summary_header(feed_details, writer):
	writer.write("File Processed: " + feed_details["file"] + "\n")
	writer.write("Time Processed: " + feed_details["process_time"] + "\n\n")

def file_summary(valid_files, invalid_files, invalid_sections, writer):
	writer.write("----------------------\nFile Report\n----------------------\n\n")
	if len(invalid_sections) > 0:
		writer.write("Invalid Sections: " + str(invalid_sections) + "\n")
	if len(invalid_files) > 0:
		writer.write("Invalid Files: " + str(invalid_files) + "\n")
	if len(valid_files) > 0:
		writer.write("Valid Files: " + str(valid_files) + "\n")
	writer.write("\n")

def source_summary(feed_details, writer):
	writer.write("----------------------\nSource Data\n----------------------\n\n")
	writer.write("Name: " + feed_details["name"] + "\n")
	writer.write("Vip ID: " + str(feed_details["vip_id"]) + "\n")
	writer.write("Datetime: " + str(feed_details["datetime"]) + "\n\n")

def election_summary(feed_details, writer):
	writer.write("----------------------\nElection Data\n----------------------\n\n")
	writer.write("Election ID: " + str(feed_details["election_id"]) + "\n")
	writer.write("Election Date: " + str(feed_details["election_date"]) + "\n")
	writer.write("Election Type: " + str(feed_details["election_type"]) + "\n\n")

def feed_errors(feed_details, error_data):
	fname = "feed_errors_" + feed_details["file_time_stamp"] + ".txt"
	cur_dir = REPORT_DIRECTORY + str(feed_details["vip_id"]) + "/current/"
	arc_dir = REPORT_DIRECTORY + str(feed_details["vip_id"]) + "/archives/"
	with open(cur_dir + fname, "a") as writer:
		out = DictWriter(writer, fieldnames=['element_name','id','error_details'])
		for row in error_data:
			out.writerow(row)
	copyfile(cur_dir + fname, arc_dir + fname)
