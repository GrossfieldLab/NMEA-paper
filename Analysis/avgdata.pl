#!/usr/bin/perl -w
#
# (c) 2009 Tod D. Romo
# Grossfield Lab, URMC
#
#
# Average together multiple sets of columnar data, optionally
# calculating the std-dev...  This tool assumes your data is layed out
# as follows:
#
#   index   d0  d1  d2  d3 ...
#
# There is minimal checking to make sure that each data-file matches
# the rest of them (i.e. same number of columns).
#
# The output, if no std-dev is requested, is,
#  index n a0 a1 a2 ...
#
# where n is the number of data-points per row use to compute the
# average 
#
# If std-dev is requested, the output is, index n a0 s0 a1 s1 a2 s2
# ...  where n is the number of data-points used, ai is the average,
# and si is the std-dev.
#


use FileHandle;
use Getopt::Long;
use Carp;

$add_std = 0;
$warn = 0;
$skip = 3;
$absf = 0;
$cl = "$0 " . join(' ', @ARGV);

GetOptions('std!' => \$add_std,
	   'warn!' => \$warn,
	   'abs!' => \$absf,
	   'skip=i' => \$skip,
	   'help' => sub { &help; exit;});

print "# $cl\n";


## Special handling for header metadata from each file...
my @hdr;
my $file;
foreach $file (@ARGV) {
  my $fh = new FileHandle $file;
  defined($fh) || die "$0: Error- cannot open $file";
  push(@hdr, "# === $file ===");
  while (<$fh>) {
    last if (!/^#/);
    chomp;
    push(@hdr, $_);
  }
}

print join("\n", @hdr), "\n";


foreach $file (@ARGV) {
  my $fh = new FileHandle $file;
  defined($fh) || die "$0: Error- cannot open $file";
  while (<$fh>) {
    next if /^#/;
    chomp;
    my @ary = split;
    my $idx = shift @ary;
    
    if ($absf) {
      for (my $i = 0; $i<=$#ary; ++$i) {
	$ary[$i] = abs($ary[$i]);
      }
    }

    defined($idx) || die 'Error- index is undef';
    if (!exists($data{$idx})) {
      $data{$idx} = [ \@ary ];
    } else {
      push @{$data{$idx}}, \@ary;
    }

  }
}


foreach $i (keys %data) {
  my $rary = $data{$i};
  my @subavg = @{$$rary[0]};
  for (my $j=1; $j<=$#$rary; ++$j) {
    &addArray(\@subavg, $$rary[$j]);
  }
  &multArrayScalar(\@subavg, 1.0/($#$rary+1));
  $averages{$i} = \@subavg;
}

if (!$add_std) {
  foreach $i (sort { $a <=> $b} keys %averages) {
    my $ravg = $averages{$i};
    print $i,"\t", $#{$data{$i}}+1, "\t", join("\t", @{$averages{$i}}), "\n";
  }
  exit(0);
}

foreach $i (keys %data) {
  my $rary = $data{$i};
  my @istd;
  for (my $j=0; $j<=$#$rary; ++$j) {
    my @substd = @{$$rary[$j]};
    &subArray(\@substd, $averages{$i});
    &multArray(\@substd, \@substd);
    if ($j == 0) {
      @istd = @substd;
    } else {
      &addArray(\@istd, \@substd);
    }
  }
  if ($#$rary < $skip-1) {
    warn "$0: Warning- n=", $#$rary+1," at i=$i" if ($warn);
    my $m = $#istd+1;
    @istd = (0.0) x $m;
  } else {
    &multArrayScalar(\@istd, 1.0/$#$rary);
    &sqrtArray(\@istd);
  }
  $stds{$i} = \@istd;
}

foreach $j (sort {$a <=> $b} keys %data) {
  my $ravg = $averages{$j};
  my $rstd = $stds{$j};
  $#$ravg == $#$rstd || die "$0: ERROR- average ($#$ravg) and std ($#$rstd) mismatch at j=$j";
  print "$j\t", $#{$data{$j}}+1, "\t";
  for (my $i=0; $i<=$#$ravg; ++$i) {
    printf "%g\t%g", $$ravg[$i], $$rstd[$i];
    if ($i == $#$ravg) {
      print "\n";
    } else {
      print "\t";
    }
  }
}


exit(0);





sub addArray {
  my $ru = shift;
  my $rv = shift;

  $#$ru == $#$rv || carp "$0: Error- arrays have different sizes";
  for (my $i = 0; $i <= $#$ru; ++$i) {
    $$ru[$i] += $$rv[$i];
  }
}


sub subArray {
  my $ru = shift;
  my $rv = shift;

  $#$ru == $#$rv || carp "$0: Error- arrays have different sizes";
  for (my $i = 0; $i <= $#$ru; ++$i) {
    $$ru[$i] -= $$rv[$i];
  }
}



sub multArray {
  my $ru = shift;
  my $rv = shift;

  $#$ru == $#$rv || carp "$0: Error- arrays have different sizes";
  for (my $i = 0; $i <= $#$ru; ++$i) {
    $$ru[$i] *= $$rv[$i];
  }
}


sub multArrayScalar {
  my $ru = shift;
  my $k = shift;

  for (my $i = 0; $i <= $#$ru; ++$i) {
    $$ru[$i] *= $k;
  }
}


sub sqrtArray {
  my $ru = shift;

  for (my $i=0; $i<=$#$ru; ++$i) {
    $$ru[$i] = sqrt($$ru[$i]);
  }
}



sub help {
  print <<EOF;
Usage- avgdata.pl [options] file1 file2 ... fileN
    --[no]std   = Add standard deviation  [nostd]
    --[no]warn  = Issue warnings about input data  [nowarn]
    --[no]abs   = Use absolute value of data [noabs]
    --skip=i    = Skip files with less than i datapoints [3]

Notes:
  Assumes input data has the following format,
    index   d0 d1 d2 d3

  Output is formatted as follows:
    index   a0 a1 a2 a3

  If --std is used, then the output is formatted this way:
    index   a0 s0  a1 s1  a2 s2

EOF

}
