# -*- coding: utf-8 -*-
import shutil, os, glob
from datetime import datetime, timedelta
import calendar
import pickle
import time
from line_profiler_pycharm import profile

import slider
from jinjafy import jinjafy_comment
from jinjafy import jinjafy_template
from coursebox.core.info_paths import get_paths
from slider.legacy_importer import slide_to_image
from slider.legacy_importer import li_import
from slider.slide import set_svg_background_images
from coursebox.book.exam_includer import HOMEWORK_PROBLEMS
from coursebox.core.info import class_information
from coursebox.material.lecture_questions import lecture_question_compiler
from slider import latexmk
import coursebox
# from line_profiler_pycharm import profile

def get_feedback_groups():
    paths = get_paths()
    feedback_file = paths['semester'] +"/feedback_groups.pkl"
    if os.path.exists(feedback_file):
        with open(feedback_file,'rb') as f:
            fbg = pickle.load(f)
    else:
        fbg = dict()

    info = class_information()
    all_students = [id for id in info['students']]

    now = datetime.today()
    already_used = []
    remaining_lectures = []
    for lecture in info['lectures']:
        lnum = lecture['number']
        if lnum == 1: continue
        if lecture['date'] < now and lnum in fbg:
            already_used += fbg[lnum]
            # already_used += g
        else:
            remaining_lectures.append(lnum)

    project_groups = [g['student_ids'] for g in info['all_groups']]
    # remove already_used from these groups
    reduced_groups = [[id for id in pg if id not in already_used] for pg in project_groups]
    reduced_groups = [rg for rg in reduced_groups if len(rg)>0]
    # groups are now partitioned.
    if len(remaining_lectures) > 0:
        fbgs = coursebox.thtools_base.partition_list(reduced_groups, len(remaining_lectures))
        for gg in fbgs:
            for g in gg:
                already_used = already_used + g

        lst = thtools.thtools_base.partition_list([s for s in all_students if s not in already_used], len(remaining_lectures))
        for i in range(len(remaining_lectures)):
            dg = []
            for g in fbgs[i]: dg += g  # flatten the list
            fbg[remaining_lectures[i]] = dg + lst[i]

        sum( [len(v) for k,v in fbg.items() ]) - sum( [len( set(v)) for k,v in fbg.items() ])

        with open(feedback_file, 'wb') as f:
            pickle.dump(fbg,f)

    for k in fbg:
        g = fbg[k]
        g2 = []
        for s in g:

            if s in info['students']:
                dl = info['students'][s]['firstname'] + " " + info['students'][s]['lastname']
                # dl = [ss['firstname']+" "+ss['lastname'] for ss in if ss['id'] == s]
                if not dl:
                    print("EMPTY LIST when making feedback groups. Probably an error in project correction sheets.")
                    continue
                g2.append(dl)
        fbg[k] = g2
    return fbg

PRESENTATION = 0
NOTES = 1
HANDOUT = 2
def make_lectures(week=None, mode=0, gather_pdf_out=True, gather_sixup=True, make_quizzes=True, dosvg=False, Linux=False):
    """
    Mode determines what is compiled into the pdfs. It can be:

    mode = PRESENTATION = 0: What I use to present from
    mode = NOTES = 1: Version containing notes (used for self-study)
    mode = HANDOUT = 2: version handed out to students.
    """
    paths = get_paths()
    if os.path.exists(paths['book']):
        book_frontpage_png = paths['shared']+"/figures/book.png" #paths['lectures']+"/static/book.png"
        slide_to_image(paths['book'] + "/02450_Book.pdf", book_frontpage_png, page_to_take=1)
        shutil.copy(paths['book'] + "/book_preamble.tex", paths['shared'])
    info = class_information()
    jinjafy_shared_templates_dir(paths, info) # Compile templates in shared/templates
    # course_number = info['course_number']
    if isinstance(week, int):
        week = [week]
    all_pdfs = []
    for lecture in info['lectures']:
        w = lecture['number']
        if week is not None and w not in week:
            continue

        ag = get_feedback_groups()

        lecture['feedback_groups'] = ag.get(w, [])
        info.update({'week': w})
        info['lecture'] = lecture
        info['lecture']['teacher'] = [t for t in info['teachers'] if t['initials'] == lecture['teacher_initials']].pop()

        lecture_texdir = paths['lectures'] + '/Lecture_%s/Latex' % w
        lecture_texfile =lecture_texdir + "/Lecture_%i.tex" % w

        fix_shared(paths, output_dir=lecture_texdir, dosvg=dosvg)

        if os.path.exists(lecture_texdir):
            print("Latex directory found for lecture %i: %s"%(w,lecture_texdir))
            lecture_texdir_generated = lecture_texdir +"/templates"
            if not os.path.exists(lecture_texdir_generated):
                # shutil.rmtree(lecture_texdir_generated)
                # time.sleep(0.2)
                os.mkdir(lecture_texdir_generated)

        if mode == PRESENTATION:
            info['slides_shownotes'] = False
            info['slides_handout'] = False
            odex = "/presentation"
        elif mode == HANDOUT:
            info['slides_shownotes'] = False
            info['slides_handout'] = True
            info['slides_showsolutions'] = False
            odex = "/handout"
        elif mode == NOTES:
            info['slides_shownotes'] = True
            info['slides_handout'] = True
            odex = "/notes"
        else:
            raise Exception("Mode not recognized")

        for f in glob.glob(paths['lectures'] + "/templates/*.tex"):
            ex = "_partial.tex"
            if f.endswith(ex):
                jinjafy_template(info, file_in=f, file_out=lecture_texdir + "/templates/"+os.path.basename(f)[:-len(ex)] + ".tex")

        # Fix questions.
        qtarg = lecture_texdir + "/questions"
        if not os.path.exists(qtarg):
            os.mkdir(qtarg)
        for f in glob.glob(paths['lectures'] + "/static/questions/*"):
            shutil.copy(f, qtarg)

        # Fix questions for this lecture
        if make_quizzes:
            lecture_question_compiler(paths, info, lecture_texfile)

        pdf_out = slider.latexmk(lecture_texfile, Linux=Linux)
        all_pdfs.append( (w,pdf_out))

    handle_pdf_collection(paths, all_pdfs, gather_pdf_out=gather_pdf_out, gather_sixup=gather_sixup, odir=odex)


def handle_pdf_collection(paths, all_pdfs, gather_pdf_out, gather_sixup, odir):
    tmp_dir = paths['lectures'] + '/Collected/tmp'
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)

    collect_template = paths['lectures'] + "/Collected/lecture_collector_partial.tex"

    for sixup in [False, True]:
        if not gather_pdf_out: continue
        if sixup and not gather_sixup: continue

        pdf_compiled_all_6up = []
        sixup_str = "-6up" if sixup else ""
        for (week, _) in all_pdfs:
            tv = {'week': week,
                  'pdffiles': [paths['lectures'] + '/Lecture_%s/Latex/Lecture_%s.pdf' % (week, week)]}
            if sixup:
                tv['sixup'] = sixup
                tex_out_sixup = tmp_dir + "/Lecture_%i%s.tex" % (week, sixup_str)
                jinjafy_comment(data=tv, file_in=collect_template, file_out=tex_out_sixup, jinja_tag=None)
                dpdf = tmp_dir + "/" + slider.latexmk(tex_out_sixup, shell=False, cleanup=True)
            else:
                dpdf = tv['pdffiles'][0]

            pdf_compiled_all_6up.append(dpdf)

        for dpdf in pdf_compiled_all_6up:
            output_dir = paths['pdf_out'] + odir
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)

            # if not info['slides_showsolutions']:
            #     odir += "/lectures_without_solutions"
            # if not os.path.isdir(odir):
            #     os.mkdir(odir)
            #
            shutil.copy(dpdf, output_dir + "/" + os.path.basename(dpdf))

    for f in glob.glob(tmp_dir + "/*"):
        os.remove(f)

def compile_simple_files(paths, info, template_file_list, verbose=False):
    jinjafy_shared_templates_dir(paths, info)
    fix_shared(paths, output_dir=paths['shared_latex_compilation_dir'], verbose=verbose)
    for fname,dd in template_file_list:
        d2 = info.copy()
        d2.update(dd)
        file = os.path.basename(fname)
        if file.endswith("_template.tex"):
            file = file.replace("_template.tex", ".tex")
        tex_out = paths['shared_latex_compilation_dir'] + "/" + file
        jinjafy_template(data=d2, file_in=fname, file_out=tex_out, filters=get_filters(), template_searchpath=paths['instructor'])
        latexmk(tex_out, pdf_out= paths['pdf_out'] + "/" + os.path.basename(tex_out)[:-4]+".pdf")

# rec_fix_shared(shared_base=paths['shared'], output_dir=output_dir)
import time
# import dirsync
# dirsync.sync(paths['shared'], output_dir, 'diff')


# Do smarter fixin'
from pathlib import Path

from jinjafy.cache.simplecache import hash_file_

@profile
def get_hash_from_base(base):
    if not os.path.exists(base + "/sharedcache.pkl"):
        source = {}
    else:
        with open(base + "/sharedcache.pkl", 'rb') as f:
            source = pickle.load(f)

    actual_files = {}
    for f in glob.glob(base + "/**", recursive=True):
        if os.path.isdir(f):
            continue
        rel = os.path.relpath(f, base)

        # d = dict(mtime=os.path.getmtime(f))
        actual_files[rel] = dict(mtime=os.path.getmtime(f), hash=-1, modified=False)

        if rel not in source or (actual_files[rel]['mtime'] != source[rel].get('mtime', -1)): # It has been modified, update hash
            # print(rel, time.ctime(actual_files[rel]['mtime']), time.ctime(source[rel].get('mtime', -1)))
            new_hash = hash_file_(f)
            # actual_files[rel] = {}
            actual_files[rel]['modified'] = new_hash != source.get(rel, {}).get('hash', -1)
            actual_files[rel]['hash'] = new_hash
        else:
            actual_files[rel]['hash'] = source[rel]['hash']
    return actual_files


@profile
def fix_shared(paths, output_dir, pdf2png=False,dosvg=True,verbose=False, compile_templates=True,shallow=True):
    '''
    Copy shared files into lecture directories
    '''
    cache_base = output_dir
    from jinjafy.cache import cache_contains_file, cache_update_file
    from slider.convert import svg2pdf, pdfcrop
    from slider import convert
    import filecmp

    t0 = time.time()
    shared_base = paths['shared']
    output_dir = output_dir

    import glob
    # def get_cache_from_dir(shared_base):
    # print("Beginning file cache..")


    source = get_hash_from_base(shared_base)
    target = get_hash_from_base(output_dir)

    # update_source_cache = False
    for rel in source:
        if rel.endswith(".svg") and source[rel]['modified']:
            pdf_file = svg2pdf(shared_base + "/"+rel, crop=True, text_to_path=True, verbose=True)
            rel = os.path.relpath(pdf_file, shared_base)
            source[rel] = dict(mtime=os.path.getmtime(pdf_file), hash=hash_file_(pdf_file), modified=True)

            # update_source_cache = True
    # Perform sync here.
    for rel in source:
        if rel.endswith("_partial.tex"):
            continue

        if rel not in target or target[rel]['hash'] != source[rel]['hash']:
            print(" -> ", output_dir + "/" + rel)
            shutil.copy(shared_base +"/" + rel, output_dir + "/" + rel)
            target[rel] = source[rel].copy()
            target[rel]['modified'] = True
            target[rel]['mtime'] = os.path.getmtime(output_dir + "/" + rel)

    if pdf2png:
        for rel in target:
            if rel.endswith(".pdf") and target[rel]['modified']:
                # print("pdf2png: ")
                png = convert.pdf2png(output_dir + "/" + rel, verbose=True)
                target[rel]['modified'] = False
                target[rel]['hash'] = hash_file_(output_dir + "/" + rel)
                target[rel]['mtime'] = os.path.getmtime(output_dir + "/" + rel)

    # Save the cache.

    with open(shared_base + "/sharedcache.pkl", 'wb') as f:
        pickle.dump(source, f)

    with open(output_dir + "/sharedcache.pkl", 'wb') as f:
        pickle.dump(target, f)

    print("fix_shared()", time.time() - t0)

    #
    # if pdf2png:
    #     if f.endswith(".pdf") and pdf2png:
    #         if verbose:
    #             print("converting to png", f)
    #         convert.pdf2png(of)
    #
    #     for f in source:
    #         if f not in target:
    #             print(f)
    #         else:
    #             if source[f]['hash'] != target[f]['hash']:
    #                 print(f, f)
    #
    #
    #
    # a = 234
    # # if rel not in source:
    #
    #     #     source[rel] = dict(mtime=os.path.getmtime(f), hash=hash_file_(f))
    #     #
    #
    #
    # # Everything has a hash/mtime that is up to date. Now look at target dir
    #
    # get_cache_from_dir(output_dir)
    #
    # # Get the corresponding output at destination:
    #
    #
    #
    #
    #
    #
    # for path in Path(shared_base).rglob('*'):
    #     print(path)
    # a = 234
    # def rec_fix_shared(shared_base, output_dir):
    #     if dosvg:
    #         for svg in glob.glob(shared_base+"/*.svg"):
    #             # if not os.path.exists(shared_base + )
    #             if not cache_contains_file(cache_base, svg):
    #                 # if verbose:
    #                 print("converting to pdf", svg)
    #                 svg2pdf(svg,crop=True, text_to_path=True)
    #                 cache_update_file(cache_base, svg)
    #                 assert False
    #
    #     files = glob.glob(shared_base+"/*")
    #     for f in files:
    #         if f.endswith("cache.pkl"):
    #             continue
    #
    #         if "templates" in f and f.endswith("_partial.tex"):
    #             continue
    #
    #         if os.path.isdir(f):
    #             od2 = output_dir + "/" + os.path.basename(f)
    #             if not os.path.exists(od2):
    #                 os.mkdir(od2)
    #             rec_fix_shared(f, od2)
    #         else:
    #             of = output_dir + "/" + os.path.basename(f)
    #             if not os.path.exists(of) or not filecmp.cmp(f, of,shallow=shallow):
    #                 print(f"> fix_shared() -> {of}")
    #                 shutil.copy(f, of)
    #                 if f.endswith(".pdf") and pdf2png:
    #                     if verbose:
    #                         print("converting to png", f)
    #                     convert.pdf2png(of)
    #                 # cache_update_file(cache_base, f)
    #
    #         if verbose:
    #             print(" done!")

    # if pdf2png:
    #     assert False



    # get diff.

    # directory_cmp = filecmp.dircmp(a=paths['shared'], b=output_dir)
    # from filecmp import dircmp
    # from filecmp import dircmp
    # def print_diff_files(dcmp):
    #     for name in dcmp.diff_files:
    #         print("diff_file %s found in %s and %s" % (name, dcmp.left, dcmp.right))
    #         print("")
    #     for sub_dcmp in dcmp.subdirs.values():
    #         print_diff_files(sub_dcmp)
    #

    # t0 = time.time()
    # dcmp = dircmp(paths['shared'], output_dir)
    # print_diff_files(dcmp)
    # print("dircmp", time.time() - t0)
    # directory_cmp.report()
    # import time
    # t0 = time.time()
    # rec_fix_shared(shared_base=paths['shared'], output_dir=output_dir)
    # import time
    # # import dirsync
    # # dirsync.sync(paths['shared'], output_dir, 'diff')
    # print("mine", time.time() - t0)
    a = 234


def jinjafy_shared_templates_dir(paths, info):
    tpd = paths['shared'] + "/templates"
    for f in glob.glob(tpd + "/*.tex"):
        print(f)
        ex = "_partial.tex"
        if f.endswith(ex):
            jinjafy_template(info, file_in=f, file_out=f"{tpd}/{os.path.basename(f)[:-len(ex)]}.tex")


def get_filters():
    return {'safetex': safetex, 'tt': tt, 'bf': bf, 'verb': verb}

def make_exercises_projects_tutors(week=None, only_exercises=False, make_exercises=True, make_projects=True, dosvg=False):
    paths = get_paths()
    filters = get_filters()
    info = class_information()
    course_number = info['course_number']
    jinjafy_shared_templates_dir(paths, info) # Compile files in the shared/templates  directory.

    if not only_exercises:  # Don't do any of this if we are in continuing education mode
        for proj in range(len(info['reports_handin']) if not info['CE'] else 1):
            info['project'] = proj+1
            info['is_project'] = True
            handout_week = info['reports_handout'][proj]
            handin_week =info['reports_handin'][proj]

            info['lecture'] = info['lectures'][ handout_week-1]
            info['lecture_handin'] = info['lectures'][handin_week-1]

            if info['CE']:
                proj_base = paths['instructor'] + "/ExercisesShared/%sprojectCE_Base.tex"%(course_number, )
                proj_tex_out = paths['instructor'] + "/Project/latex%i/%sprojectCE.tex" % (1,course_number,)
            else:
                proj_base = paths['instructor'] + "/ExercisesShared/%sproject%i_Base.tex" % (course_number,proj+1,)
                proj_tex_out = paths['instructor'] + "/Project/latex%i/%sproject%i.tex" % (proj+1, course_number, proj+1)
            info['week'] = -1

            if not os.path.exists(proj_base):
                continue

            jinjafy_template(info, proj_base, file_out=proj_tex_out, filters=filters, template_searchpath=paths['instructor'])
            fix_shared(paths, output_dir=os.path.dirname(proj_tex_out), dosvg=dosvg)
            latexmk(proj_tex_out, pdf_out=paths['pdf_out'] + "/" + os.path.basename(proj_tex_out)[:-4] + ".pdf")

    langs = ["Matlab", "Python", "R"]
    info['is_project'] = False
    for lang in langs:
        if not make_exercises:
            break
        # Handle exercise 0 seperately:

        ex0_date = info['lectures'][0]['date'] - timedelta(days=0 if info['CE'] else 7)
        ex0 = { 'number': 0,
                'date': ex0_date,
                'year': ex0_date.year,
                'month': calendar.month_name[ex0_date.month],
                'day': ex0_date.day}
        all_lectures = [ex0] + info['lectures'][:-1]

        exercises_to_compile = all_lectures[week:week+1] if week != None else all_lectures

        for lecture in exercises_to_compile: # not number 13.
            w = lecture['number']
            info['lecture'] = lecture
            info['week'] = w

            nicelang = lang.upper()
            tb = '''<base-dir>/02450Toolbox_%s/''' % lang
            if lang == "Matlab":
                ext = "m"
            elif lang == "Python":
                ext = "py"
            else:
                ext = "R"

            tv = {
                  "lang": lang,
                  "nicelang": nicelang,
                  "tbscripts": tb + "Scripts/",
                  "tbdata": tb + "Data/",
                  "tbtools": tb + "Tools/",
                  "tbname": '''02450Toolbox\_%s''' % lang,
                  "tb": tb,
                  "ext": ext,
                  "tbsetup": tb + "setup.%s" % ext,
                  "Python": lang == "Python",
                  "Matlab": lang == "Matlab",
                  "R": lang == "R",
                  'HOMEWORK_PROBLEMS': HOMEWORK_PROBLEMS,
                  }

            # get lang dir
            if not os.path.exists("%s/Exercises%s"%(paths['instructor'], lang)):
                continue

            info.update(tv)
            ex_base =  "%s/ExercisesShared/%sex%i_Base.tex"%(paths['instructor'], course_number, w)
            ex_tex_out = "%s/Exercises%s/Exercise%i/latex/%sex%i_%s.tex" % ( paths['instructor'], lang, w, course_number, w, lang)
            # fbody = os.path.dirname(ex_tex_out) +f"/ex{w}_body.tex"

            if os.path.exists(ex_base):
                jinjafy_template(info, ex_base, file_out=ex_tex_out, filters=filters, template_searchpath=paths['instructor'])
                fix_shared(paths, output_dir=os.path.dirname(ex_tex_out), dosvg=dosvg)
                # mvfiles(shared_tex, os.path.dirname(ex_tex_out)+"/")
                latexmk(ex_tex_out, pdf_out=paths['pdf_out']+"/" + os.path.basename(ex_tex_out)[:-4] + ".pdf")

def mvfiles(source_dir, dest_dir):
    src_files = os.listdir(source_dir)
    for file_name in src_files:
        full_file_name = os.path.join(source_dir, file_name)
        if (os.path.isfile(full_file_name)):
            shutil.copy(full_file_name, os.path.dirname(dest_dir))

@profile
def make_webpage(dosvg=True):
    cinfo = class_information()
    paths = get_paths()
    fix_shared(paths, output_dir=os.path.dirname(paths['homepage_out']), pdf2png=True, dosvg=dosvg)
    wdir = paths['homepage_template']
    jinjafy_template(cinfo, file_in=wdir, file_out=paths['homepage_out'])
    print("Instructors for course: ")
    s = ""
    for dex,i in enumerate(cinfo['instructors']):
        if dex > 0:
            s += "; "
        s += i['email']

    blrb = os.path.dirname(paths['homepage_template']) +"/homepage_widget_blurb_template.html"
    if os.path.exists( blrb):
        jinjafy_template(cinfo, file_in=blrb, file_out=blrb.replace("_template.html", ".html"))
    print(s)


# This should probably  be moved into jinjafy
def tt(value):
    return "\\texttt{" + value + "}"

def bf(value):
    return "\\textbf{" + value + "}"

def verb(value):
    return '\\verb"' + value + '"'

def safetex(value):
    return value.replace("_", "\_")

def slide_converter(week=None, verbose=True, clean_temporary_files=False, copy_template_resource_files=True, fix_broken_osvg_files=False, **kwargs):
    """ Legacy function. """
    print("Checking if slides should be converted from odf -> pdf format..")
    paths = get_paths()
    info = class_information()
    # week = [week] if week not isinstance(week, list) else []
    week = week if week is None else [week] #[week] if not week is None else

    for lecture in info['lectures']:
        # for n in range(1,14):
        n = lecture['number']
        if week is not None and n not in week:
            continue
        ldir = "%s/Lecture_%i"%(paths['lectures'], n)
        texdir = ldir +"/Latex"
        print("Testing conversion between directories:\n   > %s -> %s"%(ldir, texdir))

        if not os.path.exists(texdir):
            os.mkdir(texdir)
            pdf_in = "%s/Lecture_%i.pdf"%(ldir, n)
            pdf_out = texdir +"/Lecture_%i.pdf"%n
            shutil.copyfile(pdf_in, pdf_out)

            print("operating...")
            lecture_tex_out = li_import(pdf_out, output_dir=texdir)
            print("Wrote new main file: " + lecture_tex_out)
        else:
            print("%s exists; no conversion possible. "% (texdir,))

        print("Handling .svg conversion in slides..")
        slide_tex_path = texdir +"/Lecture_%i.tex"%n
        print("   > "+slide_tex_path)
        set_svg_background_images(slide_tex_path,
                                  verbose=verbose,
                                  clean_temporary_files=clean_temporary_files,
                                  copy_template_resource_files=copy_template_resource_files,
                                  fix_broken_osvg_files=fix_broken_osvg_files, **kwargs)

    print("Slides converted!")
