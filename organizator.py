import os
import shutil

# The directory path from where we want to clean up.
director_path = r"C:\Users\axi\Downloads"

# Dictionary used for storing extension types.
file_extensions = {
    "Documents": [".doc", ".docx", ".pdf", ".txt" ".rtf", ".odt", ".tex", ".wpd", ".md", ".wks", ".wps", ".pages"],
    "Spreadsheets": [".xls", ".xlsx", ".csv", ".ods", ".xlsm", ".xlt", ".xltx", ".xltm", ".numbers"],
    "Presentations": [".ppt", ".pptx", ".odp", ".key", ".pps", ".ppsx", ".pptm"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp", ".psd", ".heic", ".ico", ".raw",
               ".nef", ".cr2"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".wma", ".m4a", ".aiff", ".alac", ".amr", ".mid", ".midi"],
    "Video": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".mpeg", ".mpg", ".m4v", ".3gp", ".3g2", ".rm",
              ".vob"],
    "Compressed": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".iso", ".dmg", ".tgz", ".cab", ".z", ".lz",
                   ".lzma"],
    "Executables": [".exe", ".bat", ".sh", ".jar", ".msi", ".bin", ".command", ".app", ".gadget", ".wsf"],
    "Web": [".html", ".htm", ".css", ".js", ".php", ".asp", ".jsp", ".xhtml", ".xml", ".json", ".vue"],
    "Databases": [".sql", ".db", ".mdb", ".accdb", ".sqlite", ".dbf", ".ora", ".sqlitedb", ".myd", ".frm", ".ibd"],
    "Code": [".py", ".java", ".c", ".cpp", ".js", ".rb", ".php", ".html", ".css", ".cs", ".swift", ".go", ".rs", ".m",
             ".kt", ".lua", ".pl", ".vb", ".ts"],
    "System": [".dll", ".sys", ".ini", ".log", ".cfg", ".reg", ".bak", ".dmp", ".drv", ".icns", ".pf"],
    "Fonts": [".ttf", ".otf", ".woff", ".woff2", ".eot", ".fon", ".fnt"],
    "CAD": [".dwg", ".dxf", ".dgn", ".stp", ".step", ".igs", ".iges", ".3ds", ".sat", ".prt"],
    "GIS": [".shp", ".gdb", ".kml", ".kmz", ".gpx", ".mxd", ".lyr", ".dwg", ".dxf", ".tif", ".tiff"],
    "Vector Images": [".ai", ".eps", ".ps", ".svg", ".pdf", ".cdr", ".cmx", ".emf", ".wmf"],
    "3D Models": [".stl", ".obj", ".fbx", ".dae", ".3ds", ".blend", ".ply", ".max", ".3dm"],
    "Emails": [".eml", ".msg", ".pst", ".ost", ".mbox", ".oft", ".vcf", ".ics"],
    "Backups": [".bak", ".tmp", ".old", ".bkp", ".backup", ".gho", ".iso", ".bkf", ".adi"],
    "Scripts": [".pl", ".sh", ".py", ".rb", ".js", ".php", ".asp", ".aspx", ".cgi", ".tcl", ".vbs", ".ps1"],
    "Miscellaneous": [".iso", ".bin", ".cue", ".dmg", ".toast", ".img", ".nrg", ".mds", ".mdf", ".vcd", ".ccd", ".sub"],
    "Unknown": [],
}


def search_for_specific_key(values, search_for):
    """
    Function that search the extension name in the dictionary and return specific key
    :param values: file_extensions(dictionary)
    :param search_for: extension name
    :returns: True and the key associated with the found value
    """
    for key in values:
        for value in values[key]:
            if search_for in value:
                return True, key
    return False


def create_folder(file, root):
    """
    Function to check if folder exist in directory, if exists pass, if not creates it.
    :param file: File from the directory
    :param root: Root of the specific file
    :return:
    """
    extension = os.path.splitext(file)
    if search_for_specific_key(file_extensions, extension[1]):
        check_key = search_for_specific_key(file_extensions, extension[1])[1]
        path = os.path.join(root, check_key)
        if os.path.exists(path):
            pass
        else:
            path = os.path.join(director_path, check_key)
            os.mkdir(path)
    else:
        file_extensions['Unknown'].append(extension)
        create_folder(file, root)


def organize_files():
    """
    Function to organize the files found in a directory
    :return:
    """
    for root, directory, files in os.walk(director_path):  # Iterate trought each file from /Downloads folder
        for file in files:
            create_folder(file, root)
            source_path = os.path.join(root, file)
            destination_path = os.path.join(root,
                                            search_for_specific_key(file_extensions, os.path.splitext(file)[1])[1])
            shutil.move(source_path, destination_path)
        break


organize_files()
