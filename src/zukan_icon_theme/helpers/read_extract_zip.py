import logging
import os
import shutil
import tempfile

from ..utils.zukan_paths import (
    ZUKAN_INSTALLED_PKG_PATH,
)
from zipfile import ZipFile

logger = logging.getLogger(__name__)


def extract_folder(
    name: str, dir_destiny: str, zip_file_path: str = ZUKAN_INSTALLED_PKG_PATH
):
    """
    Extract folder when package installed using Package Control. File sublime-package
    is a zip file.

    Parameters:
    name (str) -- folder name.
    dir_destiny (str) -- path where will extract folder.
    zip_file_path (Optional[str])  -- path to zip file, default to
    'ZUKAN_INSTALLED_PKG_PATH'.
    """
    with ZipFile(zip_file_path, 'r') as zf:
        if any(
            file_in_zip.startswith('{n}'.format(n=name.rstrip('/')))
            for file_in_zip in zf.namelist()
        ):
            logger.debug('moving %s folder to %s', name, dir_destiny)

            for file_in_zip in zf.namelist():
                if file_in_zip.startswith(name):
                    zf.extract(file_in_zip, dir_destiny)
        else:
            raise FileNotFoundError(
                logger.error('folder %s does not exist in %s.', name, dir_destiny)
            )


def extract_remove_folder(
    name: str, dir_destiny: str, zip_file_path: str = ZUKAN_INSTALLED_PKG_PATH
):
    """
    Extract, move and remove folder from zip file.

    When package installed using Package Control, need to extract 'icons' and
    'icons_data' folder, move them to destiny Packages folder and remove from
    zip. File sublime-package is a zip file.

    Parameters:
    name (str) -- folder name.
    dir_destiny (str) -- path where will extract folder.
    zip_file_path (Optional[str])  -- path to zip file, default to
    'ZUKAN_INSTALLED_PKG_PATH'.
    """
    tempdir = tempfile.mkdtemp()
    temp_zip_path = os.path.join(tempdir, 'temp_pkg.zip')

    try:
        with ZipFile(zip_file_path, 'r') as zf:
            for file_in_zip in zf.infolist():
                # Currently this will move all folders/filenames
                # that starts wtih 'icons'.
                if file_in_zip.filename.startswith(name):
                    zf.extract(file_in_zip, dir_destiny)

            with ZipFile(temp_zip_path, 'w') as zf_write:
                for file_in_zip in zf.infolist():
                    if not file_in_zip.filename.startswith(name):
                        data = zf.read(file_in_zip.filename)
                        zf_write.writestr(file_in_zip, data)

            shutil.move(temp_zip_path, zip_file_path)

        shutil.rmtree(tempdir)

    except Exception:
        shutil.rmtree(tempdir)
        logger.exception('error occurred while extracting the sublime-package file.')
