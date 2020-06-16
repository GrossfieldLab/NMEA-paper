#!/usr/bin/perl -w
#
# Usage- binnedavg.pl low high nbins datafile [datafile ...]
#


my $low = shift(@ARGV);
my $high = shift(@ARGV);
my $nbins = shift(@ARGV);

$low *= 1.0;
$high *= 1.0;
my $range = $high - $low;
my $delta = $nbins / $range;

my @bins;
for (my $i=0; $i<$nbins; ++$i) { push(@bins, []); }
my $ob = 0;
my $ob2 = 0;
my $td = 0;

while (<>) {
  chomp;
  next if /^#/;
  s/#.*$//;
  my @ary = split;
  $#ary == 1 || die "Error- too many items... '$_'\n";
  ++$td;
  my $freq = $ary[0];
  my $coll = $ary[1];

  if ($freq >= $high || $freq < $low) { ++$ob; next; }
  my $bin = int(($freq - $low) * $delta);
  if ($bin < 0 || $bin >= $nbins) { ++$ob2; next; }
  push(@{$bins[$bin]}, $coll);
}

print "# Total data = $td\n# OB1 = $ob\n# OB2 = $ob2\n";

for (my $i = 0; $i < $nbins; ++$i) {
  my $f = $i * $range / $nbins + $low;
  my $avg = &average($bins[$i]);
  my $sd = &stddev($bins[$i], $avg);
  my $cnt = $#{$bins[$i]}+1;
  print "$f\t$avg\t$sd\t$cnt\n";
}




sub average {
  my $rary = shift;
  my $avg = 0.0;

  if ($#$rary < 0) { return(0.0); }

  foreach my $x (@$rary) {
    $avg += $x;
  }
  return($avg/($#$rary+1));
}



sub stddev {
    my $rary = shift;
    my $avg = shift;

    if ($#$rary < 1) { return(0.0); }

    my $std = 0.0;
    foreach my $x (@$rary) {
	my $d = $x - $avg;
	$std += $d*$d;
    }

    return(sqrt($std/$#$rary));
}
