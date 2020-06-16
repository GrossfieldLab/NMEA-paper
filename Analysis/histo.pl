#!/usr/bin/perl -w
#
# (c) 2009 Tod D. Romo
#          Grossfield Lab
#          Univ of Rochester
#
# Simple histogram tool
#
# Usage- histo.pl [options] data >output

use FileHandle;
use Getopt::Long;
use POSIX qw(DBL_MAX);

### Defaults...

$bounds=undef;
my @kol;
$norm = undef;
$scale = 1.0;
$nbins = 20;
$verb = 1;
$discard = 0;
$rows = undef;
$absval = 0;


### First, capture the command-line...
$cmd = "$0 " . join(' ', @ARGV);
print "# $cmd\n";

$result = GetOptions(
		     "bounds=s" => \$bounds,
		     "column=s" => \@kol,
		     "normalize=f" => \$norm,
		     "scale=f" => \$scale,
		     "nbins=i" => \$nbins,
		     "help" => sub { &showHelp },
		     "verbose!" => \$verb,
		     "quiet" => sub { $verb = 0; },
		     "discard!" => \$discard,
		     "rows=s" => \$rows,
		     "abs!" => \$absval
		    );

$result || die "$0: Error in parsing command options";


my @cols;

if ($#kol < 0) {
  push(@col, 1);
} else {
  foreach my $spec (@kol) {
    my @list = split(/,/, $spec);
    foreach my $part (@list) {
      if ($part =~ /:/) {
	my @ary = split(/:/, $part);
	if ($#ary == 1) {
	  for (my $i=$ary[0]; $i<$ary[1]; ++$i) {
	    push(@col, $i)
	  }
	} elsif ($#ary == 2) {
	  for (my $i=$ary[0]; $i<$ary[2]; $i += $ary[1]) {
	    push(@col, $i)
	  }
	} else {
	  die "Error- unknown range spec '$part'";
	}
      } else {
	push(@col, int($part));
      }
    }
  }
}

@kol = @col;
print STDERR "$0: Using cols - ", join(',', @kol), "\n";

# First, read in all data...
my $warned = 0;
@data = ();
while (<>) {
  next if /^#/;
  chomp;
  my @ary = split;
  foreach my $col (@kol) {
    my $val = $ary[$col];
    if (!defined($val)) {
      if (!$warned) {
	warn "$0: Some lines are missing col $col and will be ignored";
	$warned = 1;
      }
      next;
    }
    if ($absval) {
      $val = abs($val);
    }
    push(@data, $val);
    
  }

}

if (defined($rows)) {
  my @ary = split(/:/, $rows);
  my $low = $ary[0];
  my $high = $ary[1];
  my $step = ($low < $high) ? 1 : -1;

  if ($#ary == 2) {
    $high = $ary[2];
    $step = $ary[1];
  }

  my @subsampled;
  for (my $i=$low; $i <=$high; $i += $step) {
    push(@subsampled, $data[$i]);
  }

  @data = @subsampled;
}



# Defines the bin centers...
if (defined($bounds)) {
  ($lower, $upper) = split(/,/, $bounds);
} else {
  ($lower, $upper) = &getRange(\@data);
}
$step = ($upper - $lower) / $nbins;
print STDERR "$0: Auto-range - $lower <= $upper ($step)\n" if ($verb);

$npts = 0;

@bins = (0) x $nbins;

foreach (@data) {
  my $i = int(($_ - $lower)/ $step);
  if ($i < 0) {
    if ($discard) {
      next;
    } else {
      $i = 0;
    }
  } elsif ($i >= $nbins) {
    if ($discard) {
      next;
    } else {
      $i = $nbins-1;
    }
  }
  
  ++$npts;
  $bins[$i] += 1;
  
}


# Normalize?
if (defined($norm)) {
  my $sum = 0;
  foreach (@bins) {
    $sum += $_;
  }
  print STDERR "$0: Normalization is 1/$sum\n" if ($verb);
  for ($i=0; $i<=$#bins; ++$i) {
    $bins[$i] /= $sum;
  }
} else {   # No normalize, so scale them...
  for ($i=0; $i<=$#bins; ++$i) {
    $bins[$i] *= $scale;
  }
}



for ($i=0, $x=$lower + $step/2.0; $i<=$#bins; ++$i, $x += $step) {
  print "$x\t$bins[$i]\n";
}




sub getRange {
  my $rary = shift;
  my $minval = &DBL_MAX;
  my $maxval = -&DBL_MAX;

  foreach (@$rary) {
    if ($_ < $minval) {
      $minval = $_;
    }
    if ($_ > $maxval) {
      $maxval = $_;
    }
  }

  return( ($minval, $maxval) );
}



sub showHelp {
  print <<EOF;
Usage - hist.pl [options] input >output

Options:
   --[no]abs                   Use absolute value of data
   --bounds=low,high           Matlab-style range defining the centers
                               of the histogram bins.

   --column=i                  Extracts data from the ith column (relative
                               to 0) from the input data.  Default is 1.

   --normalize=f               Normalize the sum of the bins to f

   --nbins=i                   Use i evenly spaced bins, auto-ranging from
                               the input data.  The --range option overrides
                               this flag.

   --[no]discard               Discards values that lie outside the range,
                               otherwise they are folded into the extreme
                               bins.  The default is to not discard.

   --[no]verbose               Display informational messages

   --rows=start[:step]:stop    Which rows to use (in Matlab notation)
EOF

  exit(0);
}
