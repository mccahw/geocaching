# geotravel.py 
# calculates the shortest path between 10 geocaches
# https://www.geocaching.com/geocache/GC7XNRW
# correct solution verified to be N 42° 43.314 W 073° 40.676

from math import sqrt, pow, factorial as fac
from itertools import permutations as perm
import numpy as np
import matplotlib.pyplot as plt

# convert coordinate strings in HDDD° MM.MMM (DDM) form to decimal form
def parseCoords( loc ):
	for i in range( len(loc) ):
		n = loc[i][1].split()
		w = loc[i][2].split()
		
		north = int( n[1].split("°")[0] ) + float( n[2] )/60
		west = int( w[1].split("°")[0] ) + float( w[2] )/60		
		
		# forgo rounding for accuracy
		loc[i][1] = north
		loc[i][2] = -1 * west
		
	return loc

# calculate distance between two coordinates
def dist( a, b ):
	c = sqrt( pow( (a[1] - b[1]), 2 ) + pow( (a[2] - b[2]), 2 ) )
	return c

# calculate the total length of a given path
def pathCalc( path, loc ):
	# first calculate airport to first node
	edges = dist( loc[0], loc[ path[0] ] )	
	
	# calculate other nodes
	for i in range( len(path)-1 ):
		edges += dist( loc[ path[i] ], loc[ path[i+1] ] )
	
	# calculate last node back to airport
	edges += dist( loc[ path[-1] ], loc[0] )
	
	return edges

# create a formatted solution string given a path
def buildSol( loc, path ):
	n = ""
	w = ""
	for i in range( len( path ) ):
		if i<5: n += str( loc[ path[i] ][0] )
		else: w += str( loc[ path[i] ][0] )		
	n = "N 42° " + n[0:2] + "." + n[2:5]
	w = "W 073° " + w[0:2] + "." + w[2:5]
	
	return (n, w)

# sorting function for top shortest paths
def sortFunc( c ):
	return c[2]
 
if __name__ == "__main__":
	
	# locations are copied directly from the geocache page
	loc = [
		[0, "N 43° 03.673", "W 108° 27.504"],
		[4, "N 43° 03.105", "W 108° 28.308"],
		[3, "N 43° 02.023", "W 108° 25.561"],
		[4, "N 43° 00.962", "W 108° 21.202"],
		[3, "N 43° 01.097", "W 108° 23.805"],
		[1, "N 43° 00.917", "W 108° 23.974"],
		[4, "N 42° 59.476", "W 108° 22.195"],
		[6, "N 43° 01.379", "W 108° 23.534"],
		[7, "N 43° 01.496", "W 108° 23.651"],
		[0, "N 43° 01.519", "W 108° 23.226"],
		[6, "N 43° 01.975", "W 108° 23.779"]]
		
	# convert coordintes from DDM to decimal
	loc = parseCoords(loc)
	print("\nConverted coordinates:\n")
	for i in range( len(loc) ):
		print("N {:.06f} W {:.06f}".format( loc[i][1], loc[i][2] ) )
	
	# create all 3,628,800 paths with 10 nodes each
	paths = list( perm( range(1,11) ) )
	
	if( len( paths ) != fac(10) ):
		print( "ERROR: permutation count mismatch" )
		print( "{} != {}".format( len( paths ), fac(10) ) )
		quit()
	
	print( "\nTotal permutations: {}\n".format( len( paths ) ) )	
	
	dists = np.zeros( len( paths ) )
	topDists = []	
	
	# calculate total path distance
	for i in range( len(paths) ):	
		if i%100000 == 0:
			progress = 100*(i+1)/len(paths)
			print( "Checking paths: {:06.3f}% complete".format( progress ) )
		
		# save all distances for histogram
		dists[i] = pathCalc( paths[i], loc )
		
		# impossible to have >=60 minutes in coordinate scheme
		# therefore solution cannot have a value of >=6 as the 1st or 6th path node
		if paths[i][0] != 10 and paths[i][0] != 7 and paths[i][0] != 8\
			and paths[i][5] != 10 and paths[i][5] != 7 and paths[i][5] != 8:			
			# histogram data shows smallest paths cluster around <0.3 degrees
			if dists[i] < 0.3:
				data = [ i, paths[i], dists[i] ]
				topDists.append( data )
	
	topDists.sort( reverse=True, key=sortFunc )
	print( "\nThe shortest path has been determined:" )
	print( "Path {}: {} with distance {:.06f}".format( *topDists[-1] ) )
	
	# build solutions from top shortest paths
	print("\nTop Shortest Paths:")	
	for i in range( len( topDists ) ):
		sol = buildSol( loc, topDists[i][1] )
		print( "Path: {:07} {} Dist: {:.06f}°\t{} {} ".format( *topDists[i], *sol ) )
	
	'''
	# build histogram
	print("\nPath Length Histogram:")
	plt.hist(dists, bins='auto')
	plt.title("Distribution of Path Lengths")
	plt.show()
	'''