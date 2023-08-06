__app_name__ = "camt"
__version__ = "0.1.2"

(
    SUCCESS,
    DEST_DIR_ERROR,
    SRC_DIR_ERROR
) = range(3)

ERRORS = {
    DEST_DIR_ERROR: "destination dir error",
    SRC_DIR_ERROR: "source dir error",
}
