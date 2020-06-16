#!/usr/bin/perl -w
#
#


while (<>) {
    chomp;
    my @ary = split(/,/, $_);
    my $freq = shift @ary;
    for (my $k=0; $k<=$#ary; ++$k) {
        print $k*15.0, "\t", $freq, "\t", $ary[$k], "\n";
    }
    print "\n";
}
