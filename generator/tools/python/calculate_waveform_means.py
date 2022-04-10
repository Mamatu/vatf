if __name__ == "__main__":
    from vatf_utils import rosa
    import sys
    if len(sys.argv) == 4:
        rosa.CalculateMeansAndSaveTo(sys.argv[1], sys.argv[2], segment_duration = float(sys.argv[3]))
    elif len(sys.argv) == 3:
        rosa.CalculateMeansAndSaveTo(sys.argv[1], sys.argv[2])
