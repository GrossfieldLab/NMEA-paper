#!/bin/env perl


### This will remove the eigenvector section from the CHARMm output.
# It will preserve the *first* eigenvector so you can see what atoms were used.
# Also preserves the extra info printed per mode.

my $state = 0;
my $first = 1;

while (<>) {
    if ($state == 0) {
	if (/EIGENVECTOR:/) {
	    $state = 1;
	    if ($first) {
		print "$_";
	    }
	} else {
	    print "$_";
	}
    } elsif ($state == 1) {
	if ($first) {
	    print "$_";
	}
	chomp;
	if ($_ eq '') {
	    print "\n\n";
	    $state = 0;
	    $first = 0;
	}
    }
}
