from werkzeug.utils import secure_filename

def validate_file(file, allowed_extensions):
    if not file or not file.filename: raise ValueError('Choose a document to upload.')
    filename = secure_filename(file.filename)
    if not filename or '.' not in filename: raise ValueError('The file must have a supported extension.')
    extension = filename.rsplit('.', 1)[1].lower()
    if extension not in allowed_extensions: raise ValueError('Unsupported file type. Use PDF, DOCX, or TXT.')
    return filename, extension
