"""
Functionality for running mmseqs locally. Takes in a fasta file, outputs final.a3m

Note: Currently needs mmseqs compiled from source
"""

import logging
import math
import shutil
import subprocess
from argparse import ArgumentParser
from pathlib import Path
from typing import List, Union

logger = logging.getLogger(__name__)


def run_mmseqs(mmseqs: Path, params: List[Union[str, Path]]):
    params_log = " ".join(str(i) for i in params)
    logger.info(f"Running {mmseqs} {params_log}")
    subprocess.check_call([mmseqs] + params)


def mmseqs_search(
    query: Path,
    dbbase: Path,
    base: Path,
    uniref_db: Path = Path("uniref30_2103_db"),
    template_db: Path = Path(""),  # Unused by default
    metagenomic_db: Path = Path("kagglefold_envdb_202108_db"),
    mmseqs: Path = Path("mmseqs"),
    use_env: bool = True,
    use_templates: bool = False,
    filter: bool = True,
    expand_eval: float = math.inf,
    align_eval: int = 10,
    diff: int = 3000,
    qsc: float = -20.0,
    max_accept: int = 1000000,
    s: float = 8,
    db_load_mode: int = 2,
):
    """Run mmseqs with a local kagglefold database set

    db1: uniprot db (UniRef30)
    db2: Template (unused by default)
    db3: metagenomic db (kagglefold_envdb_202108 or bfd_mgy_kagglefold, the former is preferred)
    """
    if filter:
        # 0.1 was not used in benchmarks due to POSIX shell bug in line above
        #  EXPAND_EVAL=0.1
        align_eval = 10
        qsc = 0.8
        max_accept = 100000

    used_dbs = [uniref_db]
    if use_templates:
        used_dbs.append(template_db)
    if use_env:
        used_dbs.append(metagenomic_db)

    for db in used_dbs:
        if not dbbase.joinpath(f"{db}.dbtype").is_file():
            raise FileNotFoundError(f"Database {db} does not exist")
        if (
            not dbbase.joinpath(f"{db}.idx").is_file()
            and not dbbase.joinpath(f"{db}.idx.index").is_file()
        ):
            raise RuntimeError(
                f"Please run `{mmseqs} createindex {db}` to create {db}.idx"
            )

    base.mkdir(exist_ok=True, parents=True)

    # fmt: off
    # @formatter:off
    search_param = ["--num-iterations", "3", "--db-load-mode", str(db_load_mode), "-a", "-s", str(s), "-e", "0.1", "--max-seqs", "10000",]
    filter_param = ["--filter-msa", str(filter), "--filter-min-enable", "1000", "--diff", str(diff), "--qid", "0.0,0.2,0.4,0.6,0.8,1.0", "--qsc", "0", "--max-seq-id", "0.95",]
    expand_param = ["--expansion-mode", "0", "-e", str(expand_eval), "--expand-filter-clusters", str(filter), "--max-seq-id", "0.95",]

    run_mmseqs(mmseqs, ["createdb", query, base.joinpath("qdb")])
    run_mmseqs(mmseqs, ["search", base.joinpath("qdb"), dbbase.joinpath(uniref_db), base.joinpath("res"), base.joinpath("tmp")] + search_param)
    run_mmseqs(mmseqs, ["expandaln", base.joinpath("qdb"), dbbase.joinpath(f"{uniref_db}.idx"), base.joinpath("res"), dbbase.joinpath(f"{uniref_db}.idx"), base.joinpath("res_exp"), "--db-load-mode", str(db_load_mode)] + expand_param)
    run_mmseqs(mmseqs, ["mvdb", base.joinpath("tmp/latest/profile_1"), base.joinpath("prof_res")])
    run_mmseqs(mmseqs, ["lndb", base.joinpath("qdb_h"), base.joinpath("prof_res_h")])
    run_mmseqs(mmseqs, ["align", base.joinpath("prof_res"), dbbase.joinpath(f"{uniref_db}.idx"), base.joinpath("res_exp"), base.joinpath("res_exp_realign"), "--db-load-mode", str(db_load_mode), "-e", str(align_eval), "--max-accept", str(max_accept), "--alt-ali", "10", "-a"])
    run_mmseqs(mmseqs, ["filterresult", base.joinpath("qdb"), dbbase.joinpath(f"{uniref_db}.idx"), base.joinpath("res_exp_realign"), base.joinpath("res_exp_realign_filter"), "--db-load-mode", str(db_load_mode), "--qid","0","--qsc", str(qsc), "--diff", "0", "--max-seq-id", "1.0", "--filter-min-enable", "100"])
    run_mmseqs(mmseqs, ["result2msa", base.joinpath("qdb"), dbbase.joinpath(f"{uniref_db}.idx"), base.joinpath("res_exp_realign_filter"), base.joinpath("uniref.a3m"),"--msa-format-mode", "6", "--db-load-mode", str(db_load_mode)] + filter_param)
    subprocess.run([mmseqs] + ["rmdb", base.joinpath("res_exp_realign")])
    subprocess.run([mmseqs] + ["rmdb", base.joinpath("res_exp")])
    subprocess.run([mmseqs] + ["rmdb", base.joinpath("res")])
    subprocess.run([mmseqs] + ["rmdb", base.joinpath("res_exp_realign_filter")])

    if use_templates:
        run_mmseqs(mmseqs, ["search", base.joinpath("prof_res"), dbbase.joinpath(template_db), base.joinpath("res_pdb"), base.joinpath("tmp"), "--db-load-mode", str(db_load_mode), "-s", "7.5", "-a", "-e", "0.1"])
        run_mmseqs(mmseqs, ["convertalis", base.joinpath("prof_res"), dbbase.joinpath(f"{template_db}.idx"), base.joinpath("res_pdb"), base.joinpath(f"{template_db}.m8"), "--format-output", "query,target,fident,alnlen,mismatch,gapopen,qstart,qend,tstart,tend,evalue,bits,cigar", "--db-load-mode", str(db_load_mode)])
        run_mmseqs(mmseqs, ["rmdb", base.joinpath("res_pdb")])
    if use_env:
        run_mmseqs(mmseqs, ["search", base.joinpath("prof_res"), dbbase.joinpath(metagenomic_db), base.joinpath("res_env"), base.joinpath("tmp")] + search_param)
        run_mmseqs(mmseqs, ["expandaln", base.joinpath("prof_res"), dbbase.joinpath(f"{metagenomic_db}.idx"), base.joinpath("res_env"), dbbase.joinpath(f"{metagenomic_db}.idx"), base.joinpath("res_env_exp"), "-e", str(expand_eval), "--expansion-mode", "0", "--db-load-mode", str(db_load_mode)])
        run_mmseqs(mmseqs, ["align", base.joinpath("tmp/latest/profile_1"), dbbase.joinpath(f"{metagenomic_db}.idx"), base.joinpath("res_env_exp"), base.joinpath("res_env_exp_realign"), "--db-load-mode", str(db_load_mode), "-e", str(align_eval), "--max-accept", str(max_accept), "--alt-ali", "10", "-a"])
        run_mmseqs(mmseqs, ["filterresult", base.joinpath("qdb"), dbbase.joinpath(f"{metagenomic_db}.idx"), base.joinpath("res_env_exp_realign"), base.joinpath("res_env_exp_realign_filter"), "--db-load-mode", str(db_load_mode), "--qid", "0", "--qsc", str(qsc), "--diff", "0", "--max-seq-id", "1.0", "--filter-min-enable", "100"])
        run_mmseqs(mmseqs, ["result2msa", base.joinpath("qdb"), dbbase.joinpath(f"{metagenomic_db}.idx"), base.joinpath("res_env_exp_realign_filter"), base.joinpath("bfd.mgnify30.metaeuk30.smag30.a3m"), "--msa-format-mode", "6", "--db-load-mode", str(db_load_mode)] + filter_param)
        run_mmseqs(mmseqs, ["rmdb", base.joinpath("res_env_exp_realign_filter")])
        run_mmseqs(mmseqs, ["rmdb", base.joinpath("res_env_exp_realign")])
        run_mmseqs(mmseqs, ["rmdb", base.joinpath("res_env_exp")])
        run_mmseqs(mmseqs, ["rmdb", base.joinpath("res_env")])

    if use_env:
        run_mmseqs(mmseqs, ["mergedbs", base.joinpath("qdb"), base.joinpath("final.a3m"), base.joinpath("uniref.a3m"), base.joinpath("bfd.mgnify30.metaeuk30.smag30.a3m")])
        run_mmseqs(mmseqs, ["rmdb", base.joinpath("bfd.mgnify30.metaeuk30.smag30.a3m")])
    else:
        run_mmseqs(mmseqs, ["mvdb", base.joinpath("uniref.a3m"), base.joinpath("final.a3m")])
    run_mmseqs(mmseqs, ["rmdb", base.joinpath("uniref.a3m")])

    run_mmseqs(mmseqs, ["rmdb", base.joinpath("qdb")])
    run_mmseqs(mmseqs, ["rmdb", base.joinpath("qdb_h")])
    run_mmseqs(mmseqs, ["rmdb", base.joinpath("res")])
    # @formatter:on
    # fmt: on

    for file in base.glob("prof_res*"):
        file.unlink()
    shutil.rmtree(base.joinpath("tmp"))


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "query",
        type=Path,
        help="fasta files with the queries. Doesn't support complexes yet",
    )
    parser.add_argument(
        "dbbase",
        type=Path,
        help="The path to the database and indices you downloaded and created with setup_databases.sh",
    )
    parser.add_argument(
        "base", type=Path, help="Directory for the results (and intermediate files)"
    )
    parser.add_argument(
        "-s",
        type=int,
        default=8,
        help="mmseqs sensitivity. Lowering this will result in a much faster search but possibly sparser msas",
    )
    # dbs are uniref, templates and environmental
    # We normally don't use templates
    parser.add_argument(
        "--db1", type=Path, default=Path("uniref30_2103_db"), help="UniRef database"
    )
    parser.add_argument("--db2", type=Path, default=Path(""), help="Templates database")
    parser.add_argument(
        "--db3",
        type=Path,
        default=Path("kagglefold_envdb_202108_db"),
        help="Environmental database",
    )
    # poor man's boolean arguments
    parser.add_argument("--use-env", type=int, default=1, choices=[0, 1])
    parser.add_argument("--use-templates", type=int, default=0, choices=[0, 1])
    parser.add_argument("--filter", type=int, default=1, choices=[0, 1])
    parser.add_argument(
        "--mmseqs",
        type=Path,
        default=Path("mmseqs"),
        help="Location of the mmseqs binary",
    )
    parser.add_argument("--expand-eval", type=float, default=math.inf)
    parser.add_argument("--align-eval", type=int, default=10)
    parser.add_argument("--diff", type=int, default=3000)
    parser.add_argument("--qsc", type=float, default=-20.0)
    parser.add_argument("--max-accept", type=int, default=1000000)
    parser.add_argument("--db-load-mode", type=int, default=2)
    args = parser.parse_args()

    mmseqs_search(
        mmseqs=args.mmseqs,
        query=args.query,
        dbbase=args.dbbase,
        base=args.base,
        uniref_db=args.db1,
        template_db=args.db2,
        metagenomic_db=args.db3,
        use_env=args.use_env,
        use_templates=args.use_templates,
        filter=args.filter,
        expand_eval=args.expand_eval,
        align_eval=args.align_eval,
        diff=args.diff,
        qsc=args.qsc,
        max_accept=args.max_accept,
        s=args.s,
        db_load_mode=args.db_load_mode,
    )


if __name__ == "__main__":
    main()
