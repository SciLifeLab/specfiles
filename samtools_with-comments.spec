#
# spec file for package samtools
#
# Copyright (c) 2013 Mario Giovacchini <mario@scilifelab.se>
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


# Following openSUSE guidelines here:
#   http://en.opensuse.org/openSUSE:Specfile_guidelines
# See here for a specfile template and some more guidlines:
#   https://fedoraproject.org/wiki/How_to_create_an_RPM_package#SPEC_templates_and_examples


# http://en.opensuse.org/openSUSE:Package_naming_guidelines
Name:		samtools
Version:	0.1.19
Release:	1%{?dist}
Summary:	A set of tools for processing / filtering SAM- and BAM-formatted data

# Non-standard group as required by http://en.opensuse.org/openSUSE:Package_group_guidelines
Group:		Productivity/Scientific/Other
License:	MIT
URL:		http://samtools.sourceforge.net/
Source:		http://sourceforge.net/projects/samtools/files/samtools/%{version}/samtools-%{version}.tar.bz2/download
# preferred path (as per http://en.opensuse.org/openSUSE:Specfile_guidelines)
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

# BuildRequires are packages needed to actually build binaries form source
BuildRequires: zlib
BuildRequires: ncurses
#BuildRequires:	autoconf
#BuildRequires:	automake
#BuildRequires:	python-devel
#BuildRequires:	samtools-devel
#BuildREquires:	zlib-devel
#BuildRequires:	dos2unix

# Requires are generally handled by rpmbuild or similar
#Requires:	bowtie


%description
SAM (Sequence Alignment/Map) format is a generic format for storing large nucleotide sequence alignments. SAM aims to be a format that:

- Is flexible enough to store all the alignment information generated by various alignment programs;
- Is simple enough to be easily generated by alignment programs or converted from existing alignment formats;
- Is compact in file size;
- Allows most of operations on the alignment to work on a stream without loading the whole alignment into memory;
- Allows the file to be indexed by genomic position to efficiently retrieve all reads aligning to a locus.

SAM Tools provide various utilities for manipulating alignments in the SAM format, including sorting, merging, indexing and generating alignments in a per-position format.

%prep
# Uses the setup RPM macro, which knows about tar archives, to extract the files (tar -xvf)
%setup -q

#Fix bad permissions
#chmod -x src/align_status.*
#chmod -x src/deletions.*
#chmod -x src/insertions.*


%build
# also we have no configure macro for samtools (it's not part of the build procedure)
# NOTE that the files produced by make will be in the directory {_builddir}
make %{?_smp_mflags}
make %{?_smp_mflags} razip


# NOTE that this install section is NOT run when the end-user installs a binary RPM;
# it is only run when creating the package (i.e. on Open Build Service)
# NOTE that normally this is when files move from {_builddir} to {buildroot}
%install
# samtools does not have a make install but instead packages are manually copied into place
#make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}%{_bindir}
cp samtools %{buildroot}%{_bindir}/samtools
cp bcftools/bcftools %{buildroot}%{_bindir}/bcftools
cp razip %{buildroot}%{_bindir}/razip

#I believe the clean section is no longer necessary for the openSUSE Open Build Service
%clean
rm -rf %{buildroot}

# Here are listed the files created by the build that "belong" to the RPM that will be installed by the end-user
# There are sotred in %{buildroot} within the RPM, but the path following buildroot is where they will be installed on the system
# Note that if you write a directory /without/a/trailing/slash, you are saying that that directory and everything under it
# belong to the package; this is wrong if it is e.g. /usr/local
# If you want just the dir but not everything under it you must use the %dir directive, e.g. %dir /your/mom
%files
# defattr no longer needed?
%defattr(-,root,root,-)
#%doc AUTHORS COPYING NEWS README THANKS
# NOTE {_bindir} becomes %{buildroot}/usr/bin or similar, see https://fedoraproject.org/wiki/Packaging:RPMMacros
#%{_bindir}/*
%{_bindir}/samtools
%{_bindir}/bcftools
%{_bindir}/razip
#samtools
#bcftools/bcftools
#razip

%changelog
* Tue Nov 19 2013 Mario Giovacchini <mario@scilifelab.se> - 1.0
- Intial version
