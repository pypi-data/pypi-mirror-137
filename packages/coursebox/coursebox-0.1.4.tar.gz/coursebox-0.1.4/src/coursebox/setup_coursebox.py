from coursebox.core import info_paths

def setup_coursebox(working_dir, course_number="02450", semester='spring', year=2019,
    slides_showsolutions=True,
    slides_includelabels=False,
    continuing_education_mode = False,
    slides_shownotes=False,
    continuing_education_month = "March", **kwargs):

    info_paths.core_conf['working_dir'] = working_dir
    info_paths.core_conf['course_number'] = course_number
    info_paths.core_conf['semester'] = semester
    info_paths.core_conf['year'] = year
    info_paths.core_conf['slides_showsolutions'] = slides_showsolutions
    info_paths.core_conf['slides_includelabels'] = slides_includelabels
    info_paths.core_conf['continuing_education_mode'] = continuing_education_mode
    info_paths.core_conf['continuing_education_month'] = continuing_education_month
    info_paths.core_conf['slides_shownotes'] = slides_shownotes
    for a, val in kwargs.items():
        info_paths.core_conf[a] = val
