## TRACK FIXER## 
#  @file fixTracks.py
#  @brief Tries to fix gaps in tracks, both small and large (very slow with higher settings)
## For MCEdit / Python 3
## Alpha ver. 0.2.4  
## by Garrett Martin (GDroidbot)
## Changelog:
#0.2: Added optional trackbed laying
#0.2.4: Fixed bugs about trackbed

# Based off of SethBling's filters.
# Feel free to modify and use this filter however you wish. If you do,
# please give credit to SethBling.
# http://youtube.com/SethBling

from pymclevel import TAG_Compound
from pymclevel import TAG_Int
from pymclevel import TAG_Short
from pymclevel import TAG_Byte
from pymclevel import TAG_String
railBlocks = (27, 28, 66, 157)
transparentBlocks = [0,6, 8, 9, 10, 11, 18, 20, 26, 27, 28, 29, 30, 31, 32, 33, 34, 36, 37, 38, 39, 40, 44, 46, 50, 51, 52, 53, 54, 55, 59, 60, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 75, 76, 77, 78, 79, 81, 83, 85, 89, 90, 92, 93, 94, 95, 96, 97, 101, 102, 104, 105, 106, 107, 108, 109, 111, 113, 114, 115, 116, 117, 118, 119, 120, 122, 126, 127]

inputs = (
		("For fixing or creating tracks (Like ones made by mineshafts)", "label"),
		("Distance to check", (2, 1, 16)),
		("Aggressive Mode", False),
		("Fill in track bed?", False)
		# 'Aggressive Mode' fills in larger gaps in tracks when run just once (To save a step)
)
displayName = "Fix broken tracks"
global trackBed

def perform(level, box, options):
		distance = options["Distance to check"]
		aggressive = options["Aggressive Mode"]
		#global trackBed
		trackBed = options["Fill in track bed?"]
		if distance < 1 or distance > 8:
				print("The distance " , distance, "may compute slowly, or even crash MCEdit.")
		for x in xrange(box.minx, box.maxx):
				for y in xrange(box.miny, box.maxy):
						for z in xrange(box.minz, box.maxz):
								if level.blockAt(x, y, z) == 66:
										fixTracks(level, x, y, z, distance)
										if aggressive:
											fixTracks(level, x, y, z, distance-1)
											continue
										continue
								

def fixTracks(level, x, y, z, distance): # X+ = EAST  X- = WEST Z+ = SOUTH Z- = NORTH
		if distance < 1:
				return
		bData = level.blockDataAt(x, y, z)
		global bedBlock
		bedBlock = level.blockAt(x, y-1, z)
		# East-West flat
		if bData == 1:
				directionalCheck(level, x, y, z, xdir = 1, r = distance)
				return
		# North-South flat rail
		elif bData == 0:
				directionalCheck(level, x, y, z, zdir = 1, r = distance)
				return
		# Up to the East
		elif bData == 2: # Only check west
				directionalCheck(level, x, y, z, -1, 0, 1)
				return
		# Up to West
		elif bData == 3: # Only check east
				directionalCheck(level, x, y, z, 1, 0, 1)
				return
		# Up to the North
		elif bData == 4:
				directionalCheck(level, x, y, z, 0, 1, 1)
				return
		# Up to the South
		elif bData == 5:
				directionalCheck(level, x, y, z, 0, -1, 1)
				return
		else:
			isCornerTrack(level, x, y, z, distance, bData )
			
		chunk = level.getChunk(x / 16, z / 16)
		chunk.dirty = True

def isCornerTrack(level, x, y, z, distance = 1, data = 0):
		# data = level.blockDataAt(x, y, z) ## redundant
		print("Corner Data: ", data)
		if data==6:   # East and South corner
			directionalCheck(level, x, y, z, 1, 1, distance)
		elif data==7: # West and South corner
			directionalCheck(level, x, y, z, -1, 1, distance)
		elif data==8: # West and North corner
			directionalCheck(level, x, y, z, -1, -1, distance)
		elif data==9: # East and North corner
			directionalCheck(level, x, y, z, 1, -1, distance)
			return
		else:
			return False

def directionalCheck(level,x, y, z, xdir = None, zdir = None, r = 1):
		i = r
		global trackBed			
		if xdir == 1 and zdir is None: # Special case: flat track east-west
				#for i in xrange(1, r, 2):
						if level.blockAt(x+1+i, y, z) in railBlocks:
									print("Laying track at:", x+i, y, z)
									level.setBlockAt(x+i, y, z, 66)
									level.setBlockDataAt(x+i, y, z, 1)
									if trackBed:
										layTrackBed(level, x+i, y-1, z)
						if level.blockAt(x-1-i, y, z) in railBlocks:
									print("Laying track at:", x-i, y, z)
									level.setBlockAt(x-i, y, z, 66)
									level.setBlockDataAt(x-i, y, z, 1)
									if trackBed:
										layTrackBed(level, x-i, y-1, z)
						
						return
		if xdir is None and zdir == 1: # Special case: flat track north-south
				#for i in xrange(1, r, 2):
						if level.blockAt(x, y, z+1+i) in railBlocks:
									print("Laying track at:", x, y, z+i)
									level.setBlockAt(x, y, z+i,66)
									level.setBlockDataAt(x, y, z+i, 0)
									if trackBed:
										layTrackBed(level, x, y-1, z+i)
						if level.blockAt(x, y, z-1-i) in railBlocks:
									print("Laying track at:", x, y, z-i)
									level.setBlockAt(x, y, z-i,66)
									level.setBlockDataAt(x, y, z-i, 0)
									if trackBed:
										layTrackBed(level, x, y-1, z-i)
						return
		if abs(xdir) == 1 and abs(zdir) == 1:
				#for i in reverse(xrange(1, r)):
						if level.blockAt((xdir * (i + 1)) + x, y, z) in railBlocks:
									level.setBlockAt((xdir * i) + x, y, z,66)
									level.setBlockDataAt((xdir * i) + x, y,z, 1)
									if trackBed:
										layTrackBed(level, (xdir *i) + x, y-1, z)
										 
		if abs(zdir) == 1 and abs(xdir) == 1:
				#for i in reverse(xrange(1, r)):
						if level.blockAt(x, y, (zdir * (i + 1)) + z) in railBlocks:
									level.setBlockAt(x, y, (zdir*i) + z,66)
									level.setBlockDataAt(x, y, (zdir * i) + z, 0)
									if trackBed:
										layTrackBed(level, x, y-1, (zdir * i) + z)
		return

def layTrackBed(level, x, y, z, ablock = None):
	beforeBlock = level.blockAt(x, y, z)
	block = bedBlock
	if beforeBlock in transparentBlocks:
		if block not in transparentBlocks:
			level.setBlockAt(x, y, z, block)
		
		
	
