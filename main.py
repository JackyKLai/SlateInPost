import multiprocessing
from package.app import SlateInPost

if __name__ == "__main__":
    import sys
    multiprocessing.freeze_support()
    app = SlateInPost(sys.argv)
    sys.exit(app.run())
