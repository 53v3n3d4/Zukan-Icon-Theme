import logging

from ..utils.zukan_dir_paths import (
    ZUKAN_INSTALLED_PKG_PATH,
)
from zipfile import ZipFile

logger = logging.getLogger(__name__)


def dir_exist(z, name):
    return any(
        file_in_zip.startswith('{n}'.format(n=name.rstrip('/')))
        for file_in_zip in z.namelist()
    )


def extract_folder(name: str, dir_destiny: str):
    with ZipFile(ZUKAN_INSTALLED_PKG_PATH, 'r') as zf:
        if dir_exist(zf, name):
            # print('Zukan Icon Theme: moving %(n)s folder to %(d)s' % {'n': name, 'd': dir_destiny})
            logger.debug('moving %s folder to %s', name, dir_destiny)

            for file_in_zip in zf.namelist():
                if file_in_zip.startswith(name):
                    zf.extract(file_in_zip, dir_destiny)
        else:
            raise FileNotFoundError(
                # print(
                #     'Zukan Icon Theme: folder %(n)s does not exist in %(d)s.'
                #     % {'n': name, 'd': dir_destiny}
                # )
                logger.error('folder %s does not exist in %s.', name, dir_destiny)
            )
