#!/usr/bin/perl -w
#
# Combines frequency with collectivity
#
# Usage- add_freq_to_coll.pl frequency.asc collectivity.asc >combined.asc
#
#

use FileHandle;

my $freqname = shift(@ARGV);
my $collname = shift(@ARGV);

my $rfreqs = &readData($freqname);
my $rcolls = &readData($collname);

for (my $i=0; $i<=$#$rcolls; ++$i) {
  my $coll = $rcolls->[$i];
  my $idx = $coll->[0];
  my $collectivity = $coll->[1];
  my $f = $rfreqs->[$idx]->[0];
  print "$f\t$collectivity\n"
}



sub readData {
  my $fn = shift;
  my $fh = new FileHandle $fn; defined($fh) || die "Cannot open $fn";

  my @data;
  while (<$fh>) {
    next if /^#/;
    s/#.*$//;
    chomp;
    my @ary = split;
    push(@data, \@ary);
  }

  return(\@data);
}
