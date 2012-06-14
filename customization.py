# Copyright (c) 2012 Nokia Corporation
# Original author John Ankcorn
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

#
# Classes for customizing parts of the rpmbuild processing
#

import os, re

basepackage = 'NRCC'
packagecross = {'Standard':basepackage + 'STD',
    'Tools':basepackage + 'TOOL'}

blacklist = ['home:', 'crossbuild:', 'deleted', 'susebased',
    'Archive:', 'Demo:', 'openSUSE.org']

scripthome = os.path.dirname(os.path.abspath(__file__))

sudoprog = 'sudo'
sudoprog = scripthome + '/really_scary'

bannedpackages = []
need_unique_chroot = []
added_rpmbuild_environment = ''
job_count = 2

# can't parse Recommends in telepathy-mission-control, telepathy-gabble in rpmspec
def FORCE_HOST_TOOLS(packname):
    if re.match(r'.*pkgconfig$|xcb-proto$|.*-python$|libxml2-python-build$|.*cmake$|.*-devel-tools$|ruby|injection.*-host-|openssl$|bison$|byacc$|python-|perl-|tp-cita-wrapper$', packname):
        #print('FORCEH', packname)
        return True
    return False
def FORCE_TARGET(packname):
    if re.match(r'.*-target-glibc.*$|.*ncurses.*$|.*expat..*$|.*gcrypt.*$|.*-lib.*$|.*-devel.*$|lib.*$|flex$|pam$|nss$|gdbm$|nspr$|tcl$|db4$|readline$|.*-target-openssl.*$|.*-target-pcre.*$|.*-target-popt.*$|injection-.*-host-.*$|injection-.*-target-.*lib.*$|lib.*$|.*-devel$|zlib$|dbus-1$|dbus-1-glib$|libltdl.*', packname):
        #print('FORCET', packname)
        return True
    return False

def file_initial(archtype):
    return [ \
    ('dir', '/dev'), \
    ('dir', '/root'), \
    ('dir', '/var/lib/rpm'), \
    ('dir', '/sysroot/var/tmp'), \
    ('dir', '/usr/sbin'), \
    ('dir', '/sysroot/var/lib/rpm'), \
    ('dir', '/sysroot/usr/lib'), \
    ('dir', '/sysroot/usr/include'), \
    ('dir', '/sysroot/usr/share'), \
    ('dir', '/var/cache'), \
    ('dir', '/sysroot/var/cache'), \
    ('dir', '/etc'), \
    ('dir', os.environ['HOME']), \
    ('dir', '/sysroot' + os.environ['HOME']), \
    ('ln', '/sysroot/usr/include', '/usr/include'), \
    ('ln', '/sysroot/usr/share',   '/usr/share'), \
    ('ln', '../../../zypp.i586',           '/var/cache/zypp'), \
    ('ln', '../../../../zypp.armv7hl',     '/sysroot/var/cache/zypp'), \
    ('ln', '../../zypp',                   '/etc/zypp'), \
    ('ln', os.environ['HOME'] + '/.zypp',  os.environ['HOME'] + '/.zypp'), \
    ('ln', os.environ['HOME'] + '/.zypp',  '/sysroot/' + os.environ['HOME'] + '/.zypp'), \
    ]

def file_edit_list(archtype):
    e = [ \
    ('dir', '/usr/share'), \
    ('dir', '/usr/include'), \
    ('dir', '/dev/pts'), \
    ('dir', '/root'), \
    ('dir', '/var/lib/rpm'), \
    ('dir', '/var/run/dbus'), \
    ('dir', '/usr/local/bin'), \
    ('dir', '/usr/local/lib'), \
    ('dir', '/opt/mt'), \
    ('touch', '/var/log/wtmp'), \
    ('touch', '/var/run/utmp'), \
    ('touch', '/dev/fd/0'), \
    ('sed', r's/i586-suse-linux-gnu/armv7hl-suse-linux-gnueabi/', '/usr/lib/rpm/macros'), \
    ('sed', r's/! rpm -ql filesystem | egrep -q /0 \&\& ! rpm -ql filesystem | egrep -q /', '/usr/lib/rpm/find-lang.sh'), \
    ('rm', '/lib/*2.13.so'), \
    ('ln', '/bin/gawk',                    '/bin/awk'), \
    ('mv', '/bin/uname',                   '/bin/uname_real'), \
    ('ln', 'uname_hack',                   '/bin/uname'), \
    ('ln', 'pts/ptmx',                     '/dev/ptmx'), \
    ('ln', '/sysroot/opt/mt/imports',      '/opt/mt/imports'), \
    ('ln', '/usr/bin/moc',                 '/sysroot/usr/bin/moc'), \
    ('ln', '/sysroot/usr/bin/orcc',        '/usr/bin/orcc'), \
    ('ln', '/sysroot/usr/lib/libxml2.so',  '/usr/lib/libxml2.so'), \
    ('ln', '/sysroot/usr/bin/msgfmt',      '/usr/local/bin/msgfmt'), \
    ('ln', '/sysroot/usr/bin/msgmerge',    '/usr/local/bin/msgmerge'), \
    ('ln', '/sysroot/usr/bin/xgettext',    '/usr/local/bin/xgettext'), \
    ('ln', '/sysroot/usr/lib/libcheck.so', '/usr/local/lib/libcheck.so'), \
    ('ln', '/sysroot/usr/lib/libexpat.so', '/usr/local/lib/libexpat.so'), \
    ('ln', '/sysroot/usr/lib/librpm.so',   '/usr/local/lib/librpm.so'), \
    ('ln', '/sysroot/usr/lib/libz.so',     '/usr/local/lib/libz.so'), \
    ('ln', '/sysroot' ,                    '/sysroot/etc/qemu-binfmt/arm'), \
    ('ln', '/tmp' ,                        '/var/tmp'), \
    ('ln', 'qemu-arm-static' ,             '/usr/bin/qemu-arm'), \
    ('ln', '/usr/bin/gcc' ,                '/usr/bin/gcc-uClibc'), \
    ('ln', '/sysroot' ,                    '/usr/gnemul/qemu-arm'), \
    ('ln', 'bash',                         '/bin/sh'), \
    ('ln', '/tmp/pci.ids',                 '/sysroot/usr/share/misc/pci.ids'), \
    ('ln', '/sysroot/usr/bin/app_text_packager.sh', '/usr/bin/app_text_packager.sh'), \
    ('ln', '/sysroot/usr/bin/MT_locales.list', '/usr/bin/MT_locales.list'), \
    ]
    for item in editlist:
        e.append(item)
    return e

def editconfig(fconfig, aarch):
    append9 = False
    append10 = False
    thisconfig = []
    for line in fconfig:
        if line.startswith('%ifarch armv7hl'):
            thisconfig.append('%if %{?targ_arch:1}0')
            thisconfig.append('%if %targ_arch==armv7hl')
        elif line.startswith('%ifarch i586'):
            thisconfig.append('%if %targ_arch==i586')
        elif line.startswith('%endif # i586'):
            thisconfig.append(line)
            thisconfig.append('%endif #target_arch')
        elif line.startswith('# Workaround definitions for current package selection'):
            thisconfig.append('%if %{?targ_arch:1}0')
            append9 = True
        elif append9 and line.find('injection-i586-target-glibc-devel') > 0:
            append10 = True
        elif line.startswith('%endif') and append10:
            thisconfig.append(line)
            thisconfig.append('%endif #target_arch')
        elif not line.startswith('#'):
            thisconfig.append(line)
    thisconfig.append('%if %{?targ_arch:1}0')
    thisconfig.append('%if %targ_arch==armv7hl')
    thisconfig.append('Preinstall: injection-armv7hl-host-glibc')
    thisconfig.append('Prefer: injection-armv7hl-target-glibc injection-armv7hl-target-libgcc injection-armv7hl-target-libstdc++')
    thisconfig.append('%endif')
    thisconfig.append('%if %targ_arch==i586')
    thisconfig.append('Preinstall: injection-i586-host-glibc')
    thisconfig.append('Prefer: injection-i586-target-glibc injection-i586-target-libgcc injection-i586-target-libstdc++')
    thisconfig.append('%endif')
    thisconfig.append('%else #targ_arch')
    thisconfig.append('%ifarch %arm')
    thisconfig.append('Prefer: injection-armv7hl-target-glibc injection-armv7hl-target-libstdc++ injection-armv7hl-target-libgcc')
    thisconfig.append('%endif')
    thisconfig.append('%ifarch %ix86')
    thisconfig.append('Prefer: injection-i586-target-glibc injection-i586-target-libstdc++ injection-i586-target-libgcc')
    #thisconfig.append('#needed for telepathy-qt4, since this contains a .so file, it must be loaded first (to be i586)')
    thisconfig.append('Support: dbus-python')
    # python-ply needed by ofono, but for some reason, 'down' doesn't work!!!!!
    thisconfig.append('Support: python-ply')
    # perl-XML-Parser needed by pulseaudio
    thisconfig.append('Support: perl-XML-Parser')
    thisconfig.append('Support: strace nano')
    thisconfig.append('Support: libqt5base-devel-tools')
    thisconfig.append('Support: openssl bison cmake')
    thisconfig.append('Support: libcurl4 libxml2-python')
    thisconfig.append('Support: perl-gettext')
    thisconfig.append('Support: python-devel python-distribute python-gobject2 python-pyOpenSSL')
    thisconfig.append('Support: python-Twisted python-zope.interface')
    thisconfig.append('Support: tp-cita-wrapper')
    thisconfig.append('%endif')
    thisconfig.append('Substitute: libbz2-devel bash')
    thisconfig.append('Substitute: linux-glibc-devel bash')
    thisconfig.append('Ignore: linux-glibc-devel')
    thisconfig.append('Substitute: kernel-headers bash')
    thisconfig.append('Support: config(bash)')
    thisconfig.append('%endif #targ_arch')
    thisconfig.append('Prefer: -busybox')
    thisconfig.append('Prefer: -busybox-fota')
    thisconfig.append('Prefer: -injection-i586-target-glibc-fota')
    thisconfig.append('Substitute: injection-i586-target-glibc-devel bash')
    thisconfig.append('Ignore: injection-i586-target-glibc-devel')
    # how did this get pulled in?
    thisconfig.append('Ignore: qt5-qdoc')
    thisconfig.append('Substitute: qt5-qdoc bash')
    #psycopathy stuff
    thisconfig.append('Ignore: dbus-test-helpers')
    thisconfig.append('Substitute: dbus-test-helpers bash')
    thisconfig.append('Substitute: dbus-python dbus-1-python-devel')
    #mt-qt5-curator
    thisconfig.append('Prefer: taglib-devel')
    return thisconfig

def disable_check_section():
    return '%__spec_check_pre echo "dont_run_%check"; exit 0\n'

def rpmbuild_commands(archtype, SPECFILE, verbose, rpmbuilddir):
    thisarch = archtype
    if thisarch.startswith('arm'):
        thisarch = 'arm'
    stracecmd = ''
    #stracecmd = 'strace -etrace=open '
    #stracecmd = 'strace -F -f -etrace=open '
    #stracecmd = 'strace -F -f -etrace=all '
    q = ' --quiet'
    jobs = ' --define "jobs ' + str(job_count) + '"'
    if verbose > 0:
        q = ''
        jobs = ' --define "jobs 1"'
    return \
        'export MACHINE=' + archtype + '\n' \
        'export PKG_CONFIG_PATH=/sysroot/usr/lib/pkgconfig\n' \
        + added_rpmbuild_environment + \
        'export PATH=$PATH:/sysroot/usr/bin:/sysroot/bin\n' \
        'export VPATH=/sysroot/usr/lib:/sysroot/lib\n' \
        'export MT_SYSROOT=/sysroot\n' \
        'chown `id -u`:`id -g` ' + rpmbuilddir + '/SOURCES/*\n' \
        'alias rm="rm -f"\n' \
        'export QMAKESPEC=linux-g++\n' \
        + stracecmd + 'rpmbuild -ba ' + q + jobs + ' --define "_srcdefattr (-,root,root)" \
            --define "_topdir ' + rpmbuilddir + '" --root /sysroot --nodeps \
            --define "_arch ' + thisarch + '" \
            --define "__spec_install_pre  export INSTALL_ROOT=%{buildroot}; %{___build_pre}" \
            --define "_unpackaged_files_terminate_build 0" \
            --target=' + archtype + '-suse-linux ' \
            + rpmbuilddir + '/SOURCES/' + SPECFILE + '\n\n'

#        'rm -f /tmp/_mt_init_lang_packages.executed\n' \
#the idiot hack for 'INSTALL_ROOT' is needed because so many packages forget to use %make_install instead of 'make install'
# for example 'mt-notionclient'
#this hack causes /sysroot to be definted for certificate-tools
#            --define "__spec_build_post ln -s %{buildroot} %{buildroot}/sysroot; %{___build_post}" \
#HACK HACK HACK caused by app_text_packager.sh (Michael Melber)
#        'rm -f /tmp/_mt_init_lang_packages.executed\n' \
#            --define "_arch ' + archtype + '" \

# main
if os.path.exists('profconfig'):
    #execfile('profconfig')
    exec(compile(open('profconfig').read(), 'profconfig', 'exec'))