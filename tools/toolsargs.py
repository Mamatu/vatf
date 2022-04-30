def parse():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", help = "Number of jobs, as default is 4")
    parser.add_argument("--root", help = "root directory of script, as default it is current directory of test")
    args = parser.parse_args()
    jobs = 4
    root = "."
    if args.jobs:
        jobs = args.jobs
    if args.root:
        root = args.root
    return {"jobs" : jobs, "root" : root}
