if __name__ == "__main__":
    import sys
    import datetime
    if len(sys.argv) != 5:
        raise Exception(f"Invalid number of argumnets. It should be 5. It is {len(sys.argv)}")
    dt1 = datetime.datetime.strptime(sys.argv[1], sys.argv[2])
    dt2 = datetime.datetime.strptime(sys.argv[3], sys.argv[4])
    print(dt1 - dt2)
