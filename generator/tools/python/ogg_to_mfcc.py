if __name__ == "__main__":
    from vatf_utils import rosa
    import sys
    print(f"{sys.argv[1]} -> {sys.argv[2]}")
    rosa.CreateMfccAndSaveToImageFile(sys.argv[1], sys.argv[2])
