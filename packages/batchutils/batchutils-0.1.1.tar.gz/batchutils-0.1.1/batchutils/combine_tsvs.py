# based on Dan King's code located at https://gist.github.com/danking/60aaf68ee9dcba4f5895b0546e4f46fb

from typing import List, Optional, Callable
import hailtop.batch as hb
import math

from hailtop.utils import grouped
from hailtop.utils.utils import digits_needed


def batch_combine2(base_combop: Callable[[hb.job.BashJob, List[str], str], None],
                   combop: Callable[[hb.job.BashJob, List[str], str], None],
                   b: hb.Batch,
                   name: str,
                   paths: List[str],
                   final_location: str,
                   branching_factor: int = 100,
                   suffix: Optional[str] = None):
    """A hierarchical merge using Batch jobs.
    We combine at most `branching_factor` paths at a time. The first layer is given by
    `paths`. Layer n combines the files produced by layer n-1.
    For the first layer, we use `base_combop` to construct a job to combine a given group. For
    subsequent layers, we use `combop`. This permits us, for example, to start with uncompressed
    files, but use compressed files for the intermediate steps and the final step.
    The fully combined (single) file is written to `final_location`.
    """
    assert isinstance(branching_factor, int) and branching_factor >= 1
    n_levels = math.ceil(math.log(len(paths), branching_factor))
    level_digits = digits_needed(n_levels)
    branch_digits = digits_needed((len(paths) + branching_factor) // branching_factor)
    assert isinstance(b._backend, hb.ServiceBackend)
    tmpdir = b._backend.remote_tmpdir.rstrip('/')

    def make_job_and_path(level: int,
                          i: int,
                          make_commands: Callable[[hb.job.BashJob, List[str], str], None],
                          paths: List[str],
                          dependencies: List[hb.job.BashJob],
                          ofile: Optional[str] = None):
        if ofile is None:
            ofile = f'{tmpdir}/{level:0{level_digits}}/{i:0{branch_digits}}'
            if suffix:
                ofile += suffix
        j = b.new_job(name=f'{name}-{level:0{level_digits}}-{i:0{branch_digits}}')
        for d in dependencies:
            j.depends_on(d)
        make_commands(j, paths, ofile)
        return (j, ofile)

    assert n_levels > 0

    if n_levels == 1:
        return make_job_and_path(0, 0, base_combop, paths, [], final_location)

    jobs_and_paths = [
        make_job_and_path(0, i, base_combop, paths, [])
        for i, paths in enumerate(grouped(branching_factor, paths))]

    for level in range(1, n_levels - 1):
        jobs_and_paths = [
            make_job_and_path(level,
                              i,
                              combop,
                              [x[1] for x in jobs_and_paths],
                              [x[0] for x in jobs_and_paths])
            for i, jobs_and_paths in enumerate(grouped(branching_factor, jobs_and_paths))]

    jobs = [x[0] for x in jobs_and_paths]
    paths = [x[1] for x in jobs_and_paths]
    make_job_and_path(n_levels - 1, 0, combop, paths, jobs, final_location)



def combine_tsvs_with_headers(j: hb.job.BashJob, xs: List[str], ofile: str):
    j.command('set -ex -o pipefail')
    j.command('''
function retry() {
    "$@" || { sleep 2 && "$@" ; } || { sleep 5 && "$@" ; }
}''')
    j.command('retry gcloud auth activate-service-account --key-file=/gsa-key/key.json')
    serially_read_tail_of_files_to_stdout = " && ".join([
        f'gsutil -m cat {x} | tail -n +2 -q' for x in xs[1:]])
    j.command(f'''
join-files() {{
    rm -f sink
    mkfifo sink
    ( {{ gsutil -m cat {xs[0]} &&
         {serially_read_tail_of_files_to_stdout}
      }} | bgzip > sink
    ) & pid=$!
    gsutil -m cp sink {ofile}
    wait $pid
}}
retry join-files
''')

def combine_compressed_tsvs_with_headers(j: hb.job.BashJob, xs: List[str], ofile: str):
    """Combine many compressed TSVs into one compressed TSV.
    We use a named sink to link the subsequent reads of each file with the single output
    file. The first file is read in its entireity. The subsequent files have their header
    removed.
    """
    j.command('set -ex -o pipefail')
    j.command('''
function retry() {
    "$@" || { sleep 2 && "$@" ; } || { sleep 5 && "$@" ; }
}''')
    j.command('retry gcloud auth activate-service-account --key-file=/gsa-key/key.json')
    serially_read_tail_of_files_to_stdout = " && ".join([
        f'gsutil -m cat {x} | bgzip -d | tail -n +2 -q' for x in xs[1:]])
    j.command(f'''
join-files() {{
    rm -f sink
    mkfifo sink
    ( {{ gsutil -m cat {xs[0]} | bgzip -d &&
         {serially_read_tail_of_files_to_stdout}
      }} | bgzip > sink
    ) & pid=$!
    gsutil -m cp sink {ofile}
    wait $pid
}}
retry join-files
''')
