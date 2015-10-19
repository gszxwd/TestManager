ALLOWED_EXTENSIONS = set(['gif', 'png', 'jpg', 'jpeg'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    print allowed_file("")
