#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import get

WorkDir = "."

NoStrip = ["/usr"]

def setup():
    
    shelltools.move("libcxx-%s.src" %get.srcVERSION(), "libcxx")
    shelltools.move("libcxxabi-%s.src" %get.srcVERSION(), "libcxxabi")

def build():   
    shelltools.export("CC", "clang")
    shelltools.export("CXX", "clang++")
    
    for arch in ["x86_64", "i686"]:
		
		if arch == "x86_64":
			pisitools.cflags.add("-m64")
			pisitools.cxxflags.add("-m64")
			shelltools.export("LDFLAGS", " -fuse-ld=lld -rtlib=compiler-rt -L/usr/lib -ldl -lpthread")
			libsuffix = " "
		
		if arch == "i686":
			pisitools.cflags.add("-m32")
			pisitools.cxxflags.add("-m32")
			shelltools.export("LDFLAGS", "-fuse-ld=lld -L/usr/lib32 -ldl -lpthread")
			libsuffix = "32"
			
		shelltools.cd("%s/libcxxabi" %get.workDIR())
		shelltools.system("mkdir build-%s" %arch)
		shelltools.cd("build-%s" %arch)
	    
		shelltools.system("cmake .. -G 'Unix Makefiles' \
			               -DCMAKE_BUILD_TYPE=Release \
			               -DCMAKE_INSTALL_PREFIX=/usr \
			               -DCMAKE_AR=/usr/bin/llvm-ar \
			               -DCMAKE_RANLIB=/usr/bin/llvm-ranlib \
			               -DCMAKE_STRIP=' ' \
			               -DLIBCXXABI_ENABLE_EXCEPTIONS=ON \
			               -DLIBCXXABI_ENABLE_THREADS=ON \
			               -DLIBCXXABI_ENABLE_SHARED=OFF \
			               -DLIBCXXABI_LIBCXX_INCLUDES=../../libcxx/include \
			               -DLLVM_NO_OLD_LIBSTDCXX=TRUE \
			               -DCXX_SUPPORTS_CXX11=TRUE \
			               -DLIBCXXABI_HAS_PTHREAD_API=ON \
			               -DLIBCXXABI_INSTALL_LIBRARY=OFF \
			               -DLIBCXXABI_INSTALL_STATIC_LIBRARY=OFF \
			               -DLIBCXXABI_ENABLE_NEW_DELETE_DEFINITIONS=OFF \
			               -DLIBCXXABI_ENABLE_STATIC_UNWINDER=ON \
			               ")
		
		autotools.make()
		
		shelltools.cd("%s/libcxx" %get.workDIR())
		shelltools.system("mkdir build-%s" %arch)
		shelltools.cd("build-%s" %arch)
		
		shelltools.system("cmake .. -G 'Unix Makefiles' \
			             -DCMAKE_BUILD_TYPE=Release \
			             -DCMAKE_INSTALL_PREFIX=/usr \
			             -DCMAKE_AR=/usr/bin/llvm-ar \
                         -DCMAKE_RANLIB=/usr/bin/llvm-ranlib \
                         -DCMAKE_STRIP=' ' \
                         -DLIBCXXABI_ENABLE_STATIC_UNWINDER=ON \
                         -DLIBCXX_INSTALL_HEADERS=ON \
                         -DLIBCXX_ENABLE_EXCEPTIONS=ON \
                         -DLIBCXX_ENABLE_THREADS=ON \
                         -DLIBCXX_ENABLE_MONOTONIC_CLOCK=ON \
                         -DLIBCXX_ENABLE_SHARED=ON \
                         -DLIBCXX_SUPPORTS_STD_EQ_CXX11_FLAG=TRUE \
                         -DLIBCXX_ENABLE_EXPERIMENTAL_LIBRARY=ON \
                         -DLIBCXX_ENABLE_FILESYSTEM=ON \
                         -DLIBCXX_ENABLE_STATIC_ABI_LIBRARY=TRUE \
                         -DLIBCXX_USE_COMPILER_RT=ON \
                         -DLIBCXX_CXX_ABI=libcxxabi \
                         -DLIBCXX_CXX_ABI_INCLUDE_PATHS=../../libcxxabi/include \
                         -DLIBCXX_CXX_ABI_LIBRARY_PATH=../../libcxxabi/build-%s/lib \
                         -DLIBCXX_HAS_PTHREAD_API=ON \
                         -DLIBCXX_LIBDIR_SUFFIX=%s \
                         " % (arch, libsuffix) )
		
		autotools.make()                         
	    

def install():
	
	for arch in ["x86_64", "i686"]:
		shelltools.cd("%s/libcxx/build-%s" % (get.workDIR(), arch) )
		autotools.rawInstall("DESTDIR=%s" %get.installDIR())
   
	pisitools.dodoc("%s/libcxx/CREDITS.TXT" % get.workDIR(), "%s/libcxx/LICENSE.TXT" % get.workDIR(), "%s/libcxx/NOTES.TXT" % get.workDIR(), "%s/libcxx/TODO.TXT" % get.workDIR())
