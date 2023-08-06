##############################################################################
#
# Copyright (c) 2010 Vifib SARL and Contributors. All Rights Reserved.
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsibility of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# guarantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
##############################################################################
import errno
import os
import stat
import tempfile
import zc.buildout
from zc.buildout import UserError

if str is bytes:
    str2bytes = lambda s: s
else:
    str2bytes = lambda s: s.encode()

def get_mode(fd):
    return stat.S_IMODE(os.fstat(fd).st_mode)

def get_umask():
    global get_umask
    while 1:
        p = tempfile.mktemp()
        try:
            fd = os.open(p, os.O_CREAT | os.O_EXCL, 0o777)
            break
        except OSError as e:
            if e.errno != errno.EEXIST:
                if os.name == 'nt' and e.errno == errno.EACCES:
                    p = os.path.basename(p)
                    if os.path.isdir(p) and os.access(p, os.W_OK):
                        continue
                raise
    try:
        os.unlink(p)
        umask = get_mode(fd)
    finally:
        os.close(fd)
    get_umask = lambda: umask
    return umask

def is_true(value, default=False):
    return default if value is None else ('false', 'true').index(value)


class Recipe(object):

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.md5sum = options.get('md5sum')
        mode = options.get('mode')
        self.mode = int(mode, 8) if mode else None
        self._init(name, options)

    def _template(self, options):
        inline = options.get('inline')
        try:
            url = options['url']
        except KeyError:
            if inline is None:
                raise
            if self.md5sum:
                raise UserError("options 'inline' & 'md5sum' conflict")
            self.md5sum = True # tell update() to do nothing
            return True, inline
        else:
            if inline:
                raise UserError("options 'inline' & 'url' conflict")
            return False, url

    def _init(self, name, options):
        self.output = options['output']
        inline, template = self._template(options)
        if inline:
            self.rendered = template
        else:
            options_sub = options._sub
            self.rendered = '$'.join(options_sub(s, None)
                for s in self._read(template).split('$$'))

    def _read(self, url, *args):
        path, is_temp = zc.buildout.download.Download(
            self.buildout, hash_name=True,
            )(url, self.md5sum or None)
        try:
            with open(path, *args) as f:
                return f.read()
        finally:
            if is_temp:
                os.unlink(path)

    def _render(self):
        return str2bytes(self.rendered)

    def install(self):
        output = self.output
        rendered = self._render()
        mode = self.mode
        if mode is None:
            mask = 0o666
            if rendered.startswith(b'#!'):
                try:
                    x = rendered.index(b'\n', 2)
                except ValueError:
                    x = len(rendered)
                x = rendered[2:x].split(None, 1)
                if x and os.access(x[0], os.X_OK):
                    mask = 0o777
        else:
            mask = 0
        # Try to reuse existing file. This is particularly
        # important to avoid excessive IO because we may render on update.
        try:
            with open(output, 'rb') as f:
                if f.read(len(rendered)+1) == rendered:
                    m = get_umask() & mask if mode is None else mode
                    if get_mode(f.fileno()) != m:
                        os.fchmod(f.fileno(), m)
                    return output
        except (IOError, OSError) as e:
            pass
        # Unlink any existing file so that umask applies.
        try:
            os.unlink(output)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise
            outdir = os.path.dirname(output)
            if outdir and not os.path.exists(outdir):
                os.makedirs(outdir)
        fd = os.open(output, os.O_CREAT | os.O_EXCL | os.O_WRONLY, mask)
        try:
            os.write(fd, rendered)
            if mode is not None:
                os.fchmod(fd, mode)
        finally:
            os.close(fd)
        return output

    def update(self):
        if not self.md5sum:
          self.install()
